# =========================
# Load libraries
# =========================

import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer

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

# Create unique integer index for every word
tokenizer = Tokenizer(num_words = 1000)
tokenizer.fit_on_texts(train_data)

# One-hot encode
data = tokenizer.texts_to_matrix(train_data, mode = 'binary')

# Prepare labels
labels = train_labels - 1

# =========================
# Split data
# =========================

# First randomly shuffle data
indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]

# Split into training and validation data (approximately 80:20)
x_train = data[:24000]
y_train = labels[:24000]
x_val   = data[24000:]
y_val   = labels[24000:]
