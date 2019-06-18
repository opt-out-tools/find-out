import pandas as pd
import sys
import regex as re
import pytest
# path_to_dataset=sys.argv[1]
# df = pd.read_csv(path_to_dataset)

pattern_matches_word_between_single_quotes = r"'\b.+?(?=':|',)"
example = '{\'created_at\': \'Thu Nov 02 08:46:28 +0000 2017\', \'id\': 926007588604579840, \'id_str\': \'926007588604579840\', \'text\': \'Psykolog om #MeToo: – Har pasienter som angrer på at de har deltatt i kampanjen https://t.co/vVXzFH07ol\', \'truncated\': False, \'entities\': {\'hashtags\': [{\'text\': \'MeToo\', \'indices\': [12, 18]}], \'symbols\': [], \'user_mentions\': [], \'urls\': [{\'url\': \'https://t.co/vVXzFH07ol\', \'expanded_url\': \'https://www.nrk.no/norge/1.13758025\', \'display_url\': \'nrk.no/norge/1.137580…\', \'indices\': [80, 103]}]}, \'source\': \'<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>\', \'in_reply_to_status_id\': None, \'in_reply_to_status_id_str\': None, \'in_reply_to_user_id\': None, \'in_reply_to_user_id_str\': None, \'in_reply_to_screen_name\': None, \'user\': {\'id\': 64358383, \'id_str\': \'64358383\', \'name\': \'Baard Fossli Jensen\', \'screen_name\': \'fosslijensen\', \'location\': \'Norway\', \'description\': \'Patients need both warmth and competence. Training Crisis Linguistics with doctors, nurses and 911-operators. Pediatrician, Ph.D. doctor-patient communication.\', \'url\': None, \'entities\': {\'description\': {\'urls\': []}}, \'protected\': False, \'followers_count\': 1328, \'friends_count\': 1108, \'listed_count\': 23, \'created_at\': \'Mon Aug 10 08:02:11 +0000 2009\', \'favourites_count\': 296, \'utc_offset\': None, \'time_zone\': None, \'geo_enabled\': True, \'verified\': False, \'statuses_count\': 2180, \'lang\': None, \'contributors_enabled\': False, \'is_translator\': False, \'is_translation_enabled\': False, \'profile_background_color\': \'C0DEED\', \'profile_background_image_url\': \'http://abs.twimg.com/images/themes/theme1/bg.png\', \'profile_background_image_url_https\': \'https://abs.twimg.com/images/themes/theme1/bg.png\', \'profile_background_tile\': False, \'profile_image_url\': \'http://pbs.twimg.com/profile_images/956194813501673473/O1vVBpCU_normal.jpg\', \'profile_image_url_https\': \'https://pbs.twimg.com/profile_images/956194813501673473/O1vVBpCU_normal.jpg\', \'profile_banner_url\': \'https://pbs.twimg.com/profile_banners/64358383/1422109549\', \'profile_link_color\': \'1DA1F2\', \'profile_sidebar_border_color\': \'C0DEED\', \'profile_sidebar_fill_color\': \'DDEEF6\', \'profile_text_color\': \'333333\', \'profile_use_background_image\': True, \'has_extended_profile\': False, \'default_profile\': True, \'default_profile_image\': False, \'following\': False, \'follow_request_sent\': False, \'notifications\': False, \'translator_type\': \'none\'}, \'geo\': None, \'coordinates\': None, \'place\': None, \'contributors\': None, \'is_quote_status\': False, \'retweet_count\': 2, \'favorite_count\': 3, \'favorited\': False, \'retweeted\': False, \'possibly_sensitive\': False, \'possibly_sensitive_appealable\': False, \'lang\': \'no\'}'


def substitute(string):
    """
    """
    first = re.sub(r"'\b", "\"", string)
    last = re.sub(r"'\B", "\"", first)
    return last


def test_substitutes_single_for_double():
    basic_json = '{\'created_at\': \'Thu Nov 02 08:46:28 +0000 2017\', \'id_str\': \'926007588604579840\'}'
    print(repr(substitute(basic_json)))
    assert substitute(basic_json).find("\'") == -1

def test_ignores_apostrophies():
    basic_json = '{\'created_at\': \'Thu Nov 02 08:46:28 +0000 2017\', \'id_str\': \'9260075886\'04579840\', \'text\': \'I am a test\'}'
    print(repr(substitute(basic_json)))
    assert substitute(basic_json).find("\'") != -1



