# scripts/api_access.py

import os
from kaggle.api.kaggle_api_extended import KaggleApi
from dotenv import load_dotenv

def download_titanic_dataset(destination_folder):
    """
    Downloads the Titanic dataset from Kaggle and stores it in the specified folder.

    Args:
        destination_folder (str): Path to the folder where the dataset will be stored.
    """
    # Load environment variables
    load_dotenv()

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Initialize the Kaggle API with environment variables
    os.environ['KAGGLE_USERNAME'] = os.getenv("KAGGLE_USERNAME")
    os.environ['KAGGLE_KEY'] = os.getenv("KAGGLE_KEY")
    
    api = KaggleApi()
    api.authenticate()

    # Dataset information
    competition_name = "titanic"

    print("Downloading Titanic dataset...")
    api.competition_download_files(competition_name, path=destination_folder)
    print(f"Dataset downloaded to {destination_folder}")

    # Unzip the dataset
    zip_file = os.path.join(destination_folder, f"{competition_name}.zip")
    if os.path.exists(zip_file):
        import zipfile
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        print("Dataset extracted.")
        os.remove(zip_file)
    else:
        print("Zip file not found. Please check the Kaggle API or competition name.")

if __name__ == "__main__":
    # Define the destination folder
    destination = "../data/raw"  # Adjust path as needed
    download_titanic_dataset(destination)
