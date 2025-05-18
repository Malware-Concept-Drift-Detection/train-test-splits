import pandas as pd
from sklearn.feature_selection import VarianceThreshold
import os
from sklearn.model_selection import train_test_split
from splits.motif.motif_dataset import MotifDataset
from splits.motif.utils.best_split_utils import print_statistics_from_train_test

def train_test_split():
    # Load the dataset
    ember_dataset_path = os.getenv("RAW_DATASET_PATH")
    X = pd.read_csv(ember_dataset_path, index_col=0, header=0)

    motif_dataset = MotifDataset("split_scripts/motif/dataset/motif_dataset.jsonl")
    l = list(motif_dataset.df_motif.index)
    assert any([ll in X.index for ll in l]), "Motif dataset not found in ember dataset"

    X = X.loc[l]

    X["family"] = motif_dataset.df_motif["family"]
    y = X["family"]
    X.drop(columns=["family"], inplace=True)

    # # Remove features with zero variance

    sel = VarianceThreshold()
    sel.fit(X)
    X = X.loc[:, sel.get_support()]

    X_train, X_test = (
        X.loc[motif_dataset.df_motif_train.index],
        X.loc[motif_dataset.df_motif_test.index],
    )

    y_train, y_test = (
        y.loc[motif_dataset.df_motif_train.index],
        y.loc[motif_dataset.df_motif_test.index],
    )

    print_statistics_from_train_test(X_train, X_test)

    pe_dataset_type = os.getenv("PE_DATASET_TYPE")
    output_path = os.path.join(os.getenv("BASE_OUTPUT_PATH"), pe_dataset_type, "time_split")
    os.makedirs(output_path, exist_ok=True)

    X_train.to_csv(os.path.join(output_path, "X_train.csv"), index=True, header=True)
    X_test.to_csv(os.path.join(output_path, "X_test.csv"), index=True, header=True)
    y_train.to_csv(os.path.join(output_path, "y_train.csv"), index=True, header=True)
    y_test.to_csv(os.path.join(output_path, "y_test.csv"), index=True, header=True)

    # Perform random split
    test_p = y_test.shape[0] / (y_train.shape[0] + y_test.shape[0])

    rnd_seed = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_p, random_state=rnd_seed)

    output_path = os.path.join(os.getenv("BASE_OUTPUT_PATH"), pe_dataset_type, "random_split")
    os.makedirs(output_path, exist_ok=True)

    X_train.to_csv(os.path.join(output_path, "X_train.csv"), index=True, header=True)
    X_test.to_csv(os.path.join(output_path, "X_test.csv"), index=True, header=True)
    y_train.to_csv(os.path.join(output_path, "y_train.csv"), index=True, header=True)
    y_test.to_csv(os.path.join(output_path, "y_test.csv"), index=True, header=True)