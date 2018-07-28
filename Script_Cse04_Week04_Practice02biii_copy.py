"""
Project instructions:
> Base on  Week01 solution. draw_USA_map function is from Week01
> From Week03 add code for reading csv file
> Sort table
> Draw circle at county centres from global_table


"""
import csv
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import matplotlib.colors as colors


def draw_cancer_risk_map(joined_csv_file_name, map_name, num_counties):
    """
    Given the name of a PNG map of the USA (specified as a string),
    draw this map using matplotlib
    """
    USA_SVG_SIZE = [555, 352]

    # Read in csv data and sort
    joined_table = read_csv_file(joined_csv_file_name)
    joined_table.sort(key=lambda row: float(row[4]), reverse=False)
    print("JT0", joined_table[0])
    # find max and min risk values for circle color maps, for later
    risk_min = joined_table[0][4]
    risk_max = joined_table[-1][4]
    print(risk_max, risk_min)

    # Load map image, note that using 'rb'option in open() is critical since png files are binary
    with open(map_name, 'rb') as map_file:        # using 'r' causes Python to crash :(
        map_img = plt.imread(map_file)

    #  Get dimensions of USA map image
    ypixels, xpixels, bands = map_img.shape
    # print(xpixels, ypixels, bands)

    # Optional code to resize plot as fixed size figure -
    # DPI = 80.0                  # adjust this constant to resize your plot
    # xinch = xpixels / DPI
    # yinch = ypixels / DPI
    # plt.figure(figsize=(xinch,yinch))

    # Plot USA map
    implot = plt.imshow(map_img)

    # Compute function that maps cancer risk to RGB colors
    risk_map = create_riskmap(mpl.cm.RdYlGn_r)
    # color maps from https://matplotlib.org/gallery/color/colormap_reference.html

    # draw circle at county centres from global_table
    for row in joined_table:
        circle_size = compute_county_circle(row[3])
        plt.scatter(x=float(row[5]) * xpixels / USA_SVG_SIZE[0],
                    y=float(row[6]) * ypixels / USA_SVG_SIZE[1], s=circle_size,
                    c=risk_map(float(row[4])))

    plt.title("Cancer risk in US counties")
    plt.show()


def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list consisting of the fields in the CSV file
    """

    with open(file_name, newline='') as csv_file:       # don't need to explicitly close the file now
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table


def compute_county_circle(county_population):
    MAGIC_CONSTANT = 0.025
    circle_size = MAGIC_CONSTANT * math.sqrt(float(county_population))
    # print("CS", circle_size)
    return circle_size


def create_riskmap(colormap):
    """
    largely used model answer provided:
        Initialize the colormap "jet" from matplotlib, <= RA I changed this
        Return function that takes risk and returns RGB color for use with scatter() in matplotlib
        # Note that this code is tricky - remember to return a lambda expression
    """
    # this max/min risk numbers are either from visual inspection of table
    # # or print from draw_cancer_risk_map
    risk_max = 1.50E-04
    risk_min = 8.60E-06
    # not surprisingly, model answer turns these to logs
    log_risk_max = math.log(risk_max, 10)    # maximum cancer risk in table
    log_risk_min = math.log(8.60E-06, 10)    # minimum cancer risk in table

    risk_norm = mpl.colors.Normalize(vmin=log_risk_min, vmax=log_risk_max)
    color_mapper = mpl.cm.ScalarMappable(norm=risk_norm, cmap=colormap)
    return lambda risk: color_mapper.to_rgba(math.log(risk, 10))

# # = = = = test and develop below here = = = =


joined_file = "/Users/RAhmed/RiceScriptingMOOC/Course4/Week04/Practice_Project/practice_joined_file.csv"
joined_table = read_csv_file(joined_file)
joined_length = len(joined_table)

# # sort table as requested
joined_table.sort(key=lambda row: float(row[4]), reverse=False)
print(joined_table[:5])


# # V function below is very slow! (Used the model answer function)
map_name = "/Users/RAhmed/RiceScriptingMOOC/Course4//Week04/Practice_Project/USA_Counties_555x352.png"
# draw_USA_map(map_name, joined_table)
# # draw_USA_map("USA_Counties_1000x634.png")
draw_cancer_risk_map(joined_file, map_name, None)
