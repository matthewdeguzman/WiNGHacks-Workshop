# WiNG Hacks Workshop

Creating our own RAG chat-bot with LangChain and HuggingFace.

\<Upload video once rate limit goes away...\>

## What is RAG (Retrieval Augmented Generation)?

**Definition taken from [Nvidia](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/)**: Retrieval-augmented generation (RAG) is a technique for enhancing 
the accuracy and reliability of generative AI models with facts fetched from external sources.

For example, If I had a database of shows I watched over the past 5 years and I asked
a chatbot using RAG to tell me what shows I binged in March 2023, the chatbot might
tell me that I watched "Business Proposal", "Twenty-Five Twenty-One", and "Family Guy" during 
that time.

Here is a diagram I took from [some LinkedIn post](https://www.linkedin.com/pulse/what-retrieval-augmented-generation-grow-right/):

![RAG Image](./media/RAG.png)

## What is LangChain 🦜

**Definition taken from [LangChain](https://langchain.com/)**: LangChain gives developers a framework to construct LLM‑powered apps easily.

LangChain is a framework I'm [somewhat familiar with](https://twitter.com/LangChainAI/status/1686763366696787968). It allows you to develop a variety of applications with 
language models like make chatbots, work with agents, chain tools, and more.

We will be using it to parse documents, but you can get a lot more creative with it!

## What is HuggingFace 🤗

**Definition from [Wikipedia](https://en.wikipedia.org/wiki/Hugging_Face)**:
Hugging Face, Inc. is an French-American company based in New York City that develops computer tools for building applications using machine learning. It is most notable for its transformers library built for natural language processing applications and its platform that allows users to share machine learning models and datasets and showcase their work.

HuggingFace hosts a variety of models that you can use for your projects. We will be using
a few of the hosted models to create our RAG chatbot.
