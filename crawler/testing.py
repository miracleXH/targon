import requests
from bs4 import BeautifulSoup

from db import VectorDBClient
from llm import MODEL_REGISTRY


llm_name = "bert-base-uncased"
llm_model = MODEL_REGISTRY[llm_name]()

db_client = VectorDBClient(embed_size=llm_model.embed_size, batch_size=1)

inital_url = "https://cnn.com"

def crawl(url, depth, max_depth):
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract text from the webpage
        full_text = soup.get_text()

        # Generate BERT embeddings for the text
        embeddings = llm_model.text_to_embedding(full_text)

        # Insert data into Milvus
        db_client.insert(url, full_text, embeddings)

        # Find and crawl child links
        # links = soup.find_all("a")
        # for link in links:
        #     child_url = link.get("href")
        #     if child_url and child_url.startswith("http") or child_url and child_url.startswith("https"):
        #         # print(child_url)
        #         crawl(child_url, depth + 1, max_depth)

crawl(inital_url, 0, 10)