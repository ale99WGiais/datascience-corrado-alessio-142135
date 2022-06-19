


library(readxl)
library(tidyverse)
library(dplyr)

list_of_files <- list.files(path = "out",
                            recursive = TRUE,
                            pattern = "\\.csv$",
                            full.names = TRUE)
df <- list_of_files %>%
  set_names() %>% 
  map_df(read_csv, .id = "file_name")


df
