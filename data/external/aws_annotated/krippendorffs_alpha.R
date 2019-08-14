library(tidyverse)
library(glue)
library(jsonlite)
library(rel)

# ================================
# Load data
# ================================

# List of annotator id's
ids <- c(1, 3, 4, 5)

# Empty value to intiate bind_rows() below
unannotated_data <- NULL
annotated_data <- NULL

# --------------------------------

# Load unannotated data sets
for(i in ids){
  
  # Load file and create new id column
  value = read_csv(glue("unannotated/annotator_{i}.csv")) %>% 
    mutate(id = i)
  
  # Combine all files
  unannotated_data <- bind_rows(unannotated_data, value)
}

# --------------------------------

# Load annotated data sets
for(i in ids){
  
  # Load file and create new id column
  value = stream_in(file(glue("annotated/annotator_{i}.jsonl")),
                    flatten = TRUE) %>% 
    as_tibble() %>% 
    mutate(id = i)
  
  # Combine all files
  annotated_data <- bind_rows(annotated_data, value)
}

# ================================
# Wrangle Data
# ================================

# unannotated_data
# Keep only inter-rater shared Tweets and drop cols
inter_rater_true <- unannotated_data %>% 
  filter(inter_rater == TRUE) %>% 
  select(text, id)

# --------------------------------

# annotated_data
# Drop cols
annotated_dropped <- annotated_data %>% 
  select(text, id, answer)

# --------------------------------

# Join data
inter_rater <- left_join(inter_rater_true, annotated_dropped)

# Check inter_rater tweets are in the same order by id
mean(inter_rater$text[1:100] == inter_rater$text[101:200])
mean(inter_rater$text[1:100] == inter_rater$text[201:300])
mean(inter_rater$text[1:100] == inter_rater$text[301:400])

# Create matrix with n id's and m labels (n*m)
annotated_matrix <- inter_rater %>%
  group_by(id) %>% 
  mutate(group_id = row_number()) %>%
  spread(id, answer) %>% 
  select(`1`, `3`, `4`, `5`) %>% 
  as.matrix()

# Create matrix dropping "ignore" answers
annotated_matrix_no_ignore <- inter_rater %>%
  group_by(id) %>% 
  mutate(group_id = row_number()) %>%
  filter(answer == "reject" | answer == "accept") %>% 
  spread(id, answer) %>% 
  select(`1`, `3`, `4`, `5`) %>% 
  as.matrix()

# ================================
# Calculate Krippendorff's alpha
# ================================

kra(annotated_matrix, metric = "nominal")

kra(annotated_matrix_no_ignore, metric = "nominal")
