import spacy
import json

corpus = json.load(open("../../../../data/external/hatespeech/hs_data.csv"))

nlp = spacy.load("en_core_web_md")
docs = [nlp(tweet) for tweet in corpus[1]]

relations = []
for i,doc in enumerate(docs):
    dep_relation = " ".join(token.dep_ for token in doc)
    relations.append(dep_relation)

    print(f"Completed doc {i}")

