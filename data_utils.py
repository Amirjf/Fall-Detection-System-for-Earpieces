import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_sensor_data(file_path):
    """
    Robust method to load sensor data with multiple parsing strategies
    """
    try:
        # Strategy 1: Direct loading with explicit parsing
        df = pd.read_csv(
            file_path, 
            comment='%',  # Ignore comment lines
            header=None,  # No header
            names=['TimeStamp', 'Sample_No', 'X_Axis', 'Y_Axis', 'Z_Axis', 'Sensor_Type', 'Sensor_ID'],
            dtype={
                'TimeStamp': float,
                'Sample_No': int,
                'X_Axis': float,
                'Y_Axis': float,
                'Z_Axis': float,
                'Sensor_Type': int,
                'Sensor_ID': int
            },
            engine='python'  # More flexible parsing
        )
        
        # Additional data cleaning
        df = df.dropna()  # Remove any NaN rows
        
        return df
    
    except Exception as e:
        print(f"Error loading CSV: {e}")
        
        # Fallback strategy: Manual parsing
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
            # Filter out comment lines and empty lines
            data_lines = [line.strip() for line in lines 
                          if not line.startswith('%') and line.strip()]
            
            # Manual parsing
            parsed_data = []
            for line in data_lines:
                values = line.split(';')
                if len(values) == 7:
                    parsed_data.append([float(v) for v in values])
            
            df = pd.DataFrame(
                parsed_data, 
                columns=['TimeStamp', 'Sample_No', 'X_Axis', 'Y_Axis', 'Z_Axis', 'Sensor_Type', 'Sensor_ID']
            )
            
            return df
        
        except Exception as e:
            print(f"Fallback parsing failed: {e}")
            return None


def analyze_sensor_data(df):
    """
    Perform comprehensive analysis of sensor data
    """
    analysis = {
        'basic_stats': df[['X_Axis', 'Y_Axis', 'Z_Axis']].describe(),
        'sensor_counts': df['Sensor_ID'].value_counts(),
        'total_samples': len(df)
    }
    
    return analysis

def plot_sensor_data(df):
    """
    Create multiple visualizations to understand data characteristics
    """
    plt.figure(figsize=(20, 15))
    
    # 1. Raw Time Series for X, Y, Z Axes
    plt.subplot(3, 2, 1)
    plt.plot(df['Sample_No'], df['X_Axis'], label='X-Axis')
    plt.plot(df['Sample_No'], df['Y_Axis'], label='Y-Axis')
    plt.plot(df['Sample_No'], df['Z_Axis'], label='Z-Axis')
    plt.title('Raw Acceleration Data')
    plt.xlabel('Sample Number')
    plt.ylabel('Acceleration')
    plt.legend()
    
    # 2. Derivative to detect changes
    plt.subplot(3, 2, 2)
    plt.plot(df['Sample_No'][1:], np.diff(df['X_Axis']), label='X-Axis Derivative')
    plt.plot(df['Sample_No'][1:], np.diff(df['Y_Axis']), label='Y-Axis Derivative')
    plt.plot(df['Sample_No'][1:], np.diff(df['Z_Axis']), label='Z-Axis Derivative')
    plt.title('Acceleration Change Rate')
    plt.xlabel('Sample Number')
    plt.ylabel('Change in Acceleration')
    plt.legend()
    
    # 3. Detailed Zoomed View
    plt.subplot(3, 2, 3)
    plt.plot(df['Sample_No'][:400], df['X_Axis'][:400], label='X-Axis (First 400 Samples)')
    plt.title('X-Axis First 400 Samples')
    plt.xlabel('Sample Number')
    plt.ylabel('Acceleration')
    
    # 4. Detailed Zoomed View - Latter Part
    plt.subplot(3, 2, 4)
    plt.plot(df['Sample_No'][350:], df['X_Axis'][350:], label='X-Axis (After 350 Samples)', color='red')
    plt.title('X-Axis After 350 Samples')
    plt.xlabel('Sample Number')
    plt.ylabel('Acceleration')
    
    # 5. Histogram of Acceleration Values
    plt.subplot(3, 2, 5)
    df[['X_Axis', 'Y_Axis', 'Z_Axis']].hist(bins=50, ax=plt.gca())
    plt.title('Distribution of Acceleration Values')
    
    # 6. Correlation Heatmap
    plt.subplot(3, 2, 6)
    sns.heatmap(df[['X_Axis', 'Y_Axis', 'Z_Axis']].corr(), annot=True, cmap='coolwarm')
    plt.title('Acceleration Axes Correlation')
    
    plt.tight_layout()
    plt.show()

def sensor_correlation_heatmap(df):
    """
    Create correlation heatmap for sensor axes
    """
    plt.figure(figsize=(8, 6))
    correlation_matrix = df[['X_Axis', 'Y_Axis', 'Z_Axis']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Acceleration Axes Correlation Heatmap')
    plt.show()

def signal_quality_analysis(df):
    """
    Analyze signal quality and detect potential issues
    """
    # Calculate variance in sliding windows
    window_size = 50
    x_variance = df['X_Axis'].rolling(window=window_size).var()
    y_variance = df['Y_Axis'].rolling(window=window_size).var()
    z_variance = df['Z_Axis'].rolling(window=window_size).var()
    
    plt.figure(figsize=(15, 10))
    plt.subplot(3, 1, 1)
    plt.plot(df['Sample_No'], x_variance)
    plt.title(f'X-Axis Variance (Window Size: {window_size})')
    
    plt.subplot(3, 1, 2)
    plt.plot(df['Sample_No'], y_variance)
    plt.title(f'Y-Axis Variance (Window Size: {window_size})')
    
    plt.subplot(3, 1, 3)
    plt.plot(df['Sample_No'], z_variance)
    plt.title(f'Z-Axis Variance (Window Size: {window_size})')
    
    plt.tight_layout()
    plt.show()