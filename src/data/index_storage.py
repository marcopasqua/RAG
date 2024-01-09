import os
import time
from contextlib import contextmanager
from multiprocessing import Lock
from typing import Tuple

from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.llms import OpenAI, HuggingFaceLLM, AzureOpenAI
from llama_index.indices.base import BaseIndex
from llama_index import (
    ServiceContext,
    load_index_from_storage,
    StorageContext,
    VectorStoreIndex, set_global_handler
)
from llama_index.vector_stores import PineconeVectorStore

from utils.logger import logger
from utils.constants import *
import pinecone


def initialize_index(pinecone_index) -> BaseIndex:


    llm = AzureOpenAI(
        model="gpt-35-turbo-16k",
        deployment_name="gpt-35-turbo-16k",
        api_key=AZURE_API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION,
    )

    embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="text-embedding-ada-002",
        api_key=AZURE_API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION,
    )

    # set your ServiceContext for all the next steps
    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model
    )

    # if os.path.exists(INDEX_PATH) and os.path.exists(os.path.join(INDEX_PATH, "docstore.json")):
    #     logger.info(f"Loading index from dir: {INDEX_PATH}")
    #     index = load_index_from_storage(
    #         StorageContext.from_defaults(persist_dir=INDEX_PATH),
    #         service_context=service_context,
    #     )
    # else:
    #     index = VectorStoreIndex.from_documents([], service_context=service_context)
    #     index.storage_context.persist(persist_dir=INDEX_PATH)
    # return index

    if pinecone_index is not None:
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        index = VectorStoreIndex.from_vector_store(vector_store, service_context=service_context)
    else:
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            [], storage_context=storage_context,
            service_context=service_context
        )
    return index


class IndexStorage:
    def __init__(self):
        self._current_model = "gpt-3.5-turbo"
        set_global_handler("wandb", run_args={"project": "llamaindex",
                                              "dir": DIR_PATH,
                                              "name": "llamaindex_" + str(time.time())})
        pinecone.init(
            api_key= PINECONE_API_KEY,
            environment= PINECONE_ENV
        )
        pinecone_index = pinecone.Index(PINECONE_INDEX)

        logger.info("initializing index and mongo ...")
        self._index = initialize_index(pinecone_index=pinecone_index)
        logger.info("initializing index and mongo done")


    @property
    def current_model(self):
        return self._current_model

    # def mongo(self):
    #     return self._mongo

    def index(self):
        return self._index


    def delete_doc(self, doc_id):
        """remove from both index and mongo"""
        self._index.delete_nodes(doc_id)
        pass


    def add_doc(self, nodes):
        """add to both index and mongo"""
        self._index.insert_nodes(nodes)
        pass


# singleton of index storage
index_storage = IndexStorage()
