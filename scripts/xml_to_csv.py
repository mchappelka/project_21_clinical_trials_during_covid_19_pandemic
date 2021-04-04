# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 11:25:42 2021

@author: hpfla
"""

import os
from xml.etree import ElementTree
import pandas as pd
import numpy as np



data_path = "C:/Users/hpfla/OneDrive/Documents/DVRN/clinical_trials/code/project_21_clinical_trials_during_covid_19_pandemic"
in_path = os.path.join(data_path, "input", "raw")
out_path = os.path.join(data_path, "output")



xml_folder = os.path.join(in_path, "search_result")


xmlfiles = os.listdir(xml_folder)
  

# create a dataframe

dfs = []
print("Printing dsf")
print(dfs)

# columns
def create_col(df, col):
    if col not in df.columns:
        df[col] = "np.nan"
    #print("created {}".format(col))
    return df


class trialData:
    
    def __init__(self):
        self.dfs = []
    
    def add_row(self,
                study_id
                ,category,
                subcategory
                ,value
                ,title=[]
                ,design=[]
                ,group=[]
                

                ):
        
        
         df = pd.DataFrame(
                 columns=["study_id"

                          , "category",
                          "subcategory",
                          "value"
                         
                          ], 
                 index=range(1))
         
         df["study_id"] = study_id
         if len(title) > 0:
             df["title"] = title
         if len(design) > 0:
             df["type"] = design
         if len(group) > 0:
             df["group"] = group
         df["category"] = category
         df["subcategory"] = subcategory
         df["value"] = value
         self.dfs.append(df.copy())
                
         
    def getTrialData(self):
        return pd.concat(self.dfs)
    
trial_info_td = trialData()
group_info_td = trialData()


dict_list = [np.nan for file in xmlfiles]
for i,filename in enumerate(xmlfiles): 
    print("")
    print("")
    print(str(i) + ". " + filename)
    dom = ElementTree.parse(os.path.join(xml_folder, filename))
   
    #print(dom.find("brief_title").text)
    
    title = dom.find("brief_title").text
    study_type = dom.find("study_type").text
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
            trial_info_td.add_row(i, category, subcategory, category_value, title, study_type)
            


    for e in dom.find("study_design_info"):
            category = "study_design_info"
            subcategory = e.tag.lower()
            category_value = e.text
            trial_info_td.add_row(i, category, subcategory, category_value, title, study_type)

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
            group_info_td.add_row(study_id = i, 
                                  category = "milestone",  
                                  subcategory = milestone,
                                  value=p.attrib["count"],
                                  group=p.attrib["group_id"])
    try:
        for r in pflow.find("period_list/period/drop_withdraw_reason_list"):
            reason = r.find("title").text
            participants = r.find("participants_list")
            for p in participants:
                group_info_td.add_row(study_id = i, 
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
                    group_info_td.add_row(study_id = i, 
                                  category = "enrollment region",  
                                  subcategory = country_str,
                                  value=count.attrib["value"],
                                  group=count.attrib["group_id"])
        elif measure.find("title").text.lower() == "disease severity":
            for severity in measure.find("class_list"):
                for count in severity.find("category_list/category/measurement_list"):                              
                    group_info_td.add_row(study_id = i, 
                                  category = measure.find("title").text,  
                                  subcategory = severity.find("title").text,
                                  value=count.attrib["value"],
                                  group=count.attrib["group_id"])
        else:
            try:
                if measure.find("units").text.lower() == "participants":
                    for submeasure in measure.find("class_list/class/category_list"):

                        for count in submeasure.find("measurement_list"):                              
                            group_info_td.add_row(study_id = i, 
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
meta_df = meta_df.rename(columns=rename_dict)

merged_df = pd.merge(meta_df,group_df,on='study_id',how='outer')
merged_df = merged_df[["study_id", "title", "type", "enrollment_category",	
                       "enrollment_subcategory", "enrollment_value", "category",
                       "category", "group",	"group_description", "value"]]
merged_df.to_csv(os.path.join(out_path, "processed_trials_long.csv"))   



