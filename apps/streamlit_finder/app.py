import streamlit as st
import pandas as pd
import hashlib
import glob
import random
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.category import UnitData
from matplotlib.markers import MarkerStyle

matplotlib.rcParams['font.sans-serif'] = ["Arial Bold", 'Tahoma', 'DejaVu Sans', 'Lucida Grande', 'Verdana']
matplotlib.rcParams['font.family'] = ['sans-serif']

st.set_page_config(layout="wide")

if 'password' not in st.session_state:
    st.session_state['password'] = ''

df = pd.read_parquet("data/explore.parquet.gzip")
df["Source_Title"] = df["Source_Title"].apply(lambda x: str(x).replace("\n"," "))
df.Source = df.Source.apply(lambda x: str(x).strip(".").strip().strip(".").strip().strip(".").strip())
df.loc[df.Place == "Pbn", "Place"] = "Other/All"
df.loc[df.Place == "Probono", "Place"] = "Other/All"
df.loc[df.Origin == "DLV37", "Origin"] = "D3.7"
df.loc[df.Origin == "DLV38B", "Origin"] = "D3.8"
dfVisions = df[df.Type == "Vision"]
print(len(df.Source.unique()))

def getXY(PATH="data/content.md"):
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



def createImg(df,dfRef=pd.DataFrame(),title="Placeholder"):


    X, Y, terms = getXY(PATH="data/content.md")

    x = "Purpose"
    y = "Issue"
    h = "Scale"

    bin_dic = {0: "Building", 1: "Neighbourhood"}

    #counting the X-Y-H category entries
    plt_df = df.groupby([x, y, h]).size().to_frame(name="vals").reset_index()
    M = plt_df.vals.max()

    if len(dfRef):
        plt_dfRef = dfRef.groupby([x, y, h]).size().to_frame(name="vals").reset_index()
        MdfRef = plt_dfRef.vals.max()
    #figure preparation with grid and scaling
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title(title)
    if True:
        ax.set_ylim(11 + 0.15 + 0.5, -0.9)
        ax.set_xlim(-1.15+0.5, 6+0.15-0.5)
    ax.grid(ls="--")

    #upscale factor for scatter marker size
    scale=1500/plt_df.vals.max()
    #left marker for category 0
    ax.scatter(plt_df[plt_df[h]==bin_dic[0]][x], 
            plt_df[plt_df[h]==bin_dic[0]][y], 
            s=plt_df[plt_df[h]==bin_dic[0]].vals*scale, 
            c=[(0, 0, 1, 0.5)], edgecolor="black", marker=MarkerStyle("o", fillstyle="left"), 
            label=bin_dic[0], xunits=UnitData(X), yunits=UnitData(Y))
    #right marker for category 1
    ax.scatter(plt_df[plt_df[h]==bin_dic[1]][x], 
            plt_df[plt_df[h]==bin_dic[1]][y], 
            s=plt_df[plt_df[h]==bin_dic[1]].vals*scale, 
            c=[(1, 0, 0, 0.5)], edgecolor="black", marker=MarkerStyle("o", fillstyle="right"), 
            label=bin_dic[1])
    l=ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
            fancybox=True, shadow=False, ncol=1)
    l.legendHandles[0]._sizes = l.legendHandles[1]._sizes = [800]

    if len(dfRef):

        scale=1500/MdfRef
        #left marker for category 0
        ax.scatter(plt_dfRef[plt_dfRef[h]==bin_dic[0]][x], 
                plt_dfRef[plt_dfRef[h]==bin_dic[0]][y], 
                s=plt_dfRef[plt_dfRef[h]==bin_dic[0]].vals*scale, 
                c=[(1, 1, 0, 0.8)], edgecolor="black", marker=MarkerStyle("*", fillstyle="left"), 
                label=bin_dic[0], xunits=UnitData(X), yunits=UnitData(Y))
        #right marker for category 1
        ax.scatter(plt_dfRef[plt_dfRef[h]==bin_dic[1]][x], 
                plt_dfRef[plt_dfRef[h]==bin_dic[1]][y], 
                s=plt_dfRef[plt_dfRef[h]==bin_dic[1]].vals*scale, 
                c=[(1, 1, 0, 0.8)], edgecolor="black", marker=MarkerStyle("*", fillstyle="right"), 
                label=bin_dic[1])
        
    ax.xaxis.set_ticks_position('top')
    plt.xticks(rotation=90)
    plt.xticks(rotation=-20, ha='right')

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(16)
    ax.title.set_fontsize(20)

    labels = ['Attractiveness',
    'Preservation and improvement\nof environment',
    'Resilience',
    'Responsible resource use',
    'Social cohesion',
    'Well-being']
    ax.set_xticklabels(labels)

    labels = ['Governance, empowerment\nand engagement',
        'Education and\ncapacity building',
        'Innovation, creativity\nand research',
        'Health and care\nin the community',
        'Culture and\ncommunity identity',
        'Living together,\ninterdependence and mutuality',
        'Economy and sustainable\nproduction and consumption',
        'Living and\nworking environment',
        'Safety and security',
        'Biodiversity and \necosystem services',
        'Community smart\ninfrastructures',
        'Mobility']
    ax.set_yticklabels(labels)


    #plt.savefig(FILE+"_review.pdf",format="pdf", bbox_inches='tight')
    #if OUTPUT:
    #    plt.savefig(OUTPUT,format=ext, bbox_inches='tight')
    return fig, ax


if not st.session_state['password'] == 'probono':
    print("TEST",st.session_state['password'])
    password = st.text_input("Enter a password", type="password")
    st.session_state['password'] = password
    print("NEW PWD",st.session_state['password'])
if (st.session_state['password'] == 'probono') or (password == "probono"):
    WHAT = st.sidebar.selectbox(
    "What do you want",
    ("Explore","Play"))

    if WHAT =="Explore":
        lstTYPES = df.Type.unique()
        lstPURPOSE = df["Purpose"].unique()
        lstISSUE = df["Issue"].unique()

        VISIONS = list(df[df.Type == "Vision"].Place.unique())
        st.sidebar.write("### Visions")
        targets = st.sidebar.multiselect(
            "Visions",
            options=VISIONS,
            default=[])
        if len(targets):
            dfVisions = dfVisions[dfVisions.Place.isin(targets)]
        else:
            dfVisions = pd.DataFrame()
        st.sidebar.write("### Aspects")
        purposes = st.sidebar.multiselect(
            "Purposes to consider",
            options=lstPURPOSE,
            default=[])

        issues = st.sidebar.multiselect(
            "Issues to consider",
            options=lstISSUE,
            default=[])

        DF = df.copy()
        if len(purposes):
            DF = DF[DF.Purpose.isin(purposes)]
        if len(issues):
            DF = DF[DF.Issue.isin(issues)]

        ListActions = DF.Source.unique()
        df = df[df.Source.isin(ListActions)]

        st.sidebar.write("### Details")
        lstPLACES = df.Place.unique()
        places = st.sidebar.multiselect(
            "Places to consider",
            options=lstPLACES,
            default=[])
        if len(places):
            df = df[df.Place.isin(places)]

        lstORIGIN = df.Origin.unique()
        origin = st.sidebar.multiselect(
            "Sources of info",
            options=lstORIGIN,
            default=[])
        if len(origin):
            df = df[df.Origin.isin(origin)]

        lstREVIEWED = df.Reviewed.unique()
        reviewed = st.sidebar.multiselect(
            "Is it reviewed?",
            options=lstREVIEWED,
            default=[])
        if len(reviewed):
            df = df[df.Reviewed.isin(reviewed)]
            dfVisions = dfVisions[dfVisions.Reviewed.isin(reviewed)]


        optionActivity = st.selectbox(
        "Would you like to zoom in on an activity?",
        ["All"]+list(df["Source_Title"].unique())
        )

        overLimit = False
        if optionActivity == "All":
            items = []
            X = df.drop_duplicates(subset=["Source"]).reset_index(drop=True)
            Y = len(X)
            if len(X) > 50:
                overLimit = True
                X = X.sample(frac=1).reset_index(drop=True).head(50)

            fig, ax = createImg(df, dfRef=dfVisions, title="Mapping of Probono activities and visions")
        else:
            X =df[df["Source_Title"] == optionActivity].reset_index(drop=True)
            Y = len(X)
            st.write("# Overview of initiatives map")

            if optionActivity:
                st.write(optionActivity)

            fig, ax = createImg(X, dfRef=dfVisions, title="Mapping of Probono activities and visions")



        if overLimit:
            st.warning("#### __Beware__ - there are more than 50 initiatives ("+str(Y)+"), we'll pick randomly 50 of them")

        st.pyplot(fig)


        if optionActivity == "All":
            st.write("# Initiatives map with "+str(len(X))+" items")
            for ix, row in X.iterrows():
                st.write("### "+str(ix+1)+". "+row["Source_Title"].replace("\n"," "))
                st.write("__Summary__\n",row["Source"].strip("#"))
        else:
            st.write("# Details ")
            st.write("### Origin: "+str(X["Origin"].unique()))
            st.write("### Reviewed: "+str(X["Reviewed"].unique()))
            st.write("### Model: "+str(X["model"].unique()))
            st.write("### Place: "+str(X["Place"].unique()))
            st.write(X.iloc[0]["Source"].strip("#"))
            for ix,row in X.iterrows():
                st.write("#### "+row["Purpose"]+" x " + row["Issue"]+ " (Assessment: " +row["Scale"]+": "+str(row["Score"])+")")
                st.write(row["Justification"])
    
    elif  WHAT =="Play":
        st.sidebar.write("## Serious game")


        VISIONS = list(df[df.Type == "Vision"].Place.unique())
        st.sidebar.write("### Visions")
        targets = st.sidebar.selectbox(
            "Visions",
            options=VISIONS)
        print(targets)
        dfVisions = dfVisions[dfVisions.Place == targets]


        df = df[df.Type == "Activities"]
        df = df[~df.Origin.isin(["KERs file"])]
        DFF = df
        DFF = DFF.drop_duplicates(subset=["Source"])
        for ix, row in DFF.iterrows():
            df.loc[df.Source == row["Source"], "Source_Title"] = row["Source_Title"]
        allActivities = []

        lstD2 = df[df.Origin.str.startswith("D2")].Source_Title.unique()
        wp2 = st.sidebar.multiselect(
            "WP2 content",
            options=lstD2,
            default=[])
        if len(wp2):
            for x in wp2:
                allActivities.append(x) 

        lstD3 = df[df.Origin.str.startswith("D3")].Source_Title.unique()
        wp3 = st.sidebar.multiselect(
            "WP3 content",
            options=lstD3,
            default=[])
        if len(wp3):
            for x in wp3:
                allActivities.append(x) 

        lstD5 = df[df.Origin.str.startswith("D5")].Source_Title.unique()
        wp5 = st.sidebar.multiselect(
            "WP5 content",
            options=lstD5,
            default=[])
        if len(wp5):
            for x in wp5:
                allActivities.append(x) 

        lstD7 = df[df.Origin.str.startswith("D7")].Source_Title.unique()
        wp7 = st.sidebar.multiselect(
            "WP7 content",
            options=lstD7,
            default=[])
        if len(wp7):
            for x in wp7:
                allActivities.append(x) 
        st.write("### Your propositions")

        st.write("* "+"\n* ".join(allActivities))
        st.write("### Visualisation")
        fig, ax = createImg(df[df.Source_Title.isin(allActivities)], dfRef=dfVisions, title="Serious game:\nProposition of activities for "+targets+".")
        st.pyplot(fig)