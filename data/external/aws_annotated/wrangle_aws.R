# Load libraries
library(tidyverse)
library(glue)
library(jsonlite)

# Load data List of annotator id's
ids <- c(1, 3, 4, 5)

# Empty value to intiate bind_rows() below
annotated_data <- NULL

# Load annotated data sets
for (i in ids) {
  
  # Load file and create new id column
  value = stream_in(file(glue("annotated/annotator_{i}.jsonl")), flatten = TRUE) %>% 
    as_tibble() %>% mutate(id = i)
  
  # Combine all files
  annotated_data <- bind_rows(annotated_data, value)
}

# Wrangle
annotated <- annotated_data %>% select(content = text, label = answer) %>% filter(label == 
  "accept" | label == "reject") %>% distinct(content, .keep_all = TRUE) %>% mutate(label = replace(label, 
  label == "accept", 1)) %>% mutate(label = replace(label, label == "reject", 0))

# Save
write_csv(annotated, "aws_data_en.csv")
