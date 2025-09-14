# Using Large Language Models for an ISO37101 standard assessment mapping for sustainable communities

This works presents a tool to support a new approach to urban sustainability assessment through the use of Large Language Models (LLMs) to streamline the use of the ISO 37101 framework - to automate and standardise the assessment of urban initiatives against the six "sustainability purposes" and twelve "issues" outlined in the standard.While benefits for the application of the standard approach to mapping initiatives are direct, it can also hopefully contribute to the growing body of work on AI applications in urban planning and provides a novel method for operationalising standardised sustainability frameworks in different urban contexts, as well as suggesting a way forward to reviews and audits of projects and initiatives against set criteria.

 
This code and data have been used in the article [Using Large Language Models for a standard assessment mapping for sustainable communities](https://doi.org/10.48550/arXiv.2411.00208).


# Installation

`pip install -e .`

# What about the code

The tool provides the following features:
* Review source content and map it on the 12x6 grid.
* Produce excel files for human review of the LLM-generated content
* Visualize the map
* Import human-reviewed excel file
* Find initiatives that match users requirements, based on the grid.
  * An use case example is included, under the form of a Streamlit-based visualisation tool 

This relies on definitions inspired by the standard, but adapted to a specific context, that of the PROBONO project. Further modifications more aligned to specific context can be made by users.

Calls to OpenAI rely on a custom tool (OAI) developped outside of this project. It should be straightforward to update the calls to LLMs to streamline the whole process and only use existing, widespread tools (eg langchain). This is only a legacy at the time when other libraries did not propose the options they offer today.

# Application

The code mentionned above is used on the Paris Participatory Budget database

![](outputs/Paris.png)

# What about the repo datasets

The main datasets used in the proof of concept consist in:
* `data/bp_projets_gagnants.csv`
* `data/budget-participatif_operations-projets-gagnants-realisations.geojson`

And the processed data is stored at:
* `data/dataset_final.parquet.gzip` contains the processed projects from  `bp_projets_gagnants`.


# Acknowledgement 
 
This work has been used in the PROBONO project (doi: 10.3030/101037075 ), which has received funding from the European Union’s Horizon 2020 Europe Research and Innovation programme under Grant Agreement No 101037075. This output reflects only the author’s view, and the European Union cannot be held responsible for any use that may be made of the information contained therein. 


## Disclaimer(s)

This project is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR A PARTICULAR PURPOSE. See the Licenses used below for more details. Also:
* We are at the early stage of LLM-based solutions. Quality will vary depending on the models used, at the point of time they will be used.
* Human in the loop validation, checks and approval are required in any case.
* You will have to implement your own controls, including the usual guardrails and checks.
 
## License

An LLM-based tool to streamline reviews of urban initiatives using the ISO37101 12x6 approach 

Copyright (c) 2024 Luc Jonveaux

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the [GNU General Public License](LICENSE_GPLv3.0.txt) along with this program. If not, see <https://www.gnu.org/licenses/>.
