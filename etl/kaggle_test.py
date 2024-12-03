import kagglehub
import pandas as pd

# Download latest version
path = kagglehub.dataset_download("winston56/fortune-500-data-2021")
df = pd.read_csv(path)

print(df.head())