import glob
import pandas as pd


def getPrompt(PATH="content.md"):
    with open(PATH, "r") as f:
        txt = f.read()
    return txt


def getXY(PATH="content.md"):
    file1 = open(PATH, 'r')
    Lines = file1.readlines()
    terms = {}
    X = []
    Y = []
    # Strips the newline character
    for line in Lines:
        TXT = line.strip()
        if TXT.startswith("## A") or TXT.startswith("## B"):
            P = TXT.split(" ")
            #print(P[1], " ".join(P[2:]))
            terms[P[1]] = " ".join(P[2:]).strip()
            if TXT.startswith("## A"):
                X.append(" ".join(P[2:]).strip())
            else:
                Y.append(" ".join(P[2:]).strip())
    return X, Y, terms

