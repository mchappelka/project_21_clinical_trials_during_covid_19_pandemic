# An exploration of covid-19 clinical trials during the pandemic

### Gathering the raw json data of all clinical trials:
A dump of all the clinical trials registered in clinicaltrials.gov can be found [in this link](https://clinicaltrials.gov/api/gui/ref/download_all), both in [xml format](https://ClinicalTrials.gov/AllAPIXML.zip) ([xml schema](https://clinicaltrials.gov/api/info/study_structure?fmt=XML)) and [json format](https://ClinicalTrials.gov/AllAPIJSON.zip) ([json schema](https://clinicaltrials.gov/api/info/study_structure?fmt=JSON)). The dataset size is around 1.6GB for xml format and 1.8GB for json format (as of February 17, 2021)

Preferably save it in `./input/untracked/`.

### Creating a target list of studies from clinical trials website:
The target list of covid-19 trials can generated using the follwoing steps:
- First search for a keyword
- Then the search results can be downloaded as csv from the Download url found in the top right corner, just beside "Subscribe to RSS".
- Before downloading the results as csv, make sure to click "Show/Hide Columns" and "NCT Number as a column".
