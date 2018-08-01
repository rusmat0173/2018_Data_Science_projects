"""
files from here

Updates:
> Originally did as a list of lists, but sorting is much better with a list of dictionaries, so will convert
> Cleaned up data to remove notes & sort by int(str)
> Needed to right justify all the columns printed tables
> Added function print_named_cols to only print (e.g.) 2 columns
> Added merge other data files (data files for population and GDP)
> Create some composite statistics

Sequence:
Dictionary of two-letter country_codes:
1. use read_csv_file function
2. remove brackets around two-letter codes
3. turn code-country pair into dictionary

Raw data to csv file to table:
1. Some work in Excel to save tab-delimited data to a good csv type
2. create table using read_csv_file
3. clean  data in each row of table (custom function for this data, clean_ord_dict)
4. sort high or low by year (sort_by_year)
5. print all (list_of_dictionaries_as_table) or selected columns(print_named_cols)

"""
import csv
from collections import OrderedDict

# read and write functions


def write_csv_file(csv_table, file_name):
    """
    USED FROM RICE MOOC - thank you!
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)


def read_csv_file(file_name):
    """
    USED FROM RICE MOOC - thank you!
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """
    with open(file_name, 'rt', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        table = []
        for row in csv_reader:
            table.append(row)
    return table


def dictreader_csv_file(filename, separator, quote):
    table = []
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


# functions for cleaning the immigration data
def clean_first_entry(ord_dict):
    """
    cleans first value of each ordered dictionary
    https://stackoverflow.com/questions/4406501/change-the-name-of-a-key-in-dictionary
    """
    temp_list = ord_dict["country_code"].split(",")
    ord_dict["country_code"] = temp_list[-1]
    return ord_dict


def clean_all_numbers(info, ord_dict):
    """
    found that all numbers (are strings) in the tables need cleaning and
    formatting so they can be properly ranked.
    Needs info for clean_all_numbers function
    """
    for year in info["datafields"]:
        str_a = ord_dict[info[year]]
        str_b = str_a.rstrip('p')
        str_c = str_b.rstrip('b')
        str_d = str_c.rstrip('e')
        str_e = str_d.rstrip(' ')
        str_f = str_e.replace(':', '0')
        str_g = str(int(float(str_f)))
        ord_dict[info[year]] = str_g
    return ord_dict


def clean_ord_dict(info, list_of_ord_dicts):
    """
    take a table and clean each line using the clean_first_entry and clean_all_numbers functions
    Input - needs info for the clean_all_numbers function
    """
    for ord_dict in list_of_ord_dicts:
        ord_dict = clean_first_entry(ord_dict)
    for ord_dict in list_of_ord_dicts:
        ord_dict = clean_all_numbers(info, ord_dict)
    return list_of_ord_dicts


#  other functions for sorting and print_formatting
def sort_by_year(stats, year, parameter):
    """
    Inputs:
      stats - a list of dictionaries of immigration data (values are strings)
      year - year for data
      parameter - "high" or "low" (which is checked)
    Output:
      list of dictionaries sorted by highest or lowest
    """
    # direction of sorting
    if parameter.lower() == "high":
        order = True
    elif parameter.lower() == "low":
        order = False
    else:
        return "Error in sort parameter"
    stats = sorted(stats, key=lambda k: int(k[year]), reverse=order)
    return stats


def sort_by_col(stats, col, parameter):
    """
    Is genric form of sort_by_year function
    Inputs:
      stats - a list of dictionaries of immigration data (values are strings)
      col - the column title to sort by
      parameter - "high" or "low" (which is checked)
    Output:
      list of dictionaries sorted by highest or lowest
    """
    # direction of sorting
    if parameter.lower() == "high":
        order = True
    elif parameter.lower() == "low":
        order = False
    else:
        return "Error in sort parameter"
    stats = sorted(stats, key=lambda k: float(k[col]), reverse=order)
    return stats


def list_of_dictionaries_as_table(stats):
    """
    Inputs:
      stats - list_of dictionaries from sort function
    Output:
      readable table as a list of lists
    """
    # header only
    list0 = []
    for item in stats[0]:
        list0.append(item)
    print(immigration_info["print_formatting"].format(*list0))
    # body with no headers
    list1 = []
    for row in stats:
        list1.append(row.items())
        # https://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict
    for row in list1:
        list2 = []
        for items in row:
            list2.append(items[1])
        print(immigration_info["print_formatting"].format(*list2))
    return ""


def print_named_cols(stats, list_of_col_names):
    """
    Inputs:
      stats - list_of dictionaries (e.g. from sort function year?)
      list col_names - immigration_info dictionary's names of columns to print_table, as a list
    Output:
      only a printed table; return is just ""
    Mutates input?
      No
    Idea:
      Just print the cols you want
    """
    # print header only
    list0 = []
    for item in stats[0]:
        # print(item)
        if item in list_of_col_names:
            list0.append(item)
    format_string = ""
    for i in range(len(list_of_col_names)):
        format_string += "{:>15}"
    print(format_string.format(*list0))
    # print body only
    for row in stats:
        list1 = []
        # print(row)
        for key in row.keys():
            if key in list_of_col_names:
                list1.append(row[key])
        print(format_string.format(*list1))
    return ""

# function to change table of countries/two-letter codes to a dictionary


def remove_brackets(listoflists):
    """
    custom function to remove brackets around two-letter country_codes in the csv file
    """
    for pair in listoflists:
        str_a = pair[1].rstrip(')')
        str_b = str_a.lstrip('(')
        pair[1] = str_b
    return listoflists


def lofl2lofd(listoflists):
    """
    function to turn table of countries/two-letter codes to a dictionary
    after this function we have the final dictionary we want matching country codes to names
    """
    a_dict = {item[1]: item[0] for item in listoflists}
    return a_dict


# function to add a column to an ordered dict
def add_col(left_side, left_key, left_value, right_side):
    """
    Input:
        left_side:
        2 columns of a csv file that go on left hand of new output ordered dict (DONOR)
        assumes file is in form of country_code.csv, where each row is a 2-letter country code then a value
        N.B. this file format does not have a header row
        also, the file is put through the read_csv_file function to be a list of dictionaries
        left_key: key for left_side dictionary
        left_value: value for left_side dictionary
        right_side:
        the 'HOST' csv file (list of ordered dictionaries)
        N.B. both files have to have 2-letter country codes
    Output:
        joined DONOR + HOST
    Mutates?:
        No. It's a new dictionary
    Idea:
        if same country codes in both files, HOST data appended to front of each DONOR narrow_table
        N.B. formatting won't work for standard in info_dict
        N.B. print_named_cols printing function should work (beware col names not in info_dict)
    """
    new_ord_dict = []
    for ord_dict in right_side:
        a_dict = {}
        for value in left_side:
            if value in ord_dict.values():
                a_dict = {"Name": left_side[value]}
        y = {**a_dict, **ord_dict}
        z = OrderedDict(y)
        new_ord_dict.append(z)
    return new_ord_dict



# Meta data dictionary
immigration_info = {"sourcefile": "/Users/RAhmed/Atom_projects/Dictionaries_practice/\
tps00176_halfdata.csv",
                    "separator": ",",
                    "quote": '"',
                    "country_code": "country_code",
                    "2005": "2005",
                    "2006": "2006",
                    "2007": "2007",
                    "2008": "2008",
                    "2009": "2009",
                    "2010": "2010",
                    "2011": "2011",
                    "2012": "2012",
                    "2013": "2013",
                    "2014": "2014",
                    "2015": "2015",
                    "2016": "2016",
                    "datafields": ["2005", "2006", "2007", "2008", "2009", "2010",
                                   "2011", "2012", "2013", "2014", "2015", "2016"],
                    "print_formatting": "{:>20}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}"
                    }

# Meta data dictionary
gdp_info = {"sourcefile": "/Users/RAhmed/Atom_projects/Dictionaries_practice/tec00001_third_data.csv",
            "separator": ",",
            "quote": '"',
            "country_code": "country_code",
            "2006": "2006",
            "2007": "2007",
            "2008": "2008",
            "2009": "2009",
            "2010": "2010",
            "2011": "2011",
            "2012": "2012",
            "2013": "2013",
            "2014": "2014",
            "2015": "2015",
            "2016": "2016",
            "2017": "2017",
            "datafields": ["2006", "2007", "2008", "2009", "2010", "2011",
                           "2012", "2013", "2014", "2015", "2016", "2017"],
            "print_formatting": "{:>20}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}"
            }


def merge_tables(ord_dict0, descr0, ord_dict1, descr1, year, composite):
    """
    Input:
        - two cleaned up ordered dictionaries (EU immigration data and EU GDP data)
        - merge as one new ordered dict
        - as years in both inputs have same name, need descriptors to change year names (e.g. descr0)
        - later, create composite statistics
    Output:
        - new merged ordered Dictionary
        - additional composite gdp/immigration metric
    Mutate?:
        No
    """
    new_list = []
    for row in ord_dict0:
        new_row = {}
        new_row.update({"Name": row["Name"]})
        new_row.update({"country_code": row["country_code"]})
        new_str = year + "_" + descr0
        new_row.update({new_str: row[year]})
        for row1 in ord_dict1:
            if new_row["country_code"] in row1.values():
                new_str1 = year + "_" + descr1
                new_row.update({new_str1: row1[year]})
                # create composite function
                comp_func = str(float(new_row[new_str1])/float(new_row[new_str]))
                comp_func1 = "{0:.4}".format(comp_func)
                new_row.update({composite: str(comp_func1)})
        new_list.append(new_row)

    return(new_list)


# = = = = = test and develop below here = = = = =


# create dictionary of two-letter country_code
dict_test = read_csv_file("/Users/RAhmed/Atom_projects/country_codes.csv")
# print(dict_test)

clean_dict = remove_brackets(dict_test)
# print(clean_dict)

country_dict = lofl2lofd(clean_dict)
print(country_dict)

# turn raw immigration data to csv file to table
# one step is to use Excel (not shown)

test_file = immigration_info["sourcefile"]
separator = immigration_info["separator"]
quote = immigration_info["quote"]

test_table = dictreader_csv_file(test_file, separator, quote)
# print("test_table", test_table)
# print(len(test_table))

clean_table = clean_ord_dict(immigration_info, test_table)
print(clean_table)

# print_table = list_of_dictionaries_as_table(clean_table)
# print(print_table)

year = immigration_info["2016"]
# sort_table = sort_by_year(clean_table, year, "high")
# # print_table = list_of_dictionaries_as_table(sort_table)
# # print(print_table)
#
# cols_to_print = [immigration_info["country_code"], immigration_info["2014"],
#                  immigration_info["2015"], immigration_info["2016"]]
# narrow_table = print_named_cols(sort_table, cols_to_print)
# print(narrow_table)

# print("\n")
key = "Name"
value = "country_code"
left_side = country_dict
right_side = clean_table

larger_table = add_col(left_side, key, value, right_side)
print(larger_table)

cols_to_print = ["Name", immigration_info["country_code"], immigration_info["2014"],
                 immigration_info["2015"], immigration_info["2016"]]
descriptive_table = print_named_cols(larger_table, cols_to_print)

# now sort larger tables, which has country names also
print("\n")
year = immigration_info["2012"]
sort_table = sort_by_year(larger_table, year, "high")
descriptive_table = print_named_cols(sort_table, cols_to_print)

# turn raw gdp data to csv file to table
# one step is to use Excel (not shown)


test_file2 = gdp_info["sourcefile"]
separator2 = gdp_info["separator"]
quote2 = gdp_info["quote"]

test_table2 = dictreader_csv_file(test_file2, separator2, quote2)
# print(test_table2)

clean_table2 = clean_ord_dict(gdp_info, test_table2)
# print(clean_table2)

year = gdp_info["2016"]
key = "Name"
value = "country_code"
left_side = country_dict
right_side = clean_table2

larger_table2 = add_col(left_side, key, value, right_side)
# print(larger_table2)

cols_to_print2 = ["Name", gdp_info["country_code"], gdp_info["2014"],
                  gdp_info["2015"], gdp_info["2016"]]
# descriptive_table2 = print_named_cols(larger_table2, cols_to_print2)

# now sort larger tables, which has country names also
print("\n")
year = gdp_info["2016"]
sort_table2 = sort_by_year(larger_table2, year, "high")
# descriptive_table2 = print_named_cols(sort_table2, cols_to_print2)

# the composite figure here is with a lower number taking a higher burden wrt gdp
year = "2016"
imm_and_gdp = merge_tables(sort_table, "imm", sort_table2, "gdp", year, "comp")
print("###", imm_and_gdp)

list2print = ["Name", "country_code", "2016_imm", "2016_gdp", "comp"]
sort_imm_and_gdp = sort_by_col(imm_and_gdp, "comp", "low")
print("$$$")
good_print = print_named_cols(sort_imm_and_gdp, list2print)
# ^ finally a table that is insightful!

# # do something in matplotlib
import matplotlib.pyplot as plt
import numpy as np
x = []
y = []
for row in sort_imm_and_gdp:
    country = row['country_code']
    comp_stat = row['comp']
    x.append(country)
    y.append(float(comp_stat))
print(x)
print(y)
plt.bar(x, y, label="2016", color="#33BFFF")
plt.xlabel('Nations')
plt.rc('xtick', labelsize=12)
plt.rc('font', size=12)
plt.rc('axes', titlesize=12)
plt.ylabel('GDP/immigration ')
plt.title('Relative EU immigration ')
plt.legend()
plt.show()

# foo comments
