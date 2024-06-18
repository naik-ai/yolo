import requests
from bs4 import BeautifulSoup
import json


class CommentaryScraperFactory:
    def __init__(self, match_id):
        self.match_id = match_id
        self.base_url = "https://www.iplt20.com/match/2024/{}"
        self.commentary_data = []

    def fetch_commentary(self):
        url = self.base_url.format(self.match_id)
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Fetching commentary for match ID {self.match_id}")
            soup = BeautifulSoup(response.text, "html.parser")
            # Find the main container for each ball's data
            ball_containers = soup.find_all("div", class_="cmdEvent")
            for container in ball_containers:
                self.parse_commentary_elements(container)
        else:
            print(f"Failed to fetch commentary for match ID {self.match_id}")

    def parse_commentary_elements(self, container):
        # Extract over and ball number
        over_info = container.find("p", class_="cmdOver")
        if over_info:
            over_number = over_info.text.strip()
        else:
            over_number = "Unknown"

        # Extract runs scored, if available
        runs_scored_element = container.find("i", class_="ovRun")
        runs_scored = runs_scored_element.text.strip() if runs_scored_element else "N/A"

        # Extract detailed commentary text
        commentary_text_element = container.find("div", class_="commentaryText")
        commentary_text = (
            commentary_text_element.text.strip()
            if commentary_text_element
            else "No commentary available"
        )

        # Append the extracted data to the commentary_data list
        self.commentary_data.append(
            {
                "over": over_number,
                "runs_scored": runs_scored,
                "commentary": commentary_text,
            }
        )

    def get_commentary_as_json(self):
        return json.dumps(self.commentary_data, ensure_ascii=False)


# Example usage
match_id = "1410"
scraper = CommentaryScraperFactory(match_id=match_id)
scraper.fetch_commentary()
print(scraper.get_commentary_as_json())
# save data to data/ipl_t20/commentary/1410.json
with open(f"data/ipl_t20_{match_id}.json", "w") as f:
    f.write(scraper.get_commentary_as_json())
