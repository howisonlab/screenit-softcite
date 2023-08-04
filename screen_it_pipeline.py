from article_dataset_builder.harvest import Harverster
from article_dataset_builder.nlm2tei import Nlm2tei
from software_mentions_client.client import software_mentions_client
import requests
import tqdm
from importlib.metadata import version

from pathlib import Path
import pandas as pd

version('article_dataset_builder')
version('software_mentions_client')
version('lmdb')

# Patrice pointed out the input file is pcmids not DOIs.
#https://github.com/howisonlab/screenit-softcite/issues/1
# First convert file so that it is one pmcid per line.
# !cut -d ',' -f1 config/comparison_full_set.csv | tail -n +2 > config/comparison_full_set-pmcids.csv

harvester = Harverster(config_path="config/config-harvester.json", dump_metadata=True)
harvester.harvest_pmcids("config/comparison_full_set-pmcids-short.csv")

# Not clear to me if the resulting tei.xml files are used by the client?
# Running it is not idempotent, seems to repeat even if the tei.xml files are there?
# Also requires running: git clone https://github.com/kermitt2/Pub2TEI
nlm2tei = Nlm2tei(config_path="config/config-harvester.json")
nlm2tei.process()

# Currently the server doesn't prioritize the TEI XML files.  
# See https://github.com/softcite/software_mentions_client/issues/4
# But seeing PDF processing failures on laptop. See https://github.com/howisonlab/screenit-softcite/issues/6
# Therefore rename all PDF files so they are ignored.
# for filename in list(Path("./data").rglob("*.pdf")):
#       filename.rename(filename.with_suffix('.ignore'))

# ignored_pdf_files = list(Path("./data").rglob("*.ignore"))
# print("Number of Ignored PDF files:")
# print(len(ignored_pdf_files))

# harvester.diagnostic(full=True)

client = software_mentions_client(config_path="config/config-client.json")
# This method seems to only annotate PDFs? 
client.annotate_collection("./data", force=True)

# Trying:
# python3 -m software_mentions_client.client --repo-in ./data/ --config config/config-client.json --reprocess




all_paths = list(Path("./data").rglob("*.pdf"))
print("\nNumber of PDF files:")
print(len(all_paths))
software_paths = list(Path("./data").rglob("*.software.json"))
print("Number of software.json files:")
print(len(software_paths))

import json

# Obtain the mentions from the .software.json files and the metadata from the 
# accompanying metadata.json files.
df = pd.DataFrame()
for filename in software_paths:
      base_name = filename.stem.rsplit('.pub2tei')[0]
      metadata_json_name = filename.with_name(base_name + ".json")
      json_string = metadata_json_name.read_text()
      metadata_dict =  json.loads(json_string)
      # print(metadata_dict)
      row_df = ( pd.DataFrame([pd.read_json(filename, typ="series")])
                   .assign(pmcid = metadata_dict['pmcid'])
                   .assign(glob_filename = filename)
      )
      # print(row_df["metadata"])

      df = pd.concat([df, row_df])

(   df.explode("mentions")
      .assign(#article_pmcid = lambda df_: df_.metadata.str['pmcid'],
              software_name = lambda df_: df_.mentions.str['software-name'].str['normalizedForm'],
              sentence_context = lambda df_: df_.mentions.str['context']
             )
      .filter(axis = "columns", items = ['pmcid', 'software_name', 'sentence_context', 'glob_filename'])
  #    .replace('', np.nan)
  #    .dropna()
      .to_csv("mentions_one_per_row.csv", index=False)
)
