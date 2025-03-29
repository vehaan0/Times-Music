import os
import pandas as pd

downloads_folder = r"C:\Users\maste\Desktop\Times Music\Daily_tops\downloads"
output_csv = r"C:\Users\maste\Desktop\Times Music\Daily_tops\merged_daily_tops.csv"


dataframes = []

for filename in os.listdir(downloads_folder):
    if filename.endswith(".csv") and filename.startswith("regional-in-daily"):
        date_str = filename.replace("regional-in-daily-", "").replace(".csv", "")

        # format YYYY-MM-DD
        file_path = os.path.join(downloads_folder, filename)
        df = pd.read_csv(file_path)
        df['date'] = date_str 


        dataframes.append(df)

# Concatenate all dataframes into one
merged_df = pd.concat(dataframes, ignore_index=True)

#  new CSV file
merged_df.to_csv(output_csv, index=False)

print(f"Merged CSV with date column (YYYY-MM-DD) saved at: {output_csv}")
