# word-embeddings

## Install

Dependencies are listed in `requirements.txt` for all uses. Only [fasttext](https://fasttext.cc/docs/en/support.html) needs to be installed separately.

## Basic Use

The scripts can be used independently. `src/baselines.py` is the main file in which experiments can be conducted. `embeddings.py, similarities.py` contain the code for the models and ranking methods used. `device.py` is a mac-friendly pytorch utility.

## api for use with webapp

`api.py` is powered by flask. Run `src/api.py` to start up the server. It needs some time to start up before it can receive api calls.