"""
 Data wrangling for this project.
 DATA SOURCE FILES are given in code book. They have been downloaded and stored locally.
 REPLICATING THIS?: Need to add your own correct file paths and file names.

"""
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# utility functions for data wrangling


def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Lists of lists consisting of the fields in the CSV file
    """

    with open(file_name, newline='') as csv_file:  # don't need to explicitly close the file now
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def write_csv_file(csv_table, file_name):
    """
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)


def has_these_col_variables(data_file, category_list, position_of_index):
    """
    Idea:
    > Creates a list of the actual indices you want, from a large csv file that has numerous indices
    including many you do not want
    > With this list you can compare a number of csv files to see whether they have the same indices
   NOTE:
    > Will need the categories_list entries to be actual variables responses
    Why?:
    > Use this list of indices for making data files that only have the data you want
    Input:
    > data_file: a (large) csv file of data with a header row. (String)
    > category_list: a list of the variables by which you want to select your subset of data. (List of strings)
    > position_of_index: the numerical position in each row that has the index you wish to list. (Integer)
    Output:
    > A list of strings that has the indices you want
    Mutates input?:
    > No
    """
    output_list = []
    for row in data_file:
        index = 0
        for category in category_list:
            if category in row:
                index += 1
        if index == len(category_list):
            output_list.append(row[position_of_index])
    return output_list


def simple_get_desired_indices(data_file, position_of_index):
    """
    Idea:
    > Creates a list of the actual indices you want, from a large csv file that has numerous indices
    including many you do not want
    > With this list you can compare a number of csv files to see whether they have the same indices
   NOTE:
    > Will need the categories_list entries to be actual variables responses
    Why?:
    > Use this list of indices for making data files that only have the data you want
    Input:
    > data_file: a (large) csv file of data with a header row. (String)
    > position_of_index: the numerical position in each row that has the index you wish to list. (Integer)
    > rows_to_pop: the number of leading/header rows to pop in the output_list, to just get list of indices
    Output:
    > A list of strings that has the indices you want
    Mutates input?:
    > No
    """
    output_list = []
    for row in data_file:
        output_list.append(row[position_of_index])
    # you also have header value that has to be removed
    output_list.pop(0)
    return output_list


def has_these_row_variables(data_file, category_list, input_index, output_index):
    """
        Idea:
        > Creates a list of the actual indices you want, from a large csv file that has numerous indices
        including many you do not want
        > Here, the item in the category list may or may not be in the row
        > With this list you can compare a number of csv files to see whether they have the same indices
       NOTE:
        > Will need the categories_list entries to be actual variables responses
        Why?:
        > Use this list of indices for making data files that only have the data you want
        Input:
        > data_file: a (large) csv file of data with a header row. (String)
        > category_list: a list of the variables by which you want to select your subset of data. (List of strings)
        > position_of_index: the numerical position in each row that has the index you wish to list. (Integer)
        Output:
        > A list of strings that has the indices you want
        Mutates input?:
        > No
        """
    output_list = []
    for row in data_file:
        if row[input_index] in category_list:
            output_list.append(row[output_index])
    return output_list


def cat_and_years_only(data_file, responses_list):
    """
    Idea:
    > Creates a file only of the actual observations you want, from a large csv file that has numerous observations
    including many you do not want
    Why?:
    > This file is easier to manage than (e.g.) a 100,000 observation file, 99% of which you don't care about
   NOTE:
    > Will need the categories_list entries to be responses you want

    Input:
    > data_file: a (large) csv file of data with a header row. (String)
    > category_list: a list of the variables by which you want to select your subset of data. (List of strings)
    Output:
    > A much smaller file?
    Mutates input?:
    > No
    """
    header = data_file[0]
    output_list = []
    for row in data_file:
        index = 0
        for response in responses_list:
            if response in row:
                index += 1
        if index == len(responses_list):
            output_list.append(row)
    # put back header
    output_list.insert(0, header)
    return output_list


# = = = data wrangling below here = = =
# STEP 1: check same local authority data in each file
print("\nStep 1")
# get huge csv file with all UK childhood obesity data,
filename = '/Users/RAhmed/data store/NCMPLocalAuthorityProfile-DistrictUA.data.csv'
data_file = read_csv_file(filename)

# get correct local authority indices in 2015/16 for the 'Prevalence of obesity' category for 4-5 year olds
category_list = ['Reception: Prevalence of obesity', 'District & UA', '4-5 yrs', '2015/16']
list_2015_45 = has_these_col_variables(data_file, category_list, 4)
print("Number of local authorities in obesity data for 4-5-year olds:", len(list_2015_45))

# get correct local authority indices in 2015/16 for the 'Prevalence of obesity' category for 10-11 year olds
category_list = [
    'Year 6: Prevalence of overweight (including obese)', 'District & UA', '10-11 yrs', '2015/16']
list_2015_1011 = has_these_col_variables(data_file, category_list, 4)
print("Number of local authorities in obesity data for 10-11-year olds:", len(list_2015_1011))

# check that the data for 4-5-year olds and 10-11-year olds is for same local authorities. If so result is True
print("Obesity data for 4-5-year olds is same as for 10-11-year olds?:",
      list_2015_45.sort() == list_2015_1011.sort())

# get csv file with UK local authority deprivation data (IMD).
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/IMD.csv'
data_file = read_csv_file(filename)
# Check same local authorities with IMD data as for childhood obesity data. If so result is True
list_2015_IMD = simple_get_desired_indices(data_file, 0)
print("Number of local authorities in IMD data:", len(list_2015_IMD))
# check that the data IMD is for same local authorities.If so result is True
print("Local authorities in IMD files same as for obesity data?:",
      list_2015_IMD.sort() == list_2015_1011.sort())

# get csv file with UK local authority household gross domestic income per head (GDHIph).
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/2015_LA_GDHI_perhead.csv'
data_file = read_csv_file(filename)

# Check same local authorities with GDHIph data as for childhood obesity data. If so result is True
category_list = ['North East', 'North West', 'Yorkshire and The Humber', 'East Midlands',
                 'West Midlands', 'East of England', 'London', 'South East', 'South West']
list_2015_GDHIph = has_these_row_variables(data_file, category_list, 0, 1)
print("Number of local authorities in GDHI data:", len(list_2015_GDHIph))
# check that the data IMD is for same local authorities.If so result is True
print("Local authorities in GDHI file same as for obesity data?:",
      list_2015_GDHIph.sort() == list_2015_1011.sort())

# STEP 2: need to pare down the multi-year, nearly 100,000 entries for childhood obesity data to just the
# two categories (4-5-year olds, 10-11-year olds) I want for the given year.
# Needs a dedicated function called cat_and_years_only
print("\nStep 2")
# for 4-5-year olds
filename = '/Users/RAhmed/data store/NCMPLocalAuthorityProfile-DistrictUA.data.csv'
data_file = read_csv_file(filename)
# the following responses will get the observations you need for 4-5-year olds
responses_list = ['Reception: Prevalence of obesity', 'District & UA', '4-5 yrs', '2015/16']
obesity_45 = cat_and_years_only(data_file, responses_list)
print("Visual check of file below:")
print(obesity_45[:2])  # <= visually check content
# <= check correct length. (Subtract 1 due to header)
print("Number of local authorities in new file for 4-5-year old data:", len(obesity_45) - 1)
# write to a permanent file
write_csv_file(obesity_45, '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/obesity_45.csv')

# for 10-11-year olds
# the following responses will get the observations you need for 10-11-year olds
responses_list = ['Year 6: Prevalence of obesity', 'District & UA', '10-11 yrs', '2015/16']
obesity_1011 = cat_and_years_only(data_file, responses_list)
print("Visual check of file below:")
print(obesity_1011[:2])  # <= visually check content
# <= check correct length. (Subtract 1 due to header)
print("Number of local authorities in new file for 10-11-year old data:", len(obesity_1011) - 1)
# write to a permanent file
write_csv_file(obesity_1011, '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/obesity_1011.csv')


# STEP 3: harmonise name of key local authority index across all files. Use name given in (both) obesity_45 & obesity_1011
print("\nStep 3")
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/obesity_1011.csv'
data_file = read_csv_file(filename)
common_index_name = data_file[0][4]
print("Common index name will be this: ", common_index_name)
# this checks header, gives name in correct location and checks, for IMD data
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/IMD.csv'
data_file = read_csv_file(filename)
data_file[0][0] = common_index_name
newname = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/IMD_CI.csv'
write_csv_file(data_file, newname)
# this checks header, gives name in correct location and checks, for GDHI data
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/2015_LA_GDHI_perhead.csv'
data_file = read_csv_file(filename)
data_file[0][1] = common_index_name
newname = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/2015_LA_GDHI_perhead_CI.csv'
write_csv_file(data_file, newname)

# STEP 4: for 4-5-year olds, import obesity data in pandas and only keep the variables I want
# and merge with IMD and GHDI data
print("\nStep 4")
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/obesity_45.csv'
df = pd.read_csv(filename, low_memory=False)
df45 = df[['Area Code', 'Parent Name', 'Area Name', 'Value']]

filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/IMD_CI.csv'
df = pd.read_csv(filename, low_memory=False)
dfIMD = df[['Area Code', 'IMD - Average score',
            'IMD - Proportion of LSOAs in most deprived 10% nationally']]

filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/2015_LA_GDHI_perhead_CI.csv'
df = pd.read_csv(filename, low_memory=False)
dfGDHI = df[['Area Code', '2015']]

df45 = pd.merge(df45, dfIMD, on='Area Code')
df45 = pd.merge(df45, dfGDHI, on='Area Code')

# rename some header titles
df45 = df45.rename({'Value': 'Obesity proportion', '2015': 'GDHI'}, axis='columns')


# STEP 5: for 10-11-year olds, do as for 4-5-year olds
print("\nStep 5")
filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/obesity_1011.csv'
df = pd.read_csv(filename, low_memory=False)
df1011 = df[['Area Code', 'Parent Name', 'Area Name', 'Value']]

filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/IMD_CI.csv'
df = pd.read_csv(filename, low_memory=False)
dfIMD = df[['Area Code', 'IMD - Average score',
            'IMD - Proportion of LSOAs in most deprived 10% nationally']]

filename = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/2015_LA_GDHI_perhead_CI.csv'
df = pd.read_csv(filename, low_memory=False)
dfGDHI = df[['Area Code', '2015']]

df1011 = pd.merge(df1011, dfIMD, on='Area Code')
df1011 = pd.merge(df1011, dfGDHI, on='Area Code')

# rename some header titles
df1011 = df1011.rename({'Value': 'Obesity proportion', '2015': 'GDHI'}, axis='columns')


# Progress check: ^^^ so to now you have a dataframe for 4-5-year old obesity and for 10-11-year old obesity
# Each has obesity data merged with IMD data and GDHI data

# STEP 6: for dataframe 4-5-year olds, merge the other social deprivation data in an automated way
print("\nStep 6")
pathname = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/'
file_list = ['Income.csv', 'Income Deprivation Affecting Children Index (IDACI).csv', 'Employment.csv', 'Education, Skills and Training.csv',
             'Health Deprivation and Disability.csv', 'Crime.csv', 'Barriers to Housing and Services.csv', 'Living Environment.csv']
for file in file_list:
    filename = pathname + file
    df = pd.read_csv(filename, low_memory=False)
    # Need to standardise index name in all social deprivation index files to 'Area Code'
    df = df.rename({'Local Authority District code (2013)': 'Area Code'}, axis='columns')
    var_base = file.split(".")[0]
    var_1 = var_base + ' - Average score'
    var_2 = var_base + ' - Proportion of LSOAs in most deprived 10% nationally'
    df = df[['Area Code', var_1, var_2]]
    df45 = pd.merge(df45, df, on='Area Code')
    df1011 = pd.merge(df1011, df, on='Area Code')
#

print("Visually check df45:\n", df45.head(2))
print("Visually check df1011:\n", df1011.head(2))

# STEP 7: shorten name of Parent Name entries, as too long for plotting (delete ' region')
# Also, change Parent Name to Region
# Also, shorten Yorkshire and the Humber
print("\nStep 7")
df45['Parent Name'] = df45['Parent Name'].map(lambda x: str(x)[:-7])
df45 = df45.rename({'Parent Name': 'Region'}, axis='columns')

df1011['Parent Name'] = df1011['Parent Name'].map(lambda x: str(x)[:-7])
df1011 = df1011.rename({'Parent Name': 'Region'}, axis='columns')

df45 = df45.replace(to_replace='Yorkshire and the Humber', value='Yorks and Humber')
df1011 = df1011.replace(to_replace='Yorkshire and the Humber', value='Yorks and Humber')

# STEP 8: for df45 and df1011, write dataframes to a csv file that will be used in the study
print("\nStep 8")
newname45 = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/study_data45.csv'
df45.to_csv(newname45, index=False)
newname1011 = '/Users/RAhmed/WesleyanMOOC/W_data_store/csv_files/study_data1011.csv'
df1011.to_csv(newname1011, index=False)
