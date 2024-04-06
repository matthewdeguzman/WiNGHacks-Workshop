import time
import os
from typing import Annotated
from heapq import nlargest

import requests
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from fastapi import FastAPI, Form, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import dotenv_values

from load import parse_and_split

config = dotenv_values("../.env")
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
        "fry": "https://api-inference.huggingface.co/models/openai-community/gpt2",
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
    response = requests.post(endpoint, json=payload)
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
    
    # # Check if LLM is in the list of available models
    # llm = llm.lower()
    # if llm not in llm_endpoints:
    #     res.status_code = 404
    #     return {"error": "Model not found."}
    #
    # # Check if the user has uploaded a file
    # if file:
    #     # Save the file
    #     with open("./user_file.pdf", "wb+") as f:
    #         f.write(await file.read())
    #
    #     # Parse document
    #     documents: list[str] = [doc.page_content for doc in parse_and_split("./user_file.pdf")]
    #     os.remove("./user_file.pdf")
    #
    #     # Return document with highest similarity to user prompt
    #     output: list[float] = query({
    #         "inputs": {
    #             "source_sentence": user_prompt,
    #             "sentences": documents,
    #             },
    #     }, embedding_endpoint)
    #
    #     # Get the top 3 most relevant documents
    #     context: str = "\n".join([p[1] for p in nlargest(3, zip(output, documents), key=lambda x: x[0])])
    #     prompt = file_prompt.format(name=llm, context=context, user_prompt=user_prompt)
    # else:
    #   # Create prompt without file context
    #     prompt = no_file_prompt.format(name=llm, user_prompt=user_prompt)
    #
    # # Query LLM
    # print(f"Querying {llm_endpoints[llm]}...")
    # response = query({
    #     "inputs":  prompt,
    #     "parameters": {
    #         "return_full_text": False,
    #         "temperature": 0.1,
    #         "max_new_tokens": 512
    #         }
    #     }, llm_endpoints[llm])
    # print(response)
    # # Return llm response
    # return clean_output(LLMResponse(generated_text=response[0]["generated_text"]))
    time.sleep(3)
    return {"generated_text": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like)."}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
