#!/bin/bash

# Extract EMBER features from the Norton dataset
# docker run \
#   --name ember-feature-extraction-pipeline \
#   -e MALWARE_DIR_PATH=/usr/input_data/malware/ \
#   -e FINAL_DATASET_DIR=/usr/app/dataset/ \
#   -e N_PROCESSES=32 \
#   -v /home/luca/WD/NortonDataset670/MALWARE/:/usr/input_data/malware/ \
#   -v $(pwd)/raw_dataset/:/usr/app/dataset/ \
#   ghcr.io/malware-concept-drift-detection/ember-features-extraction:master


# Perform train/test split
docker build -t train-test-split .

docker run \
  --name train-test-split \
  -e RAW_DATASET_PATH="/usr/app/raw_dataset/malware_ember_features.csv" \
  -e BASE_OUTPUT_PATH="/usr/app/splitted_dataset/" \
  -v $(pwd)/raw_dataset/:/usr/app/raw_dataset/ \
  -v $(pwd)/splitted_dataset/:/usr/app/splitted_dataset/ \
  train-test-split


# Detect Concept Drift using Conformal Evaluation
docker run \
  --name transcendent \
  -e BASE_DATASET_PATH=/usr/app/dataset/ \
  -e PE_DATASET_TYPE=ember \
  -e TRAIN_TEST_SPLIT_TYPE=time_split \
  -v $(pwd)/results/:/usr/app/models/ \
  -v $(pwd)/splitted_dataset/:/usr/app/dataset/ \
  ghcr.io/malware-concept-drift-detection/transcendent-multiclass:main