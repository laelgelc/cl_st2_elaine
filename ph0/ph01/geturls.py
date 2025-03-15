import pandas as pd
import os
import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def main():
    # Defining input variables
    html_talks_dir = 'html_talks'
    input_file = 'valid_urls'
    log_filename = 'cl_st2_elaine.log'
    
    # Setting up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename = log_filename
    )

    # Creating output directories
    if os.path.exists(html_talks_dir):
        logging.info(f"Output directory {html_talks_dir} already exists.")
    else:
        try:
            os.makedirs(html_talks_dir)
            logging.info(f"Output directory {html_talks_dir} successfully created.")
        except OSError as e:
            logging.error(f"Failed to create the {html_talks_dir} directory:", e)
            sys.exit(1)
        
    # Importing the data into a DataFrame
    df_tedtalks_urls3 = pd.read_csv(input_file, sep='\t', header=None)
    df_tedtalks_urls3.columns = ['File ID', 'TED Talks URL']
    
    # Ensure the 'File ID' column is treated as strings
    df_tedtalks_urls3['File ID'] = df_tedtalks_urls3['File ID'].astype('str')
    
    # Pad the values in the 'File ID' column with leading zeros to make them 6 digits
    df_tedtalks_urls3['File ID'] = df_tedtalks_urls3['File ID'].str.zfill(6)
    
    # Getting the `TED Talks` URLs
    # Retry mechanism setup
    retry_strategy = Retry(
        total=3,  # Retry up to 3 times
        backoff_factor=2,  # Exponential backoff: wait 2s, 4s, 8s...
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP error codes
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    
    # Loop through the DataFrame rows
    for _, row in df_tedtalks_urls3.iterrows():
        file_id = row['File ID']  # Get the File ID
        url = row['TED Talks URL']  # Get the URL
    
        try:
            # Log the start of the request
            logging.info(f"Fetching HTML for File ID: {file_id} from URL: {url}")
    
            # Fetch the HTML content from the URL
            response = http.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
    
            # Save the HTML content to a file in the 'html_talks' directory
            file_path = os.path.join(html_talks_dir, f"{file_id}.html")
            with open(file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(response.text)
    
            # Log success
            logging.info(f"Successfully saved HTML for File ID: {file_id} to {file_path}")
    
        except requests.exceptions.RequestException as e:
            # Log any failures or retries
            logging.error(f"Failed to fetch HTML for File ID: {file_id} from URL: {url}: {e}")

if __name__ == "__main__":
    main()
