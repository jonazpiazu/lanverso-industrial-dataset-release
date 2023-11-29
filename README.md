# lanverso-industrial-dataset

This repository holds the industrial dataset used in the [RANSACLP paper](https://github.com/jmartinezot/ransaclp/).

To facilitate the usage of the dataset there is a convenience wrapper class in `lanverso_industrial_dataset_helper` that follows a similar API to [Open3D's dataset class](http://www.open3d.org/docs/release/tutorial/data/index.html#livingroompointclouds) to download and interact with the dataset.

To install it, the recommended way is to use a Python virtual environment:

```bash
cd lanverso_industrial_dataset_helper
python3 -m venv venv
source venv/bin/activate
pip install .
```

The file [test_dataset_use.py](./lanverso_industrial_dataset_helper/test_dataset_use.py) shows how to use the wrapper class to load the pointclouds in Open3D.
