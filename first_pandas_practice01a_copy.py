import csv
import pandas
import numpy
import random

# pandas works differently and doesn't need the functions below


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


def write_csv_file(csv_table, file_name):
    """
    Input: Nested list csv_table and a string file_name
    Action: Write fields in csv_table into a comma-separated CSV file with the name file_name
    """

    with open(file_name, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in csv_table:
            csv_writer.writerow(row)


# you can see that print works differently between regular python and pandas
pan_data = pandas.read_csv('/Users/RAhmed/WesleyanMOOC/gapminder.csv')
print(len(pan_data))
print(len(pan_data.columns))
for header in pan_data:
    titles = header
print("titles", type(titles))
variables = list(titles.split(','))
print(len(variables))
print(pan_data)
print(pan_data.head(n=3))

py_data0 = read_csv_file('/Users/RAhmed/WesleyanMOOC/gapminder.csv')
# print("> Whole csv file: ", py_data)
print()
for row in py_data0:
    # print("> csv by row:", row)
    pass

py_table0 = write_csv_file(py_data0, '/Users/RAhmed/WesleyanMOOC/Course01/Week02/practice_00.csv')


# clean up additional """ in first and last entry in row
for row in py_data0:
    for index in range(len(row)):
        row[index] = row[index].lstrip('"')
        row[index] = row[index].rstrip('"')

# clean up second entry country name spread over two cells,; ignore first row (headers)
for idx in range(len(py_data0)):
    if idx != 0:
        if not (py_data0[idx][1][0].isdigit() or py_data0[idx][1] == ' '):
            py_data0[idx][0] += py_data0[idx][1]
            py_data0[idx].pop(1)

py_table1 = write_csv_file(py_data0, '/Users/RAhmed/WesleyanMOOC/Course01/Week02/practice_01.csv')

# going to add an additional column to end of this table, to practice the categorical function in pandas
# problem is last entry might be '', best general solution is to add '0' where any ''
py_data1 = read_csv_file('/Users/RAhmed/WesleyanMOOC/Course01/Week02/practice_01.csv')

for row in py_data1[1:]:
    for idx in range(len(row)):
        if row[idx] == ' ':
            row[idx] = '0'
        if len(row) != len((py_data1[0])):
            row.append('0')
    row.append(str(random.randrange(0, 4)))  # <= my categorical variable

py_data1[0].append('Extra column for practice')

# write clean table to a csv to keep
py_table1 = write_csv_file(py_data1, '/Users/RAhmed/WesleyanMOOC/Course01/Week02/practice_02.csv')


# back to the hw assignments, will use the py_table1 as start point (since has extra column)
pan_data1 = pandas.read_csv('/Users/RAhmed/WesleyanMOOC/Course01/Week02/practice_02.csv')

# frequency
pan_data1['polityscore'] = pan_data1['polityscore'].astype(
    int)  # <= make categorical string into an integer
cat1 = pan_data1['polityscore'].value_counts(sort=True)
print("Cat1", cat1)
# <= docs says yoo cannot order by category only by frequency
cat1a = pan_data1['polityscore'].value_counts().values.tolist()
print("Cat1a", cat1a)

# percent
percent1 = pan_data1['polityscore'].value_counts(sort=False, normalize=True)
print("Percent1", percent1)


# # for practice select certain variables only. Here those with relatively low urbansation and Extra Column <3
sub_data1 = pan_data1[(pan_data1['urbanrate'] <= 60) & (pan_data1['Extra column for practice'] < 3)]
print(sub_data1.head(n=3))
# <= write to csv in pandas
sub_data1.to_csv('/Users/RAhmed/WesleyanMOOC/Course01/Week02/practice_03.csv')
