import csv
import json
import requests
from bs4 import BeautifulSoup

file_out = "journals/journal_abbreviations_ubc.csv"


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.text.split("(", 1)[1].rsplit(")", 1)[0]
        return json.loads(json_data)["html"]
    except Exception as e:
        print("Error:", e)
        return None


def parse_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    journal_dict = {
        row.find_all("td")[1].get_text(strip=True): row.find_all("td")[0].get_text(
            strip=True
        )
        for row in soup.find_all("tr")
        if len(row.find_all("td")) == 2
    }
    return dict(sorted(journal_dict.items()))


def save_file(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for full_name, abbreviation in data.items():
            if full_name and abbreviation:  # Remove empty rows
                writer.writerow([full_name, abbreviation])
    print(f"Journal abbreviation data saved as '{filename}'")


def main():
    url = "https://journal-abbreviations.library.ubc.ca/dump.php"
    html_content = fetch_data(url)
    if html_content:
        parsed_data = parse_html(html_content)
        if parsed_data:
            save_file(parsed_data, file_out)


if __name__ == "__main__":
    main()
