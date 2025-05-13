import os

def split_dataset():
    if os.getenv("PE_DATASET_TYPE") == "MOTIF":
        from .motif.motif_splits import train_test_split
        train_test_split()
    elif os.getenv("PE_DATASET_TYPE") == "Norton670":
        from .norton.norton_splits import train_test_split
        #train_test_split()
    else:
        raise ValueError("Invalid PE_DATASET_TYPE. Must be either 'MOTIF' or 'Norton670'.")

if __name__ == "__main__":
    split_dataset()