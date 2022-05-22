#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
from argparse import ArgumentParser
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    logger.info("Download input artifact and log that this script is using this particular version of the artifact")

    local_path = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(local_path)

    # Drop outliers
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser: ArgumentParser = argparse.ArgumentParser(description="Create a component called basic_cleaning")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="this is the name of the component",
        required=True)

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="this is the name of the component",
        required=True)

    parser.add_argument(
        "--output_type",
        type=str,
        help="this is the name of the component",
        required=True)

    parser.add_argument(
        "--output_description",
        type=str,
        help="this is the name of the component",
        required=True)

    parser.add_argument(
        "--min_price",
        type=float,
        help="this is the name of the component",
        required=True)

    parser.add_argument(
        "--max_price",
        type=float,
        help="this is the name of the component",
        required=True)


    args = parser.parse_args()
    go(args)
