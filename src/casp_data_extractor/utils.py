import requests


def download_url(url) -> str:
  """Download the given url."""
  try:
    response = requests.get(url)
    response.raise_for_status()
  except Exception as e:
    print(f"Error processing {url}: {str(e)}")
    exit(1)
  return response.text
