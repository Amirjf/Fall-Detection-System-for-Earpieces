# Fall Detection

This project involves preprocessing the UMAFall dataset for fall detection research.

## 📁 Folder Structure

Before starting, create the following directories in your project root:

datasets/
output/

## 📥 Download Dataset

Download the UMAFall dataset ZIP file from the following link:

🔗 [UMA ADL FALL Dataset](https://figshare.com/articles/dataset/UMA_ADL_FALL_Dataset_zip/4214283?file=11826395)

## 📦 Move and Extract

After downloading:

1. Move the ZIP file into the `datasets/` folder.
2. Extract the contents inside the `datasets/` folder.

Your folder should now look like:

3. **Move the dataset**

After downloading, move the ZIP file into the `datasets/` folder and extract its contents there.

## ⚙️ Preprocess the Dataset

Run the preprocessing script:

```bash
python UmaFall_preprocessing.py
```

#### 🔍 What the Preprocessing Does

The script performs the following steps:
• Reads raw accelerometer and gyroscope data from the UMAFall dataset.
• Parses the corresponding activity labels (e.g., fall, ADL).
• Organizes the data into separate files grouped by subject and trial.
• Cleans and aligns sensor data with labels for easier use in modeling and analysis.
• Saves the tidied, structured output into the output/ directory.

---

### 🏷️ Fall Labeling Script – Overview and Approach

The fall_labeling.py script is designed to automatically detect and label fall events in the UMAFall dataset using raw sensor signals. It focuses specifically on a subset of activities (Activity10, Activity13, Activity14, Activity15) that represent different types of falls.

⸻

#### ⚙️ How It Works

##### 1. Target Activities:

The script only processes files corresponding to specific fall activities by matching activity names in the file names. 2. Abrupt Change Detection:
For each fall trial:
• It scans accelerometer readings (x, y, z axes) to identify points with abrupt changes, using a configurable threshold.
• These changes are considered potential indicators of impact or rapid motion shifts common in falls. 3. Windowing the Fall Event:
• From all detected changes, it selects the point with the greatest change as the center of the fall.
• A time window (by default, 1.0s before to 1.5s after the fall point) is defined around this moment using the TimeStamp column. 4. Labeling the Fall:
• The Tag column values are changed to "1" within this time window, marking it as a fall.
• This labeled data helps distinguish fall regions from non-fall regions for later analysis or training. 5. Overwriting Processed Files:
• The original CSV files are overwritten with the updated labels for simplicity, keeping the directory structure unchanged.

## 📚 References

The UMAFall dataset used in this project is sourced from the following references:

1. [UMA ADL FALL Dataset on Figshare](https://figshare.com/articles/dataset/UMA_ADL_FALL_Dataset_zip/4214283?file=11826395)
2. [Combined Fall Dataset on GitHub](https://github.com/Vani-Fula/Combined-fall-dataset)
