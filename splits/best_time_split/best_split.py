from typing import Callable
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
import math
from tqdm import tqdm
from multiprocessing import Pool
from functools import partial


fsd = "first_submission_date"


def find_balanced_split(df, timestamps, training_perc):
    low, high = 0, len(timestamps) - 1
    best_idx = None
    best_diff = float("inf")

    while low <= high:
        mid = (low + high) // 2
        mid_value = timestamps[mid]
        perc_train = len(df[df[fsd] < mid_value]) / len(df)

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

    # Step 4: Filter families with at least 5% in training
    valid_families = ratio_df[ratio_df["train_ratio"] >= 0.1].index

    df_train = df_train[df_train["family"].isin(valid_families)]
    df_test = df[~df["sha256"].isin(df_train["sha256"])]
    return df_train, df_test


def compute_bs_af(
    df: pd.DataFrame,
    date_split: pd.Timestamp,
):
    df_train, df_test = train_test_split_by_date(df, date_split)
    # Train-Test balancing: this score increases as the training test length
    # in % is approaching 80% of the samples
    train_prop = df_train.shape[0] / df.shape[0]
    r = 0.75
    sigma = 0.05

    # balance_score: Callable = lambda x: 1 - np.abs(x - 0.7) / 0.7
    balance_score: Callable = lambda x: math.exp(-((x - r) ** 2) / (2 * sigma**2))
    bs = balance_score(train_prop)

    train_families = df_train["family"].unique()
    test_families = df_test["family"].unique()
    # % Appearing families in testing set
    af = (
        len(test_families) - len(np.intersect1d(train_families, test_families))
    ) / len(df["family"].unique())

    return (bs, af)


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


def compute_best_time_split(df: pd.DataFrame):
    df_scores = df.copy()
    t_unique = df[fsd].sort_values().unique()

    perc_app_families, balance_scores = [], []

    t_max_split = find_balanced_split(df, t_unique, 0.9)
    t_min_split = find_balanced_split(df, t_unique, 0.6)

    t_unique = t_unique[
        (t_unique >= t_min_split) & (t_unique <= t_max_split)
    ]  # Filter timestamps between min and max split

    compute_bs_af_partial = partial(compute_bs_af, df_scores)

    with Pool() as pool:
        # Parallel computation of balance score and % appearing families
        results = list(
            tqdm(
                pool.map(
                    compute_bs_af_partial,
                    t_unique,
                ),
                total=len(t_unique),
                desc="Computing BS and NF scores for each split",
            )
        )
    balance_scores = [result[0] for result in results]
    perc_app_families = [result[1] for result in results]

    # for date_split in tqdm(t_unique, desc="Computing BS and NF scores for each split"):
    #     bs, af = compute_bs_af(
    #         df=df_scores, date_split=date_split
    #     )
    #     perc_app_families.append(af)
    #     balance_scores.append(bs)
    # Min-Max normalization
    if (np.max(perc_app_families) - np.min(perc_app_families)) == 0:
        perc_app_families_min_max = np.zeros_like(perc_app_families)
    else:
        perc_app_families_min_max = (perc_app_families - np.min(perc_app_families)) / (
            np.max(perc_app_families) - np.min(perc_app_families)
        )
    if (np.max(balance_scores) - np.min(balance_scores)) == 0:
        balance_scores_min_max = np.zeros_like(balance_scores)
    else:
        balance_scores_min_max = (balance_scores - np.min(balance_scores)) / (
            np.max(balance_scores) - np.min(balance_scores)
        )
    # Objective function: maximize the percentage of appearing families in the test set + balance score
    f_objective = [
        af + bs for (af, bs) in zip(perc_app_families_min_max, balance_scores_min_max)
    ]
    x = list(range(len(t_unique)))

    plt.plot(x, perc_app_families_min_max, label="Percentage of Appearing Families")
    plt.plot(x, balance_scores_min_max, label="Balance Score")
    plt.plot(x, f_objective, label="F obj")

    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Three Line Plot")
    plt.legend()
    plt.grid(True)

    plt.savefig("./splits/my_plot1.png")  # Save to PNG file
    plt.close()

    t_split_mid = t_unique[np.argmax(f_objective)]
    print_statistics(df, t_split_mid)
    return t_split_mid
