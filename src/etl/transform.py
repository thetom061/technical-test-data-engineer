from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def flatten_listen_history(history: list[dict]) -> list[dict]:
    """
    Flattens the items key in the listen history.
    """
    logging.info(f"Flatenning listen history.")
    flattened_history = []

    for item in history:
        if "items" in item:
            new_items = [{** {k: v for k, v in item.items() if k != "items"}, "track_id":track} for track in item["items"]]
            flattened_history.extend(new_items)
        else:
            logging.warning(f"Item {item} has a missing items key, can't flatten item.")
    logging.info(f"Finished flattening, {len(flattened_history)} total items after flattening.")
    return flattened_history

def transform_duration_to_seconds(duration: str) -> int:
    """
    Transforms a duration string in 'mm:ss' format to total seconds.
    """
    try:
        # Split the string into minutes and seconds
        minutes, seconds = map(int, duration.split(":"))
        total_seconds = minutes * 60 + seconds
        logging.info(f"Transformed duration '{duration}' to {total_seconds} seconds.")
        return total_seconds
    except ValueError:
        # Specific log to indicate problem with the formatting
        logging.warning(f"Invalid duration format: '{duration}'. Expected format 'mm:ss'.")
        raise ValueError

def clean_validate_listen_history(history: list[dict]) -> list[dict]:
    logging.info(f"Starting cleaning and validation of {len(history)} listen history items.")
    flattened_history = flatten_listen_history(history)
    cleaned_history = []
    for item in flattened_history:
        try:

            if not all(key in item for key in ("user_id", "track_id", "created_at", "updated_at")):

                missing_keys = [key for key in ("user_id", "track_id", "created_at", "updated_at") if key not in item]
                logging.warning(f"Missing keys {missing_keys} in item: {item}")
                continue

            # Validate and clean types
            user_id = int(item["user_id"])
            track_id = int(item["track_id"])

            # Validate and parse timestamps
            created_at = datetime.fromisoformat(item["created_at"])
            updated_at = datetime.fromisoformat(item["updated_at"])

            # Return the cleaned item
            cleaned_history.append({
                "user_id": user_id,
                "track_id": track_id,
                "created_at": created_at.isoformat(),
                "updated_at": updated_at.isoformat()
            })
        except ValueError as e:
            logging.warning(f"Validation error for item: {item}. Error: {e}")
            continue
        except KeyError as e:
            logging.warning(f"Missing key {e} in item: {item}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error for item: {item}. Error: {e}")
            continue
    logging.info(f"Finished cleaning and validating listen history, {len(cleaned_history)} items after cleaning.")
    return cleaned_history

def clean_validate_users(users: list[dict]) -> list[dict]:
    logging.info(f"Starting cleaning and validation of {len(users)} user items.")
    cleaned_users = []
    for item in users:
        try:
            if not all(key in item for key in ("id","first_name","last_name","email","gender","favorite_genres", "created_at", "updated_at")):

                missing_keys = [key for key in ("id","first_name","last_name","email","gender","favorite_genres", "created_at", "updated_at") if key not in item]
                logging.warning(f"Missing keys {missing_keys} in item: {item}")
                continue

            # Validate and clean types
            id = int(item["id"])
            first_name = str(item["first_name"]).strip()
            last_name = str(item["last_name"]).strip()
            email = str(item["email"]).strip()
            gender = str(item["gender"]).strip()
            favorite_genres = str(item["favorite_genres"]).strip()

            # Validate and parse timestamps
            created_at = datetime.fromisoformat(item["created_at"])
            updated_at = datetime.fromisoformat(item["updated_at"])

            cleaned_users.append({
                "id": id,
                "first_name":first_name,
                "last_name":last_name,
                "email":email,
                "gender":gender,
                "favorite_genres":favorite_genres,
                "created_at": created_at.isoformat(),
                "updated_at": updated_at.isoformat()
            })
        except ValueError as e:
            logging.warning(f"Validation error for item: {item}. Error: {e}")
            continue
        except KeyError as e:
            logging.warning(f"Missing key {e} in item: {item}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error for item: {item}. Error: {e}")
            continue

    logging.info(f"Finished cleaning and validating users, {len(cleaned_users)} user items after cleaning.")
    return cleaned_users

def clean_validate_tracks(tracks: list[dict]) -> list[dict]:
    logging.info(f"Starting cleaning and validation of {len(tracks)} track items.")
    cleaned_tracks = []
    for item in tracks:
        try:
            if not all(key in item for key in ("id", "name","artist","songwriters","duration","genres","album", "created_at", "updated_at")):

                missing_keys = [key for key in ("id", "name","artist","songwriters","duration","genres","album", "created_at", "updated_at") if key not in item]
                logging.warning(f"Missing keys {missing_keys} in item: {item}")
                continue

            # Validate and clean types
            id = int(item["id"])
            name = str(item["name"]).strip()
            artist = str(item["artist"]).strip()
            songwriters = str(item["songwriters"]).strip()
            duration = int(transform_duration_to_seconds(item["duration"]))
            genres = str(item["genres"]).strip()
            album = str(item["album"]).strip()


            # Validate and parse timestamps
            created_at = datetime.fromisoformat(item["created_at"])
            updated_at = datetime.fromisoformat(item["updated_at"])

            cleaned_tracks.append({
                "id": id,
                "name":name,
                "artist":artist,
                "songwriters":songwriters,
                "duration":duration,
                "genres":genres,
                "album":album,
                "created_at": created_at.isoformat(),
                "updated_at": updated_at.isoformat()
            })
        except ValueError as e:
            logging.warning(f"Validation error for item: {item}. Error: {e}")
            continue
        except KeyError as e:
            logging.warning(f"Missing key {e} in item: {item}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error for item: {item}. Error: {e}")
            continue

    logging.info(f"Finished cleaning and validating tracks, {len(tracks)} track items after cleaning.")
    return cleaned_tracks


