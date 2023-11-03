import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import DutchStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

class LemmaVectorizer(TfidfVectorizer):
    def __init__(
        self,
        *,
        input="content",
        encoding="utf-8",
        decode_error="strict",
        strip_accents=None,
        lowercase=True,
        preprocessor=None,
        tokenizer=None,
        analyzer="word",
        stop_words=None,
        token_pattern=r"(?u)\b\w\w+\b",
        ngram_range=(1, 1),
        max_df=1.0,
        min_df=1,
        max_features=None,
        vocabulary=None,
        binary=False,
        dtype=np.float64,
        norm="l2",
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=False,
    ):
        self.lemmatizer = WordNetLemmatizer()
        stop_words = [self.lemmatizer.lemmatize(word, pos="v") for word in stop_words]
        super().__init__(
            input=input,
            encoding=encoding,
            decode_error=decode_error,
            strip_accents=strip_accents,
            lowercase=lowercase,
            preprocessor=preprocessor,
            tokenizer=tokenizer,
            analyzer=analyzer,
            stop_words=stop_words,
            token_pattern=token_pattern,
            ngram_range=ngram_range,
            max_df=max_df,
            min_df=min_df,
            max_features=max_features,
            vocabulary=vocabulary,
            binary=binary,
            dtype=dtype,
            norm=norm,
            use_idf=use_idf,
            smooth_idf=smooth_idf,
            sublinear_tf=sublinear_tf,
        )

    def build_tokenizer(self):
        tokenizer = super().build_tokenizer()

        def lemma_tokenizer(text):
            tokens = tokenizer(text)
            return [self.lemmatizer.lemmatize(token, pos="v") for token in tokens]

        return lemma_tokenizer

class StemVectorizer(TfidfVectorizer):
    def __init__(
        self,
        *,
        input="content",
        encoding="utf-8",
        decode_error="strict",
        strip_accents=None,
        lowercase=True,
        preprocessor=None,
        tokenizer=None,
        analyzer="word",
        stop_words=None,
        token_pattern=r"(?u)\b\w\w+\b",
        ngram_range=(1, 1),
        max_df=1.0,
        min_df=1,
        max_features=None,
        vocabulary=None,
        binary=False,
        dtype=np.float64,
        norm="l2",
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=False,
    ):
        self.stemmer = DutchStemmer()
        stop_words = [self.stemmer.stem(word) for word in stop_words]
        super().__init__(
            input=input,
            encoding=encoding,
            decode_error=decode_error,
            strip_accents=strip_accents,
            lowercase=lowercase,
            preprocessor=preprocessor,
            tokenizer=tokenizer,
            analyzer=analyzer,
            stop_words=stop_words,
            token_pattern=token_pattern,
            ngram_range=ngram_range,
            max_df=max_df,
            min_df=min_df,
            max_features=max_features,
            vocabulary=vocabulary,
            binary=binary,
            dtype=dtype,
            norm=norm,
            use_idf=use_idf,
            smooth_idf=smooth_idf,
            sublinear_tf=sublinear_tf,
        )

    def build_tokenizer(self):
        tokenizer = super().build_tokenizer()

        def stem_tokenizer(text):
            tokens = tokenizer(text)
            return [self.stemmer.stem(token) for token in tokens]

        return stem_tokenizer