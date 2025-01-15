import pandas as pd
from pandas.errors import EmptyDataError
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def write_to_csv(csv_path: str, new_data: list[dict], unique_columns: list[str]) -> None:
    """
    Writes new_data to the CSV file at csv_path, ensuring duplicates are removed.

    :param csv_path: Path to the CSV file to write or append to.
    :param new_data: A list of dictionaries representing the new rows to add.
    :param unique_columns: A list of columns that define a unique row for deduplication.
    """
    logging.info(f"Attempting to write data to {csv_path} with {len(new_data)} new records.")

    if not new_data:
        logging.warning("No new data provided to write; skipping.")
        return

    df_new = pd.DataFrame(new_data)

    # If the file does not exist or is empty, just create/write the new data
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        logging.info(f"Creating {csv_path} because it doesn't exist or is empty.")

        if unique_columns:
            df_new.drop_duplicates(subset=unique_columns, keep='first', inplace=True)
        df_new.to_csv(csv_path, index=False)
        logging.info(f"Successfully wrote {len(df_new)} new records to {csv_path}.")
        return

    # If file exists and is non-empty, read it and append
    try:
        df_existing = pd.read_csv(csv_path)
        logging.info(f"Read existing data from {csv_path} with {len(df_existing)} records.")
    except EmptyDataError:
        # The file exists but has no valid rows/columns. We can treat it like a fresh file.
        logging.warning(f"{csv_path} is present but empty or has no columns to parse. Treating as new file.")
        df_existing = pd.DataFrame()

    df_combined = pd.concat([df_existing, df_new], ignore_index=True)

    # Drop duplicates based on unique_columns
    if unique_columns:
        original_length = len(df_combined)
        df_combined.drop_duplicates(subset=unique_columns, keep='first', inplace=True)
        logging.info(
            f"Dropped {original_length - len(df_combined)} duplicates based on {unique_columns}."
        )

    # Write the combined data back to the CSV
    df_combined.to_csv(csv_path, index=False)
    logging.info(f"Successfully wrote CSV {csv_path} with {len(df_combined)} total records.")

