import os
import pandas as pd



try:
    script_dir = os.path.dirname(os.path.abspath(__file__)) # File path where script is running
    csv_folder = os.path.join(script_dir, "original")
    output_folder = os.path.join(script_dir, "processed")

except:
    # __file__ does not exist in colab
    csv_folder= f"./original"
    output_folder = "processed"



os.makedirs(output_folder, exist_ok=True)

try:
        
    file_path = os.path.join(csv_folder, "OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0+GBR+USA+ESP+ITA+DEU+FRA..USD_PPP.....csv")
    df = pd.read_csv(file_path)
   

    # Make sure year and salary is numeric
    df['TIME_PERIOD'] = pd.to_numeric(df['TIME_PERIOD'], errors='coerce')
    df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')

    # Sort by country and year
    df = df.sort_values(by=['Reference area', 'TIME_PERIOD'])

    # Calculate percentage change per country
    df['Percentage_Change'] = df.groupby('Reference area')['OBS_VALUE'].pct_change() * 100

    # Check result
  
    output_path = os.path.join(output_folder, "OECD_withpc.csv")

    df.to_csv(output_path, index=False)

    print("Processed")
    
except:
    print("Error processing")


