import base64
import os
import time

import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
client_credential = f"{client_id}:{client_secret}"


def authorize() -> str:
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {base64.b64encode(client_credential.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "client_credentials",
        }
    )
    return response.json().get("access_token")

def get_track_release_date_batch(track_ids: list[str], access_token: str) -> list:
    response = requests.get(
        f"https://api.spotify.com/v1/tracks",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params={
            "ids": ",".join(track_ids),
        }
    )

    if response.status_code != 200:
        print(f"Error fetching tracks: {response.status_code}")
        return [None] * len(track_ids)

    tracks = response.json().get('tracks', [])
    return [track["album"]["release_date"] for track in tracks]


if __name__ == "__main__":
    df = pd.read_csv("./dataset.csv")

    access_token = authorize()
    track_ids = df["track_id"].tolist()
    release_dates = []
    for i in tqdm(range(0, len(track_ids), 50), desc="Fetching release dates"):
        batch_ids = track_ids[i:i + 50]
        batch_dates = get_track_release_date_batch(batch_ids, access_token)
        release_dates.extend(batch_dates)
        time.sleep(0.1)

    df["release_date"] = release_dates
    df.to_csv("dataset.csv", index=False)
    print("✅ Done! Data saved to tracks_with_release_dates.csv")