from typing import Callable
import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt

fsd = "first_submission_date"


def compute_bs_af(
    df: pd.DataFrame,
    ref_df: pd.DataFrame,
    date_split: pd.Timestamp,
):
    df_train = df[df[fsd] < date_split]
    df_test = df[df[fsd] >= date_split]

    # Train-Test balancing: this score increases as the training test length
    # in % is approaching 80% of the samples
    train_prop = df_train.shape[0] / df.shape[0]

    balance_score: Callable = lambda x: 1 - np.abs(x - 0.8) / 0.8
    bs = balance_score(train_prop)

    train_families = df_train["family"].unique()
    test_families = df_test["family"].unique()
    # % Appearing families in testing set
    af = (
        len(test_families) - len(np.intersect1d(train_families, test_families))
    ) / len(df["family"].unique())

    return (bs, af)


def print_statistics(df: pd.DataFrame, split: pd.Timestamp, label: str = ""):
    df_train, df_test = df[df[fsd] < split], df[df[fsd] >= split]
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
    df_scores, df_ref_scores = df.copy(), df.copy()
    t_unique = df[fsd].sort_values().unique()

    perc_app_families, balance_scores = [], []
    for date_split in t_unique:
        bs, af = compute_bs_af(
            df=df_scores, ref_df=df_ref_scores, date_split=date_split
        )
        perc_app_families.append(af)
        balance_scores.append(bs)

    # Min-Max normalization
    perc_app_families_min_max = (perc_app_families - np.min(perc_app_families)) / (
        np.max(perc_app_families) - np.min(perc_app_families)
    )
    balance_scores_min_max = (balance_scores - np.min(balance_scores)) / (
        np.max(balance_scores) - np.min(balance_scores)
    )
    # Objective function: maximize the percentage of appearing families in the test set + balance score
    f_objective = perc_app_families_min_max + balance_scores_min_max

    x = list(range(len(t_unique)))  # X-axis

    plt.plot(x, perc_app_families_min_max, label="Percentage of Appearing Families")
    plt.plot(x, balance_scores_min_max, label="Balance Score")
    plt.plot(x, f_objective, label="F obj")

    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Three Line Plot")
    plt.legend()
    plt.grid(True)

    plt.savefig("./splits/my_plot.png")  # Save to PNG file
    plt.close()

    t_split_mid = t_unique[np.argmax(f_objective)]
    print_statistics(df, t_split_mid)
    return t_split_mid
