from article_dataset_builder.harvest import Harverster
from software_mentions_client.client import software_mentions_client
import requests
import tqdm
from importlib.metadata import version

version('article_dataset_builder')
version('software_mentions_client')
version('lmdb')

harvester = Harverster(config_path="config/config-harvester.json", dump_metadata=True)
harvester.harvest_pmcids("config/comparison_full_set-pmcids.csv")

# Not clear to me if the resulting tei.xml files are used by the client?
# Running it is not idempotent, seems to repeat even if the tei.xml files are there?
# from article_dataset_builder.nlm2tei import Nlm2tei
# nlm2tei = Nlm2tei(config_path="./config/config-harvester.json")
# nlm2tei.process()

client = software_mentions_client(config_path="config/config-client.json")
client.annotate_collection("./data")

harvester.diagnostic(full=True)

from pathlib import Path
import pandas as pd

all_paths = list(Path("./data").rglob("*.pdf"))
print(len(all_paths))
software_paths = list(Path("./data").rglob("*.software.json"))

print(len(software_paths))