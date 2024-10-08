from sqlalchemy.engine import Engine
from utils.database import create_redshift_engine
from silver.create_tables import create_tables
from silver.load_parquet import load_parquet_files
from silver.table_insert_sql import (
    insert_stock_data_scd2,
    insert_date_data,
    insert_stock_prices_data
)
import pandas as pd


def run_silver(**context) -> None:
    """
    Run the silver layer process, which includes creating tables,
    loading Parquet files, and inserting data into Redshift tables.

    Steps:
        1. Create necessary tables in the Redshift database.
        2. Load data from Parquet files.
        3. Insert stock, date, and daily stock prices data into Redshift.

    """

    conn: Engine = create_redshift_engine()

    # Step 1: Create tables in the Redshift database if they don't exist
    create_tables(conn)

    # Step 2: Load Parquet files into DataFrames
    daily_stock_prices_df: pd.DataFrame
    stock_df: pd.DataFrame
    date_df: pd.DataFrame
    daily_stock_prices_df, stock_df, date_df = load_parquet_files(context["ds"])

    # Step 3: Insert data into Redshift tables
    insert_stock_data_scd2(conn, stock_df)
    insert_date_data(conn, date_df)
    insert_stock_prices_data(conn, daily_stock_prices_df)


if __name__ == "__main__":
    run_silver()
