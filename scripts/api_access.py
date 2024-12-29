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
    print("Starting the download process...")

    # Load environment variables from .env file
    print("Loading environment variables from .env file...")
    load_dotenv()

    # Get Kaggle credentials from environment variables
    kaggle_username = os.getenv("KAGGLE_USERNAME")
    kaggle_key = os.getenv("KAGGLE_KEY")
    print(f"KAGGLE_USERNAME: {kaggle_username}")
    print(f"KAGGLE_KEY: {'Set' if kaggle_key else 'Not Set'}")

    if not kaggle_username or not kaggle_key:
        raise EnvironmentError("KAGGLE_USERNAME or KAGGLE_KEY is not set in the .env file.")

    # Set Kaggle environment variables
    os.environ['KAGGLE_USERNAME'] = kaggle_username
    os.environ['KAGGLE_KEY'] = kaggle_key
    print("Kaggle environment variables set successfully.")

    # Ensure the destination folder exists
    print(f"Ensuring destination folder exists: {destination_folder}")
    os.makedirs(destination_folder, exist_ok=True)
    print(f"Destination folder is ready: {os.path.abspath(destination_folder)}")

    # Initialize Kaggle API
    print("Initializing Kaggle API...")
    api = KaggleApi()
    try:
        api.authenticate()
        print("Kaggle API authentication successful.")
    except Exception as e:
        print(f"Error during Kaggle API authentication: {e}")
        raise

    # Dataset information
    competition_name = "titanic"
    print(f"Preparing to download dataset for competition: {competition_name}")

    try:
        print("Downloading Titanic dataset...")
        api.competition_download_files(competition_name, path=destination_folder)
        print(f"Dataset downloaded to {destination_folder}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        raise

    # Unzip the dataset
    zip_file = os.path.join(destination_folder, f"{competition_name}.zip")
    print(f"Looking for zip file at: {zip_file}")

    if os.path.exists(zip_file):
        print(f"Zip file found: {zip_file}")
        try:
            import zipfile
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                print(f"Extracting zip file to: {destination_folder}")
                zip_ref.extractall(destination_folder)
            print("Dataset extracted successfully.")
            os.remove(zip_file)
            print("Zip file removed after extraction.")
        except Exception as e:
            print(f"Error during zip extraction: {e}")
            raise
    else:
        print("Zip file not found. Please check the Kaggle API or competition name.")

if __name__ == "__main__":
    # Use absolute path for the destination folder
    destination = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw"))
    print(f"Script started. Destination folder: {destination}")
    try:
        download_titanic_dataset(destination)
        print("Script completed successfully.")
    except Exception as e:
        print(f"Script encountered an error: {e}")