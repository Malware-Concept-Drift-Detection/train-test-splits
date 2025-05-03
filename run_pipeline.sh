#!/bin/bash

# Extract EMBER features from the Norton dataset
PE_DATASET_PATH="/home/luca/WD/NortonDataset670/MALWARE/"
RAW_DATASET_PATH="$(pwd)/raw_dataset/"

docker run \
  --name ember-feature-extraction-pipeline \
  -e MALWARE_DIR_PATH=/usr/input_data/malware/ \
  -e FINAL_DATASET_DIR=/usr/app/dataset/ \
  -e N_PROCESSES=32 \
  -v $PE_DATASET_PATH:/usr/input_data/malware/ \
  -v $RAW_DATASET_PATH:/usr/app/dataset/ \
  ghcr.io/malware-concept-drift-detection/ember-features-extraction:master


# Perform train/test split
docker build -t train-test-split .

SPLITTED_DATASET_PATH="$(pwd)/splitted_dataset/"
docker run \
  --name train-test-split \
  -e RAW_DATASET_PATH="/usr/app/raw_dataset/malware_ember_features.csv" \
  -e BASE_OUTPUT_PATH="/usr/app/splitted_dataset/" \
  -v $RAW_DATASET_PATH:/usr/app/raw_dataset/ \
  -v $SPLITTED_DATASET_PATH:/usr/app/splitted_dataset/ \
  train-test-split


# Detect Concept Drift using Conformal Evaluation (EMBER features + time-based split only)
CD_RESULTS_PATH="$(pwd)/results/"
docker run \
  --name transcendent \
  -e BASE_DATASET_PATH=/usr/app/dataset/ \
  -e PE_DATASET_TYPE=ember \
  -e TRAIN_TEST_SPLIT_TYPE=time_split \
  -v $CD_RESULTS_PATH:/usr/app/models/ \
  -v $SPLITTED_DATASET_PATH:/usr/app/dataset/ \
  ghcr.io/malware-concept-drift-detection/transcendent-multiclass:main