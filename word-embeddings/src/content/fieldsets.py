import pandas

from .fields_of_interest_v1 import _FIELDS_OF_INTEREST

fieldsets = {
    "v1": list(_FIELDS_OF_INTEREST.values()),
    "v2": pandas.read_csv("data/wiki_dutch_v2.csv")["TITLE"].unique()
}