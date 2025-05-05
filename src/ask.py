# Utils
import hashlib
import json
# Chats
# from langchain.chat_models import ChatOpenAI
import os
from langchain_openai import ChatOpenAI
# Caching
import pandas as pd
from langchain.embeddings import CacheBackedEmbeddings
#from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from datetime import datetime
# Messages
from langchain.schema import HumanMessage
# Caching
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
# Load env
from dotenv import load_dotenv
load_dotenv()


from .fct import getFct
from .hlp import getXY


def getPrompt(PATH="doc/definitions/content.md"):
    with open(PATH, "r") as f:
        txt = f.read()
    return txt



class sigAssistant:
    def __init__(
        self, pathDefinitions="doc/definitions/content.md", pathCache="./cache/",
        llm_highend="gpt-4o",  llm_fast="gpt-4o-mini"
    ):

        # Setting up the stores
        self.underlying_embeddings = OpenAIEmbeddings()
        set_llm_cache(SQLiteCache(database_path=pathCache+".langchain.db"))
        self.store = SQLiteCache(database_path=
                                 pathCache+"embedding/.embedding.langchain.db")
        # cached embeddings
        self.embeddings = CacheBackedEmbeddings.from_bytes_store(
            self.underlying_embeddings, self.store,
            namespace=self.underlying_embeddings.model
        )

        self.llm_fast = llm_fast
        self.llm_highend = llm_highend
        self.datastore = pathCache
        self.ai = ChatOpenAI(model=llm_fast)
        self.bigllm = ChatOpenAI(model=llm_highend)
        self.AL = getPrompt(pathDefinitions)
        self.DESCRIPTION = self.AL.split("\n\nWhat I will ask you")[0].strip()

        self.X, self.Y, self.terms = getXY(PATH=pathDefinitions)
        self.fcts = getFct(self.X, self.Y)



    def ask(self, question):
        answer = self.ai.invoke(question)
        print("--- "+self.llm_fast +":\t",
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return json.loads(answer.model_dump_json())["content"]

    def askFunctions(self, instructions, text, function, function_name):
        messages = [
            HumanMessage(content=f"""
            ## Instructions
            {instructions}

            ## Text
            {text}
            """)
        ]

        response = self.ai.invoke(
            messages,
            functions=function,
            function_call={"name": function_name}
        )
        print("--- Function call:\t",
              datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response.additional_kwargs["function_call"]["arguments"]
    
    def analyseText(
        self,
        txt: str,
        TypeOfItem,
        PBN=False,
        Source=None,
        Place=None,
        Reviewed=False,
        MIN=3,
        ow=False,
        seed="",
        MODEL="gpt-3.5-turbo",
    ):
        try:
            txt = txt.strip()
            IDtxt = str(txt) + str(seed)
            ID = str(hashlib.md5(IDtxt.encode("utf-8")).hexdigest())
            # print(ID)
            now = datetime.now()  # current date and time
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            PATH = "data/xls/" + ID + ".xlsx"
            if not os.path.isfile(PATH) or ow:


                messages = self.askFunctions(
                    instructions = self.DESCRIPTION,
                    text = "Do an ISO37k assessment of the following text:\n\n" + txt.strip(),
                    function = self.fcts,
                    function_name = "get_iso37100"#@TODOc
                )

                #print(messages)
                df = pd.DataFrame(
                    json.loads(messages)["scoring"]
                )
                #print(len(df),"elements extracted")
                df["text"] = txt.strip()
                df["Source"] = Source
                df["PBN"] = PBN
                df["Type"] = TypeOfItem
                if not Place:
                    df["Place"] = json.loads(
                        messages[-1]["function_call"]["arguments"]
                    )["location"]
                else:
                    df["Place"] = Place
                df = df[df.purpose.isin(self.X)]
                df = df[df.issue.isin(self.Y)]
                df = df[df.justification.str.len() > 3]

                df["Justification_Short"] = df.justification.apply(
                    lambda x: self.ask(
                        "Summarize in english the text below in up to 5 words:\n\n"+x
                    )
                )
                df["Source_Title"] = df.text.apply(
                    lambda x: self.ask(
                        "Summarize in english the text below in up to 5 words:\n\n"+x
                    )
                )
                df["ID"] = ID
                df = df[
                    [
                        "PBN",
                        "Source",
                        "Place",
                        "Type",
                        "text",
                        "justification",
                        "purpose",
                        "issue",
                        "scale",
                        "score",
                        "Justification_Short",
                        "Source_Title",
                    ]
                ]
                df.columns = [
                    "FromProbono",
                    "Origin",
                    "Place",
                    "Type",
                    "Source",
                    "Justification",
                    "Purpose",
                    "Issue",
                    "Scale",
                    "Score",
                    "Justification_Short",
                    "Source_Title",
                ]
                df["Reviewed"] = Reviewed
                df = df.reset_index(drop=True)
                if len(df) <= MIN:
                    while (len(df)) < MIN:
                        print("Adding another layer, len(df)=", len(df))
                        NEW = self.analyseText(
                            txt,
                            TypeOfItem,
                            PBN=PBN,
                            Source=Source,
                            Place=Place,
                            Reviewed=Reviewed,
                            MIN=1,
                            ow=ow,
                            seed=seed + "-",
                            MODEL=MODEL,
                        )
                        df = pd.concat([df, NEW])
                        print(
                            "Adding another layer now, len(NEW/df)=",
                            len(NEW),
                            "/",
                            len(df),
                            "seed:",
                            seed,
                        )
                    print("Save excel --v2, length", len(df))
                    df["model"] = MODEL
                    df["timestamp"] = date_time
                    df.to_excel(PATH, index=False)
                else:
                    # print("MIN = ",MIN,"vs",len(df))
                    print("Good du premier coup, length", len(df), "vs MIN of", MIN)
                    df.to_excel(PATH, index=False)
            else:
                df = pd.read_excel(PATH)
            df = df.reset_index(drop=True)
            return df
        except Exception as error:
            print("--> Error with ", ID, seed, "\n")
            print(error)
            return "Error"
