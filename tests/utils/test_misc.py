import numpy as np

from src.utils.misc import is_correctly_labelled


def test_create_spacy_docs(spacy_docs):
    assert len(spacy_docs) == 4


def test_is_cyber_bullying():
    score = np.array([0.6], dtype=float)
    target = np.array([1.0], dtype=float)
    assert is_correctly_labelled(score, target) == 100


def test_is_not_cyber_bullying():
    score = np.array([0.49], dtype=float)
    target = np.array([0.0], dtype=float)
    assert is_correctly_labelled(score, target) == 100


def test_boundary_test():
    score = np.array([0.5], dtype=float)
    target = np.array([1.0], dtype=float)
    assert is_correctly_labelled(score, target) == 100
