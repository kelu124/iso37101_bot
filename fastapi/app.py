from fastapi import FastAPI
import os
from pydantic import BaseModel
from typing import List, Literal
from pydantic import BaseModel, Field
import pandas as pd
import json
import utils as u

class TableEntry(BaseModel):
    Purpose: str = "Social cohesion"
    Issue: str = "Education and capacity building"
    Scale: Literal["Building", "Neighbourhood"]
    Score: int = Field(ge=1, le=5)

class TableInput(BaseModel):
    data: List[TableEntry] = Field(min_items=2)
    n: int = 3

# We open up the catalogue
catalogue = u.getCatalogue()
target = u.getRandomTarget(catalogue)

# We initiate the app
app = FastAPI()
is_prod = os.environ.get('IS_HEROKU', None) 


@app.post("/get_recommendations/")
async def process_table(table_input: TableInput):
    # Access the validated data
    entries = table_input.data
    n_entries = table_input.n
    # Creates the entries
    entries = json.dumps([entry.model_dump() for entry in entries], indent=2)
    user_target = pd.DataFrame(json.loads(entries))
    # Returns the JSON
    ans = u.findJson(user_target, catalogue, n=n_entries)

    
    return {"status": "success", "nitems": n_entries,"processed_entries": ans}