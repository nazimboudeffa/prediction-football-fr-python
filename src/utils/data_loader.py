def load_data(filepath):
    import pandas as pd
    
    # Load the CSV data into a DataFrame
    data = pd.read_csv(filepath)
    
    # Convert the DataFrame to a dictionary for easier access
    data_dict = data.to_dict(orient='records')
    
    return data_dict