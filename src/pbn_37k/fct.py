def getFct(X,Y):
    functions = [
            {
            "name": "get_iso37100",
            "description": "If the user asks for a ISO37k assessment, returns the location, and a list of criteria that constitute the text, based on the definitions of 'purposes' and 'issues' you were provided. Extract at least 10 main items, and be as exhaustive as possible. DO not invent anything, stick to what is explicitly detailed or can be inferred directly from the text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "enum": ["Aarhus", "Prague", "Brussels", "Porto", "Madrid","Dublin","Unknown"],
                        "description": "The city that is the most mentioned - it can be Unknown if none is specified.",
                    } ,
                    "scoring": {
                        "type": 'array',
                        "items": {
                            "type": 'object',
                            "description": "A criteria, which is an angle specified in the text, for the review.",
                            "properties": {
                                "purpose" :{
                                    "type": 'string', 
                                    "enum":X,
                                    "description": 'The "Purpose" that matches the more the specific aspect being considered. It must be in the provided list.'
                                },
                                "issue" :{
                                    "type": 'string', 
                                    "enum":Y,
                                    "description": 'The "Issue" that matches the more the specific aspect being considered. It must be in the provided list.'
                                },
                                "scale" :{
                                    "type": 'string', 
                                    "enum":["Building","Neighbourhood"],
                                    "description": 'The scale at which this criteria is being considered - it specifies if the text focuses on a Building or if it affects a Neighbourhood scale.'
                                },
                                "score" :{
                                    "type": 'integer', 
                                    "description": 'A likert-scale integer value between 1 and 5 capturing how important the criteria is in the given text (5 is the max). It must not be 0.'
                                },
                                "justification" :{
                                    "type": 'string', 
                                    "description": "Between three and five sentences that detail the choice of the 'purpose' and 'issue' of this criteria. It cannot be empty."
                                }
                            },
                            "required": ['purpose',"issue","scale","score","justification"],
                        }
                    },
                },
                "required": ["location","scoring"],
            },
        }
    ]
    return functions


def getFctFull(X,Y):
    functions = [
            {
            "name": "get_iso37100",
            "description": "If the user asks for a ISO37k assessment, returns the location, a title, and a summary of the text you are given, as well as a scoring that breaks down the text into the components detailed above. Extract as many criteras as possible, from most relevant to less relevant, a minimum of ten criterias if feasible.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "enum": ["Aarhus", "Prague", "Brussels", "Porto", "Madrid","Dublin","Unknown"],
                        "description": "The city that is the most mentioned - it can be Unknown if none is specified.",
                    },
                    "short_story": {
                        "type": "string",
                        "description": "Summarize in up to 20 words that the text is about.",
                    },
                    "title": {
                        "type": "string",
                        "description": "Give a title that summarizes what the text is about.",
                    },
                    "scoring": {
                        "type": 'array',
                        "items": {
                            "type": 'object',
                            "description": "A criteria, which is an angle specified in the text, for the review.",
                            "properties": {
                                "purpose" :{
                                    "type": 'string', 
                                    "enum":X,
                                    "description": 'The Purpose that matches the more the specific aspect being considered.'
                                },
                                "issue" :{
                                    "type": 'string', 
                                    "enum":Y,
                                    "description": 'The Issue that matches the more the specific aspect being considered.'
                                },
                                "scale" :{
                                    "type": 'string', 
                                    "enum":["Buildings","Neighbourhood"],
                                    "description": 'The scale at which this criteria is being considered.'
                                },
                                "score" :{
                                    "type": 'integer', 
                                    "description": 'A value between 0 and 100 capturing how important the criteria is in the given text  (100 is the max).'
                                },
                                "justification" :{
                                    "type": 'string', 
                                    "description": "Up to two sentences that detail the choice of the 'purpose' and 'issue' of this criteria."
                                }
                            },
                            "required": ['purpose',"issue","scale","score","justification"],
                        }
                    },
                },
                "required": ["location", "short_story","title","scoring"],
            },
        }
    ]
    return functions
