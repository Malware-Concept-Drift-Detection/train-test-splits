import os
from dataclasses import dataclass
import random
from typing import List

random.seed(42)


@dataclass(frozen=True)
class FeatureExtractionConfig:
    """
    Sum type modelling feature extraction configuration.
    """

    malware_directory_path: str
    dataset_type: str
    vt_reports_path: str
    experiment_directory: str
    experiment_subdirectories: List[str]
    final_dataset_directory: str
    top_features_directory: str
    opcodes_max_size: int
    temp_results_dir: str
    results_directory: str
    non_duplicated_sha256s_path: str


class ConfigFactory:
    @staticmethod
    def feature_extraction_config() -> FeatureExtractionConfig:
        """
        Creates an FeatureExtractionConfig object by extracting information from the env vars,
        :return: FeatureExtractionConfig
        """

        return FeatureExtractionConfig(
            malware_directory_path=os.environ.get("MALWARE_DIR_PATH"),
            vt_reports_path=os.environ.get("VTREPORTS_PATH"),
            dataset_type=os.environ.get("PE_DATASET_TYPE"),
            experiment_directory="experiment",
            experiment_subdirectories=["dataset", "top_features", "results"],
            final_dataset_directory=os.environ.get("BASE_OUTPUT_PATH"),
            top_features_directory="top_features",
            opcodes_max_size=3,
            temp_results_dir=".temp",
            results_directory="results",
            non_duplicated_sha256s_path=os.environ.get("NONDUPL_SHA256_FILENAME"),
        )


# Singleton
config = ConfigFactory().feature_extraction_config()
