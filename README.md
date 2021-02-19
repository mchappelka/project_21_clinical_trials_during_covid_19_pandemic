# An exploration of covid-19 clinical trials during the pandemic

### Gathering the data
A dump of all the clinical trials registered in clinicaltrials.gov can be found [in this link](https://clinicaltrials.gov/api/gui/ref/download_all), both in [xml format](https://ClinicalTrials.gov/AllAPIXML.zip) ([xml schema](https://clinicaltrials.gov/api/info/study_structure?fmt=XML)) and [json format](https://ClinicalTrials.gov/AllAPIJSON.zip) ([json schema](https://clinicaltrials.gov/api/info/study_structure?fmt=JSON)). The dataset size is around 1.6GB for xml format and 1.8GB for json format (as of February 17, 2021)

The list of covid-19 trials can generated using the follwoing steps:
