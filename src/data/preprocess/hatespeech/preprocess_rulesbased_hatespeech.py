import spacy
import pandas as pd


data = pd.read_csv("../../../../data/external/hatespeech/hs_data.csv")
misogyny = data.loc[data.loc[:,'annotation'] == "misogynistic"]

nlp = spacy.load("en_core_web_md")
docs = [nlp(tweet) for tweet in misogyny['text'].sample(frac=0.1, replace=True).to_list()]


# for ent in docs[0].ents:
#     print("entities")
#     print(ent.text, ent.label_)
#
#
# for chunk in docs[0].noun_chunks:
#     print("Noun-phrases")
#     print(chunk.text, chunk.label_, chunk.root.text)

for doc in docs[:50]:
    print(doc.text, [(token.text, token.pos_) for token in doc])
