# one-hot encode data

from keras.preprocessing.text import Tokenizer

samples = # read in tabular data from hatespeech and link to abraham and join as one dataframe

tokenizer = Tokenizer(num_words = 1000)
tokenizer.fit_on_texts(samples)

sequences = tokenizer.text_to_sequence(samples)

one_hot_results = tokenizer.texts_to_matrix(samples, mode = 'binary')

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
