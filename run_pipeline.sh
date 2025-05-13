#!/bin/bash

# Extract EMBER features from the Norton dataset
PE_DATASETS_PATH=("/home/luca/WD/NortonDataset670/MALWARE/" "/home/luca/feature_extraction/ember/MOTIF/MOTIF")
PE_DATASET_TYPES=("Norton670" "MOTIF")

RAW_DATASETS_BASE_PATH="$(pwd)/raw_dataset/"
DATASET_FILENAMES=("norton670_pe_ember_features.csv" "motif_pe_ember_features.csv")

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
  MOTIF_BASE_PATH=/home/luca/feature_extraction/ember/MOTIF/dataset/
  docker run \
    --name train-test-split-${PE_DATASET_TYPES[$i]} \
    -e RAW_DATASET_PATH="/usr/app/raw_dataset/${DATASET_FILENAMES[$i]}" \
    -e BASE_OUTPUT_PATH="/usr/app/splitted_dataset/" \
    -e PE_DATASET_TYPE="${PE_DATASET_TYPES[$i]}" \
    -v $RAW_DATASETS_BASE_PATH:/usr/app/raw_dataset/ \
    -v $SPLITTED_DATASET_PATH:/usr/app/splitted_dataset/ \
    -v $(pwd)/split_scripts/:/usr/app/split_scripts/ \
    -v $MOTIF_BASE_PATH:/usr/app/split_scripts/motif/dataset/ \
    train-test-split

  # docker run \
  #   --name transcendent \
  #   -e BASE_DATASET_PATH=/usr/app/dataset/ \
  #   -e PE_DATASET_TYPE=ember \
  #   -e TRAIN_TEST_SPLIT_TYPE=time_split \
  #   -v $CD_RESULTS_PATH:/usr/app/models/ \
  #   -v $SPLITTED_DATASET_PATH:/usr/app/dataset/ \
  #   ghcr.io/malware-concept-drift-detection/transcendent-multiclass:main

done





