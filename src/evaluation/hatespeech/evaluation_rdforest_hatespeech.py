import pandas as pd
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from src.utils.preprocess_text_helpers import normalizer


data = pd.read_csv("../../../data/external/hatespeech/hs_data.csv")
misogyny = data[data['annotation'] == "misogynistic"]
misogyny['normalized'] = normalizer(misogyny['text'])

words = " ".join(sentence for sentence in misogyny['normalized'].to_list())

wordcloud = WordCloud(background_color="white").generate(words)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.savefig("wordcloud.png")
plt.axis("off")
plt.show()
