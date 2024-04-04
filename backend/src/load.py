from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

def parse_and_split(file_path: str) -> list[Document]:
    """Parse and split the pdf at the given file path."""
    loader = PyPDFLoader(file_path)
    return loader.load_and_split(text_splitter=splitter)
