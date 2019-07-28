# ==================================
# Load libraries
# ==================================

library(tidyverse)
library(rtweet)

# ==================================
# Import hatespeech .csv files
# ==================================

file_1 <- read_tsv("/home/mike/Documents/opt-out-master/hatespeech/NLP+CSS_2016.csv")

file_2 <- read_csv("/home/mike/Documents/opt-out-master/hatespeech/NAACL_SRW_2016.csv",
                   col_names = FALSE)

# ==================================
# Wrangle files
# ==================================

# file_1
file_1 <- file_1 %>% 
  select(tweet_id = "TweetID", label = "Expert") %>% 
  filter(label == "both" | label == "sexism") %>% 
  mutate(label = replace(label, label == "both", "sexism"))

# file_2
file_2 <- file_2 %>% 
  select(tweet_id = "X1", label = "X2") %>% 
  filter(label == "sexism" | label == "none")

# Combine files, then remove duplicates, then take random sample grouped by
# label to balance classes
sexism_data <- bind_rows(file_1, file_2) %>% 
  distinct(tweet_id, .keep_all = TRUE) %>%
  group_by(label) %>% 
  sample_n(4242) %>% 
  ungroup()

# ==================================
# Return Tweets
# ==================================

  