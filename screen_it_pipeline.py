from article_dataset_builder.harvest import Harverster
from article_dataset_builder.nlm2tei import Nlm2tei
from software_mentions_client.client import software_mentions_client
import requests
import tqdm
from importlib.metadata import version

version('article_dataset_builder')
version('software_mentions_client')
version('lmdb')

harvester = Harverster(config_path="config/config-harvester.json", dump_metadata=True)
harvester.harvest_pmcids("config/comparison_full_set-pmcids.csv")

nlm2tei = Nlm2tei(config_path="config/config-harvester.json")
nlm2tei.process()

client = software_mentions_client(config_path="config/config-client.json")
client.annotate_collection("./data", force=True)

