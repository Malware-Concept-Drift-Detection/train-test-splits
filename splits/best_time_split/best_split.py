from typing import Callable, List
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
import math
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial


fsd = "first_submission_date"


def find_balanced_split(
    df: pd.DataFrame, timestamps: List[pd.Timestamp], training_perc: float
) -> pd.Timestamp:
    low, high = 0, len(timestamps) - 1
    best_idx = None
    best_diff = float("inf")

    while low <= high:
        mid = (low + high) // 2
        mid_value = timestamps[mid]
        df_train, _ = train_test_split_by_date(df, mid_value)
        perc_train = len(df_train) / len(df)

        # Track the closest match
        diff = abs(perc_train - training_perc)
        if diff < best_diff:
            best_diff = diff
            best_idx = mid

        if perc_train < training_perc:
            low = mid + 1
        else:
            high = mid - 1

    return timestamps[best_idx] if best_idx is not None else None


def train_test_split_by_date(df: pd.DataFrame, date_split: pd.Timestamp):
    df_train = df[df[fsd] < date_split]
    df_test = df[df[fsd] >= date_split]

    # Step 2: Count per-family samples in train and in total
    train_counts = df_train["family"].value_counts().rename("train_size")
    total_counts = df["family"].value_counts().rename("total_size")

    # Step 3: Join and compute ratio
    ratio_df = pd.concat([train_counts, total_counts], axis=1).fillna(0)
    ratio_df["train_ratio"] = ratio_df["train_size"] / ratio_df["total_size"]

    # Step 4: Filter families with at least 10% in training
    valid_families = ratio_df[ratio_df["train_ratio"] >= 0.1].index

    df_train = df_train[df_train["family"].isin(valid_families)]
    df_test = df[~df["sha256"].isin(df_train["sha256"])]
    return df_train, df_test


def print_statistics(df: pd.DataFrame, split: pd.Timestamp, label: str = ""):
    # df_train, df_test = df[df[fsd] < split], df[df[fsd] >= split]

    df_train, df_test = train_test_split_by_date(df, split)

    logging.info("------------------------------------------------------------------")
    logging.info(f"Report for split {split}")
    logging.info(
        f"\tTraining set length: {len(df_train)}, ({round(len(df_train) / len(df) * 100, 2)}%)"
    )
    logging.info(
        f"\tTesting set length: {len(df_test)}, ({round(len(df_test) / len(df) * 100, 2)}%)"
    )
    logging.info(f"\tNum families in training: {len(df_train['family'].unique())}")
    logging.info(f"\tNum families in testing: {len(df_test['family'].unique())}")

    n_cup = len(np.intersect1d(df_train["family"].unique(), df_test["family"].unique()))
    logging.info(f"\tCommon families: {n_cup}")
    n_new_families = len(df_test["family"].unique()) - n_cup
    n_dis_families = len(df_train["family"].unique()) - n_cup
    logging.info(
        f"\tFamilies in training but not in testing: {n_dis_families} "
        f"({round(n_dis_families / len(df['family'].unique()) * 100, 2)}%)"
    )
    logging.info(
        f"\tFamilies in testing but not in training: {n_new_families} "
        f"({round(n_new_families / len(df['family'].unique()) * 100, 2)}%)"
    )


def compute_time_split(df: pd.DataFrame, train_len: float = 0.7) -> pd.Timestamp:
    t_unique = df[fsd].sort_values().unique()
    t_best = find_balanced_split(df, t_unique, train_len)
    print_statistics(df, t_best)
    return t_best
