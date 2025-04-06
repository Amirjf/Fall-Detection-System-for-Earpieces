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
