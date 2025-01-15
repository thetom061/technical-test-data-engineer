from extract import extract_listen_history,extract_tracks,extract_users
from transform import clean_validate_listen_history,clean_validate_users,clean_validate_tracks
from load import write_to_csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_etl_to_csv() -> None:
    """
    Runs the etl pipeline, appends data to csv files while making sure there are no duplicate ids.
    """
    logging.info("Starting the etl pipeline.")
    raw_users = extract_users()
    raw_tracks = extract_tracks()
    raw_listen_history = extract_listen_history()

    cleaned_tracks = clean_validate_tracks(raw_tracks)
    cleaned_users = clean_validate_users(raw_users)
    cleaned_listen_history = clean_validate_listen_history(raw_listen_history)

    # Writting to file, not allowing duplicate ids for tracks and users
    write_to_csv("./tracks.csv",cleaned_tracks,["id"])
    write_to_csv("./users.csv",cleaned_users,["id"])
    write_to_csv("./listen_history.csv",cleaned_listen_history,[])
    logging.info("Etl pipeline finished.")

if __name__ == "__main__":
    run_etl_to_csv()