MCloud
==========
Code for the MCloud project

Workflow:
1. Get data through Opeb Data API
2. Analyze the data (thru schema matching, etc)
3. Recommend computing jobs

==========

ny_dump.py dumps the metadata of all the data sets on the NY Open Data site, and output each data set as a seprate line in ny_dump (the file will be overriden each time the script is run). 
The script will output the result (success or failure code) for each data set while dumping).
Each lines contains the following info sequentially:
1-publishing agency
2-data set name
3-data set description
4-data set category (mapping is showed below)
5-data set url id (each data set has a unique id for access)
6-field names (basically, the "column names")

ny_dump is the source input for all the demo and analysis code.

==========

Category mapping:
'Recreation': 1, 
'Transportation': 2, 
'Business': 3, 
'Public-Safety': 4, 
'Social-Services': 5, 
'Environment': 6, 
'Health': 7, 
'City-Government': 8, 
'Education': 9, 
'Housing-Development': 10

==========

api.py shows a one-off result of the schema matching: one random data set from the NY open data set list will be chosen as the target, and do the schema matching from the rest sets.
The output are 5 most matched data set with info printed including distance (as a similarity score, lower is closer) and the details of the matched data sets.

==========

clf.py run the schema matching, analyze the accuracy and output a confusion matrix

==========

demo.py runs interactively to show the schema matching results. The user is presented with the info of 10 randomly picked data sets and is asked to input several column names (or fileds) of their own data set.
The script will match a most similar one from the 10 candidates, outputting the changes mneeded to make to match perfectly with the target data set.
