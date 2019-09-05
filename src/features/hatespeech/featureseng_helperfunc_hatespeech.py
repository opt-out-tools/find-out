import numpy as np

def combine_feature_space(wordvecs, feature_to_add):
    """Returns 1 is the tweet contains the substring which are sexualized nouns often used in rapeglish and 0 if not
    Args:
        wordvectors (csr_matrix) : The tf-idf word vectors
        feature_to_add (np array : The new feature to add.
    Returns:
        combined feature space (np array)  : The combined tf-idf and feature space.
    """
    wordvecs = wordvecs.toarray()
    feature_to_add = feature_to_add.reshape(len(wordvecs), 1)
    return np.hstack((wordvecs,feature_to_add))
