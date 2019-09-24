# =========================
# Load libraries
# =========================

import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers
import keras_metrics as km
import matplotlib.pyplot as plt

# =========================
# Load data
# =========================

# Load gold data
gold_train = pd.read_csv("/home/mike/Documents/opt-out-master/gold_standard_data/gold_train_en.csv")

# Convert content columns to strings
gold_train.content = gold_train.content.astype(str)

# Split training Tweets and labels
train_data = gold_train.content.values
train_labels = gold_train.label.values

# =========================
# One-hot encode
# =========================

# Create unique index for every word and fit to training data
tokenizer = Tokenizer(num_words = 10000)
tokenizer.fit_on_texts(train_data)

# Print the number of unique words found in the data set (not the limit placed
# on the tokenizer), use this as feedback to the num_words arg of Tokenizer().
print('Found %d unique words.' % len(tokenizer.word_index))

# One-hot encode
data = tokenizer.texts_to_matrix(train_data, mode = 'binary')

# Prepare labels, transform to binary and float32
labels = train_labels.astype('float32')
labels = train_labels

# =========================
# Split data
# =========================

# Randomly shuffle data
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]

# Split into training and validation data (approximately 80:20)
x_train = data[:10410]
y_train = labels[:10410]
x_val   = data[10410:]
y_val   = labels[10410:]

# =========================
# Build model
# =========================

# Note the input_shape of the first layer will match the num_words arg from
# the Tokenizer() function. Double check with len(data[0])
# The final sigmoid layer outputs probability values between [0, 1]
model = models.Sequential()
model.add(layers.Dense(16, activation = 'relu', input_shape = (10000,)))
model.add(layers.Dense(16, activation = 'relu'))
model.add(layers.Dense(1, activation = 'sigmoid'))

# =========================
# Train model
# =========================

# As the model outputs probabilities, binary crossentropy is the best loss
# metric as it measures the distance between probability distributions
model.compile(optimizer = 'rmsprop',
              loss = 'binary_crossentropy',
              metrics=[km.binary_precision(), km.binary_recall()])

history = model.fit(x_train,
                    y_train,
                    epochs = 20,
                    batch_size = 512,
                    validation_data = (x_val, y_val))

# Prep history dictionary
precision = history.history['precision']
val_precision = history.history['val_precision']
recall = history.history['recall']
val_recall = history.history['val_recall']
epochs = range(1, len(precision) + 1)

# Plot the training and validation precision
plt.plot(epochs, precision, 'bo', label='Training recision')
plt.plot(epochs, val_precision, 'b', label='Validation precision')
plt.title('Training and validation Precision')
plt.xlabel('Epochs')
plt.ylabel('Precision')
plt.legend()
plt.show()

# Plot the training and validation accuracy
plt.clf()
plt.plot(epochs, recall, 'bo', label='Training recall')
plt.plot(epochs, val_recall, 'b', label='Validation recall')
plt.title('Training and validation recall')
plt.xlabel('Epochs')
plt.ylabel('Recall')
plt.legend()
plt.show()

# =========================
# Retrain model
# =========================
model = models.Sequential()
model.add(layers.Dense(16, activation = 'relu', input_shape = (10000,)))
model.add(layers.Dense(16, activation = 'relu'))
model.add(layers.Dense(1, activation = 'sigmoid'))

model.compile(optimizer = 'rmsprop',
              loss = 'binary_crossentropy',
              metrics=[km.binary_precision(), km.binary_recall()])

model.fit(x_train, y_train, epochs = 5, batch_size = 512)

# =========================
# Evaluate on test data
# =========================

# Load in test data
gold_test = pd.read_csv("/home/mike/Documents/opt-out-master/gold_standard_data/gold_test_en.csv")

# Convert content columns to strings
gold_test.content = gold_test.content.astype(str)

# Split test Tweets and labels
test_data = gold_test.content.values
test_labels = gold_test.label.values

# DO NOT retrain the tokenizer. Use the argument oov_token=True to reserve a
# token for unkown words. See https://bit.ly/2lNh15g

# One-hot encode
x_test = tokenizer.texts_to_matrix(test_data, mode = 'binary')

# Prepare labels, transform to binary and float32
y_test = test_labels.astype('float32')
y_test = test_labels

# Print results as ['precision', 'recall'] check names with model.metrics_names
model.evaluate(x_test, y_test)[1:]
