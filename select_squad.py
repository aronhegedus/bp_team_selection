import pandas as pd
import numpy as np

# Athletes with dispensation. Assumed to make the squad.
dispensations = [
    # {"name": "Jurins Kengamu", "sex": "M", "weight_class": "83"},
    {"name": "Ade Omisakin", "sex": "M", "weight_class": "83"}
]

# Names to exclude
excluded_names = {"Tony Cliffe", "Maxwell Gyamfi", "Sanchez Dillon", "Tyri Miller", "Jurins Kengamu"}

# File paths
british_results_file = "result_data/british_powerlifting_results.csv"
carpino_scores_file = "carpino_scores.csv"

# World records by weight class
men_records = {"59": 669.5, "66": 710.5, "74": 836.0, "83": 861.0, "93": 901.0, "105": 940.5, "120": 978.5, "120+": 1152.5}
women_records = {"47": 433.5, "52": 481.0, "57": 519.5, "63": 557.5, "69": 600.0, "76": 613.0, "84": 647.0, "84+": 731.0}

# Load data
results_df = pd.read_csv(british_results_file)
carpino_df = pd.read_csv(carpino_scores_file)

# Print the Carpino Scores at the start
# print("\nImported Carpino Scores:")
# print(carpino_df)

# Add WorldRecord and %WR to results
def calculate_world_record(row):
    if row["Sex"] == "M":
        return men_records.get(row["WeightClassKg"], None)
    elif row["Sex"] == "F":
        return women_records.get(row["WeightClassKg"], None)
    return None

results_df["WorldRecord"] = results_df.apply(calculate_world_record, axis=1)
results_df["%WR"] = (results_df["TotalKg"] / results_df["WorldRecord"]) * 100

# Clean up and preprocess the results_df
def preprocess_results(results_df):
    # Convert Place to numeric, setting invalid entries (e.g., DQ, 6, 20) to NaN
    results_df["Place"] = pd.to_numeric(results_df["Place"], errors="coerce")

    # Strip spaces and ensure consistent WeightClassKg formatting
    results_df["WeightClassKg"] = results_df["WeightClassKg"].astype(str).str.strip()

    # Drop rows with missing or invalid critical fields
    results_df = results_df.dropna(subset=["Place", "WeightClassKg", "Sex", "TotalKg"])
    return results_df

# Apply preprocessing
results_df = preprocess_results(results_df)

# Debugging: Check unique values after preprocessing
# print("\nUnique Places in results_df (post-cleaning):", results_df["Place"].unique())
# print("\nUnique WeightClassKg in results_df (post-cleaning):", results_df["WeightClassKg"].unique())

# Map Carpino scores to results_df
# Map Carpino scores to results_df
def calculate_carpino_score(row, carpino_df):
    # Filter Carpino data for this athlete's weight class and gender
    filtered = carpino_df[
        (carpino_df["Sex"] == row["Sex"]) & 
        (carpino_df["WeightClassKg"] == row["WeightClassKg"])
    ]
    
    if filtered.empty:
        print(f"No Carpino data found for {row['Name']} ({row['WeightClassKg']}kg, {row['Sex']})")
        return np.nan

    # Sort Carpino scores by Place and extract thresholds
    filtered = filtered.sort_values(by="Place")
    thresholds = filtered["CarpinoScore"].values

    # If TotalKg is above or equal to the first threshold, return 0 (world record level)
    if row["TotalKg"] >= thresholds[0]:
        return 0.0

    # If TotalKg is below the lowest threshold, return NaN
    if row["TotalKg"] < thresholds[-1]:
        return np.nan

    # Interpolate between the surrounding Carpino scores
    for i in range(len(thresholds) - 1):
        if thresholds[i + 1] <= row["TotalKg"] < thresholds[i]:
            # Interpolate between thresholds[i] and thresholds[i+1]
            score = i + (thresholds[i] - row["TotalKg"]) / (thresholds[i] - thresholds[i + 1])
            return round(score, 2)

    return np.nan  # Should not reach here

results_df["CarpinoScore"] = results_df.apply(calculate_carpino_score, axis=1, carpino_df=carpino_df)

# Debugging: Print results with the new columns
# print("\nBritish Results with %WR and Carpino Score (Post-Processing):")
# print(results_df[["Name", "WeightClassKg", "TotalKg", "%WR", "CarpinoScore"]])

# Sort results by CarpinoScore and TotalKg
sorted_results = results_df.sort_values(by=["CarpinoScore", "TotalKg"], ascending=[True, False])

# Print the sorted results
# print("\nBritish Results Ranked by Carpino Scores:")
# print(sorted_results[["Name", "WeightClassKg", "TotalKg", "%WR", "CarpinoScore"]])


# Remove excluded athletes from results
results_df = results_df[~results_df["Name"].isin(excluded_names)]

# Function to add dispensation athletes
def add_dispensation_athletes(squad, dispensations, selected_names):
    for disp in dispensations:
        if disp["name"] not in selected_names[disp["sex"]]:
            disp_athlete = {
                "Name": disp["name"],
                "Sex": disp["sex"],
                "WeightClassKg": disp["weight_class"],
                "TotalKg": None,  # Dispensation athletes have no recorded TotalKg
                "Reason": "dispensation"
            }
            squad[disp["sex"]].append(disp_athlete)
            selected_names[disp["sex"]].add(disp["name"])
            # print(f"Debug: Added dispensation athlete: {disp['name']} ({disp['weight_class']}kg)")

# Function to select the world's squad
def select_squad(results_df, dispensations, max_squad_size=8, max_per_weight_class=2, max_reserves=4):
    squad = {"M": [], "F": []}
    reserves = {"M": [], "F": []}
    selected_names = {"M": set(), "F": set()}  # Track selected names to prevent duplicates

    for gender in ["M", "F"]:
        # Filter results for this gender
        gender_results = results_df[results_df["Sex"] == gender]

        # Add dispensation athletes
        add_dispensation_athletes(squad, [d for d in dispensations if d["sex"] == gender], selected_names)

        # Select athletes by Carpino scores
        for threshold in range(0, 6):  # Prioritize Carpino scores 0 to 5
            eligible = gender_results[
                (gender_results["CarpinoScore"] <= threshold) & (~gender_results["Name"].isin(selected_names[gender]))
            ].sort_values(by=["CarpinoScore", "TotalKg"], ascending=[True, False])

            for _, athlete in eligible.iterrows():
                weight_class = athlete["WeightClassKg"]
                if (
                    len(squad[gender]) < max_squad_size
                    and len([a for a in squad[gender] if a["WeightClassKg"] == weight_class]) < max_per_weight_class
                ):
                    athlete_to_add = athlete.to_dict()
                    athlete_to_add["Reason"] = f"Carpino score {athlete['CarpinoScore']:.2f}"
                    squad[gender].append(athlete_to_add)
                    selected_names[gender].add(athlete["Name"])

        # Fill remaining slots with closest to world record percentage
        remaining = gender_results[~gender_results["Name"].isin(selected_names[gender])].sort_values(by="%WR", ascending=False)
        for _, athlete in remaining.iterrows():
            weight_class = athlete["WeightClassKg"]
            if (
                len(squad[gender]) < max_squad_size
                and len([a for a in squad[gender] if a["WeightClassKg"] == weight_class]) < max_per_weight_class
            ):
                athlete_to_add = athlete.to_dict()
                athlete_to_add["Reason"] = f"%WR achieved: {athlete['%WR']:.2f}%"
                squad[gender].append(athlete_to_add)
                selected_names[gender].add(athlete["Name"])

        # Select reserves
        for _, athlete in remaining.iterrows():
            if len(reserves[gender]) < max_reserves and athlete["Name"] not in selected_names[gender]:
                reserve_to_add = athlete.to_dict()
                if reserve_to_add["CarpinoScore"] <= 5:
                    reserve_to_add["Reason"] = f"Carpino score {reserve_to_add['CarpinoScore']:.2f} (Reserve)"
                else:
                    reserve_to_add["Reason"] = f"%WR achieved: {reserve_to_add['%WR']:.2f}% (Reserve)"
                reserves[gender].append(reserve_to_add)
                selected_names[gender].add(reserve_to_add["Name"])

    return squad, reserves

# Run the squad selection
squad, reserves = select_squad(results_df, dispensations)

print(f"Excluded from seleciton: excluded_names={excluded_names}")

# Print the selected squad and reserves
print("\nWorld's Squad:")
for gender in ["M", "F"]:
    print(f"\n{gender}:")
    for athlete in squad[gender]:
        print(f"  {athlete['Name']} ({athlete['WeightClassKg']}kg, Total: {athlete['TotalKg']}, Reason: {athlete['Reason']})")

print("\nReserves:")
for gender in ["M", "F"]:
    print(f"\n{gender}:")
    for athlete in reserves[gender]:
        print(f"  {athlete['Name']} ({athlete['WeightClassKg']}kg, Total: {athlete['TotalKg']}, Reason: {athlete['Reason']})")


# Predefined weight classes for sorting
men_weight_classes = ["59", "66", "74", "83", "93", "105", "120", "120+"]
women_weight_classes = ["47", "52", "57", "63", "69", "76", "84", "84+"]

# Prepare and print Carpino scores and WRs for Men
carpino_men = carpino_df[carpino_df["Sex"] == "M"].copy()
carpino_men["WorldRecord"] = carpino_men["WeightClassKg"].map(men_records)
carpino_men_pivot = carpino_men.pivot(index="WeightClassKg", columns="Place", values="CarpinoScore")
carpino_men_pivot["WorldRecord"] = carpino_men.drop_duplicates(subset="WeightClassKg").set_index("WeightClassKg")["WorldRecord"]
carpino_men_pivot = carpino_men_pivot.reindex(men_weight_classes)

print("\nCarpino Scores and World Records - Men:")
print(carpino_men_pivot)

# Prepare and print Carpino scores and WRs for Women
carpino_women = carpino_df[carpino_df["Sex"] == "F"].copy()
carpino_women["WorldRecord"] = carpino_women["WeightClassKg"].map(women_records)
carpino_women_pivot = carpino_women.pivot(index="WeightClassKg", columns="Place", values="CarpinoScore")
carpino_women_pivot["WorldRecord"] = carpino_women.drop_duplicates(subset="WeightClassKg").set_index("WeightClassKg")["WorldRecord"]
carpino_women_pivot = carpino_women_pivot.reindex(women_weight_classes)

print("\nCarpino Scores and World Records - Women:")
print(carpino_women_pivot)