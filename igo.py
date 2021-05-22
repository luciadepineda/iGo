import collections
import csv
import haversine
import networkx
from osmnx import *
from pandas import *
import pickle
from staticmap import *
import string
import urllib.request

PLACE = 'Barcelona, Catalonia'
GRAPH_FILENAME = 'barcelona.graph'
SIZE = 800
HIGHWAYS_URL = 'https://opendata-ajuntament.barcelona.cat/data/dataset/1090983a-1c40-4609-8620-14ad49aae3ab/resource/1d6c814c-70ef-4147-aa16-a49ddb952f72/download/transit_relacio_trams.csv'
CONGESTIONS_URL = 'https://opendata-ajuntament.barcelona.cat/data/dataset/8319c2b1-4c21-4962-9acd-6db4c5ff1148/resource/2d456eb5-4ea6-4f68-9794-2f3f1a58a933/download'

#creating a graph of "PLACE" (barcelona) using the driving type
#using the method get_digraph to choose between parallel edges minimising
#the attribute 'length'


#Highway = collections.namedtuple('Highway', '...') # Tram
#Congestion = collections.namedtuple('Congestion', '...')


def exists_graph(GRAPH_FILENAME):
    """boolean function that checks if a file exists"""
    #to check if a file exists the easiest way is to try to open it
    try:
        with open(GRAPH_FILENAME) as f:
            return True
    except:
        return False
        #if the file can't be opened, it returns false

def download_graph(PLACE):
    """function that creates a directed graph from a determined place saving
    the attribute 'length', using methods from osmnx"""
    #first it creates the graph from the place using the type 'drive'
    graph = graph_from_place(PLACE, network_type='drive', simplify=True)
    #then it creates the directed graph using the function get_digraph and using
    #the attribute 'length'
    digraph = utils_graph.get_digraph(graph, weight='length')

    return digraph

def save_graph(digraph, GRAPH_FILENAME):
    """function that saves the directed graph previously created and dumps it
    into a pickle file for later use"""
    with open(GRAPH_FILENAME, 'wb') as file:
        pickle.dump(digraph, file) #saving the graph in a pickle file

def load_graph(GRAPH_FILENAME):
    """function that loads the graph from the existing file"""
    with open(GRAPH_FILENAME, 'rb') as file:
        digraph = pickle.load(file)
        #creating the variable digraph and loading the already downloaded graph
        #from the pickle file

    return digraph

def plot_graph(PLACE):
    """function that plots the graph from a determined place into the
    screen"""
    #it doesn't use the directed graph as it doesn't work with the plot_graph
    #function, so it creates a normal graph again
    plot_graph(graph_from_place(PLACE))

def download_highways(HIGHWAYS_URL):
    """function that reads the file HIGHWAYS_URL and saves it into a pandas
    dataframe"""

    #reading the csv file and saving it into a dataframe
    highways = read_csv(HIGHWAYS_URL)

    #renaming the columns
    highways.rename(columns = {'Tram': 'way_id', 'Descripció': 'description',
    'Coordenades': 'coordinates'}, inplace=True)

    return highways

def read_coordinates(highways):
    """function that reads the coordinates from the highways dataframe and
    converts them into a list of pairs of floats representing
    latitude/longitude"""

    #converting the coordinates column into a list of lists of strings
    coordinates_list = highways['coordinates'].tolist()
    #converting every list of strings into a list of floats
    for i in range(len(coordinates_list)):
        coordinates_list[i] = coordinates_list[i].split(',')
        for j in range(len(coordinates_list[i])):
            coordinates_list[i][j] = float(coordinates_list[i][j])
    #dividing every list of floats into groups of 2
    for k in range(len(coordinates_list)):
        coordinates_list[k] = [coordinates_list[k][l:l + 2]
        for l in range(0, len(coordinates_list[k]), 2)]

    return coordinates_list

def plot_highways(highways, SIZE):
    """function that creates a map with all the highways from HIGHWAYS_URL
    plotted"""

    #using the read_coordinates function to create a list
    coordinates_list = read_coordinates(highways)

    #creating a staticmap of the size determined
    map = StaticMap(SIZE, SIZE)

    #reading all the coordinates and creating lines between points of every way
    #adding the lines into the map
    for i in range(len(coordinates_list)):
        line = Line(coordinates_list[i], '#000000', 2)
        map.add_line(line)

    #creating an image of the map and saving it into a png file named 'highways'
    image = map.render()
    image.save('highways.png')

def download_congestions(CONGESTIONS_URL):
    """function that reads the file CONGESTIONS_URL and saves it into a pandas
    dataframe"""

    column_names = ['way_id', 'time', 'actual_state', 'future_state']
    congestions = read_csv(CONGESTIONS_URL, sep='#', names=column_names)

    return congestions

def plot_congestions(highways, congestions, SIZE):

    #using the read_coordinates function to create a list
    coordinates_list = read_coordinates(highways)

    #creating a staticmap of the size determined
    map = StaticMap(SIZE, SIZE)

    #reading all the coordinates and creating lines between points of every way
    #adding the lines into the map,
    for i in range(len(coordinates_list)):
        if congestions['actual_state'][i] == 0:
            line = Line(coordinates_list[i], '#E1e1e1', 2)
        if congestions['actual_state'][i] == 1:
            line = Line(coordinates_list[i], '#3ce940', 2)
        if congestions['actual_state'][i] == 2:
            line = Line(coordinates_list[i], '#3deefc', 2)
        if congestions['actual_state'][i] == 3:
            line = Line(coordinates_list[i], '#F5f588', 2)
        if congestions['actual_state'][i] == 4:
            line = Line(coordinates_list[i], '#F5a536', 2)
        if congestions['actual_state'][i] == 5:
            line = Line(coordinates_list[i], '#F91a0e', 2)
        if congestions['actual_state'][i] == 6:
            line = Line(coordinates_list[i], '#000000', 2)
        map.add_line(line)

    #creating an image of the map and saving it into a png file named 'highways'
    image = map.render()
    image.save('congestions.png')
    print("The file has been downloaded")

def main():
    # load/download graph (using cache) and plot it on the screen
    if not exists_graph(GRAPH_FILENAME):
        digraph = download_graph(PLACE)
        save_graph(digraph, GRAPH_FILENAME)
    else:
        digraph = load_graph(GRAPH_FILENAME)
    plot_graph(PLACE)

    # download highways and plot them into a PNG image
    highways = download_highways(HIGHWAYS_URL)
    read_coordinates(highways)
    plot_highways(highways, SIZE)

    # download congestions and plot them into a PNG image
    congestions = download_congestions(CONGESTIONS_URL)
    plot_congestions(highways, congestions, SIZE)

    # get the 'intelligent graph' version of a graph taking into account the congestions of the highways
    igraph = build_igraph(graph, highways, congestions)

    # get 'intelligent path' between two addresses and plot it into a PNG image
    ipath = get_shortest_path_with_ispeeds(igraph, "Campus Nord", "Sagrada Família")
    plot_path(igraph, ipath, SIZE)
main()
