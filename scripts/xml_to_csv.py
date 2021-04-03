# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 11:25:42 2021

@author: hpfla
"""

import os
from xml.etree import ElementTree
import pandas as pd
import numpy as np




data_path = "C:/Users/hpfla/OneDrive/Documents/DVRN/clinical_trials/code/project_21_clinical_trials_during_covid_19_pandemic/input/raw"



xml_folder = os.path.join(data_path, "search_result")
json_folder = os.path.join(data_path, "json")

xmlfiles = os.listdir(xml_folder)
    

# create a dataframe
df = pd.DataFrame(columns=["Title"],index=range(len(xmlfiles)))

# columns
def create_col(df, col):
    if col not in df:
        df[col] = np.nan
        

for idx,filename in enumerate(xmlfiles): 
    print("")
    print("")
    print(str(idx) + ". " + filename)
    dom = ElementTree.parse(os.path.join(xml_folder, filename))
    
    #print(dom.find("brief_title").text)
    df.loc[idx]["Title"] = dom.find("brief_title").text
    for milestone in dom.find("clinical_results/participant_flow/period_list/period/milestone_list"):
        print(milestone.find("title").text)
        participants = milestone.find("participants_list")
        for p in participants:
            print(p.attrib["group_id"] + ": " + p.attrib["count"])
            
    try:
        for reason in dom.find("clinical_results/participant_flow/period_list/period/drop_withdraw_reason_list"):
            print(reason.find("title").text)
            participants = reason.find("participants_list")
            for p in participants:
                print(p.attrib["group_id"] + ": " + p.attrib["count"])
    except:
        print(f"Withdrawal reasons {filename} are not included")
        
    for measure in dom.find("clinical_results/baseline/measure_list"):
        print(" ")
        print(measure.find("title").text)
        if measure.find("title").text == "Region of Enrollment":
            for country in measure.find("class_list"):
                print(country.find("title").text)
                for count in country.find("category_list/category/measurement_list"):
                    print(count.attrib["group_id"] + ": " + count.attrib["value"])
        elif measure.find("title").text.lower() == "disease severity":
            print("come back to this later")
        else:
            try:
                if measure.find("units").text.lower() == "participants":
                    for submeasure in measure.find("class_list/class/category_list"):
                            print(submeasure.find("title").text)
                            for count in submeasure.find("measurement_list"):
                                print(count.attrib["group_id"] + ": " + count.attrib["value"])
            except: 
                print(measure.find("title").text)