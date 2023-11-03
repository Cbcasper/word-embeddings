import json

"""
article_export.json
{
    id
    title
    subTitle
    lead
    content
    edition
}

articles_dump.json
{
    id
    content
    keywords
    fieldsOfInterest
}

wiki_dutch_v2
{
    title
    value
    parent_id
    field_of_interest
    title_dutch
}
"""

class Unlabeled:
    def __init__(self):
        with open("data/article_export.json", "r") as file:
            self.data = json.load(file)

class Labeled:
    def __init__(self):
        pass

datasets = {
    "unlabeled": Unlabeled(),
    "labeled": Labeled()
}