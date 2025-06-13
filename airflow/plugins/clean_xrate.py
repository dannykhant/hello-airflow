import os

import pandas as pd


def clean_xrate():
    df = pd.read_csv("/tmp/xrate.csv", header=None)
    def_values = {
        int: 0,
        float: 0.0,
        str: ""
    }
    clean_df = df.fillna(value=def_values)
    now = pd.Timestamp.now()
    data_dir = f"/opt/airflow/data/xrate/{now.year}/{now.month}/{now.day}"
    os.makedirs(data_dir, exist_ok=True)
    clean_df.to_csv(f"{data_dir}/xrate.csv")
