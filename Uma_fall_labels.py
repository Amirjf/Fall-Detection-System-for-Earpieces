import os
import pandas as pd
import numpy as np

# Root directory where the folders are located
root_directory = r"output"

# List of activity names of interest
activities_of_interest = ['Activity13', 'Activity14', 'Activity15']

# Index of the column to be replaced (assuming the first column has index 0)
column_index = "Tag"

# Function to detect abrupt changes
def detect_abrupt_changes(data, threshold):
    changes = []
    for i in range(1, len(data)):
        diff = abs(data[i] - data[i-1])
        if diff > threshold:
            changes.append(i)
    return changes





def find_max_value_index(data, changes):
    max_index = max(changes, key=lambda i: abs(data[i] - data[i-1]))
    return max_index

# Function to find the start and end indices of the window
def find_window_indices(data, threshold=0.7, window_duration=3.0):
    acceleration_x = data['Accelerometer: x-axis (g)']
    acceleration_y = data['Accelerometer: y-axis (g)']
    acceleration_z = data['Accelerometer: z-axis (g)']

    changes_x = detect_abrupt_changes(acceleration_x, threshold)
    changes_y = detect_abrupt_changes(acceleration_y, threshold)
    changes_z = detect_abrupt_changes(acceleration_z, threshold)

    start_window_x = find_max_value_index(acceleration_x, changes_x)
    start_window_y = find_max_value_index(acceleration_y, changes_y)
    start_window_z = find_max_value_index(acceleration_z, changes_z)

    start_window = int(np.mean([start_window_x, start_window_y, start_window_z])) if changes_x and changes_y and changes_z else 0

    # Defining the time of greatest change
    time_of_greatest_change = data['TimeStamp'][start_window]
    # Defining the start of the window 1.5 seconds before the greatest change
    start_time_window = time_of_greatest_change - 1
    # Defining the end of the window 1.5 seconds after the greatest change
    end_time_window = time_of_greatest_change + 1.5

    idx_start_window = data.index[data['TimeStamp'] >= start_time_window]
    idx_end_window = data.index[data['TimeStamp'] >= end_time_window]

    # Checking if the end index of the window was found
    if len(idx_end_window) == 0:
        # If not found, we define the end index as the last index of the DataFrame
        idx_end_window = len(data) - 1
    else:
        # Otherwise, we take the first index found
        idx_end_window = idx_end_window[0]

    # Checking if the start index of the window was found
    if len(idx_start_window) == 0:
        # If not found, we define the start index as the first index of the DataFrame
        idx_start_window = 0
    else:
        # Otherwise, we take the first index found
        idx_start_window = idx_start_window[0]

    return idx_start_window, idx_end_window

# Function to change the values of the last column within the window to 1
def change_window_values(data, idx_start_window, idx_end_window, column_to_change):
    altered_data = data.copy()
    altered_data.loc[idx_start_window:idx_end_window, column_to_change] = "1"
    return altered_data

# Function to search for CSV files in various directories, including subdirectories,
# and filter only the files that have the names of activities of interest
def search_csv_files(directory):
    csv_files = []
    for current_folder, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                for activity in activities_of_interest:
                    if activity in file:
                        full_path = os.path.join(current_folder, file)
                        csv_files.append(full_path)
                        break
                
    return csv_files

# Search for CSV files in the directories of interest
csv_files = search_csv_files(root_directory)

def main():      
    
    # Process the CSV files one by one
    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        # Open the file for reading and load the data into a DataFrame
        try:
            data = pd.read_csv(csv_file)
            
            # Check if the DataFrame is not empty
            if not data.empty:
                # Check if the activity of the file is among the activities of interest
                activity_found = any(activity in csv_file for activity in activities_of_interest)

                if activity_found:
                    # Find the start and end indices of the window
                    idx_start_window, idx_end_window = find_window_indices(data)

                    # Change the values of the last column within the window to 1
                    altered_data = change_window_values(data, idx_start_window, idx_end_window, column_index)

                    # Save the altered data in the same original file
                    altered_data.to_csv(csv_file, index=False)
                else:
                    print(f"Activity of the file is not among the activities of interest: {csv_file}")
            else:
                print(f"Empty DataFrame in the file: {csv_file}")

        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"Error processing the file {csv_file}: {str(e)}")

    



if __name__ == "__main__":
     main()