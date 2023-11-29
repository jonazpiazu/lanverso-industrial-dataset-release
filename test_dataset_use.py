"""Minimal example of how to use the IndustrialDataset class to load and interact with the dataset."""

from lanverso_industrial_dataset_helper.lanverso_industrial_dataset_helper import (
    IndustrialDataset as industrial_dataset,
)
import open3d as o3d
import json


def test_all_datasets():
    for scene in industrial_dataset.scene_list():
        dataset = industrial_dataset(scene=scene)
        for pcd_path in dataset.paths:
            pcd = o3d.io.read_point_cloud(pcd_path)
            print(pcd)


if __name__ == "__main__":
    dataset = industrial_dataset()
    for pcd_path in dataset.paths:
        pcd = o3d.io.read_point_cloud(pcd_path)
        print(pcd)

    # show how to visualize a point cloud from the dataset using Open3D
    pcd = o3d.io.read_point_cloud(dataset.paths[0])
    o3d.visualization.draw_geometries([pcd])

    dataset = industrial_dataset(scene="EvenTableTwoPartsZivid")
    for pcd_path in dataset.paths:
        pcd = o3d.io.read_point_cloud(pcd_path)
        print(pcd)

    test_all_datasets()
