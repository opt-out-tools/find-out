from typing import Callable, List

from src.utils.preprocess_text_helpers import (
    contractions_unpacker,
    tokenizer,
    remove_stopwords,
    normalizer,
    punctuation_cleaner,
    lowercase,
)


class TextPipeline:
    def __init__(self):
        self._processors: List[Callable[[str], str]] = []

    def register_processor(self, method: Callable[[str], str]):
        self._processors.append(method)

    def process_text(self, text):
        for processor in self._processors:
            text = processor(text)

        return text


def clean(dataframe):
    """Returns cleaned text.

          Args
              df (pandas df) : the dataframe with the tweets under a column
              labeled text.

          Returns
              df (pandas df) : the cleaned tweets under the column cleaned.

    """
    pipeline = TextPipeline()
    pipeline.register_processor(contractions_unpacker)
    pipeline.register_processor(tokenizer)
    pipeline.register_processor(punctuation_cleaner)
    pipeline.register_processor(remove_stopwords)
    pipeline.register_processor(lowercase)

    dataframe["cleaned"] = dataframe["text"].apply(pipeline.process_text)
    return dataframe


def normalize(dataframe):
    """Returns normalized text.

    Args
        df (pandas df) : the dataframe with the tweets under a column
        labeled text.

    Returns
        df (pandas df) : the normalized tweets under the column normalized.

    """
    pipeline = TextPipeline()
    pipeline.register_processor(contractions_unpacker)
    pipeline.register_processor(tokenizer)
    pipeline.register_processor(punctuation_cleaner)
    pipeline.register_processor(remove_stopwords)
    pipeline.register_processor(lowercase)

    dataframe["cleaned"] = dataframe["text"].apply(pipeline.process_text)
    dataframe["normalized"] = normalizer(dataframe["cleaned"])
    return dataframe


def tokenize(dataframe):
    """Returns tokenized text in string format.

       Args
           df (pandas df) : the dataframe with the tweets under a column
           labeled text.

       Returns
           df (pandas df) : the tokenized tweets under the column tokenized.

    """
    pipeline = TextPipeline()
    pipeline.register_processor(contractions_unpacker)
    pipeline.register_processor(tokenizer)
    pipeline.register_processor(lowercase)

    dataframe["tokenized"] = dataframe["text"].apply(pipeline.process_text)
    return dataframe
