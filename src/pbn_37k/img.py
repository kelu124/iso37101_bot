import matplotlib.pyplot as plt
import matplotlib
import pandas  as pd

from matplotlib.category import UnitData
from matplotlib.markers import MarkerStyle

from .hlp import getXY
import matplotlib.font_manager as font_manager
import matplotlib.font_manager as fm
from matplotlib import ft2font
from matplotlib.font_manager import ttfFontProperty
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.image as image
from PIL import Image


from importlib import resources
path_to_defs = resources.files("pbn_37k.data.definitions").joinpath("content.md")


def brandedImg(df,dfRef=pd.DataFrame(),title="Placeholder",imgPath="tmp.png"):
    plt, ax = createImg(df,dfRef,title)
    plt.savefig(imgPath, bbox_inches='tight')


    background = Image.open(imgPath)
    foreground = Image.open("data/PB_logo_org.png").resize((int(395/2.5),int(252/2.5)))
    background.paste(foreground, (1350, 25), foreground)
    background.save(imgPath)
    return 1


def createImg(df,dfRef=pd.DataFrame(),title="Placeholder"):

    plt.style.use('fivethirtyeight')

    fpath = '/home/kelu/.local/share/fonts/1Dosis-VariableFont_wght.ttf'
    font = ft2font.FT2Font(fpath)
    fprop = fm.FontProperties(fname=fpath)
    params ={"text.color" : "#8F277D",
             "xtick.color" : "#303030",
          "ytick.color" : "#303030"}
    plt.rcParams.update(params)

    ttfFontProp = ttfFontProperty(font)

    fontsize=18

    fontprop = fm.FontProperties(family='sans-serif',
                                #name=ap.fontprop.name,
                                fname=ttfFontProp.fname,
                                stretch=ttfFontProp.stretch,
                                style=ttfFontProp.style,
                                variant=ttfFontProp.variant,
                                weight=ttfFontProp.weight)

    matplotlib.rcParams.update({'font.size': fontsize,
                            'font.family': 'sans-serif'})

    X, Y, terms = getXY(PATH=path_to_defs)

    x = "Purpose"
    y = "Issue"
    h = "Scale"
    s = "Score"

    bin_dic = {0: "Building", 1: "Neighbourhood"}

    #counting the X-Y-H category entries
    #A = df.groupby([x, y, h,s ]).size().to_frame(name="vals").reset_index()

    plt_df = df.groupby([x, y, h, s]).size().to_frame(name="vals").reset_index()
    plt_df["wals"] = plt_df["Score"]*plt_df["vals"]
    plt_df = plt_df.groupby([x, y, h])["wals"].sum().reset_index()
    M = plt_df.wals.max()

    if len(dfRef):
        plt_dfRef = dfRef.groupby([x, y, h, s]).size().to_frame(name="vals").reset_index()
        plt_dfRef["wals"] = plt_dfRef["Score"]*plt_dfRef["vals"]
        plt_dfRef = plt_dfRef.groupby([x, y, h])["wals"].sum().reset_index()
        MdfRef = plt_dfRef.wals.max()
    #figure preparation with grid and scaling
    fig, ax = plt.subplots(figsize=(12, 10))

    if True:
        ax.set_ylim(11 + 0.15 + 0.5, -0.9)
        ax.set_xlim(-1.15+0.5, 6+0.15-0.5)
    ax.grid(ls="--")

    #upscale factor for scatter marker size
    scale=1500/plt_df.wals.max()
    #left marker for category 0
    ax.scatter(plt_df[plt_df[h]==bin_dic[0]][x], 
            plt_df[plt_df[h]==bin_dic[0]][y], 
            s=plt_df[plt_df[h]==bin_dic[0]].wals*scale, 
            c=[(95/256, 151/256, 122/256, 1)], edgecolor="black", marker=MarkerStyle("o", fillstyle="left"), 
            label=bin_dic[0], xunits=UnitData(X), yunits=UnitData(Y))
    #right marker for category 1
    ax.scatter(plt_df[plt_df[h]==bin_dic[1]][x], 
            plt_df[plt_df[h]==bin_dic[1]][y], 
            s=plt_df[plt_df[h]==bin_dic[1]].wals*scale, 
            c=[(144/256, 192/256, 154/255, 1)], edgecolor="black", marker=MarkerStyle("o", fillstyle="right"), 
            label=bin_dic[1])
    l=ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),
            fancybox=True, shadow=False, ncol=1,prop=fontprop, fontsize=24)
    l.legend_handles[0]._sizes = [800]
    l.legend_handles[1]._sizes = [800]

    if len(dfRef):

        scale=1500/MdfRef
        #left marker for category 0
        ax.scatter(plt_dfRef[plt_dfRef[h]==bin_dic[0]][x], 
                plt_dfRef[plt_dfRef[h]==bin_dic[0]][y], 
                s=plt_dfRef[plt_dfRef[h]==bin_dic[0]].wals*scale, 
                c=[(1, 1, 0, 0.8)], edgecolor=[(143/255, 39/255, 125/255, 0.8)], marker=MarkerStyle("*", fillstyle="left"), 
                label=bin_dic[0], xunits=UnitData(X), yunits=UnitData(Y))
        #right marker for category 1
        ax.scatter(plt_dfRef[plt_dfRef[h]==bin_dic[1]][x], 
                plt_dfRef[plt_dfRef[h]==bin_dic[1]][y], 
                s=plt_dfRef[plt_dfRef[h]==bin_dic[1]].wals*scale, 
                c=[(1, 1, 0, 0.8)], edgecolor=[(143/255, 39/255, 125/255, 0.8)], marker=MarkerStyle("*", fillstyle="right"), 
                label=bin_dic[1])
    #legend entries for the two categories
    #l = ax.legend(title="Scale (GBN or not)", ncol=2, framealpha=0, loc="upper right", columnspacing=0.1,labelspacing=1.1) 
    plt.title(title,fontproperties=fontprop, weight='bold')

    ax.xaxis.set_ticks_position('top')
    plt.xticks(rotation=90)
    plt.xticks(rotation=-20, ha='right')



    labels = ['Attractiveness',
    'Preservation and improvement\nof environment',
    'Resilience',
    'Responsible resource use',
    'Social cohesion',
    'Well-being']
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontproperties=fontprop, fontsize=24, weight='bold')


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
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontproperties=fontprop, fontsize=24, weight='bold')

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(17)
    ax.title.set_fontsize(25)

    #plt.savefig(FILE+"_review.pdf",format="pdf", bbox_inches='tight')
    #if OUTPUT:
    #    plt.savefig(OUTPUT,format=ext, bbox_inches='tight')
    return plt, ax