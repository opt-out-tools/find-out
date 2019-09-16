# load libraries
library(tidyverse)

# Read data
hs <- read_csv("hs_data.csv")

# Wrangle
hatespeech <- hs %>%
  select(content = text, label = annotation) %>%
  mutate(label = replace(label, label == "misogynistic", 1)) %>%
  mutate(label = replace(label, label == "not_misogynistic", 0))

# Save
write_csv(hatespeech, "hatespeech_data_en.csv")
