PE_DATASETS_PATH=("/home/luca/WD/NortonDataset670/MALWARE/") #"/home/luca/feature_extraction/ember/MOTIF/MOTIF")
PE_DATASET_TYPES=("Norton670") #"MOTIF")

RAW_DATASETS_BASE_PATH="$(pwd)/raw_dataset/"
DATASET_FILENAME="norton670_pe_ember_features.csv" #"motif_pe_ember_features.csv")

SPLITTED_DATASET_PATH="$(pwd)/splitted_dataset/"
# Perform train/test split
# docker build -t train-test-split .

# Detect Concept Drift using Conformal Evaluation (EMBER features + time-based split only)
CD_RESULTS_PATH="$(pwd)/results/"

docker run \
    --name train-test-split-${PE_DATASET_TYPES[0]} \
    -e BASE_OUTPUT_PATH="/usr/app/splitted_dataset/" \
    -e PE_DATASET_TYPE=${PE_DATASET_TYPES[0]} \
    -e MALWARE_DIR_PATH="/usr/app/malware_dir/" \
    -e VTREPORTS_PATH="/usr/app/vt_reports/" \
    -e RAW_DATASET_PATH="/usr/app/raw_dataset/${DATASET_FILENAME}" \
    -v $RAW_DATASETS_BASE_PATH:/usr/app/raw_dataset/ \
    -v $SPLITTED_DATASET_PATH:/usr/app/splitted_dataset/ \
    -v /home/luca/MNTPOINT/SAMPLES/malpe/:/usr/app/malware_dir/ \
    -v /home/luca/MNTPOINT/VTREPORTS/malpe/:/usr/app/vt_reports/ \
    -v $(pwd)/raw_dataset/:/usr/app/raw_dataset/ \thefinaldataset_ember_features
    -v $(pwd)/splits/:/usr/app/splits/ \
    train-test-split