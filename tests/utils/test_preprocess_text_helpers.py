import pandas as pd

from src.utils.domain_objects_test import create_tokenized_tweets_df
from src.utils.domain_objects_test import create_tweets_df
from src.utils.preprocess_text_helpers import contractions_unpacker
from src.utils.preprocess_text_helpers import escape_unicode
from src.utils.preprocess_text_helpers import lowercase
from src.utils.preprocess_text_helpers import normalizer
from src.utils.preprocess_text_helpers import punctuation_cleaner
from src.utils.preprocess_text_helpers import remove_stopwords
from src.utils.preprocess_text_helpers import replace_spaces
from src.utils.preprocess_text_helpers import tokenizer
from src.utils.stopwords_and_contractions import contractions

tweets = create_tweets_df()
tokenized_tweets = create_tokenized_tweets_df()

df_contractions = pd.DataFrame(
    {
        "contraction": list(contractions().keys()),
        "unpacked": list(contractions().values()),
    }
)


def test_contraction_unpacking_all():
    df_contractions["unpacked_values"] = df_contractions["contraction"].apply(
        lambda contra: contractions_unpacker(contra)
    )
    assert df_contractions["unpacked_values"].all() == df_contractions["unpacked"].all()


def test_contraction_unpack_in_sentence():
    tweets["contractions"] = tweets["text"].apply(
        lambda tweet: contractions_unpacker(tweet)
    )
    assert (
        tweets.loc[3, "contractions"]
        == "RT @baum_erik: Lol I am not surprised these 2 accounts blocked me "
        "@femfreq #FemiNazi #Gamergate &amp; @MomsAgainstWWE "
        "#ParanoidParent http://t.câ€¦"
    )


def test_contraction_unpack_case_agnostic():
    assert contractions_unpacker("Ain't") == "am not"
    assert contractions_unpacker("I'm") == "I am"


def test_social_tokenizer():
    tweet1 = "@blanchettswhore Sunday,paul :)tweet? cele,blanchetts :) whore...?"
    tweet2 = ("LIKEWISE 14:40@Reni__Rinse who's f****N dumb idea was it to change "
        "Thor to a girl?"
    )

    assert (
        tokenizer(tweet1) == "@blanchettswhore Sunday , paul :) tweet ? cele , "
        "blanchetts :) whore . . . ?"
    )

    assert (
        tokenizer(tweet2) == "LIKEWISE 14:40 @Reni__Rinse who ' s f****N "
        "dumb idea was it to change Thor to a girl ?"
    )

    assert tokenizer(":-3;‑]O_o 3:‑) >.<") == ":-3 ;‑] O_o 3:‑) >.<"


def test_punctuation_cleaner_removes_colon():
    assert (
        punctuation_cleaner(tokenized_tweets.loc[0, "text"])
        == "RT @asredasmyhair Feminists take note #FemFreeFriday "
        "#WomenAgainstFeminism http://t.co/J2HqzVJ8Cx"
    )


def test_punctuation_cleaner_removes_fullstops():
    assert (
        punctuation_cleaner(tokenized_tweets.loc[2, "text"])
        == "@MGTOWKnight @FactsVsOpinion cue the NAFALT in 3 2 1"
    )


def test_punctuation_cleaner_removes_exclamation_marks():
    tweet = (
        "@MGTOWKnight @FactsVsOpinion . . . cue the NAFALT in 3 . . 2 . " ". . 1 ! ! !"
    )
    assert (
        punctuation_cleaner(tweet)
        == "@MGTOWKnight @FactsVsOpinion cue the NAFALT in 3 2 1"
    )


def test_lowercase():
    assert (
        lowercase(tokenized_tweets.loc[2, "text"])
        == "@mgtowknight @factsvsopinion . . . "
        "cue the nafalt in 3 . . 2 . . . 1 . "
        ". ."
    )


def test_normalize():
    tweets["normalized"] = normalizer(tweets["text"])
    assert (
        tweets.loc[0, "normalized"]
        == "RT <user> : Feminists, take note. <hashtag> <hashtag> <url>"
    )


def test_escape_a_acute():
    assert escape_unicode(["\\xe1"]) == ["á"]


def test_escape_a_umlaut():
    assert escape_unicode(["\\xe4"]) == ["ä"]


def test_escape_inverted_question_mark():
    assert escape_unicode(["\\xbf"]) == ["¿"]


def test_escape_sentence():
    assert escape_unicode(["Iam\\xbf trying to \\xe4figure out \\xe1 unicode"]) == [
        "Iam¿ trying to äfigure out á unicode"
    ]


def test_replace_whitespace():
    assert replace_spaces(["\\ntest"]) == [" test"]


def test_replace_beginning():
    assert replace_spaces(["\\xa0test test"]) == [" test test"]


def test_replace_middle():
    assert replace_spaces(["test\\xa0test"]) == ["test test"]


def test_replace_middle_twice():
    assert replace_spaces(["test\\xa0\\xa0test"]) == ["test  test"]


def test_replace_end():
    assert replace_spaces(["test\\xa0"]) == ["test "]


def test_replace_space():
    assert replace_spaces(["test\\n test"]) == ["test  test"]


def test_replace_two_times():
    assert replace_spaces(["test\\n test\\n test"]) == ["test  test  test"]


def test_replace_different_unicode():
    assert replace_spaces(["test\\xc2\\xa0test\\ntest"]) == ["test  test test"]


def test_remove_stopwords():
    assert remove_stopwords("the cat is king") == "cat king"


def test_remove_basic_stopwords():
    assert remove_stopwords("you i would it like") == ""


def test_remove_stopwords_capitals():
    # This does not remove capital stopwords as this is handled elsewhere in the
    # normalization step
    assert remove_stopwords("The cat Is king") == "The cat Is king"
