from fastapi import FastAPI
import os
from pydantic import BaseModel
from typing import List, Literal
from pydantic import BaseModel, Field
import pandas as pd
import json
import utils as u

# We open up the catalogue
catalogue = u.getCatalogue()
srcs = list(catalogue.data_src.unique())
print(srcs)
target = u.getRandomTarget(catalogue)
places = list(catalogue.Place.unique())


class TableEntry(BaseModel):
    Purpose: str = "Social cohesion"
    Issue: str = "Education and capacity building"
    Scale: Literal["Building", "Neighbourhood"]
    Score: int = Field(ge=1, le=5)

class TableInput(BaseModel):
    data: List[TableEntry] = Field(min_items=2)
    filtre: List[str] = Field(default_factory=[""])
    n: int = 3



# We initiate the app
app = FastAPI()
is_prod = os.environ.get('IS_HEROKU', None) 

@app.get("/get_srcs/")
async def returnssrcs():
    return {"available_sources": srcs}

@app.get("/get_places/")
async def returnplaces():
    return {"available_places": places}

@app.get("/version/")
async def versions():
    return {"v": 2.1, "date": "2025-11-21", "changelog": "Added more sources, and filtering by data source and places."}


@app.post("/get_by_place/")
async def process_table(place: str):
    if place not in places:
        return {"status": "error", "message": f"Place {place} not found in catalogue."}
    user_target = catalogue[catalogue.Place == place][["Origin","Place","id","Purpose","Issue","Scale","Score","Type",'Justification_Short',
       'Source_Title', 'Reviewed', 'reviewBy', 'reviewDate', 'pathFile',
       'timestamp', 'data_src', 'model']].to_json(orient="records", lines=False)
    n_entries = len(user_target)
    
    return {"status": "success", "nitems": n_entries,"processed_entries": user_target}


@app.post("/get_recommendations/")
async def process_table(table_input: TableInput):
    # Access the validated data
    entries = table_input.data
    n_entries = table_input.n
    filter = table_input.filtre
    OKFilter = []
    for x in list(set(filter)):
        if x in srcs:
            OKFilter.append(x)
    if not len(OKFilter):
        OKFilter = srcs
    # Creates the entries
    entries = json.dumps([entry.model_dump() for entry in entries], indent=2)
    user_target = pd.DataFrame(json.loads(entries))
    resources = catalogue[catalogue.data_src.isin(OKFilter)]
    # Returns the JSON
    ans = u.findJson(user_target, resources, n=n_entries)

    
    return {"status": "success", "nitems": n_entries,"processed_entries": ans}