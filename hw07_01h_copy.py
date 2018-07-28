"""
Issue:
[-14.3 pts] build_map_dict_by_code({'quote': '"', 'max_year': 1958, 'gdpfile': 'gdptable2.csv', 'country_name': 'Country Name', 'separator': ',', 'country_code': 'Code', 'min_year': 1953},
{'separator': ',', 'quote': "'", 'plot_codes': 'Cd2', 'data_codes': 'Cd1', 'codefile': 'code2.csv'},
{'C2': 'c2', 'C5': 'c5', 'C4': 'c4', 'C3': 'c3', 'C1': 'c1'}, '1953')
expected ({'C2': 0.0}, {'C5', 'C3', 'C1'}, {'C4'})
but received (Exception: TypeError) "unhashable type: 'dict'" at line 149, in build_map_dict_by_code
"""
import csv
import math


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


def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list consisting of the fields in the CSV file
    """
    with open(file_name, newline='') as csv_file:
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar="'")
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    filename = codeinfo['codefile']
    keyfield = codeinfo['plot_codes']
    separator = codeinfo['separator']
    quote = codeinfo['quote']
    codes_table = read_csv_as_nested_dict(filename, keyfield, separator, quote)
##    print("\ncodes table", codes_table)

    output_dict = {}
    for key, values in codes_table.items():
        output_dict.update({key: values[codeinfo['data_codes']]})

    return output_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    converter = build_country_code_converter(codeinfo)
    new_converter = {}
    for key, value in converter.items():
        new_converter.update({key.upper(): value.upper()})

    output_list = []
    output_dict = {}

    for pc_key in plot_countries.keys():
        not_found = True
        for gdp_key in gdp_countries.keys():
            if not_found:
                if pc_key.upper() in new_converter.keys():
                    if new_converter[pc_key.upper()] == gdp_key.upper():
                        output_dict.update({pc_key: gdp_key})
                        not_found = False
        if not_found:
            output_list.append(pc_key)

    output_set = set(output_list)
    return output_dict, output_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo - A GDP information dictionary
      codeinfo - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log(base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
##    filename = "/Users/RAhmed/RiceScriptingMOOC/Course4/Week04/isp_gdp_csv_files/gdptable1.csv"  #
    filename = gdpinfo['gdpfile']
    keyfield = gdpinfo['country_code']
    separator = gdpinfo["separator"]
    quote = gdpinfo["quote"]
    gdp_countries = read_csv_as_nested_dict(filename, keyfield, separator, quote)
    starter = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
    print("starter", starter)
    plot2gdp_dict = starter[0]
    not_in_gdp_set = starter[1]
    print(plot2gdp_dict, not_in_gdp_set)

    output_dict = {}
    no_gdp_year_set = set()
    for key, value in plot2gdp_dict.items():
        print(key, value)
    for key, value in plot2gdp_dict.items():
        # print(gdp_countries[value][year])
        if gdp_countries[value][year] == '':
            no_gdp_year_set.add(gdp_countries[value])
        else:
            output_dict.update({key: math.log10(float(gdp_countries[value][year]))})
##    no_gdp_year_set = set(no_gdp_year_list)
    return output_dict, not_in_gdp_set, no_gdp_year_set

# develop under here


filename = "/Users/RAhmed/RiceScriptingMOOC/Course4/Week04/isp_gdp_csv_files/gdptable1.csv"
keyfield = 'Code'
separator = ','
quote = '"'


X01 = read_csv_as_nested_dict(filename, keyfield, separator, quote)
print(X01)

gdpinfo = {'min_year': "1953", 'quote': '"', 'country_name': 'Country Name', 'separator': ',',
           'max_year': "1958",
           'gdpfile': "/Users/RAhmed/RiceScriptingMOOC/Course4/Week04/isp_gdp_csv_files/gdptable2.csv",
           'country_code': 'Code'}

codeinfo = {'data_codes': 'Cd2',
            'quote': "'",
            'codefile': '/Users/RAhmed/RiceScriptingMOOC/Course4/Week04/isp_code_csv_files/code2.csv',
            'plot_codes': 'Cd2',
            'separator': ','}

gdp_countries = read_csv_as_nested_dict(
    gdpinfo['gdpfile'], gdpinfo['country_code'], gdpinfo['separator'], gdpinfo['quote'])
print(gdp_countries)

code_tables = read_csv_file(codeinfo["codefile"])
print("\n", code_tables)

X03 = build_country_code_converter(codeinfo)
print("\n", X03)

plot_countries = {'C1': 'c1', 'C5': 'c5', 'C3': 'c3', 'C2': 'c2', 'C4': 'c4'}

X04 = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)
print("\n", "X04", X04)

year = "1955"

X05 = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
print("\n", "X05", X05)
