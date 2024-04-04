from typing import Annotated

import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from fastapi import FastAPI, File, Body
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import dotenv_values

from load import parse_and_split

config = dotenv_values(".env")
app = FastAPI()

origins = [
        "http://localhost:5173"
    ]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


embedding_endpoint = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
llm_endpoint = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
prompt = """
You will be given a document and asked to answer questions about it.
If you do not know the answer, do not guess. Simply say you do not know
and cannot provide an answer. Give the highest quality response you can
while remaining truthful and unbiased. The context is provided below in 
quotes.

```
{context}
```

Please answer the question regarding the context:
```
{user_prompt}
```
"""
headers = {"Authorization": f"Bearer {config['HF_API_TOKEN']}"}

def query(payload, endpoint):
    """Query the model with the given payload"""
    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()
	

@app.post("/{model_name}")
def get_response(model_name: str,
                       file: Annotated[bytes, File()],
                       user_prompt: Annotated[str, Body()]
                    ):
    """Get the response from the model."""
    with open("./user_file.pdf", "wb") as f:
        f.write(file)

    # Parse document
    documents: list[str] = [doc.page_content for doc in parse_and_split("./user_file.pdf")]

    # Returns document with the highest similarity
    output: list[float] = query({
        "inputs": {
            "source_sentence": user_prompt,
            "sentences": documents,
            },
    }, embedding_endpoint)
    context: str = max(zip(output, documents), key=lambda x: x[0])[1]

    # Prompt model
    response = query({
        "inputs": prompt.format(context=context, user_prompt=user_prompt),
        "parameters": {
            "return_full_text": False
            }
        }, llm_endpoint)

    return response[0]["generated_text"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
