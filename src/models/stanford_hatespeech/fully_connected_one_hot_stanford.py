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
# Load DATA
# =========================

# Load stanford DATA
STANFORD_TRAIN = pd.read_csv("../../../data/external/stanford/misogyny_training.csv")

# Convert content columns to strings
STANFORD_TRAIN.content = STANFORD_TRAIN.content.astype(str)

# Split training Tweets and LABELS
TRAIN_DATA = STANFORD_TRAIN.content.values
TRAIN_LABELS = STANFORD_TRAIN.label.values

# =========================
# One-hot encode
# =========================

# Create unique index for every word and fit to training DATA
TOKENIZER = Tokenizer(num_words=10000)
TOKENIZER.fit_on_texts(TRAIN_DATA)

# Print the number of unique words found in the DATA set (not the limit placed
# on the TOKENIZER), use this as feedback to the num_words arg of Tokenizer().
print("Found %d unique words." % len(TOKENIZER.word_index))

# One-hot encode
DATA = TOKENIZER.texts_to_matrix(TRAIN_DATA, mode="binary")

# Prepare LABELS, transform to binary and float32
LABELS = TRAIN_LABELS.astype("float32")
LABELS = TRAIN_LABELS - 1

# =========================
# Split DATA
# =========================

# Randomly shuffle DATA
INDICES = np.arange(DATA.shape[0])
np.random.shuffle(INDICES)
DATA = DATA[INDICES]
LABELS = LABELS[INDICES]

# Split into training and validation DATA (approximately 80:20)
X_TRAIN = DATA[:24000]
Y_TRAIN = LABELS[:24000]
X_VAL = DATA[24000:]
Y_VAL = LABELS[24000:]

# =========================
# Build MODEL
# =========================

# Note the input_shape of the first layer will match the num_words arg from
# the Tokenizer() function. Double check with len(DATA[0])
# The final sigmoid layer outputs probability values between [0, 1]
MODEL = models.Sequential()
MODEL.add(layers.Dense(16, activation="relu", input_shape=(10000,)))
MODEL.add(layers.Dense(16, activation="relu"))
MODEL.add(layers.Dense(1, activation="sigmoid"))

# =========================
# Train MODEL
# =========================

# As the MODEL outputs probabilities, binary crossentropy is the best LOSS
# metric as it measures the distance between probability distributions
MODEL.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])

HISTORY = MODEL.fit(
    X_TRAIN, Y_TRAIN, epochs=20, batch_size=512, validation_data=(X_VAL, Y_VAL)
)

# Prep HISTORY dictionary
ACC = HISTORY.history["acc"]
VAL_ACC = HISTORY.history["val_acc"]
LOSS = HISTORY.history["loss"]
VAL_LOSS = HISTORY.history["val_loss"]
EPOCHS = range(1, len(ACC) + 1)

# Plot the training and validation LOSS
plt.plot(EPOCHS, LOSS, "bo", label="Training loss")
plt.plot(EPOCHS, VAL_LOSS, "b", label="Validation loss")
plt.title("Training and validation LOSS")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.legend()
plt.show()

# Plot the training and validation accuracy
plt.clf()
plt.plot(EPOCHS, ACC, "bo", label="Training acc")
plt.plot(EPOCHS, VAL_ACC, "b", label="Validation acc")
plt.title("Training and validation accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.legend()
plt.show()

# =========================
# Retrain MODEL
# =========================
MODEL = models.Sequential()
MODEL.add(layers.Dense(16, activation="relu", input_shape=(10000,)))
MODEL.add(layers.Dense(16, activation="relu"))
MODEL.add(layers.Dense(1, activation="sigmoid"))

MODEL.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])

MODEL.fit(X_TRAIN, Y_TRAIN, epochs=5, batch_size=512)

# =========================
# Evaluate on test DATA
# =========================

# Load in test DATA
STANFORD_TEST = pd.read_csv("../../../data/external/stanford/misogyny_test.csv")

# Convert content columns to strings
STANFORD_TEST.content = STANFORD_TEST.content.astype(str)

# Split test Tweets and LABELS
TEST_DATA = STANFORD_TEST.content.values
TEST_LABELS = STANFORD_TEST.label.values

# DO NOT retrain to TOKENIZER. Use the argument oov_token=True to reserve a
# token for unkown words. See https://bit.ly/2lNh15g

# One-hot encode
X_TEST = TOKENIZER.texts_to_matrix(TEST_DATA, mode="binary")

# Prepare LABELS, transform to binary and float32
Y_TEST = TEST_LABELS.astype("float32")
Y_TEST = TEST_LABELS - 1

# Print results as ['LOSS', 'ACC'] check names with MODEL.metrics_names
MODEL.evaluate(X_TEST, Y_TEST)
