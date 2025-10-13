import json
import random
from nltk.corpus import wordnet as wn


def calculate_similarity(syn1, syn2):
    if not syn1 or not syn2:
        return 0.0
    return syn1.wup_similarity(syn2) or 0.0


def get_related_words(syn):
    related = set()

    related.update([lemma.name() for lemma in syn.lemmas()])

    for hyper in syn.hypernyms():
        related.update([lemma.name() for lemma in hyper.lemmas()])
    for hypo in syn.hyponyms():
        related.update([lemma.name() for lemma in hypo.lemmas()])

    for lemma in syn.lemmas():
        for antonym in lemma.antonyms():
            related.add(antonym.name())

    for part in syn.part_meronyms():
        related.update([lemma.name() for lemma in part.lemmas()])
    for whole in syn.member_holonyms():
        related.update([lemma.name() for lemma in whole.lemmas()])

    return list(related)


def start_game():
    with open("common_words.json", "r") as f:
        common_words = json.load(f)

    if len(common_words) == 0:
        return

    score = 0
    while True:
        starting_word = random.choice(common_words)
        print(f"Given word: {starting_word}")
        original_syn = wn.synsets(starting_word)[0]

        related_words = get_related_words(original_syn)
        print(f"Definition: {original_syn.definition()}")

        player_word = input("Guess a similar word (type q to quit)\n").lower()
        if player_word == 'q':
            break

        syns = wn.synsets(player_word)
        if not syns:
            print(f"'{player_word}' is not in WordNet.")
            continue
        player_syn = syns[0]

        similarity = calculate_similarity(original_syn, player_syn)
        points = int(similarity * 100) if similarity else 0
        score += points

        print(f"Your word: {player_word}")
        print(f"Semantic similarity: {similarity:.2f}")
        print(f"Points earned: {points}")
        print(f"Total score: {score}")

        if similarity > 0.7:
            print("Perfect guess")
        elif similarity > 0.5:
            print("Very Good guess")
        elif similarity > 0.2:
            print("Good try")
        else:
            print("Not a close guess")

        print(f"Similar words: {related_words}\n")

    print(f"\nGame over! Your total score: {score}")


start_game()
