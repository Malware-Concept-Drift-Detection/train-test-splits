import os
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from splits.best_time_split.malware_dataset import MalwareDataset
import os
import sklearn.model_selection as ms
import logging
import pickle

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def train_test_split(filter_dupl: bool = False):
    malware_dataset = MalwareDataset(filter_dupl=filter_dupl)

    # Load the dataset
    dataset_env_name = "RAW_DATASET_PATH"
    if dataset_env_name in os.environ:
        ember_dataset_path = os.getenv(dataset_env_name)

        with open(ember_dataset_path, "rb") as f:
            X = pickle.load(f)
        logging.info(f"SHAPE {X.shape}")

        # X = pd.read_csv(ember_dataset_path, header=0, index_col=0)

        y = X["family"]
        X.drop(columns=["family"], inplace=True)

        # Remove features with zero variance
        sel = VarianceThreshold()
        sel.fit(X)
        X = X.loc[:, sel.get_support()]

        X = X.loc[malware_dataset.df_malware_family_fsd["sha256"]]
        y = y.loc[malware_dataset.df_malware_family_fsd["sha256"]]

    else:
        X = malware_dataset.df_malware_family_fsd.copy()
        X.set_index("sha256", inplace=True)
        y = X["family"]
        X = X.drop("family", axis=1)

    # Perform time-based split
    X_train, X_test = (
        X.loc[malware_dataset.training_dataset["sha256"]],
        X.loc[malware_dataset.testing_dataset["sha256"]],
    )

    y_train, y_test = (
        y.loc[malware_dataset.training_dataset["sha256"]],
        y.loc[malware_dataset.testing_dataset["sha256"]],
    )

    test_p = y_test.shape[0] / (y_train.shape[0] + y_test.shape[0])
    logging.info(f"Test set percentage: {test_p:.2%}")

    pe_dataset_type = os.getenv("PE_DATASET_TYPE")
    dupl_dataset_type = "dupl" if filter_dupl else "nondupl"
    output_path = os.path.join(
        os.getenv("BASE_OUTPUT_PATH"), pe_dataset_type, dupl_dataset_type, "time_split"
    )
    os.makedirs(output_path, exist_ok=True)

    logging.info("Saving time-based train/test split...")
    save_data(os.path.join(output_path, "X_train.pkl"), X_train)
    save_data(os.path.join(output_path, "X_test.pkl"), X_test)
    save_data(os.path.join(output_path, "y_train.pkl"), y_train)
    save_data(os.path.join(output_path, "y_test.pkl"), y_test)
    logging.info("Done")

    # Perform random split
    rnd_seed = 42
    X_train, X_test, y_train, y_test = ms.train_test_split(
        X, y, test_size=test_p, random_state=rnd_seed
    )

    output_path = os.path.join(
        os.getenv("BASE_OUTPUT_PATH"),
        pe_dataset_type,
        dupl_dataset_type,
        "random_split",
    )
    os.makedirs(output_path, exist_ok=True)

    logging.info("Saving random train/test split...")
    save_data(os.path.join(output_path, "X_train.pkl"), X_train)
    save_data(os.path.join(output_path, "X_test.pkl"), X_test)
    save_data(os.path.join(output_path, "y_train.pkl"), y_train)
    save_data(os.path.join(output_path, "y_test.pkl"), y_test)
    logging.info("Done")


def save_data(data_path: str, obj: object):
    with open(data_path, "wb") as f:
        pickle.dump(obj, f)


if __name__ == "__main__":
    train_test_split(filter_dupl=False)
    train_test_split(filter_dupl=True)
