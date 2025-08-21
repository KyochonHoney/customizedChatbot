from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

loader = UnstructuredExcelLoader('./dataset/cures9.xlsx')

# 문서 불러오기 + 청크 분할
document_list = loader.load_and_split(text_splitter)

# 임베딩 모델
embedding = HuggingFaceEmbeddings(
    model_name='intfloat/multilingual-e5-large-instruct'
)

# Chroma DB에 저장
collection_name = 'cures'
database = Chroma.from_documents(
    documents=document_list,
    embedding=embedding,
    collection_name=collection_name,
    persist_directory='./chroma_huggingface'
)
