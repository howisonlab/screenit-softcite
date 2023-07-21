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

