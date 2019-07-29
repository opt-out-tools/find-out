# ==================================
# Load libraries
# ==================================

library(tidyverse)
library(rtweet)

# ==================================
# Import hatespeech .csv files
# ==================================

file_1 <- read_tsv("/home/mike/Documents/opt-out-master/hatespeech/NLP+CSS_2016.csv",
                   col_types = cols_only(TweetID = "c", Expert = "c"))

file_2 <- read_csv("/home/mike/Documents/opt-out-master/hatespeech/NAACL_SRW_2016.csv",
                   col_names = FALSE,
                   col_types = "cc")


# ==================================
# Wrangle files
# ==================================

# file_1
file_1 <- file_1 %>% 
  select(status_id = "TweetID", label = "Expert") %>% 
  filter(label == "both" | label == "sexism" | label == "neither") %>% 
  mutate(label = replace(label, label == "both", "sexism"))

# file_2
file_2 <- file_2 %>% 
  select(status_id = "X1", label = "X2") %>% 
  filter(label == "sexism" | label == "none")

# Combine files, then remove duplicates, then take random sample grouped by
# label to balance classes
misogyny_data <- bind_rows(file_1, file_2) %>% 
  distinct(status_id, .keep_all = TRUE) %>% 
  mutate(label = replace(label, label == "neither", "not_misogynistic")) %>% 
  mutate(label = replace(label, label == "none", "not_misogynistic")) %>% 
  mutate(label = replace(label, label == "sexism", "misogynistic"))

# ==================================
# Return Tweets
# ==================================

# Return Tweets by status_id
tweets <- lookup_tweets(misogyny_data$status_id) 

# Select columns to match AWS data sets
tweets <- select(tweets,
                 created_at,
                 user_id,
                 status_id,
                 text,
                 reply_to_status_id,
                 reply_to_user_id,
                 user_id,
                 country,
                 country_code,
                 location,
                 lang,
                 retweet_count,
                 is_retweet,
                 retweet_location,
                 retweet_status_id,
                 reply_count,
                 favorite_count,
                 retweet_favorite_count)

# Join back to original misogyny data set to retrieve label
labelled_tweets <- left_join(misogyny_data,
                             tweets,
                             by = "status_id")

# Remove any Tweets that were returned by the Twitter API
labelled_tweets <- labelled_tweets %>% 
  drop_na(text)

# Balance label classes by taking random sample of not_misogynistic Tweets
labelled_tweets <- labelled_tweets %>%
  group_by(label) %>% 
  sample_n(3468) %>%
  ungroup()
  
# Save to csv
write_csv(labelled_tweets, "zeerack_data.csv")