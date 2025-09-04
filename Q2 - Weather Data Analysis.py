# Imports libraries
import pandas as pd
import glob
import os

# Defines the directory containing temperature CSV files
file_directory = os.getcwd() + r"\temperatures"

def load_all_data():
    """Load and combine all CSVs in the folder into one DataFrame."""
    # Finds all CSV files in the directory
    files = glob.glob(os.path.join(file_directory, "*.csv"))    
    # Raises error if no CSV files are found
    if not files:
        raise FileNotFoundError(f"No CSV files found in {file_directory}")

    # Creates a list to store DataFrames
    dfs = []
    # Loops through each file and attempts to read them
    for f in files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            # Prints error message if file can't be read
            print(f"Error reading {f}: {e}")

    # Raises an error if no valid DataFrames were loaded
    if not dfs:
        raise ValueError("No valid CSVs loaded.")

    # Combines all DataFrames into one
    return pd.concat(dfs, ignore_index=True)

def seasonal_average(df):
    """Calculate average seasonal temperatures across all stations and years."""
    # Assigns months for each season
    seasons = {
        "Summer": ["December", "January", "February"],
        "Autumn": ["March", "April", "May"],
        "Winter": ["June", "July", "August"],
        "Spring": ["September", "October", "November"],
    }
    # Creates dictionary to store seasonal average temperature
    results = {}

    # Loops through each season and calculate mean temperature
    for season, months in seasons.items():
        values = df[months].values.flatten()
        avg = pd.Series(values).dropna().mean()
        results[season] = round(avg, 1)

    # Saves results into a text file
    with open("average_temp.txt", "w") as f:
        for season, avg in results.items():
            f.write(f"{season}: {avg}°C\n")

def largest_temp_range(df):
    """Find station(s) with largest temperature range (max - min)."""
    # Creates list to store temperature ranges for stations
    station_ranges = []

    # Groups data by station and calculates temperature ranges
    for stn, group in df.groupby("STATION_NAME"):
        temps = group.loc[:, "January":"December"].values.flatten()
        temps = pd.Series(temps).dropna()
        if temps.empty:
            continue
        tmax, tmin = temps.max(), temps.min()
        trange = tmax - tmin
        station_ranges.append((stn, trange, tmax, tmin))

    # Exits if there's no valid data
    if not station_ranges:
        return

    # Finds the maximum temperature range
    max_range = max(station_ranges, key=lambda x: x[1])[1]

    # Identifies all stations sharing the maximum range
    winners = [s for s in station_ranges if abs(s[1] - max_range) < 1e-6]

    # Saves results into a text file
    with open("largest_temp_range_station.txt", "w") as f:
        for stn, trange, tmax, tmin in winners:
            f.write(f"{stn}: Range {trange:.1f}°C (Max: {tmax:.1f}°C, Min: {tmin:.1f}°C)\n")

def temperature_stability(df):
    """Find stations with most stable and most variable temperatures."""
    # Creates list to store the standard deviation for stations
    station_stddevs = []

    # Groups data by station and calculates the standard deviation of temperatures
    for stn, group in df.groupby("STATION_NAME"):
        temps = group.loc[:, "January":"December"].values.flatten()
        temps = pd.Series(temps).dropna()
        if temps.empty:
            continue
        stddev = temps.std()
        station_stddevs.append((stn, stddev))

    # Exits if there's no valid data
    if not station_stddevs:
        return  

    # Finds minimum and maximum standard deviation values
    min_std = min(station_stddevs, key=lambda x: x[1])[1]
    max_std = max(station_stddevs, key=lambda x: x[1])[1]

    # Identifies stations with the lowest and highest variability
    most_stable = [s for s in station_stddevs if abs(s[1] - min_std) < 1e-6]
    most_variable = [s for s in station_stddevs if abs(s[1] - max_std) < 1e-6]

    # Saves results into a text file
    with open("temperature_stability_stations.txt", "w") as f:
        for stn, std in most_stable:
            f.write(f"Most Stable: {stn}: StdDev {std:.1f}°C\n")
        for stn, std in most_variable:
            f.write(f"Most Variable: {stn}: StdDev {std:.1f}°C\n")

def main():
    # Loads and process temperature data
    df = load_all_data()
    seasonal_average(df)
    largest_temp_range(df)
    temperature_stability(df)

    # Notifies the user of the saved results
    print("Results saved to 'average_temp.txt', 'largest_temp_range_station.txt', and 'temperature_stability_stations.txt', in", os.getcwd())

# Runs the main function when the script is executed
if __name__ == "__main__":
    main()