import pandas as pd

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
