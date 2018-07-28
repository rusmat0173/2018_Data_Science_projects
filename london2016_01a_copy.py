"""
Practice project for graphing London stuff
Years vary slightly between datasets, but are around 2016

"""
import csv
import math
import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# change matplotlib font size
mpl.rcParams.update({'font.size': 8})

deprivation_info = {'deprivation_file': '/Users/RAhmed/PycharmProjects/2018_June_London/ID_2015_for_London.csv',
                    'keyfield': 'Local Authority District code (2013)',
                    'maindata': 'IMD - Average score',
                    'separator': ',',
                    'quote': "'"
                    }

obesity_info = {'obesity_file': '/Users/RAhmed/PycharmProjects/2018_June_London/EDI_measures_24_May_2018.csv',
                'keyfield': 'Borough',
                'maindata': 'Percentage of adults (aged 18+) classified as overweight or obese',
                'separator': ',',
                'quote': '"'
                }

population_info = {'population_file': '/Users/RAhmed/PycharmProjects/2018_June_London/london_borough_profiles.csv',
                   'keyfield': 'New code',
                   'maindata': 'GLA Population Estimate 2017',
                   'separator': ',',
                   'quote': '"'
                   }

education_info = {'education_file': '/Users/RAhmed/PycharmProjects/2018_June_London/Qualifications_of_working_age_NVQ4.csv',
                  'keyfield': 'Code',
                  'maindata': 'percent',
                  'separator': ',',
                  'quote': '"'
                  }

# useful functions


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


# make dictionaries for each data_set
deprivation_dict = read_csv_as_nested_dict(
    deprivation_info['deprivation_file'], deprivation_info['keyfield'], deprivation_info['separator'], deprivation_info['quote'])
obesity_dict = read_csv_as_nested_dict(
    obesity_info['obesity_file'], obesity_info['keyfield'], obesity_info['separator'], obesity_info['quote'])
population_dict = read_csv_as_nested_dict(
    population_info['population_file'], population_info['keyfield'], population_info['separator'], population_info['quote'])
education_dict = read_csv_as_nested_dict(
    education_info['education_file'], education_info['keyfield'], education_info['separator'], education_info['quote'])

# make a keyfield converter. Base on population_dict, and also on obesity_dict. Will need to check if 2nd one matches first
converter = {}
for item in population_dict.values():
    converter.update({item['New code']: item['Area name']})
# check whether names are same in obesity dict
for key in obesity_dict.keys():
    all_match = True
    if key not in converter.values():
        print(key, "not in converter")
        all_match = False
print("all converter items match:", all_match)
print("converter", converter, "\n")

# function to trim dictionaries to just what we want
# reason this is not more code-efficient is that trying to get items from a dictionary of dictionaries,
#     not a simple dictionary dictionary


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


# function to join base dict and any other dicts with same keys
def add_dict_cols(base_dict, join_dicts_list):
    """
    Idea:
    >function to join a base_dict to other dicts with same keys for common boroughs
    Why?
    > to do matplotlib analysis later
    Input:
    > base_dict (e.g. population_dict)
    > other_dicts is a list of other dicts to join, all need to have same outer keys
    Output:
    > a larger dictionary of all the desired columns/data
    """
    output_dict = dict(base_dict)
    for join_dict in join_dicts_list:
        for key, values in join_dict.items():
            if key in output_dict.keys():
                output_dict[key].update(values)
    return output_dict

# function to create colour map, adapted from Scripting Course 4, Week 4 practice project


def create_education_map(colormap):
    """
    largely used model answer provided in Rice MOOC:
        Initialize the colormap "jet" from matplotlib, <= RA I changed this
        Return function that takes risk and returns RGB color for use with scatter() in matplotlib
        # Note that this code is tricky - remember to return a lambda expression
    """
    # this max/min risk numbers are from visual inspection of Excel table
    edu_max = 87
    edu_min = 28

    # not surprisingly, model answer turns these to logs
    log_edu_max = math.log(edu_max, 10)  # maximum cancer risk in table
    log_edu_min = math.log(edu_min, 10)  # minimum cancer risk in table

    color_norm = mpl.colors.Normalize(vmin=log_edu_min, vmax=log_edu_max)
    color_mapper = mpl.cm.ScalarMappable(norm=color_norm, cmap=colormap)
    return lambda educolour: color_mapper.to_rgba(math.log(educolour, 10))


# = = = work and devpt. under here = = =

# create dictionaries to join
base_dict = trimmed_dict2(population_dict, ['Area name', 'GLA Population Estimate 2017'])
print("base_dict", base_dict)

short_edu_dict = trimmed_dict2(education_dict, ['percent'])
print("short_edu_dict", short_edu_dict)

short_deprivation_dict = trimmed_dict2(deprivation_dict, ['IMD - Average score'])
print("short_deprivation_dict", short_deprivation_dict)

# the obesity dict needs converting to use numerical codes like the others, for ease of joining together
converted_obesity_dict = {}
for key, values in converter.items():
    converted_obesity_dict.update({key: obesity_dict[values]})
short_obesity_dict = trimmed_dict2(
    converted_obesity_dict, ['Percentage of adults (aged 18+) classified as overweight or obese'])
print("short_obesity_dict", short_obesity_dict)


# next add other dictionaries' wanted items
print()
join_dicts_list = [short_edu_dict, short_deprivation_dict, short_obesity_dict]
master_dict = add_dict_cols(base_dict, join_dicts_list)
print("master_dict", master_dict)

# create plot from master_dict, by row


def print_stuff(master_dict, plot_fields):
    edu_colours_map = create_education_map(mpl.cm.RdYlGn)
    for key, values in master_dict.items():
        if plot_fields[0] in values:
            x = 100 * float(values[plot_fields[0]])
        if plot_fields[1] in values:
            y = float(values[plot_fields[1]])
        if plot_fields[2] in values:
            size = (float(values[plot_fields[2]]))*0.005
        if plot_fields[-1] in values:
            Label = values[plot_fields[-1]]
        plt.scatter(x, y, label=Label, c=edu_colours_map(
            float(values[plot_fields[3]])), s=size)  # <= s is size
        plt.annotate(values[plot_fields[-1]], (x, y))
    plt.xlabel(plot_fields[0])
    plt.ylabel(plot_fields[1])
    plt.suptitle('Social factors in London', fontsize=10)
    plt.title('including educational achievement and borough size\n')
    # plt.legend()

    plt.show()


plot_fields = ['Percentage of adults (aged 18+) classified as overweight or obese',
               'IMD - Average score', 'GLA Population Estimate 2017', 'percent', 'Area name']
X01 = print_stuff(master_dict, plot_fields)
print(X01)

print_stuff(master_dict, plot_fields)
print(population_dict)
