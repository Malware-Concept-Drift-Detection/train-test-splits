import sys
from .utils.best_split_utils import *
import pandas as pd
import json
import os

class MotifDataset:

    def __init__(self, motif_dataset_jsonl_filename):
        with open(motif_dataset_jsonl_filename, "r") as f:
            motif_dataset = [json.loads(line) for line in f.readlines()]

        fsd = "first_submission_date"
        print(motif_dataset[0].keys())
        df_motif = pd.DataFrame({
            "reported_hash": [sample["reported_hash"] for sample in motif_dataset],
            "family": [sample["reported_family"] for sample in motif_dataset],
            fsd: [sample["appeared"] for sample in motif_dataset],
        })

        df_motif[fsd] = pd.to_datetime(df_motif[fsd], format='%Y-%m')
        samples_per_family_count = df_motif["family"].value_counts()
        samples_per_family_count = samples_per_family_count[samples_per_family_count >= 10]

        df_motif = df_motif[df_motif["family"].isin(samples_per_family_count.index)]

        df_motif_train = df_motif[df_motif[fsd] < pd.Timestamp("2019-08-01 00:00:00")]
        df_motif_test = df_motif[df_motif[fsd] >= pd.Timestamp("2019-08-01 00:00:00")]

        df_motif_train.shape, df_motif_test.shape, df_motif.shape
        assert df_motif_train.shape[0] + df_motif_test.shape[0] == df_motif.shape[0], "Train and test sets do not match the original dataset size"

        train_family_freq = df_motif_train["family"].value_counts()
        train_family_freq = train_family_freq[train_family_freq > 3]

        df_motif_train = df_motif_train[df_motif_train["family"].isin(train_family_freq.index)]
        df_motif_test = df_motif[~df_motif.index.isin(df_motif_train.index)]

        assert df_motif_train.shape[0] + df_motif_test.shape[0] == df_motif.shape[0], "Train and test sets do not match the original dataset size"

        #print_statistics_from_train_test(df_motif_train, df_motif_test)
        self.df_motif = df_motif.set_index("reported_hash")
        self.df_motif_train = df_motif_train.set_index("reported_hash")
        self.df_motif_test = df_motif_test.set_index("reported_hash")

        print(self.df_motif.head())



if __name__ == "__main__":
    motif_dataset = MotifDataset()
    df_motif_train = motif_dataset.df_motif_train
    df_motif_test = motif_dataset.df_motif_test
    print_statistics_from_train_test(df_motif_train, df_motif_test)