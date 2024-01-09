from typing import List

from fastapi import APIRouter, UploadFile, status
from llama_index.node_parser import SentenceSplitter
from utils.constants import *
from llama_index import download_loader, Document
from data.index_storage import index_storage

router = APIRouter(
    prefix="/files",
    tags=["files"]
)


PDFReader = download_loader("PDFReader")
loader = PDFReader()


@router.post("/")
async def upload_files(files: List[UploadFile], status_code=status.HTTP_201_CREATED):
    for f in files:
        # save f.file in a new file inside files folder
        with open(os.path.join(LOCAL_STORAGE_PATH, f.filename), "wb") as buffer:
            buffer.write(f.file.read())
            buffer.close()

        docs = loader.load_data(file=Path(os.path.join(LOCAL_STORAGE_PATH, f.filename)))
        doc_text = "\n\n".join([d.get_content() for d in docs])
        documents = [Document(text=doc_text)]
        node_parser = SentenceSplitter(chunk_size=1024)
        base_nodes = node_parser.get_nodes_from_documents(documents)
        index_storage.add_doc(base_nodes)
    return {"message": "Files uploaded successfully"}




