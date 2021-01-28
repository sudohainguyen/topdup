from First_Layer_Retriever import *
from modules.ml.retriever.indexer.faiss import FaissIndexer
from modules.ml.retriever.vectorizer.tf_idf import TfidfDocVectorizer

class Second_Layer_Retriever(First_Layer_Retriever):
    def __init__(self):
        super().__init__()
        pass
    
    def _get_all_paragraphs(self) -> List[Paragraph]:
        pass

    def cal_score(self) -> dict:
        pass

    def

    def retrieve(self):
        pass