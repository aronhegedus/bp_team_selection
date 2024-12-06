import os
import requests

# URL for the CSV file
url = "https://www.openpowerlifting.org/api/meetcsv/bp/2407"

# Directory to save the CSV file
output_dir = "result_data"
os.makedirs(output_dir, exist_ok=True)

# Filename for the British-specific data
file_name = "british_powerlifting_results.csv"
file_path = os.path.join(output_dir, file_name)

# Download and save the CSV file
response = requests.get(url)
if response.status_code == 200:
    with open(file_path, "w") as file:
        file.write(response.text)
    print(f"Data saved to {file_path}.")
else:
    print(f"Failed to fetch data from {url}.")
