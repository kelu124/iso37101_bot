import glob
import pandas as pd

from owlready2 import *
import numpy as np
import pandas as pd
import json
import glob, os, re
import hashlib


from .hlp import getXY

X, Y, terms = getXY(PATH="./doc/definitions/content.md")


def consolidateBits(PATH="./data/xls/"):
    files = glob.glob(PATH + "*.xlsx")
    dfs = []
    for f in files:
        dfs.append(pd.read_excel(f))
    df = pd.concat(dfs).drop_duplicates()
    df.Place = df.Place.apply(lambda x: str(x).title())
    COLS = [x for x in list(df.columns) if "Unnamed" not in x]
    df = df[COLS]
    df = df.reset_index(drop=True)
    df.to_parquet(PATH + "db.parquet.gzip", compression="gzip")
    return df


def cleanSrc(x):
    done = False
    while not done:
        y = x.strip(".").strip()
        if len(x) == len(y):
            done = True
        x = y
    return y + "."


def md5(STR):
    STR = str(STR)
    return str(hashlib.md5(STR.encode("utf-8")).hexdigest())

