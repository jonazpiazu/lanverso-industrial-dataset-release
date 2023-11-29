"""Simple wrapper class to download and extract the industrial dataset."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

import open3d as o3d
import requests
from natsort import natsorted
import json
import zipfile

from dataclasses import dataclass


class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


@dataclass
class IndustrialDatasetData:
    data_dir: Path = Path(__file__).parents[0] / "data"

    @classproperty
    def industrial_dataset_list_file(cls) -> Path:
        return cls.data_dir / "industrial_dataset_list.json"


@dataclass(frozen=False)
class IndustrialDataset:
    scene: str = "EvenTableSinglePartZivid"
    data_root: str = os.environ.get("OPEN3D_DATA_ROOT")

    def __post_init__(self):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        with open(IndustrialDatasetData.industrial_dataset_list_file) as json_file:
            self.file_index = json.load(json_file)
        if not self.file_index.get(self.scene):
            logging.error(f"Dataset {self.scene} does not exist.")
            return None

        if not self.data_root:
            logging.debug("Using default download path")
            self.data_root = os.environ.get("HOME") + "/open3d_data"

        if not Path(self.data_root).exists():
            Path(self.data_root).mkdir()
        download_path = Path(self.data_root) / Path("download")
        if not download_path.exists():
            download_path.mkdir()
        extract_base_dir = Path(self.data_root) / Path("extract")
        if not extract_base_dir.exists():
            extract_base_dir.mkdir()

        destination_file = download_path / Path(
            self.file_index.get(self.scene).split("/")[-1]
        )
        if destination_file.exists():
            logging.debug("File already downloaded, skipping download")
        else:
            logging.info(f"Downloading {self.file_index.get(self.scene)}")
            self.download_file(self.file_index.get(self.scene), destination_file)
            logging.info(f"Downloaded to {destination_file}")

        extract_path = extract_base_dir / Path(self.scene)
        self.paths = None
        if not extract_path.exists():
            extract_path.mkdir()
            logging.info(f"Created directory {extract_path}")

            logging.info(f"Extracting {destination_file}")
            self.paths = self.unzip_file(destination_file, extract_path)
            logging.info(f"Extracted to {extract_path}")
            self.paths = [str(extract_path / Path(x)) for x in self.paths]

        if not self.paths:
            self.paths = [str(f) for f in extract_path.iterdir() if f.is_file()]

        self.paths = natsorted(self.paths)

    @staticmethod
    def scene_list() -> list:
        with open(IndustrialDatasetData.industrial_dataset_list_file) as json_file:
            file_index = json.load(json_file)
        return list(file_index.keys())

    def download_file(self, url, destination_file):
        response = requests.get(url)
        if response.status_code == 200:
            with open(destination_file, "wb") as file:
                file.write(response.content)
            return destination_file
        else:
            return None

    def unzip_file(self, zip_file_path, extract_to_folder):
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extract_to_folder)
        return zip_ref.namelist()
