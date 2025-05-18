import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from splits.norton.dataset.malware_dataset import MalwareDataset
import os
import sklearn.model_selection as ms


def train_test_split():
    # Open data with time-based split and filter dataset with truncated families
    truncated_theshold = 7
    malware_dataset = MalwareDataset(
        split=pd.Timestamp("2021-09-03 13:47:49"),
        truncated_fam_path="./splits/norton/truncated_samples_per_family.csv",
        truncated_threshold=truncated_theshold,
    )

    # Load the dataset
    dataset_env_name = "RAW_DATASET_PATH"
    if dataset_env_name in os.environ:
        ember_dataset_path = os.getenv(dataset_env_name)
        X = pd.read_csv(ember_dataset_path, index_col=0, header=0)

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
    print(f"Test set percentage: {test_p:.2%}")

    pe_dataset_type = os.getenv("PE_DATASET_TYPE")
    output_path = os.path.join(
        os.getenv("BASE_OUTPUT_PATH"), pe_dataset_type, "time_split"
    )
    os.makedirs(output_path, exist_ok=True)

    print("Saving time-based train/test split")
    X_train.to_csv(os.path.join(output_path, "X_train.csv"), index=True, header=True)
    X_test.to_csv(os.path.join(output_path, "X_test.csv"), index=True, header=True)
    y_train.to_csv(os.path.join(output_path, "y_train.csv"), index=True, header=True)
    y_test.to_csv(os.path.join(output_path, "y_test.csv"), index=True, header=True)

    # Perform random split
    rnd_seed = 42
    X_train, X_test, y_train, y_test = ms.train_test_split(
        X, y, test_size=test_p, random_state=rnd_seed
    )

    output_path = os.path.join(
        os.getenv("BASE_OUTPUT_PATH"), pe_dataset_type, "random_split"
    )
    os.makedirs(output_path, exist_ok=True)

    print("Saving random train/test split")
    X_train.to_csv(os.path.join(output_path, "X_train.csv"), index=True, header=True)
    X_test.to_csv(os.path.join(output_path, "X_test.csv"), index=True, header=True)
    y_train.to_csv(os.path.join(output_path, "y_train.csv"), index=True, header=True)
    y_test.to_csv(os.path.join(output_path, "y_test.csv"), index=True, header=True)
