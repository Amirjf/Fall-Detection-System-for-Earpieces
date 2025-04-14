
import csv
import glob
import os
import math
import shutil
from datetime import datetime, timedelta
from UmaFall_Downsampling import Downsampled


def format_timestamp(timestamp):
    
    if timestamp == 'TimeStamp':
        return timestamp

    date_time = datetime.strptime(timestamp, "%Y-%m-%d %H-%M-%S")
    formatted_date_time = date_time.strftime("%Y/%m/%dT%H:%M:%S")

    return formatted_date_time

def add_milliseconds(timestamp, milliseconds):

    # Convert the time string to a datetime object
    time_object = datetime.strptime(timestamp[11:], '%H:%M:%S')
    
    new_time = time_object + timedelta(milliseconds=int(milliseconds))
    
    return new_time.strftime(timestamp[:11] + '%H:%M:%S.%f')

def process_UMA(input_folder, output_folder):
    # List all CSV files in the input folder
    csv_files = glob.glob(input_folder + "/*.csv")
    
    
    # Iterate over each CSV file
    for input_file in csv_files:
        # Extract the file name without the extension
        file_name = os.path.splitext(os.path.basename(input_file))[0]
    
        # Extract the subject from the file name
        #subject = file_name.split('_')[0] + " " + file_name.split('_')[2]
        subject = file_name.split('_')[2].lstrip('0')
        # Count the number of occurrences of the "_" character
        num_underscores = file_name.count("_")
        
        # Condition based on the number of "_"
        if num_underscores == 7:
            timeS = file_name.split('_')[6] + " " + file_name.split('_')[7]
            trial = file_name.split('_')[5] 
            formatted_timestamp = format_timestamp(timeS)
            
        else:
            timeS = file_name.split('_')[7] + " " + file_name.split('_')[8]
            trial = file_name.split('_')[6]        
            formatted_timestamp = format_timestamp(timeS)            
              
        # Extract the activity from the file name
        if file_name.split('_')[3] == 'Fall':
            tag = 0
            
        else:
            tag = 0
        
       
        activity = None
        file_info = file_name.split('_')
        activity_name = file_info[4]
        
        if activity_name == 'Walking':
            activity = 1
        elif activity_name == 'Jogging':
            activity = 2
        elif activity_name == 'Bending':
            activity = 3
        elif activity_name == 'Hopping':
            activity = 4
        elif activity_name == 'GoDownstairs':
            activity = 5
        elif activity_name == 'GoUpstairs':
            activity = 6
        elif activity_name == 'LyingDown' and file_info[5] == 'OnABed':
            activity = 7
        elif activity_name == 'Sitting' and file_info[5] == 'GettingUpOnAChair':
            activity = 8
        elif activity_name == 'Aplausing':
            activity = 9
        elif activity_name == 'HandsUp':
            activity = 10
        elif activity_name == 'MakingACall':
            activity = 11
        elif activity_name == 'OpeningDoor':
            activity = 12
        elif activity_name == 'backwardFall':
            activity = 13
        elif activity_name == 'forwardFall':
            activity = 14
        elif activity_name == 'lateralFall':
            activity = 15
            
                    
        # Define the output path for the selected file
        output_file = os.path.join(output_folder, file_name + ".csv")
        
        
        # Initialize the list to store the selected lines
        selected_lines = []
        selected_lines_gyro = []
        selected_lines_acc = []
    
        # Read the CSV file into a list of lines
        with open(input_file, 'r') as file:
            csv_reader = csv.reader(file)
            lines = list(csv_reader)
    
            # Create a new header with the existing columns plus the "Subject" and "Trial" columns
            new_header = ['TimeStamp', 'Accelerometer: x-axis (g)', 'Accelerometer: y-axis (g)', 'Accelerometer: z-axis (g)', 
                          'Gyroscope: x-axis (rad/s)','Gyroscope: y-axis (rad/s)','Gyroscope: z-axis (rad/s)','Subject', 'Activity','Trial', 'Tag']
                            
                            
            for i in range(41, len(lines)):
                line = lines[i][0].split(';')
                if len(line) >= 7:  # Check if the line has enough elements
                    sensor_type = line[5]
                    sensor_id = line[6]
                    if sensor_type.isdigit() and sensor_id.isdigit():
                        sensor_type = int(sensor_type)
                        sensor_id = int(sensor_id)
                        if (sensor_type == 0 and sensor_id == 3):
                            line = line[2:5] # Update the values of "Subject", "Trial" and "Tag"
                            selected_lines_acc.append(line)
                        elif (sensor_type == 1 and sensor_id == 3):
                            #timeStamp = add_milliseconds(formatted_timestamp, line[0])
                            line[0] = int(line[0]) /1000 # convert time from milliseconds to seconds
                            line = line[:1] + line[2:5] + [subject, activity, trial, tag]  # Update the values of "Subject", "Trial" and "Tag"
                            selected_lines_gyro.append(line)
                
        
            
        
        for i in range(len(selected_lines_acc)):
            line_gyro = selected_lines_gyro[i]
            line_acc = selected_lines_acc[i]
            new_line = line_gyro[:1] + line_acc[0:] + line_gyro[1:]
            selected_lines.append(new_line)
        
        
        
        for selected_line in selected_lines[0:]:
            for i in range(4, 7):
                value_degrees_s = selected_line[i]   
                try:
                    value_degrees_s = float(value_degrees_s)
                    value_radians_s = value_degrees_s*(math.pi/180)
                except ValueError:
                    value_radians_s = value_degrees_s  # Assign NaN to the invalid value        
                
                selected_line[i] = value_radians_s
            
          
        
        # Save the selected lines to a new CSV file
        with open(output_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            # Write the new header
            csv_writer.writerow(new_header)
            csv_writer.writerows(selected_lines)
            
    
    Downsampled(output_folder,20,18)
    print("Downsample complete")
    process_to_up(output_folder)
    print("Processing completed.") 
    
def process_to_up(output_folder):
    # Root directory where the CSV files are located
    root_directory = output_folder
    
    # Traverse all CSV files in the root directory
    for file in os.listdir(root_directory):
        if file.endswith('.csv'):
            # Extract information from the file name
            file_name = os.path.splitext(file)[0]
            name_parts = file_name.split('_')
            subject = name_parts[1] + name_parts[2].lstrip('0')  # Remove leading zero
            
            activity = None
            activity_name = name_parts[4]
            
            if activity_name == 'Walking':
                activity = 1
            elif activity_name == 'Jogging':
                activity = 2
            elif activity_name == 'Bending':
                activity = 3
            elif activity_name == 'Hopping':
                activity = 4
            elif activity_name == 'GoDownstairs':
                activity = 5
            elif activity_name == 'GoUpstairs':
                activity = 6
            elif activity_name == 'LyingDown' and name_parts[5] == 'OnABed':
                activity = 7
            elif activity_name == 'Sitting' and name_parts[5] == 'GettingUpOnAChair':
                activity = 8
            elif activity_name == 'Aplausing':
                activity = 9
            elif activity_name == 'HandsUp':
                activity = 10
            elif activity_name == 'MakingACall':
                activity = 11
            elif activity_name == 'OpeningDoor':
                activity = 12
            elif activity_name == 'backwardFall':
                activity = 13
            elif activity_name == 'forwardFall':
                activity = 14
            elif activity_name == 'lateralFall':
                activity = 15
            
            # Count the number of occurrences of the "_" character
            num_underscores = file_name.count("_")
            
            # Condition based on the number of "_"
            if num_underscores == 7:
                trial = name_parts[5]
                
            else:
                trial = name_parts[6]
            
            
            
    
            # Create the directory for the subject, activity, and trial
            destination_directory = os.path.join(root_directory, f'{subject}', f'Activity{activity}', f'Trial{trial}')
            os.makedirs(destination_directory, exist_ok=True)
            
            new_name = f'UMAFALL_{subject}Activity{activity}Trial{trial}.csv'
    
            # Move the file to the destination directory with the new name
            shutil.move(os.path.join(root_directory, file), os.path.join(destination_directory, new_name))



def main():      
    
    # Path to the directory where the UMA Fall dataset is located as downloaded
    input_folder = r"datasets/UMAFall_Dataset"
    
    # Path to the directory where we want to save the datasets
    output_folder = r"output"
    
    # 1.
    process_UMA(input_folder, output_folder)

    # 2.
    #process_to_up(output_folder)
    
      
if __name__ == "__main__":
     main()