from src.etl.transform import flatten_listen_history,clean_validate_listen_history,clean_validate_tracks,clean_validate_users

def test_flattening_valid_input():
    history = [{
            "user_id": 93289,
            "items": [
                89510,
                35681
            ],
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        }]
    result = flatten_listen_history(history)
    expected = [{
            "user_id": 93289,
            "track_id": 89510,
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        },{
            "user_id": 93289,
            "track_id": 35681,
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        }]
    assert result == expected

def test_flattening_valid_empty():
    history = []
    result = flatten_listen_history(history)
    expected = []
    assert result == expected

def test_flattening_valid_items_empty():
    history = [{
            "user_id": 93289,
            "items": [],
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        }]
    result = flatten_listen_history(history)
    expected = []
    assert result == expected

def test_flatten_track_history_missing_items_key():
    history = [{"user_id": 1, "timestamp": "2025-01-01T12:00:00"}]
    result = flatten_listen_history(history)
    expected = []
    assert result == expected

def test_clean_validate_listen_history_success():

    history = [{
            "user_id": 93289,
            "track_id": 89510,
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        },{
            "user_id": 93289,
            "track_id": 35681,
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        }]

    result = clean_validate_listen_history(history)

    expected = [{
            "user_id": 93289,
            "track_id": 89510,
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        },{
            "user_id": 93289,
            "track_id": 35681,
            "created_at": "2023-06-10T00:33:16.699605",
            "updated_at": "2023-07-26T14:45:04.953304"
        }]

    assert result == expected

def test_clean_validate_users_success():
    users = [{
            "id": 93289,
            "first_name": "Christina",
            "last_name": "Greene",
            "email": "richard27@example.net",
            "gender": "Gender questioning",
            "favorite_genres": "Rock",
            "created_at": "2023-06-22T04:06:23.683704",
            "updated_at": "2024-07-06T19:10:55.442032"
        },
        {
            "id": 68689,
            "first_name": "Robert",
            "last_name": "Coleman",
            "email": "carly62@example.net",
            "gender": "Gender nonconforming",
            "favorite_genres": "Metal",
            "created_at": "2024-02-22T05:24:02.117967",
            "updated_at": "2024-12-01T18:23:48.502485"
        }]

    result = clean_validate_users(users)

    expected = [{
            "id": 93289,
            "first_name": "Christina",
            "last_name": "Greene",
            "email": "richard27@example.net",
            "gender": "Gender questioning",
            "favorite_genres": "Rock",
            "created_at": "2023-06-22T04:06:23.683704",
            "updated_at": "2024-07-06T19:10:55.442032"
        },
        {
            "id": 68689,
            "first_name": "Robert",
            "last_name": "Coleman",
            "email": "carly62@example.net",
            "gender": "Gender nonconforming",
            "favorite_genres": "Metal",
            "created_at": "2024-02-22T05:24:02.117967",
            "updated_at": "2024-12-01T18:23:48.502485"
        }]
    assert result == expected

def test_clean_validate_tracks_success():
    tracks = [{
            "id": 84382,
            "name": "media",
            "artist": "Tracey Rangel",
            "songwriters": "Ariel Greene",
            "duration": "29:38",
            "genres": "mind",
            "album": "sing",
            "created_at": "2024-08-12T05:57:41.938768",
            "updated_at": "2025-01-07T16:55:53.278600"
        },{
            "id": 19895,
            "name": "heart",
            "artist": "Ashley Gutierrez",
            "songwriters": "Christopher Fernandez",
            "duration": "28:09",
            "genres": "safe",
            "album": "newspaper",
            "created_at": "2024-10-24T17:19:05.269431",
            "updated_at": "2024-03-26T07:42:32.385798"
        }]
    result = clean_validate_tracks(tracks)
    expected =[{
                "id": 84382,
                "name":"media",
                "artist":"Tracey Rangel",
                "songwriters":"Ariel Greene",
                "duration":1778,
                "genres":"mind",
                "album":"sing",
                "created_at": "2024-08-12T05:57:41.938768",
                "updated_at": "2025-01-07T16:55:53.278600"
            },{
                "id": 19895,
                "name":"heart",
                "artist":"Ashley Gutierrez",
                "songwriters":"Christopher Fernandez",
                "duration":1689,
                "genres":"safe",
                "album":"newspaper",
                "created_at": "2024-10-24T17:19:05.269431",
                "updated_at": "2024-03-26T07:42:32.385798"
            }]
    assert result == expected

