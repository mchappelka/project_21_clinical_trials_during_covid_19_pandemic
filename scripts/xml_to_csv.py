
import os
from xml.etree import ElementTree
import pandas as pd
import numpy as np

import trialDataObject as tdo



data_path = "C:/Users/hpfla/OneDrive/Documents/DVRN/clinical_trials/code/project_21_clinical_trials_during_covid_19_pandemic"
in_path = os.path.join(data_path, "input", "raw")
out_path = os.path.join(data_path, "output")



xml_folder = os.path.join(in_path, "search_result")
xmlfiles = os.listdir(xml_folder)
  

trial_info_td = tdo.trialDataObject()
group_info_td = tdo.trialDataObject()


dict_list = [np.nan for file in xmlfiles]
for i,filename in enumerate(xmlfiles): 
    print("")
    print("")
    print(str(i) + ". " + filename)
    dom = ElementTree.parse(os.path.join(xml_folder, filename))
   
    #print(dom.find("brief_title").text)
    
    title = dom.find("brief_title").text
    study_type = dom.find("study_type").text

    optional_cols_dict = {
        "start_date" : dom.find("start_date").text
        ,"completion_date" : dom.find("completion_date").text
        ,"primary_completion_date" : dom.find("primary_completion_date").text
        ,"study_type" : dom.find("study_type").text
        ,"sponsor" : dom.find("sponsors/lead_sponsor/agency").text
        ,"is_fda_regulated_drug" : dom.find("oversight_info/is_fda_regulated_drug").text

        }
        
    
    try: 
        detailed_description = dom.find("detailed_description/textblock").text.strip()
    except: 
        print("optional detailed description not included")
    
    pflow = dom.find("clinical_results/participant_flow")
    
    
    for e in dom.find("eligibility"):
        if e.tag != "criteria": # because this contains paragraphs which is too much info
            category = "eligibility"
            subcategory = e.tag.lower()
            category_value = e.text
            trial_info_td.addRow(i, category, subcategory, category_value, title, study_type, optional_cols_dict=optional_cols_dict)
            


    for e in dom.find("study_design_info"):
            category = "study_design_info"
            subcategory = e.tag.lower()
            category_value = e.text
            trial_info_td.addRow(i, category, subcategory, category_value, title, study_type, optional_cols_dict=optional_cols_dict)

    pflow = dom.find("clinical_results/participant_flow")
        
    study_dict = {}
    for g in pflow.find("group_list"):
        study_dict[g.attrib["group_id"]] = g.find("title").text
        
    for g in dom.find("clinical_results/baseline/group_list"):
        study_dict[g.attrib["group_id"]] = g.find("title").text
    
    dict_list[i] = study_dict
        
    
    for m in pflow.find("period_list/period/milestone_list"):
        milestone = m.find("title").text
        #print(milestone)
        participants = m.find("participants_list")
        for p in participants:
            group_info_td.addRow(study_id = i, 
                                  category = "milestone",  
                                  subcategory = milestone,
                                  value=p.attrib["count"],
                                  group=p.attrib["group_id"])
    try:
        for r in pflow.find("period_list/period/drop_withdraw_reason_list"):
            reason = r.find("title").text
            participants = r.find("participants_list")
            for p in participants:
                group_info_td.addRow(study_id = i, 
                                  category = "withdrawal reason",  
                                  subcategory = reason,
                                  value=p.attrib["count"],
                                  group=p.attrib["group_id"])
    except:
        print(f"Withdrawal reasons {filename} are not included")
        

    
    for measure in dom.find("clinical_results/baseline/measure_list"):

        if measure.find("title").text == "Region of Enrollment":
            for country in measure.find("class_list"):
                country_str = country.find("title").text

                for count in country.find("category_list/category/measurement_list"):                    
                    group_info_td.addRow(study_id = i, 
                                  category = "enrollment region",  
                                  subcategory = country_str,
                                  value=count.attrib["value"],
                                  group=count.attrib["group_id"])
        elif measure.find("title").text.lower() == "disease severity":
            for severity in measure.find("class_list"):
                for count in severity.find("category_list/category/measurement_list"):                              
                    group_info_td.addRow(study_id = i, 
                                  category = measure.find("title").text,  
                                  subcategory = severity.find("title").text,
                                  value=count.attrib["value"],
                                  group=count.attrib["group_id"])
        else:
            try:
                if measure.find("units").text.lower() == "participants":
                    for submeasure in measure.find("class_list/class/category_list"):

                        for count in submeasure.find("measurement_list"):                              
                            group_info_td.addRow(study_id = i, 
                                  category = measure.find("title").text.lower(),  
                                  subcategory = submeasure.find("title").text,
                                  value=count.attrib["value"],
                                  group=count.attrib["group_id"])
            except: 
                print(measure.find("title").text)


group_df = group_info_td.getTrialData()


for i in range(0, len(dict_list)):
    d = dict_list[i]
    group_df.loc[group_df.study_id == i, "group_description"] = group_df[group_df.study_id == i]["group"].replace(d)

group_df['group'].str.replace('B','P')

# rename columsn before merging    
meta_df = trial_info_td.getTrialData()
rename_dict = {"category":"enrollment_category",
               "subcategory":"enrollment_subcategory",
               "value":"enrollment_value"}
meta_df.to_csv(os.path.join(out_path, "processed_trials_long_design.csv"))  
group_df.to_csv(os.path.join(out_path, "processed_trials_long_arm_counts.csv"))  

meta_df = meta_df.rename(columns=rename_dict)

merged_df = pd.merge(meta_df,group_df,on='study_id',how='outer')
merged_df = merged_df[["study_id", "title", "start_date",	"completion_date",	"primary_completion_date",	"study_type",	"sponsor",	"is_fda_regulated_drug"
,"type", "enrollment_category",	
                       "enrollment_subcategory", "enrollment_value", "category",
                       "category", "group",	"group_description", "value"]]
merged_df.to_csv(os.path.join(out_path, "processed_trials_long.csv"))   