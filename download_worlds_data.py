import os
import requests

# URLs for the CSV files
urls = {
    "2203": "https://www.openpowerlifting.org/api/meetcsv/ipf/2203",
    "2303": "https://www.openpowerlifting.org/api/meetcsv/ipf/2303",
    "2404": "https://www.openpowerlifting.org/api/meetcsv/ipf/2404"
}

# Directory to save the CSV files
output_dir = "result_data"
os.makedirs(output_dir, exist_ok=True)

# Download and save the CSV files
for year, url in urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(output_dir, f"powerlifting_{year}.csv")
        with open(file_path, "w") as file:
            file.write(response.text)
        print(f"Data for year {year} saved to {file_path}.")
    else:
        print(f"Failed to fetch data for year {year}.")
