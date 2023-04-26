import requests
from tqdm import tqdm

url = "https://www.youtube.com/watch?v=iAHgpTtZOYo&t=697s"
response = requests.get(url)
print(response)
