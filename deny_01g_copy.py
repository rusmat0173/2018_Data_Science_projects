"""
Quick go to work with denied persons list
Versions
01a - use a classic read file format, rather than an csv style
"""
import csv


def ascii_file_no_lines(filename):
    """
    check how many lines in ascii file
    # http://gsp.humboldt.edu/OLM/Courses/GSP_318/03_3_ReadingFiles.html
    """
    TheFile = open(filename, "r")
    TheLine = "r@nd@nw@rd"  # <= a starting assignment that won't be used
    numlines = 0
    while (TheLine != ""):
        TheLine = TheFile.readline()  # read the next line in the file
        numlines += 1
    TheFile.close()
    return("File has {} lines.".format(numlines))


def clean_string(a_string):
    """
    clean up a single ascii a_string
    This is the key tidy up function! Is used in convert_ascii_to_csvtable
    """
    # remove left and right "
    z_string = a_string.rstrip('\n')
    b_string = z_string.lstrip('"')
    c_string = b_string.rsplit('"')
    # remove empty ''. ' '. '  ', etc.
    spacer = ' '
    spacer_list = []
    for i in range(1, 10):
        new_spacer = spacer * i
        spacer_list.append(new_spacer)
    d_list = []
    for item in c_string:
        if item not in spacer_list:
            d_list.append(item)
    # need to remove empty columns created by '', '',
    # pass
    return d_list


def convert_ascii_to_csvtable(filename, max_lines):
    """
    convert an ascii file to a csv file
    # http://gsp.humboldt.edu/OLM/Courses/GSP_318/03_3_ReadingFiles.html
    """
    table = []
    TheFile = open(filename, "r")
    TheLine = "r@nd@nw@rd"  # <= a starting assignment that won't be used
    numlines = 0
    while (TheLine != "") and numlines < max_lines:
        TheLine = TheFile.readline()  # read the next line in the file
        table.append(clean_string(TheLine))
        numlines += 1

    TheFile.close()
    return table


def remove_empty_rows_and_cols(table):
    """
    A bespoke function to remove cases of 2 empty columns between columns with data
    It could be done in Excel usually, but done as practice here
    In real life you would want this if files had hundreds of columns

    """
    body = table[1:]
    header = table[:1]
    # remove empty remove_empty_rows
    for row in body:
        if row == ['']:
            body.remove(row)
    # establish ranges
    len_body = len(body)
    for item in header:
        len_header = len(item)
    new_table = []
    # first create a new body. (Much less confusing to create new one than replace rows in old one)
    for i in range(len_body):
        new_row = []
        for j in range(len_header):
            if body[i][j] != header[0][j]:
                new_row.append(body[i][j])
        new_table.append(new_row)
    # now have to remove ''s in len_header. Will do as above for ease
    another_row = []
    for i in range(len_header):
        if header[0][i] != '':
            another_row.append(header[0][i])
    new_table.insert(0, another_row)
    return new_table


def write_csv_file(csv_table, file_name):
    """
    USED FROM RICE MOOC - thank you!
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    HOWEVER: there are several empty columns. It is simply easier to just delete these in Excel!
    THE ALTERNATIVE would be to read as list of dictionaries and delete ('','') pairs - but not worth it
    """

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)


# = = = Test and develop code below where
input_file = ("/Users/RAhmed/Atom_projects/Dictionaries_practice/denied_persons_list.txt")
output_file = ("/Users/RAhmed/Atom_projects/Dictionaries_practice/denied_persons_list.csv")
deny01_length = ascii_file_no_lines(input_file)
print(deny01_length)

deny01 = convert_ascii_to_csvtable(input_file, 40)
# print(deny01)

deny02 = remove_empty_rows_and_cols(deny01)
print(deny02)

deny03 = write_csv_file(deny02, output_file)
