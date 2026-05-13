import os
import pandas as pd

"""
pip install pandas
pip install xlrd
pip install openpyxl

"""


try:
    script_dir = os.path.dirname(os.path.abspath(__file__)) # File path where script is running
    csv_folder = os.path.join(script_dir, "edited names")
    output_folder = os.path.join(script_dir, "processed")

except:
    # __file__ does not exist in colab
    csv_folder= f"./edited names"
    output_folder = "processed"



os.makedirs(output_folder, exist_ok=True)

df = pd.DataFrame()
df20_24 = pd.DataFrame()

for file in os.listdir(csv_folder):
    try:
        file_path = os.path.join(csv_folder, file)
        
        if file.endswith(".xls"):
            engine = "xlrd"
        elif file.endswith(".xlsx"):
            engine = "openpyxl"
        else:
            continue


        temp_df = pd.read_excel(file_path, sheet_name="Full-Time", engine=engine, header=4, usecols=["Description", "Code", "Median","change", "Mean", "change.1"]) # Load excel columns from full time sheet
        
        cols = ["Code","Median", "Mean", "change", "change.1"]

        temp_df[cols] = temp_df[cols].apply(pd.to_numeric, errors="coerce")

        temp_df = temp_df.rename(columns={
                        "change": "median_annualpc",
                        "change.1": "mean_annualpc"})

        codes_to_keep = [8231, 22, 23, 531, 7, 41, 213, 9273]

        year = file.split(".")[0] # Getting just the year without file extension

        if year > "2020":
          codes_to_keep = [8231, 2232, 2313, 7111, 2134, 8212]

        temp_df = temp_df[temp_df["Code"].isin(codes_to_keep)] # Keep only specific codes
        temp_df = temp_df[temp_df["Description"].str.contains("London", case=False, na=False)] # Keep only London
        temp_df["Description"] = temp_df["Description"].str.replace(r"London,\s*", "", regex=True) # Removing London from name
        temp_df["Description"] = temp_df["Description"].str.strip() # Removing leading/trailing whitespaces
        temp_df["Year"] = year

        # Adding to data frame

        if year > "2020":
          df20_24 = pd.concat([df20_24, temp_df], ignore_index=True)
        else:
          df = pd.concat([df, temp_df], ignore_index=True)

        print("Processed:", file)
    except:
        print("Error processing:", file)
        continue



# Sorting by year
df = df.sort_values(by=["Code", "Year"])
df20_24 = df20_24.sort_values(by=["Code", "Year"])

df.to_excel(os.path.join(output_folder,"2011_2020.xlsx"), index=False)
df20_24.to_excel(os.path.join(output_folder, "2021_2024.xlsx"), index=False)
print("Processing complete.")