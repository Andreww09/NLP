from nltk.corpus import wordnet as wn


def get_wordnet_relations(word):
    synsets = wn.synsets(word)

    for syn in synsets:
        print(f"\nSynset: {syn.name()} ({syn.pos()})")
        print(f"Definition: {syn.definition()}")

        synonyms = [lemma.name() for lemma in syn.lemmas()]
        print(f"Synonyms: {synonyms}")

        hypernyms = [lemma.name() for h in syn.hypernyms() for lemma in h.lemmas()]
        if hypernyms:
            print(f"Hypernyms: {hypernyms}")

        hyponyms = [lemma.name() for h in syn.hyponyms() for lemma in h.lemmas()]
        if hyponyms:
            print(f"Hyponyms: {hyponyms}")

        antonyms = [lemma.name() for h in syn.lemmas() for lemma in h.antonyms()]

        if antonyms:
            print(f"Antonyms: {antonyms}")

        meronyms = [lemma.name() for h in syn.lemmas() for lemma in h.part_meronyms()]

        if meronyms:
            print(f"Meronyms (parts): {meronyms}")


user_word = input("word = ")
get_wordnet_relations(user_word)
