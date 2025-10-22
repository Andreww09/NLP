import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import pandas as pd
from difflib import get_close_matches
from googletrans import Translator
import asyncio


def get_dataset():
    coqa = pd.read_json('http://downloads.cs.stanford.edu/nlp/data/coqa/coqa-train-v1.0.json')
    del coqa["version"]

    cols = ["text", "question", "answer"]
    comp_list = []
    for index, row in coqa.iterrows():
        for i in range(len(row["data"]["questions"])):
            temp_list = []
            temp_list.append(row["data"]["story"])
            temp_list.append(row["data"]["questions"][i]["input_text"])
            temp_list.append(row["data"]["answers"][i]["input_text"])
            comp_list.append(temp_list)
    new_df = pd.DataFrame(comp_list, columns=cols)
    new_df.to_csv("CoQA_data.csv", index=False)


def find_best_context(question, text_column='text', question_column='question', n=1, cutoff=0.6):
    all_questions = data[question_column].to_list()

    matches = get_close_matches(question, all_questions, n=n, cutoff=cutoff)

    complete_context = ""
    for match in matches:
        context = data.loc[data[question_column] == match, text_column].values
        for value in context:
            complete_context += value

    return complete_context


def get_answer(question, text):
    input_ids = tokenizer.encode(question, text)

    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    # for token, id in zip(tokens, input_ids):
    #     print('{:8}{:8,}'.format(token, id))

    sep_idx = input_ids.index(tokenizer.sep_token_id)
    # print("SEP token index: ", sep_idx)
    num_seg_a = sep_idx + 1

    num_seg_b = len(input_ids) - num_seg_a

    segment_ids = [0] * num_seg_a + [1] * num_seg_b
    assert len(segment_ids) == len(input_ids)

    output = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]))

    answer = ""
    answer_start = torch.argmax(output.start_logits)
    answer_end = torch.argmax(output.end_logits)
    if answer_end >= answer_start:
        answer = tokens[answer_start]
        for i in range(answer_start + 1, answer_end + 1):
            if tokens[i] in ["[CLS]", "[SEP]"]:
                continue
            elif tokens[i][0:2] == "##":
                answer += tokens[i][2:]
            elif tokens[i].startswith("n") and tokens[i][1:].isdigit():
                answer += tokens[i][1:]
            else:
                answer += " " + tokens[i]
    answer = answer.replace("Ġ", " ")

    if answer.startswith("[CLS]"):
        answer = "Unable to find the answer to your question."

    return answer


async def translate(text):
    async with Translator() as translator:
        result = await translator.translate(text, "ro")
        print(f"result {result}")
        return result


data = pd.read_csv('CoQA_data.csv')

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# random_num = np.random.randint(0, len(data))
# question = data["question"][random_num]
# text = data["text"][random_num]

# question = 'how many states in the USA today?'
question = input("Enter a question (quit to exit): ")
while question != 'quit':
    text = find_best_context(question)
    if text is None:
        print("Can't find relevant conext. Try another question.")
        continue
    answer = get_answer(question, text)

    translated_answer = asyncio.run(translate(answer))
    print(translated_answer)
    print(translated_answer.text)

    print(f"Context: {text}")
    print("Question:{}".format(question.capitalize()))
    print("Answer: {}.".format(answer.capitalize()))
    print("Translated Answer: {}.".format(translated_answer.text.capitalize()))
    question = input("Enter a question (quit to exit): ")
