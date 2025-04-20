import os
import pandas as pd

def uma_search_csv_files(directory, activities_of_interest=None):
    csv_files = []
    for current_folder, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                if activities_of_interest is not None:
                    for activity in activities_of_interest:
                        if activity in file:
                            full_path = os.path.join(current_folder, file)
                            csv_files.append(full_path)
                            break
                else:
                    full_path = os.path.join(current_folder, file)
                    csv_files.append(full_path)
                    break
    return csv_files

def read_sisfall_dataset(base_path):
    subject_ids = [f'SA{str(i).zfill(2)}' for i in range(1, 24)] + [f'SE{str(i).zfill(2)}' for i in range(1, 16)]
    all_data = []
    all_labels = []
    activity_code_list = []
    adls = []
    falls = []
    counter = 0
    ADL = 0
    FALL = 0

    for subject_id in subject_ids:
        folder_path = os.path.join(base_path, subject_id)

        if not os.path.isdir(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)

                try:
                    activity_code = filename.split('_')[0]
                    activity_code_list.append(activity_code)
                    
                    df = pd.read_csv(file_path, header=None, delimiter=',', usecols=[0, 1, 2, 3, 4, 5], on_bad_lines='skip')
                    data = df.to_numpy()
                    data = data.transpose()

                    if activity_code.startswith('D'):
                        adls.append(data)
                        label = 'ADL'
                        ADL += 1
                    elif activity_code.startswith('F'):
                        falls.append(data)
                        label = 'Fall'
                        FALL += 1
                    else:
                        label = 'Unknown'
                    
                    all_data.append(data)
                    all_labels.append(label)
                    counter += 1

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    
    print(f"Total files processed: {counter}")
    print(f"Total ADL labels: {ADL}")
    print(f"Total Fall labels: {FALL}")

    return all_data, all_labels, activity_code_list, adls, falls
