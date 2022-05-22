#!/usr/bin/env python
# coding: utf-8

import wandb
import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport


#
def go():
    run = wandb.init(project="nyc_airbnb", group="eda", save_code=True)
    local_path = wandb.use_artifact("sample.csv:latest").file()
    df = pd.read_csv(local_path)

    profile = ProfileReport(df,
                            title="NYC Airbnb Data Data",
                            dataset={
                                "description": "This profiling report was generated for a NYC Airbnb as \n"
                                               " my own little addition to the Udacity nano  MLop project ",
                                "copyright_holder": "Emmanuel Akinwale",
                                "copyright_year": "2022",
                                "url": "https://github.com/LopeWale/build-model-workflow-starter.git"
                            })

    st.title("NYC AIRBNB EXPLORATORY DATA ANALYSIS!")
    st.write(st.dataframe(df, 100, 200))
    st_profile_report(profile)


if __name__ == "__main__":
    go()

# mlflow run --finish
