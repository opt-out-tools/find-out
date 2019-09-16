# ==================================
# Load libraries
# ==================================

library(tidyverse)
library(jsonlite)

# ==================================
# Import .json files
# ==================================

amateur_expert <- jsonlite::stream_in(file("amateur_expert.json"),
                                      flatten = TRUE)

neither <- jsonlite::stream_in(file("neither.json"),
                               flatten = TRUE)

sexism <- jsonlite::stream_in(file("sexism.json"),
                              flatten = TRUE)

# ==================================
# Wrangle files
# ==================================

# amateur_expert -------------------

# Make tibble then select and rename columns to match AWS scripts
amateur_expert <- amateur_expert %>%
  as_tibble() %>%
  select(annotation = "Annotation",
         created_at,
         user_id = "user.id_str",
         status_id = "id_str",
         text,
         reply_to_status_id = "in_reply_to_status_id",
         reply_to_user_id = "in_reply_to_user_id_str",
         country = "place.country",
         country_code = "place.country_code",
         lang,
         retweet_count,
         retweet_status_id = "retweeted_status.id",
         favorite_count,
         retweet_favorite_count = "retweeted_status.favorite_count")

# Drop racism annotations and convert "both" to "sexism"
amateur_expert <- amateur_expert %>%
  filter(annotation == "Both"   |
         annotation == "Sexism" |
         annotation == "Neither") %>%
  mutate(annotation = replace(annotation,
                              annotation == "Both",
                              "Sexism"))

# neither --------------------------

# Make tibble then select and rename columns to match AWS scripts
neither <- neither %>%
  as_tibble() %>%
  select(annotation = "Annotation",
         created_at,
         user_id = "user.id_str",
         status_id = "id_str",
         text,
         reply_to_status_id = "in_reply_to_status_id",
         reply_to_user_id = "in_reply_to_user_id_str",
         country = "place.country",
         country_code = "place.country_code",
         lang,
         retweet_count,
         retweet_status_id = "retweeted_status.id",
         favorite_count,
         retweet_favorite_count = "retweeted_status.favorite_count")

# sexism ---------------------------

# Make tibble then select and rename columns to match AWS scripts
sexism <- sexism %>%
  as_tibble() %>%
  select(annotation = "Annotation",
         created_at,
         user_id = "user.id_str",
         status_id = "id_str",
         text,
         reply_to_status_id = "in_reply_to_status_id",
         reply_to_user_id = "in_reply_to_user_id_str",
         country = "place.country",
         country_code = "place.country_code",
         lang,
         retweet_count,
         retweet_status_id = "retweeted_status.id",
         favorite_count,
         retweet_favorite_count = "retweeted_status.favorite_count")


# Combined data --------------------

# Combine data, then rename annotations, then remove duplicates
zeerack_data <- bind_rows(amateur_expert, neither, sexism) %>%
  mutate(annotation = replace(annotation, annotation == "Neither", "not_misogynistic")) %>%
  mutate(annotation = replace(annotation, annotation == "none", "not_misogynistic")) %>%
  mutate(annotation = replace(annotation, annotation == "sexism", "misogynistic")) %>%
  mutate(annotation = replace(annotation, annotation == "Sexism", "misogynistic")) %>%
  arrange(annotation) %>%
  distinct(status_id, .keep_all = TRUE)

# Balance label classes by taking random sample of not_misogynistic Tweets
zeerack_data <- zeerack_data %>%
  group_by(annotation) %>%
  sample_n(4242) %>%
  ungroup()

# ==================================
# Export to .csv
# ==================================

# Save to csv
write_csv(zeerack_data, "hs_data.csv")
