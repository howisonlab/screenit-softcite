# Workflow for ScreenIT usign softcite

To enable comparisons of software mention extraction, we have a shared list of DOIs:

This repo uses that shared list of PMCIDs, runs a full crawl, grobid conversion, extraction, and an export to a csv file (one row per mention).

The repo is setup to run via docker-compose:

```
docker-compose up
```

The software-mention server is run (from a docker image) and listens on port 8060.

The software-mention client is built using the Dockerfile.  Connect to the software-mention client using:

```
docker exec -it client_software_mentions /bin/bash   
```

Run the pipeline with:

```
cd workspaces
python3 screen_it_pipeline.py
```

The `.devcontainer` folder also contains a setup that works using dev containers on vscode.
