import pandas as pd

def load_files(file_paths):
    dataframes = [pd.read_excel(file) for file in file_paths]
    return {file: df for file, df in zip(file_paths, dataframes)}
