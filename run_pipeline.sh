#!/bin/bash

# Extract EMBER features from the Norton dataset
PE_DATASETS_PATH=("/home/luca/MNTPOINT/SAMPLES/malpe/")
PE_DATASET_TYPES=("Norton670") #"MOTIF")

RAW_DATASETS_BASE_PATH="$(pwd)/raw_dataset/"
DATASET_FILENAMES=("norton670_pe_ember_features.csv") #"norton670_pe_ember_features.csv") #"motif_pe_ember_features.csv")

SPLITTED_DATASET_PATH="$(pwd)/splitted_dataset/"
# Perform train/test split
# docker build -t train-test-split .

# Detect Concept Drift using Conformal Evaluation (EMBER features + time-based split only)
CD_RESULTS_PATH="$(pwd)/results/"

for i in "${!PE_DATASETS_PATH[@]}"; do

  PE_DATASET_PATH="${PE_DATASETS_PATH[$i]}"
  
  # docker run \
  #   --name ember-feature-extraction-pipeline \
  #   -e MALWARE_DIR_PATH="/usr/input_data/malware/" \
  #   -e FINAL_DATASET_FILENAME="/usr/app/dataset/${DATASET_FILENAMES[$i]}" \
  #   -e N_PROCESSES=32 \
  #   -v $PE_DATASET_PATH:/usr/input_data/malware/ \
  #   -v $RAW_DATASETS_BASE_PATH:/usr/app/dataset/ \
  #   ghcr.io/malware-concept-drift-detection/ember-features-extraction:master

  # Perform train/test split
  #-e RAW_DATASET_PATH="/usr/app/raw_dataset/${DATASET_FILENAMES[$i]}" \

  docker run \
    --name train-test-split-${PE_DATASET_TYPES[$i]} \
    -e BASE_OUTPUT_PATH="/usr/app/splitted_dataset/" \
    -e PE_DATASET_TYPE="${PE_DATASET_TYPES[$i]}" \
    -e MALWARE_DIR_PATH="/usr/app/malware_dir/" \
    -e VTREPORTS_PATH="/usr/app/vt_reports/" \
    -v $RAW_DATASETS_BASE_PATH:/usr/app/raw_dataset/ \
    -v $SPLITTED_DATASET_PATH:/usr/app/splitted_dataset/ \
    -v /home/luca/MNTPOINT/SAMPLES/malpe/:/usr/app/malware_dir/ \
    -v /home/luca/MNTPOINT/VTREPORTS/malpe/:/usr/app/vt_reports/ \
    -v $(pwd)/splits/:/usr/app/splits/ \
    train-test-split

  docker rm train-test-split-${PE_DATASET_TYPES[$i]}

  # docker run \
  #   --name transcendent \
  #   -e BASE_DATASET_PATH=/usr/app/dataset/ \
  #   -e PE_DATASET_TYPE=ember \
  #   -e TRAIN_TEST_SPLIT_TYPE=time_split \
  #   -v $CD_RESULTS_PATH:/usr/app/models/ \
  #   -v $SPLITTED_DATASET_PATH:/usr/app/dataset/ \
  #   ghcr.io/malware-concept-drift-detection/transcendent-multiclass:main

done





