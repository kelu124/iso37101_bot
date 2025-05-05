import pandas as pd
import hashlib
import glob
import os


def getCatalogue():
    catalogue_un = pd.read_parquet("sample_data/t35_bp_iso.parquet.gzip").drop_duplicates()
    catalogue_deux = pd.read_parquet("sample_data/uc.parquet.gzip").drop_duplicates()
    df = pd.concat([catalogue_un,catalogue_deux]).reset_index(drop=True)
    df.Origin = df.Origin.apply(lambda x: x.replace("ZP_UCS--",""))
    return df

def getRandomTarget(df):
    target = df.drop_duplicates(subset=["Purpose","Issue","Scale"]).sample(20)
    target.Score = 1
    target = df.sample(10)
    return target[["Purpose","Issue","Scale","Score"]]

def findAction(target,catalogue,n=3):
    results = []
    target["combo"] = target["Purpose"]+"-"+target["Issue"]+"-"+target["Scale"]
    catalogue["combo"] = catalogue["Purpose"]+"-"+catalogue["Issue"]+"-"+catalogue["Scale"]
    while len(results) < n:
        # Let's start
        for ix, row in target.iterrows():
            X, Y, Z, S = row["Purpose"],row["Issue"], row["Scale"], row["Score"]
            sl = catalogue[(catalogue.Purpose == X) & (catalogue.Issue == Y)][["Source_Title","Purpose","Issue","Scale","Score","combo"]]
            sl["mult"] = sl.Scale.apply(lambda x: 5 if x == row["Scale"] else 1)
            sl["fScore"] = sl.Score * sl.mult * S
        choice = pd.pivot_table(sl, values='fScore', index='Source_Title',aggfunc='sum').sort_values(by="fScore", ascending=False).reset_index().iloc[0]
        results.append(choice["Source_Title"])
        # Now removing the points ticked
        #print(choice)
        thechoice = list(catalogue[catalogue.Source_Title == choice.Source_Title].combo)
        target = target[~(target.combo.isin(thechoice))]
        #print(thechoice)
        # Now removing the possible from the catalogue
        catalogue = catalogue[~(catalogue.Source_Title == choice.Source_Title)]
        catalogue = catalogue[~(catalogue.combo.isin(thechoice))]

    return results

def findJson(target,catalogue,n=3):
    ans = findAction(target,catalogue,n)
    return catalogue[catalogue.Source_Title.isin(ans)][["Origin","Source","Justification","Purpose","Issue","Scale","Score","Source_Title"]].to_json(orient="table")