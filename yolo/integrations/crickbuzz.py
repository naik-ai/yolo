import pytz
import json
import httpx
import uvicorn
import aiohttp
import asyncio
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.websocket("/ws")
async def cricket_updates(websocket: WebSocket):
    await websocket.accept()
    while True:
        scraper = IPLMatchDetailsScraper()
        data = await scraper.fetch_cricbuzz_data()
        await websocket.send_json(data)
        await asyncio.sleep(30)  # Wait for 30 seconds before sending the next update


# utility functions
def convert_timestamp_to_ist_format(timestamp_ms: int) -> str:
    """
    Converts a timestamp in milliseconds to IST (Indian Standard Time)
    and formats it as 'MMM dd, EEE'.

    Parameters:
    - timestamp_ms: The timestamp in milliseconds.

    Returns:
    - A string representing the formatted date in IST.
    """
    # Convert milliseconds to seconds
    timestamp_s = int(timestamp_ms) / 1000

    # Create a timezone-aware datetime object in UTC
    dt_utc = datetime.utcfromtimestamp(timestamp_s).replace(tzinfo=pytz.utc)

    # Convert to IST timezone
    dt_ist = dt_utc.astimezone(pytz.timezone("Asia/Kolkata"))

    return dt_ist.strftime("%b %d, %a, %I:%M %p")


def short_form_name(match_name: str) -> str:
    """
    Converts a full team name to its short form.
    """

    team_names_to_short = {
        "Mumbai Indians": "MI",
        "Delhi Capitals": "DC",
        "Kolkata Knight Riders": "KKR",
        "Chennai Super Kings": "CSK",
        "Royal Challengers Bengaluru": "RCB",
        "Punjab Kings": "PBKS",
        "Sunrisers Hyderabad": "SRH",
        "Rajasthan Royals": "RR",
        "Lucknow Super Giants": "LSG",
        "Gujarat Titans": "GT",
    }

    teams = match_name.split(" vs ")
    short_forms = []
    for team in teams:
        if team in team_names_to_short:
            short_forms.append(team_names_to_short[team])
        else:
            raise ValueError(f"Unknown team name: {team}")
    return " vs ".join(short_forms)


# make it a dataclass
class IPLMatchDetailsScraper:
    def __init__(self):
        self.base_url = "https://www.cricbuzz.com"
        self.ipl_schedule_url = (
            f"{self.base_url}/cricket-series/7607/indian-premier-league-2024/matches"
        )

    async def fetch_html(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(self.ipl_schedule_url)
            return response.text

    async def scrape_ipl_schedule_and_results(self):
        html_content = await self.fetch_html()
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all elements with the specified class
        match_elements = soup.find_all("div", class_="cb-col-75 cb-col")

        match_details = []
        for element in match_elements:
            # Find the timestamp within the current element
            timestamp_element = element.find("span", class_="schedule-date")
            # Find the match URL within the current element
            match_url_element = element.find("a", class_="text-hvr-underline")
            # name
            cb_name = (
                match_url_element["title"] if match_url_element else "Name not found"
            )

            name_element = match_url_element.find("span") if match_url_element else None
            name = name_element.text if name_element else "Name not found"

            # Extract the location
            location_element = element.find("div", class_="text-gray")
            location = (
                location_element.text if location_element else "Location not found"
            )
            if (
                timestamp_element
                and "timestamp" in timestamp_element.attrs
                and match_url_element
            ):
                timestamp = timestamp_element["timestamp"]
                match_url = (
                    "https://www.cricbuzz.com" + match_url_element["href"]
                )  # Prepend the base URL if needed
                match_details.append(
                    {
                        "match_url": match_url,
                        "timestamp": timestamp,
                        "name": name,
                        "cb_name": cb_name,
                        "location": location,
                    }
                )

        return match_details

    async def fetch_cricbuzz_commentary(self, match_index):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/api/cricket-match/commentary/{match_index}"
            ) as response:
                return await response.json()

    async def get_next_match_preview_info(self, match_url: str):

        # get the next match/Todays match preview info from the match url using timestamp

        # get the next match preview info from the match url using timestamp
        async with httpx.AsyncClient() as client:
            response = await client.get(match_url)
            return response.text

    @staticmethod
    async def extract_match_index(url: str) -> str:
        # Extract the number immediately following 'live-cricket-scores/' or 'cricket-scores/'
        parts = url.split("/")
        for i, part in enumerate(parts):
            if part in ["live-cricket-scores", "cricket-scores"]:
                # Assuming the next part is the match number
                return parts[i + 1]
        return "Match index not found"

    @staticmethod
    async def separate_name_and_match_number(text: str) -> dict:
        # Split the text by comma
        parts = text.split(", ")
        # Assuming the format is always "<Team 1> vs <Team 2>, <Match Number> Match"
        team_names = parts[0]
        match_number = parts[1].split(" ")[
            0
        ]  # Extracting the match number before "Match"
        return {"match_names": team_names, "match_number": match_number}

    async def clean_match_url(self, data: dict) -> dict:
        url = data["match_url"]
        text = data["name"]
        match_index = await self.extract_match_index(url)
        match_name = await self.separate_name_and_match_number(text)
        return {
            "match_index": match_index,
            "match_url": url,
            "match_names": match_name["match_names"],
            "match_number": match_name["match_number"],
            "cb_name": data["cb_name"],
            "location": data["location"],
            "timestamp": data["timestamp"],
            "timestamp_sec": int(data["timestamp"]) / 1000,
            # conver timestamp to date in IST
            "datetime": convert_timestamp_to_ist_format(data["timestamp"]),
            "short_names": short_form_name(match_name["match_names"]),
            "team1": match_name["match_names"].split(" vs ")[0],
            "team2": match_name["match_names"].split(" vs ")[1],
        }

    async def main(self) -> dict:
        # get match index from ipl schedule results

        raw = await self.scrape_ipl_schedule_and_results()
        intermediate_data = []
        for each in raw:
            intermediate_data.append(await self.clean_match_url(each))

        return intermediate_data


# if __name__ == "__main__":
#     # uvicorn.run(app, host="0.0.0.0", port=8000)

#     scraper = IPLMatchDetailsScraper()
#     raw_data = asyncio.run(scraper.main())
