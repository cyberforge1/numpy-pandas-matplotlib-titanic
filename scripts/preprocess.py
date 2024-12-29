# scripts/preprocess.py

import pandas as pd
import os

def clean_data(df):
    """
    Cleans the Titanic dataset by handling missing values and creating new features.
    
    Args:
        df (pd.DataFrame): The raw Titanic dataset.

    Returns:
        pd.DataFrame: The cleaned dataset.
    """
    print("Starting data cleaning...")
    
    # Handle missing values
    df['Age'].fillna(df['Age'].median(), inplace=True)
    print("Filled missing values in 'Age' column.")
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
    print("Filled missing values in 'Embarked' column.")
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    print("Filled missing values in 'Fare' column.")
    
    # Drop columns with too many missing values or irrelevant data
    df.drop(['Cabin', 'Ticket'], axis=1, inplace=True)
    print("Dropped 'Cabin' and 'Ticket' columns.")
    
    # Create new features
    df['FamilySize'] = df['SibSp'] + df['Parch']
    print("Created 'FamilySize' feature.")
    df['IsAlone'] = (df['FamilySize'] == 0).astype(int)
    print("Created 'IsAlone' feature.")
    
    # Simplify 'Name' to include only titles
    df['Title'] = df['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    print("Extracted 'Title' feature from 'Name' column.")
    df.drop(['Name'], axis=1, inplace=True)
    print("Dropped 'Name' column.")
    
    # Simplify 'Title' by grouping uncommon titles
    title_mapping = {
        'Mr': 'Mr', 'Miss': 'Miss', 'Mrs': 'Mrs', 'Master': 'Master',
        'Dr': 'Other', 'Rev': 'Other', 'Col': 'Other', 'Major': 'Other',
        'Mlle': 'Miss', 'Countess': 'Other', 'Ms': 'Miss', 'Lady': 'Other',
        'Jonkheer': 'Other', 'Don': 'Other', 'Mme': 'Mrs', 'Capt': 'Other',
        'Sir': 'Other'
    }
    df['Title'] = df['Title'].map(title_mapping)
    print("Simplified 'Title' feature.")
    
    # Convert categorical features to dummy variables
    df = pd.get_dummies(df, columns=['Sex', 'Embarked', 'Title'], drop_first=True)
    print("Converted categorical features to dummy variables.")
    
    return df

def process_data(input_path, output_path):
    """
    Loads the raw Titanic dataset, cleans it, and saves the processed data.
    
    Args:
        input_path (str): Path to the raw dataset (CSV file).
        output_path (str): Path to save the processed dataset (CSV file).
    """
    print(f"Input file path: {input_path}")
    print(f"Output file path: {output_path}")
    
    # Verify input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at: {input_path}")
    
    # Load raw data
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    print("Data loaded successfully. Preview:")
    print(df.head())

    # Clean data
    print("Cleaning data...")
    cleaned_df = clean_data(df)
    print("Data cleaned successfully. Preview:")
    print(cleaned_df.head())

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    print(f"Ensured output directory exists: {output_dir}")

    # Save processed data
    print(f"Saving processed data to {output_path}...")
    cleaned_df.to_csv(output_path, index=False)
    print("Processed data saved successfully.")

if __name__ == "__main__":
    # Define relative paths for input and output
    script_dir = os.path.dirname(__file__)  # Directory of the script
    input_file = os.path.join(script_dir, "../data/raw/train.csv")
    output_file = os.path.join(script_dir, "../data/processed/cleaned_titanic.csv")
    
    print(f"Script directory: {script_dir}")
    print(f"Relative input file path: {input_file}")
    print(f"Relative output file path: {output_file}")
    
    # Process the data
    try:
        process_data(input_file, output_file)
        print("Script completed successfully.")
    except Exception as e:
        print(f"Error: {e}")
