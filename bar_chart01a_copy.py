"""
08 June 20i8
Using British Survey of Attitudes to try to create a bar chart for 2 categorical variables

"""
# import stuff here
import csv
import numpy
import matplotlib.pyplot as plt


# basic functions here
def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

# my own function here


def trimmed_dict2(base_dict, required_fields):
    """
    Idea:
    >function to trim any dict to just the (key:) borough codes and (values:) desired columns from the base dict
    Why?
    > to join the various dictionaries together with a common set of keys
    Input:
    > base_dict (e.g. population_dict) and required fields which is a list that defines the required fields
    >> the first item in the list becomes the key
    Output:
    > a trimmed dictionary of any desired columns
    """
    new_dict = {}
    for key, values in base_dict.items():
        sub_dict = {}
        for field in required_fields:
            if field in values.keys():
                sub_dict.update({field: values[field]})
        new_dict.update({key: sub_dict})
    return new_dict

# core function here for plotting 2 categorical variables


def catplot2(main_dict, x_field, no_x_categories, y_field, custom_title, custom_x_label):
    """
    a function to create a plot for 2 categorical variables
    Inputs:
    > x_field is a category such as age groups - a string
    > no_x_categories is the number of categories in x_field - a number
    > y_field is a binary no/yes category, e.g. are you worried about crime? - a string
    > base_dict is the dictionary that contains all the data
    Output:
    > a plot showing what %age of each x category is concerned about issue in y
    > the plotting will be done in matplotlib, as a bivariate categorical plotting is not well supported in seaborn, etc.
    """
    # create dictionaries that will be used for counting
    x_dict = {x: 0 for x in range(1, no_x_categories+1)}
    y_dict = {y: 0 for y in range(1, no_x_categories+1)}

    # the core of the function
    for entry in main_dict.values():
        if x_field in entry.keys():
            x_dict[int(entry[x_field])] += 1
            # <= needed to take out rogue numbers in data
            if 0 <= int(entry[y_field]) <= 1:
                y_dict[int(entry[x_field])] += int(entry[y_field])

    x_list = list(x_dict.values())  # <= these are raw counts
    y_list = list(y_dict.values())  # <= these are raw counts
    sum = 0
    for item in x_list:
        sum += item

    # want a list of percentages of y relative to x
    percent_list = []
    for idx in range(len(x_list)):
        if x_list[idx] != 0:
            percent_list.append(y_list[idx]/x_list[idx])
        else:
            percent_list.append(0)

    # now plotting
    if custom_x_label:
        category_list = custom_x_label
    else:
        category_list = [c for c in range(1, no_x_categories+1)]
    z_list = [1 for z in range(no_x_categories)]
    plt.rc('font', size=8)
    plt.bar(category_list, z_list, color="lightsteelblue")
    plt.bar(category_list, percent_list, color="mediumorchid")
    plt.xlabel(x_field)
    plt.ylabel("percentage " + y_field)
    plt.title(custom_title)
    plt.suptitle('British Social Attitudes Survey 2016', fontsize=11)
    plt.title(custom_title)
    plt.show()


# = = = test and develop below here = = =
bsa = '/Users/RAhmed/WesleyanMOOC/Course01/Week02/UKDA-8252-tab/bsa16_to_ukda.csv'
base_dict = read_csv_as_nested_dict(bsa, 'Sserial', separator=",", quote='"')
# used lines below to make a smaller dict, but this is not needed once it worls
# required_fields = ['RAgeCat', 'HEdQual', 'CrPCrim']
# bsa_dict = trimmed_dict2(base_dict, required_fields)

# variables for function. Use 'RAgeCat' (no_x_categories = 8) or 'HEdQual' (no_x_categories = 8)
# x_field = 'RAgeCat'
# no_x_categories = 8
# custom_x_label = ['18-24', '25-34', '35-44', '45-54', '55-59', '60-64', '65+', 'DK/Refused']
x_field = 'HEdQual'
no_x_categories = 8
custom_x_label = ['Degree', 'Higher Ed', 'A level',
                  'O level', 'CSE', 'Foreign', 'No qual+', 'DK/NA']
# x_field = 'GOR_ID'
# no_x_categories = 11
# custom_x_label = ['North East', 'North West', 'Y&H', 'E Midlands', 'W Midlands', 'East of Eng', 'London', 'S East', 'S west', 'Wales', 'Scotland']

y_field = 'CrPImm'
custom_title = "Percentage concern about immigration, by age\n"
# run function
# no need to to use the trimmed_dict2 function, can just use the whole original base_dict
catplot2(base_dict, x_field, no_x_categories, y_field, custom_title, custom_x_label)
