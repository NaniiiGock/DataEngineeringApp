import kaggle.cli
import sys
import pandas as pd
from pathlib import Path
from zipfile import ZipFile

# download data set
# https://www.kaggle.com/unsdsn/world-happiness?select=2017.csv
dataset = "winston56/fortune-500-data-2021/"
sys.argv = [sys.argv[0]] + f"datasets download {dataset}".split(" ")
kaggle.cli.main()

zfile = ZipFile(f"{dataset.split('/')[1]}.zip")

dfs = {f.filename:pd.read_csv(zfile.open(f)) for f in zfile.infolist() }

print(dfs['Fortune_1000.csv'].head())
