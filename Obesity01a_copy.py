"""
    Project for processing UK Home office data
    from internally stored file
    obesity.csv

    Based on SeriousViolentCrime04a.py

    Uses files from Rice Introduction to Scripting Course 3, Week 4 h/w assignment


"""

import csv

##
# Provided code from Rice Scripting Cse 03, Week 3 Project
##


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


##
# Meta data dictionary
##


obesity_info = {"sourcefile": "/Users/RAhmed/ThonnyProjects/UKHomeOfficeDataOct2010/\
Obesity.csv",
                "separator": ",",
                "quote": '"',
                "authority": "Authority",
                "year1": "sch_2006/07",
                "year2": "sch_2007/08",
                "year3": "sch_2008/09",
                "datafields": ["year1", "year2", "year3"],
                "types": ["LB", "UA", "CC", "DC", "MD"],
                "print_formatting": "{:50}{:15}{:15}{:15}{:15}"
                }
##
# Sort functions
##


def sort_by_name(stats, parameter):
    """
    Inputs:
      stats - a nested dictionary of obesity data (values are strings)
    Output:
      nested list of dictionaries sorted by name. N.B. You can't sort a dictionary directly
    """
    # direction of sorting
    if parameter.lower() == "high":
        order = True
    elif parameter.lower() == "low":
        order = False
    else:
        return "Error in sort parameter"
    stats = sorted(stats, key=lambda k: k["Authority"], reverse=order)
    return stats


def sort_by_year(stats, year, parameter):
    """
    Inputs:
      stats - a list of dictionaries of crime data (values are strings)
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
    stats = sorted(stats, key=lambda k: k[year], reverse=order)
    return stats

##
# Creating useful tables for viewing
##


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
    print(obesity_info["print_formatting"].format(*list0))
    # body with no headers
    list1 = []
    for row in stats:
        list1.append(row.items())
        # https://stackoverflow.com/questions/10058140/accessing-items-in-a-ordereddict
    for row in list1:
        list2 = []
        for items in row:
            list2.append(items[1])
        print(obesity_info["print_formatting"].format(*list2))

    return ""


##
# Other functions
##
def auth_in_list(info, stats, name):
    """
    Inputs:
      info - obesity meta file
      stats - a list of dictionaries of crime data (values are strings)
      name of authority (which is checked) whose info to display
    Output:
      a dictionary key, or Error message
    Trying to be Pythonic and catch wrong/no type of authority: my idea: do algorithm a natural way
      1. check if a type ending to the name:
        a. if 'no' add them in and create a search list with all types
        b. if 'yes' prioritise the search list with the given type ending
      2. check if name in dictionary
    """
    output_row = []
    types = info["types"]
    type_ending = name[-2:]
    search_list = []
    if type_ending not in types:
        add_endings = [n + t for n in [name + " "] for t in types]
        for item in add_endings:
            search_list.append(item)
    else:
        types.remove(type_ending)
        types.insert(0, type_ending)
        add_endings = [n + t for n in [name[:-2]] for t in types]
        for item in add_endings:
            search_list.append(item)
    # loops to find if item in search list is in the statistics
    found = False
    for name in search_list:
        if not found:
            for row in stats:
                if not found:
                    if (info["authority"], name) in row.items():
                        found = True
                        # print(row)
                        output_row = row
    if found:
        # header
        list0 = []
        for item in output_row:
            list0.append(item)
        print(info["print_formatting"].format(*list0))
        # body with no headers
        list1 = []
        for item in output_row:
            list1.append(output_row[item])
        print(info["print_formatting"].format(*list1))
        return ""


# = = = Development and Testing below here  = = =
obesity_stats = read_csv_as_list_dict(
    obesity_info["sourcefile"], obesity_info["separator"], obesity_info["quote"])
# print("obesity_stats", obesity_stats)


year = "sch_2008/09"
parameter = "high"
zulu = sort_by_year(obesity_stats, year, parameter)

shanti = sort_by_name(obesity_stats, parameter)
# print(shanti)

cherokee = list_of_dictionaries_as_table(zulu)
# print(cherokee)

navaho = auth_in_list(obesity_info, obesity_stats, "Surrey")
