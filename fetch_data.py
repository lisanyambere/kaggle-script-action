import requests
import argparse

def fetch_data(url):
    """
    Fetches data from the given URL and returns it as JSON.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch JSON data from a specified URL.")
    parser.add_argument('-u', '--url', type=str, required=True, help="The URL to fetch data from")

    args = parser.parse_args()
    url = args.url

    data = fetch_data(url)
    print(data)
