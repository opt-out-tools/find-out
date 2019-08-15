from spacy import displacy
import spacy
import pandas as pd

from src.utils.normalize import normalize

data = pd.read_csv("../../../../data/external/hatespeech/hs_data.csv")
misogyny = data[data['annotation'] == "misogynistic"]
misogyny['normalized'] = misogyny['text'].apply(normalize)

nlp = spacy.load("en_core_web_md")
docs = [nlp(tweet) for tweet in misogyny['normalized'].to_list()]

displacy.render(docs[0], style='dep', jupyter=True, options={'distance': 90})
#
# for token in doc:
#     print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(
#         token.text,
#         token.idx,
#         token.lemma_,
#         token.is_punct,
#         token.is_space,
#         token.shape_,
#         token.pos_,
#         token.tag_
#     ))
