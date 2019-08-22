library(tidyverse)
library(jsonlite)

# ================================
# Load data
# ================================

annotator_1 <-
  stream_in(file("annotated/annotator_1.jsonl"),
            flatten = TRUE) %>% 
  as_tibble()

annotator_3 <-
  stream_in(file("annotated/annotator_3.jsonl"),
            flatten = TRUE) %>% 
  as_tibble()

annotator_4 <-
  stream_in(file("annotated/annotator_4.jsonl"),
            flatten = TRUE) %>% 
  as_tibble()

annotator_5 <-
  stream_in(file("annotated/annotator_5.jsonl"),
            flatten = TRUE) %>% 
  as_tibble()

unannotated_1 <- 
  read_csv("unannotated/annotator_1.csv")

unannotated_3 <- 
  read_csv("unannotated/annotator_3.csv")

unannotated_4 <- 
  read_csv("unannotated/annotator_4.csv")

unannotated_5 <- 
  read_csv("unannotated/annotator_5.csv")

unannotated_data <- bind_rows(unannotated_1,
                              unannotated_3,
                              unannotated_4,
                              unannotated_5)

annotated_data <- bind_rows(annotator_1,
                            annotator_3,
                            annotator_4,
                            annotator_5)
 
zeerack_data <- 
  read_csv("find-out/data/external/zeerack/zeerack_data.csv")


# ================================
# Wrangle Data
# ================================

# unannotated_data
unannotated_data <- unannotated_data %>% 
  distinct(text, .keep_all = TRUE)

# annotated_data
# Drop unwated cols
# Drop ignored Tweets
# Remove duplicates
annotated_data <- annotated_data %>% 
  select(text, answer) %>%                             
  filter(answer == "accept" | answer == "reject") %>%
  distinct(text, .keep_all = TRUE)                     

# Add annotation labels to original data (with meta data)
# Rename answer col
# Rename annotation labels
# Change data column to char to make bindable to zeerack's data
opt_out_data <- left_join(annotated_data, unannotated_data) %>% 
  rename("annotation" = answer) %>%                    
  mutate(annotation = replace(annotation,
                              annotation == "reject",
                              "not_misogynistic")) %>% 
  mutate(annotation = replace(annotation,
                              annotation == "accept",
                              "misogynistic")) %>% 
  mutate(created_at = as.character(created_at))

# Find and keep indices of colnames in opt_out_data that appear in zeerack data
opt_out_data <- opt_out_data %>% 
  select(which(colnames(opt_out_data) %in% colnames(zeerack_data)))

# Combine opt_out_data and zeerack_data
nlp_test_data <- bind_rows(opt_out_data,
                           zeerack_data)

# Write to csv
write_csv(nlp_test_data, "nlp_test_data.csv")
