import os
import logging
import re
from typing import Any, Dict, List, Optional

from modules.ml.plugins.vncorenlp import VnCoreNLPSingleton

from .base import BasePreProcessor
from .cleaning import normalize_text

logger = logging.getLogger(__name__)


class ViPreProcessor(BasePreProcessor):
    def __init__(
        self,
        use_fixed_stopwords: Optional[bool] = False
    ):
        """
        :param use_fixed_stopwords: remove stopwords that appears in pre-defined files
        """
        self.rdrsegmenter = VnCoreNLPSingleton.get_instance(annotators='wseg',
                                                            max_heap_size='-Xmx500m')
        
        self.stopwords = None
        self.use_fixed_stopwords = use_fixed_stopwords
        if use_fixed_stopwords:
            self._load_stopwords()

    def clean(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Perform document cleaning on a single document and return a single document.
        Includes dealing with whitespaces, empty lines.
        """
        text = document['text']

        text = normalize_text(text)
        text = self._word_segment(text)

        document['text'] = text
        return document

    def split(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        return super().split(document)

    def _word_segment(self, text: str) -> str:
        """Use VnCoreNLP-based tokenizer for word segmentation
        """
        sentences = self.rdrsegmenter.tokenize(text)

        tokenized_sents = []
        for words in sentences:
            if self.use_fixed_stopwords:
                words = filter(lambda w: w not in self.stopwords, words)
            tokenized_sents.append(" ".join(words))

        result = " ".join(tokenized_sents)
        return result

    def _load_stopwords(self, stopword_path: str = 'modules/ml/data/vietnamese-stopwords.txt'):
        """Load list of stopwords from given path
        """
        if not os.path.isfile(stopword_path):
            logger.error('File not found, stopwords list not initialized')
            return
        if not self.stopwords:
            self.stopwords = []
        with open(stopword_path, 'r') as f:
            for line in f:
                word = "_".join(line.split(' '))
                self.stopwords.append(word)
