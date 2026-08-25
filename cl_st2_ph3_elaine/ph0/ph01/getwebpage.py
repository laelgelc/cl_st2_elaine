import argparse
import requests
import validators

def main(file_id, url):
    """Fetch a web page and save it as an HTML file."""
    # Validate URL
    if not validators.url(url):
        print("Invalid URL. Please provide a valid URL.")
        return

    http = requests.Session()
    try:
        # Fetch the web page with a timeout
        response = http.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Save the HTML content to a file
        file_path = f"{file_id}.html"
        with open(file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(response.text)
        print(f"Successfully saved HTML to {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the URL: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get a web page.")
    parser.add_argument('file_id', type=str, help="Web page's filename")
    parser.add_argument('url', type=str, help="Web page's URL")
    args = parser.parse_args()
    main(args.file_id, args.url)
