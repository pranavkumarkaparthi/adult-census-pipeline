import logging
import sqlite3

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Extract
logger.info("Extract: loading raw data")
df = pd.read_csv("data/raw/adult.csv")
logger.info(f"Extracted {len(df)} rows")

# Transform
logger.info("Transform: cleaning disguised nulls and duplicates")
df = df.replace("?", np.nan)
df = df.fillna("Unknown")
df = df.drop_duplicates()
logger.info(f"Transformed: {len(df)} rows after cleaning")


# Validate
logger.info("Validate: running checks")
assert df.isnull().sum().sum() == 0, "Null values found in cleaned data!"
assert (df == "?").sum().sum() == 0, "Disguised nulls (?) still present!"
assert df.duplicated().sum() == 0, "Duplicate rows found!"
logger.info("All validation checks passed!")

# Load
logger.info("Load: writing to CSV, SQLite, and PostgreSQL")
df.to_csv("data/processed/adult_clean.csv", index=False)

conn = sqlite3.connect("data/processed/adult_census.db")
df.to_sql("adult", conn, if_exists="replace", index=False)
conn.close()

engine = create_engine("postgresql+psycopg2://localhost/adult_census")
df.to_sql("adult", engine, if_exists="replace", index=False)

logger.info(f"Pipeline complete! {len(df)} rows loaded.")

