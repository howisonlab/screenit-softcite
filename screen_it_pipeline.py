from article_dataset_builder.harvest import Harverster
from article_dataset_builder.nlm2tei import Nlm2tei
from software_mentions_client.client import software_mentions_client
import requests
import tqdm
from importlib.metadata import version

version('article_dataset_builder')
version('software_mentions_client')
version('lmdb')

# Patrice pointed out the input file is pcmids not DOIs.
#https://github.com/howisonlab/screenit-softcite/issues/1
# First convert file so that it is one pmcid per line.
# !cut -d ',' -f1 config/comparison_full_set.csv | tail -n +2 > config/comparison_full_set-pmcids.csv

harvester = Harverster(config_path="config/config-harvester.json", dump_metadata=True)
# harvester.harvest_pmcids("config/comparison_full_set-pmcids.csv")

# Not clear to me if the resulting tei.xml files are used by the client?
# Running it is not idempotent, seems to repeat even if the tei.xml files are there?
# Also requires running: git clone https://github.com/kermitt2/Pub2TEI
# nlm2tei = Nlm2tei(config_path="config/config-harvester.json")
# nlm2tei.process()

client = software_mentions_client(config_path="config/config-client.json")
client.annotate_collection("./data", force=True)

harvester.diagnostic(full=True)

from pathlib import Path
import pandas as pd

all_paths = list(Path("./data").rglob("*.pdf"))
print("Number of PDF files:")
print(len(all_paths))
software_paths = list(Path("./data").rglob("*.software.json"))
print("Number of software.json files:")
print(len(software_paths))
