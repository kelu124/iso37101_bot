import pandas as pd
import numpy as np
import json
import glob, os
import hashlib
import datetime
from openpyxl import load_workbook
from openpyxl.styles import Alignment


from .hlp import getXY

from importlib import resources
path_to_defs = resources.files("pbn_37k.data.definitions").joinpath("content.md")
path_to_xls_template = resources.files("pbn_37k.data.template").joinpath("template.xlsx")


def createExcel(dfUC, PATHOUT, coverTitle, coverPlace, coverTopic):

    if len(dfUC) == 0:
        print("Empty dataframe, won't be able to create a report")
        return "Empty dataframe, won't be able to create a report"
    templatePos = {}
    templatePos["activity"] = "C4"
    templatePos["Title"] = "C5"
    templatePos["Deliverable"] = "C6"
    templatePos["ID"] = "L5"
    templatePos["LL"] = "L6"
    templatePos["Review"] = "C8"
    templatePos["initItem"]= 11

    X, _, terms = getXY(PATH=path_to_defs)
    inv_terms = {v: k for k, v in terms.items()}

    wb = load_workbook(path_to_xls_template)

    dfUC["Source"] = dfUC["Source"].apply(lambda x: str(x).strip().strip(".").strip().strip(".").strip().strip(".").strip().strip(".").strip().strip(".").strip().strip("."))
    dfUC["ID"] = dfUC.Source.apply(lambda x: str(hashlib.md5(str(x).encode("utf-8")).hexdigest()))
    TABS = []
    target = wb['Template']
    for id in dfUC.ID.unique():
        dfID = dfUC[dfUC.ID == id].reset_index(drop=True)
        row = dfID.iloc[0]

        s = wb.copy_worksheet(target)
        if 1:
            for x in target.conditional_formatting:
                s.conditional_formatting.add(list(x.cells.ranges)[0].coord, x.cfRule[0])
        s[templatePos["activity"]] = "Review of " + str(row.Origin)
        s[templatePos["Title"]] = row["Source_Title"]
        s[templatePos["Deliverable"]] = row["Origin"]
        s[templatePos["ID"]] = row["ID"][:12]
        s[templatePos["LL"]] = row["Place"]
        src = row["Source"]
        while "\n\n" in src:
                src = src.replace('\n\n',"\n")
        s[templatePos["Review"]] = src
        i = 0

        for ix, row in dfID.iterrows():
            if ix < 9:
                s["B"+str(11+i)] = ""
                s["G"+str(11+i)] = row["Justification"]
                s["C"+str(11+i)] = inv_terms[row["Purpose"]].replace(".","") 
                s["D"+str(11+i)] = inv_terms[row["Issue"]].replace(".","") 
                s.row_dimensions[11+i].height = (round(len(str(row["Justification"]).strip('"')) / 69) +0.3 )*16 
                SCALE = row["Scale"]
                if SCALE == "Building":
                    s["E"+str(11+i)] = row["Score"]
                elif SCALE == "Neighbourhood":
                    s["F"+str(11+i)] = row["Score"]
                # Fill in the excel
                i += 1
        s.title = row["ID"][:12]
        TABS.append(str(s.title))
    c = wb['Cover']
    c["C6"] = coverTitle # "Review of Aarhus vision"
    c["C8"] = coverPlace # "Aarhus"
    c["C9"] = coverTopic # "WP7, D7.2"
    c["C10"] = datetime.datetime.now().strftime("%B %d, %Y - %I:%M%p")
    c["C12"] = "Automated" 

    X = 9
    for id in dfUC.ID.unique():
        dfID = dfUC[dfUC.ID == id].reset_index(drop=True)
        row = dfID.iloc[0]
        if row["Reviewed"] == True:
            c["T"+str(X)] = "Y"
        else:
            c["T"+str(X)] = "N"
        c["U"+str(X)] = row["ID"][:12]
        c["V"+str(X)] = row["Origin"]
        c["W"+str(X)] = row["Source_Title"]
        X += 1

    for x in range(12):
        for y in range(12): #rows
            L =  chr(ord('G')+x)
            CELLS = []
            for sheet in TABS:
                FORM = "=IF("
                letter = chr(ord('C')+x)
                CELLS.append("ISNUMBER("+sheet+"!"+letter+str(39+y)+")")
                FORM += "+".join(CELLS)
                FORM += ','+"+".join(CELLS)+',"")'
            c[L+str(26+y)] = FORM

            CELLS = []
            for sheet in TABS:
                FORM = "=IFERROR(AVERAGE("
                letter = chr(ord('C')+x)
                CELLS.append(sheet+"!"+letter+str(39+y))
                FORM += ",".join(CELLS)
                FORM += '),"")'
            c[L+str(10+y)] = FORM
    wb.remove(wb['Template'])
    wb.save(PATHOUT)
    return PATHOUT


