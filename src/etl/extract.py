import requests
import logging

BASE_URL = "http://127.0.0.1:8000"
USERS_ENDPOINT = "/users"
TRACKS_ENDPOINT = "/tracks"
LISTEN_HISTORY_ENDPOINT = "/listen_history"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_all_pages(url: str,page_size: int = 100) -> list[dict]:
    """
    Fetches paginated data from a given URL.

    :param url: The base endpoint from which to fetch data.
    :param page_size: The number of items to fetch per page (default: 100).
    :return: A list of dictionaries representing all fetched items.
    """

    page = 1
    all_items = []
    logging.info(f"Fetching data from {url} with page size {page_size}.")

    while True:

        params = {"size":page_size, "page":page}

        try :
            response = requests.get(url, params = params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Error occurred: {e}")
            return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for {url} with params {params}: {e}")
            return []

        try:
            data = response.json()
        except ValueError:
            logging.error(f"Invalid JSON from URL {url}")
            return []

        items = data.get("items",[])
        if not items:
            logging.warning(f"No items found on page {page} for {url}")
        all_items.extend(items)

        total_pages = data.get("pages",1)
        if "pages" not in data:
            logging.warning(f"Number of pages not found for {url}, only working with first page.")

        if total_pages <= page:
            break
        page += 1

    logging.info(f"Finished fetching data from {url}.")
    return all_items


def extract_users() -> list[dict]:
    logging.info("Starting extraction process for USERS.")
    user_items = fetch_all_pages(f"{BASE_URL}{USERS_ENDPOINT}")
    logging.info(f"Completed extraction for USERS. Retrieved {len(user_items)} items.")
    return user_items

def extract_tracks() -> list[dict]:
    logging.info("Starting extraction process for TRACKS.")
    track_items = fetch_all_pages(f"{BASE_URL}{TRACKS_ENDPOINT}")
    logging.info(f"Completed extraction for TRACKS. Retrieved {len(track_items)} items.")
    return track_items

def extract_listen_history() -> list[dict]:
    logging.info("Starting extraction process for LISTEN_HISTORY.")
    listen_history_items = fetch_all_pages(f"{BASE_URL}{LISTEN_HISTORY_ENDPOINT}")
    logging.info(f"Completed extraction for LISTEN_HISTORY. Retrieved {len(listen_history_items)} items.")
    return listen_history_items


if __name__ == "__main__" :
    users = extract_users()
    tracks = extract_tracks()
    listen_history = extract_listen_history()
