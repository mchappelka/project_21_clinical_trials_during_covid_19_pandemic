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
        

for idx,filename in enumerate(xmlfiles): 
    print("")
    print("")
    print(str(idx) + ". " + filename)
    dom = ElementTree.parse(os.path.join(xml_folder, filename))
    mydf = pd.DataFrame(columns=["Title", "Study type",	
                                 "Detailed Description",	
                                 "gender",	
                                 "minimum_age",	
                                 "maximum_age",	
                                 "healthy_volunteers",	
                                 "allocation",
                                 "intervention_model",	
                                 "primary_purpose"	,
                                 "masking"	,
                                 "P1"	,
                                 "P2",
                                 "P3"	,
                                 "P4",
                                 "P5"	,
                                 "P6",
],index=range(1))
    #print(dom.find("brief_title").text)
    mydf["Title"] = dom.find("brief_title").text
    mydf["Study type"] = dom.find("study_type").text
    try: 
        mydf["Detailed Description"] = dom.find("detailed_description/textblock").text.strip()
    except: 
        print("optional detailed description not included")
    
    for e in dom.find("eligibility"):
        if e.tag != "criteria": # because this contains paragraphs which is too much info
            print(e.tag)
            newcol = e.tag.lower()
            count = e.text
            mydf = create_col(mydf, newcol)
            mydf[newcol] = count
    for i in dom.find("study_design_info"):
            newcol = i.tag.lower()
            count = i.text
            mydf = create_col(mydf, newcol)
            mydf[newcol] = count
            
    pflow = dom.find("clinical_results/participant_flow")
    
    for g in pflow.find("group_list"):
        newcol = g.attrib["group_id"]
        count = g.find("title").text
        mydf = create_col(mydf, newcol)
        mydf[newcol] = count
    for m in pflow.find("period_list/period/milestone_list"):
        milestone = m.find("title").text
        #print(milestone)
        participants = m.find("participants_list")
        for p in participants:
            newcol = (milestone + p.attrib["group_id"]).lower()
            count = p.attrib["count"]
            mydf = create_col(mydf, newcol)
            mydf[newcol] = count
    try:
        for r in pflow.find("period_list/period/drop_withdraw_reason_list"):
            reason = r.find("title").text
            participants = r.find("participants_list")
            for p in participants:
                #print(p.attrib["group_id"] + ": " + p.attrib["count"])
                newcol = (reason + p.attrib["group_id"]).lower()
                count = p.attrib["count"]
                mydf = create_col(mydf, newcol)
                mydf[newcol] = count
    except:
        print(f"Withdrawal reasons {filename} are not included")
        

    
    for measure in dom.find("clinical_results/baseline/measure_list"):
        print(" ")
        print(measure.find("title").text)
        if measure.find("title").text == "Region of Enrollment":
            for country in measure.find("class_list"):
                country_str = country.find("title").text
                print(country.find("title").text)
                for count in country.find("category_list/category/measurement_list"):
                    print(count.attrib["group_id"] + ": " + count.attrib["value"])
                    newcol = (country_str + count.attrib["group_id"]).lower()
                    count = count.attrib["value"]
                    mydf = create_col(mydf, newcol)
                    mydf[newcol] = count
        elif measure.find("title").text.lower() == "disease severity":
            print("come back to this later")
        else:
            try:
                if measure.find("units").text.lower() == "participants":
                    for submeasure in measure.find("class_list/class/category_list"):
                            print(submeasure.find("title").text)
                            for count in submeasure.find("measurement_list"):
                                print(count.attrib["group_id"] + ": " + count.attrib["value"])
                                newcol = submeasure.find("title").text + count.attrib["group_id"].lower()
                                count = count.attrib["value"]
                                mydf = create_col(mydf, newcol)
                                mydf[newcol] = count
            except: 
                print(measure.find("title").text)
    dfs.append(mydf.copy())


final_df = pd.concat(dfs)
print(final_df.columns)

final_df.to_csv(os.path.join(out_path, "processed_trials.csv"))