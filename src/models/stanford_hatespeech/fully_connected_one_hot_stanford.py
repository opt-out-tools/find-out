# =========================
# Load libraries
# =========================

import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras import models
from keras import layers
import matplotlib.pyplot as plt

# =========================
# Load data
# =========================

# Load stanford data
stanford_train = pd.read_csv("data/external/stanford/misogyny_training.csv")

# Convert content columns to strings
stanford_train.content = stanford_train.content.astype(str)

# Split training Tweets and labels
train_data = stanford_train.content.values
train_labels = stanford_train.label.values

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
labels = train_labels - 1

# =========================
# Split data
# =========================

# Randomly shuffle data
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]

# Split into training and validation data (approximately 80:20)
x_train = data[:24000]
y_train = labels[:24000]
x_val   = data[24000:]
y_val   = labels[24000:]

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
              metrics = ['accuracy'])

history = model.fit(x_train,
                    y_train,
                    epochs = 20,
                    batch_size = 512,
                    validation_data = (x_val, y_val))

# Prep history dictionary
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)

# Plot the training and validation loss
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Plot the training and validation accuracy
plt.clf()
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
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
              metrics = ['accuracy'])

model.fit(x_train, y_train, epochs = 5, batch_size = 512)

# =========================
# Evaluate on test data
# =========================

# Load in test data
stanford_test = pd.read_csv("data/external/stanford/misogyny_test.csv")

# Convert content columns to strings
stanford_test.content = stanford_test.content.astype(str)

# Split test Tweets and labels
test_data = stanford_test.content.values
test_labels = stanford_test.label.values

# DO NOT retrain to tokenizer. Use the argument oov_token=True to reserve a
# token for unkown words. See https://bit.ly/2lNh15g

# One-hot encode
x_test = tokenizer.texts_to_matrix(test_data, mode = 'binary')

# Prepare labels, transform to binary and float32
y_test = test_labels.astype('float32')
y_test = test_labels - 1

# Print results as ['loss', 'acc'] check names with model.metrics_names
model.evaluate(x_test, y_test)

model.metrics_names
