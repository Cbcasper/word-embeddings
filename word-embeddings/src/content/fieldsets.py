import pandas

from .fields_of_interest_v1 import _FIELDS_OF_INTEREST

fieldsets = {
    "v1": [{"id": id, "content": content} for id, content in _FIELDS_OF_INTEREST.items()],
    "v2": [{"id": content, "content": content} for content in pandas.read_csv("data/wiki_dutch_v2.csv")["TITLE"].unique()]
}