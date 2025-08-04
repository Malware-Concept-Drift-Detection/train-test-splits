#!/bin/bash

PE_DATASETS_PATHS=("/home/luca/MNTPOINT/SAMPLES/chunk/" "/home/luca/MNTPOINT/SAMPLES/malpe/")
VTREPORTS_PATHS=("/home/luca/MNTPOINT/VTREPORTS/chunk/" "/home/luca/MNTPOINT/VTREPORTS/malpe/")

PE_DATASET_TYPES=("TheFinalDataset" "Norton670")

RAW_DATASETS_BASE_PATH="/home/luca/Malware-Concept-Drift-Detection/ember/dataset/"
DATASET_FILENAMES=("thefinaldataset_ember_features.pkl"  "norton670_pe_ember_features.pkl")

NONDUPL_FILENAMES=("thefinaldataset_sha256_nondupl.pkl" "norton670_sha256_nondupl.pkl")

SPLITTED_DATASET_PATH="$(pwd)/splitted_dataset/"
DUPL_PATH="/home/luca/Malware-Concept-Drift-Detection/duplicated-pe-malware/"

DATASET_TYPE_SUFFIXES=("_post" "_pre")

for i in "${!PE_DATASETS_PATHS[@]}"; do

    DATASET_FILENAME="${DATASET_FILENAMES[$i]}"
    PE_DATASET_TYPE="${PE_DATASET_TYPES[$i]}"
    PE_DATASET_PATH="${PE_DATASETS_PATHS[$i]}"
    VTREPORTS_PATH="${VTREPORTS_PATHS[$i]}"
    NONDUPL_FILENAME="${NONDUPL_FILENAMES[$i]}"

    echo "Splitting dataset: $PE_DATASET_TYPE (post + pre feature selection)"

    for SUFFIX in "${DATASET_TYPE_SUFFIXES[@]}"; do
      PE_DATASET_TYPE_F="${PE_DATASET_TYPE}${SUFFIX}"

      ENV_VARS=(
        -e BASE_OUTPUT_PATH="/usr/app/splitted_dataset/"
        -e PE_DATASET_TYPE="$PE_DATASET_TYPE"
        -e MALWARE_DIR_PATH="/usr/app/malware_dir/"
        -e VTREPORTS_PATH="/usr/app/vt_reports/"
        -e NONDUPL_SHA256_FILENAME="/usr/app/duplicated_pe_malware/$NONDUPL_FILENAME"
      )

      if [[ "$SUFFIX" == "_post" ]]; then
        ENV_VARS+=(-e RAW_DATASET_PATH="/usr/app/raw_dataset/$DATASET_FILENAME")
      fi

      docker run \
        --name train-test-split-$PE_DATASET_TYPE_F \
        "${ENV_VARS[@]}" \
        -v $RAW_DATASETS_BASE_PATH:/usr/app/raw_dataset/ \
        -v $SPLITTED_DATASET_PATH:/usr/app/splitted_dataset/ \
        -v $DUPL_PATH:/usr/app/duplicated_pe_malware/ \
        -v $PE_DATASET_PATH:/usr/app/malware_dir/ \
        -v $VTREPORTS_PATH:/usr/app/vt_reports/ \
        -v "$(pwd)"/splits/:/usr/app/splits/ \
        train-test-split

      docker rm train-test-split-$PE_DATASET_TYPE_F
    done

done