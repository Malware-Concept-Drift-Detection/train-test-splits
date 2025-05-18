from typing import Callable

import pandas as pd
import numpy as np


fsd = "first_submission_date"


def print_statistics_from_train_test(
    df_train: pd.DataFrame, df_test: pd.DataFrame, label: str = ""
):
    df = pd.concat([df_train, df_test])
    print("------------------------------------------------------------------")
    print(f"Report: {label}")
    print(
        f"\tTraining set length: {len(df_train)}, ({round(len(df_train) / len(df) * 100, 2)}%)"
    )
    print(
        f"\tTesting set length: {len(df_test)}, ({round(len(df_test) / len(df) * 100, 2)}%)"
    )
    print(f"\tNum families in training: {len(df_train['family'].unique())}")
    print(f"\tNum families in testing: {len(df_test['family'].unique())}")

    n_cup = len(np.intersect1d(df_train["family"].unique(), df_test["family"].unique()))
    print(f"\tCommon families: {n_cup}")
    n_new_families = len(df_test["family"].unique()) - n_cup
    n_dis_families = len(df_train["family"].unique()) - n_cup
    print(
        f"\tFamilies in training but not in testing: {n_dis_families} "
        f"({round(n_dis_families / len(df['family'].unique()) * 100, 2)}%)"
    )
    print(
        f"\tFamilies in testing but not in training: {n_new_families} "
        f"({round(n_new_families / len(df['family'].unique()) * 100, 2)}%)"
    )
    new_families_in_test = set(df_test["family"].unique()) - set(
        np.intersect1d(df_train["family"].unique(), df_test["family"].unique())
    )
    df = df[~df["family"].isin(new_families_in_test)]
    df_test = df_test[~df_test["family"].isin(new_families_in_test)]
    print(
        f"\tTraining set length (not considering new testing fam): {len(df_train)}, ({round(len(df_train) / len(df) * 100, 2)}%)"
    )
    print(
        f"\tTesting set length (not considering new testing fam): {len(df_test)}, ({round(len(df_test) / len(df) * 100, 2)}%)"
    )


def print_statistics(df: pd.DataFrame, split: pd.Timestamp, label: str = ""):
    df_train, df_test = df[df[fsd] < split], df[df[fsd] >= split]
    print("------------------------------------------------------------------")
    print(f"Report: {label}")
    print(f"\tSplit at: {split}")
    print(
        f"\tTraining set length: {len(df_train)}, ({round(len(df_train) / len(df) * 100, 2)}%)"
    )
    print(
        f"\tTesting set length: {len(df_test)}, ({round(len(df_test) / len(df) * 100, 2)}%)"
    )
    print(f"\tNum families in training: {len(df_train['family'].unique())}")
    print(f"\tNum families in testing: {len(df_test['family'].unique())}")

    n_cup = len(np.intersect1d(df_train["family"].unique(), df_test["family"].unique()))
    print(f"\tCommon families: {n_cup}")
    n_new_families = len(df_test["family"].unique()) - n_cup
    n_dis_families = len(df_train["family"].unique()) - n_cup
    print(
        f"\tFamilies in training but not in testing: {n_dis_families} "
        f"({round(n_dis_families / len(df['family'].unique()) * 100, 2)}%)"
    )
    print(
        f"\tFamilies in testing but not in training: {n_new_families} "
        f"({round(n_new_families / len(df['family'].unique()) * 100, 2)}%)"
    )
    new_families_in_test = set(df_test["family"].unique()) - set(
        np.intersect1d(df_train["family"].unique(), df_test["family"].unique())
    )
    df = df[~df["family"].isin(new_families_in_test)]
    df_test = df_test[~df_test["family"].isin(new_families_in_test)]
    print(
        f"\tTraining set length (not considering new testing fam): {len(df_train)}, ({round(len(df_train) / len(df) * 100, 2)}%)"
    )
    print(
        f"\tTesting set length (not considering new testing fam): {len(df_test)}, ({round(len(df_test) / len(df) * 100, 2)}%)"
    )
