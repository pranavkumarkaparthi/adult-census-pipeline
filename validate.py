import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


df = pd.read_csv("data/processed/adult_clean.csv")

assert df.isnull().sum().sum() == 0, "Null values found in cleaned data!"
assert (df == "?").sum().sum() == 0, "Disguised nulls (?) still present!"
assert df.duplicated().sum() == 0, "Duplicate rows found!"

# print("All validation checks passed!")

logger.info("All validation checks passed!")


