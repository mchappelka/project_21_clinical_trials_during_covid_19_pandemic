# -*- coding: utf-8 -*-

"""
Summary:
    It takes a input file that has a list of NCT trials and then outputs the
    needed columns as a csv file
Input:
    list of NCTs
Output
    CSV file containing the needed row for analysis for the selected NCTs
"""

import pandas as pd
import json

def grab_single_nct_json_from_whole_dump(nct_number, json_dump_dir = "../input/untracked/AllAPIJSON"):
	nct_dictionary = f"{json_dump_dir}/{nct_number[:7].upper()}xxxx/{nct_number.upper()}.json"
	try:
		with open(nct_dictionary,"r") as f:
			json_doc = json.load(f)
		return json_doc
	except:
		print(f"Current NCT file for {nct_number} is not found in the directory")

studies_input_base_dirname = "../input/raw/studies"
studies_input_file_basename = "covid19_20210225"
studies_input_fname = f"{studies_input_base_dirname}/{studies_input_file_basename}.csv"
df_input_studies = pd.read_csv(studies_input_fname, na_filter = False, dtype=str)

header = [
	"NCTId",
	"Gender",
	"MinimumAge",
	"BriefSummary",
	"DetailedDescription",
	]

df_output_studies = pd.DataFrame(columns =(header))

for nct_id in df_input_studies["NCT Number"]:
	current_nct_whole_doc = grab_single_nct_json_from_whole_dump(nct_id)
	## In case we did not get a json document we will keep the loop
	if not current_nct_whole_doc:
		print(f"Current NCT file for {nct_id} is not found in the directory")
		continue
	else:
		print(f"Adding NCT file for {nct_id} in the dataframe")
	current_nct_row_to_write = {}
	current_nct_row_to_write["NCTId"] = nct_id
	## It seems that in side each json there are two sections in the study
	## ['ProtocolSection', 'DerivedSection']

	## and there are 11 modules inside the ProtocolSection
	##['IdentificationModule', 'StatusModule', 'SponsorCollaboratorsModule', 'OversightModule', 'DescriptionModule', 'ConditionsModule', 'DesignModule', 'ArmsInterventionsModule', 'OutcomesModule', 'EligibilityModule', 'ContactsLocationsModule']

	## Before extractinge and writing to csv, always double check
	## whatever you are extracting is a list of items or a single item
	## If it is a list of items then you need to do some join when outputting
	## to the csv file


	## In some cases a key might noe exist in the document so you need to check 
	## whether the key exist or not.
	if "Gender" in current_nct_whole_doc["FullStudy"]["Study"]\
										["ProtocolSection"]["EligibilityModule"]:
		current_nct_row_to_write["Gender"] = current_nct_whole_doc["FullStudy"]["Study"]\
											["ProtocolSection"]["EligibilityModule"]["Gender"]
	else:
		current_nct_row_to_write["Gender"] = ""

	## In some cases a key might noe exist in the document so you need to check 
	## whether the key exist or not.
	if "MinimumAge" in current_nct_whole_doc["FullStudy"]["Study"]\
										["ProtocolSection"]["EligibilityModule"]:
		current_nct_row_to_write["MinimumAge"] = current_nct_whole_doc["FullStudy"]["Study"]\
											["ProtocolSection"]["EligibilityModule"]["MinimumAge"]
	else:
		current_nct_row_to_write["MinimumAge"] = ""

	current_nct_row_to_write["BriefSummary"] = current_nct_whole_doc["FullStudy"]["Study"]\
										["ProtocolSection"]["DescriptionModule"]["BriefSummary"]

	
	## In some cases a key might noe exist in the document so you need to check 
	## whether the key exist or not.
	if "DetailedDescription" in current_nct_whole_doc["FullStudy"]["Study"]\
										["ProtocolSection"]["DescriptionModule"]:
		current_nct_row_to_write["DetailedDescription"] = current_nct_whole_doc["FullStudy"]["Study"]\
											["ProtocolSection"]["DescriptionModule"]["DetailedDescription"]
	else:
		current_nct_row_to_write["DetailedDescription"] = ""

	df_output_studies = df_output_studies.append(current_nct_row_to_write, ignore_index=True)



studies_output_base_dirname = "../output/studies"
studies_output_file_basename = studies_input_file_basename
studies_ouput_fname = f"{studies_output_base_dirname}/{studies_output_file_basename}.csv"

df_output_studies.to_csv(studies_ouput_fname,index=False)