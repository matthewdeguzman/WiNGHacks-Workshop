import time
import os
from typing import Annotated
from heapq import nlargest

import requests
from pydantic import BaseModel
from fastapi import FastAPI, Form, UploadFile, Response
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

llm_endpoints: dict[str, str] = {
        "mushwoom": "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        "william": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
    }
file_prompt = """
Pretend your name is {name}. You will be given a document and asked to answer questions about it.
If you do not know the answer, do not guess. Simply say you do not know
and cannot provide an answer. Give the highest quality response you can
while remaining truthful and unbiased. Here is an example of how you
you will be asked a question and how you should respond.

Context:
```
GPA: 3.89
Major: Computer Science
Courses: Data Structures, Algorithms, Operating Systems
School: University of California, Berkeley
```

Question:
```
What is the student's GPA?
```

Your response:
The student's GPA is 3.89.

Now, you will be given context and a question. Please provide a response
in the format we just specified.

Context:
```
{context}
```

Question:
```
{user_prompt}
```

Your response:
"""

no_file_prompt = """
Your name is {name}. You are given a prompt and will respond to it. Give the highest quality
reponse you can while remaining truthful and unbiased. If you do not know
the answer and cannot provide an answer, simply say you do now know. Do
not try to make up an answer.

Prompt:
{user_prompt}

Response:
"""

readers = {"Authorization": f"Bearer {config['HF_API_TOKEN']}"}

class LLMResponse(BaseModel):
    generated_text: str

def query(payload, endpoint):
    """Query the model with the given payload"""
    headers = {
            "Authorization": f"Bearer {config['HF_API_TOKEN']}",
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    return response.json()
	
def clean_output(response: LLMResponse) -> LLMResponse:
    """Clean the output from the model."""
    response.generated_text = response.generated_text.strip('`')
    return response

@app.post("/prompt")
async def get_prompt(res: Response, llm: str,
                     user_prompt: Annotated[str, Form()],
                     file: Annotated[UploadFile | None, Form()] = None
                ) -> LLMResponse | dict[str, str]:
    """Get the response from the model."""
    
    # Check if LLM is in the list of available models
    llm = llm.lower()
    if llm not in llm_endpoints:
        res.status_code = 404
        return {"error": "Model not found."}
    
    # Check if the user has uploaded a file
    if file:
        pass
        # Save the file
    
        # Parse document
    
        # Return document with highest similarity to user prompt
    
        # Get the top 3 most relevant documents
    else:
        pass
      # Create prompt without file context
    
    # Query LLM
    print(f"Querying {llm_endpoints[llm]}...")
    response = LLMResponse(generated_text="test")

    # Return llm response
    return clean_output(response)
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
