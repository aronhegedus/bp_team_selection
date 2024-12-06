import pandas as pd
import os

# Directory containing the CSV files
input_dir = "result_data"
output_file = "carpino_scores.csv"

# Load the CSV files into a single dataframe
dataframes = []
year_mapping = {"2203": 2022, "2303": 2023, "2404": 2024}
for year, mapped_year in year_mapping.items():
    file_path = os.path.join(input_dir, f"powerlifting_{year}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df["Year"] = mapped_year
        dataframes.append(df)
    else:
        print(f"File for year {year} not found at {file_path}")

results_df = pd.concat(dataframes, ignore_index=True)

# Ensure Place is numeric; drop rows where Place is not a number
results_df = results_df[pd.to_numeric(results_df['Place'], errors='coerce').notnull()]
results_df['Place'] = results_df['Place'].astype(int)

# Initialize weight classes
male_weight_classes = ['59', '66', '74', '83', '93', '105', '120', '120+']
female_weight_classes = ['47', '52', '57', '63', '69', '76', '84', '84+']

# Calculate Carpino scores
carpino_data = []
for gender, weight_classes in [("M", male_weight_classes), ("F", female_weight_classes)]:
    for weight_class in weight_classes:
        for place in range(1, 6):  # Places 1 to 5
            # Filter results for the last 3 years
            relevant_data = results_df[
                (results_df['Sex'] == gender) &
                (results_df['WeightClassKg'] == weight_class) &
                (results_df['Place'] == place)
            ]

            # Ensure all years are present
            years_present = relevant_data['Year'].unique()
            missing_years = set(year_mapping.values()) - set(years_present)
            if len(missing_years) > 0:
                print(f"Warning: Missing years {missing_years} for Sex={gender}, "
                      f"WeightClassKg={weight_class}, Place={place}")
                continue

            # Compute the average TotalKg (Carpino score)
            average_total = relevant_data['TotalKg'].mean()
            carpino_data.append({
                "Sex": gender,
                "WeightClassKg": weight_class,
                "Place": place,
                "CarpinoScore": round(average_total * 2) / 2
            })

# Convert the Carpino scores into a dataframe
carpino_df = pd.DataFrame(carpino_data)

# Export Carpino scores to CSV
carpino_df.to_csv(output_file, index=False)
print(f"Carpino scores saved to {output_file}")