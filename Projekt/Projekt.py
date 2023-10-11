from email import contentmanager
from operator import indexOf
from matplotlib import pyplot as plt, animation
import networkx as nx
import random
import numpy as np

#############PARAMETRY###############
plt.rcParams["figure.figsize"] = [12, 7] # szerokosc figury 7.5, wysokosc 3.5
plt.rcParams["figure.autolayout"] = True #automatycznie dostosowuje marginesy i odstêpy
nr_nodes = 15 # ilosc wierzcholkow
colors_egdes = {} # kolory {(node1, node2): 'color'}
colors_nodes = {} # kolory {node1: 'color'}
width = {} #grubosc wierzcholkow
wartosc = False #wlaczenie wyswietlania wartosci

##############SETUP################
G = nx.Graph()
for t in range(1,nr_nodes+1):
    G.add_node(t)#dodanie wierzcholkow
    colors_nodes[t] = 'blue'

pos = nx.random_layout(G) #zapisanie pozycji 

def graph_edges():#dodanie krawedzi
    for x in range(1, nr_nodes):
        for y in range(x+1, nr_nodes+1):
            G.add_edge(x,y,dis=distance(x,y)) # dodanie krawedzi miedzy x i y oraz ustawienie odleglosci
            colors_egdes[(x,y)] = 'black' # bazowy kolor
            width[(x,y)] = 1 #bazowa gruboœæ
           
def distance(x, y) -> int: #zwraca dystans miedzy 2 nodes
    pos_x = pos[x]
    pos_y = pos[y]
    return round((np.linalg.norm(pos_x - pos_y)), 2)

def edge_labels_repair(edge): #dodanie krawdzi odwrotych ((1,2) -> (2,1))
    edge_new = edge.copy()
    for x in edge:
        edge_new[x[1],x[0]] = edge_new[x[0],x[1]]
    return edge_new

graph_edges() #stworzenie wierzcholkow i krawedzi 
#width edge
nx.set_edge_attributes(G, width, 'width')

#colors edge
nx.set_edge_attributes(G, colors_egdes, 'color')

#distance
edge_distance = nx.get_edge_attributes(G, 'dis')

#colors nodes
nx.set_node_attributes(G, colors_nodes, 'color')

#start point
start_point = random.randint(1,len(G.nodes)) #losowanie punktu startowego
G.nodes[start_point]['color'] = "red" #ustawienie koloru startowego node

#draw
fig = plt.figure() 
nx.draw(G, pos=pos, with_labels=True, 
        edge_color=[G.edges[edge]['color'] for edge in G.edges()],
        node_color=[G.nodes[node]['color'] for node in G.nodes()],
        width=[G.edges[edge]['width'] for edge in G.edges()])
if wartosc: nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_distance)

edge_distance_anim = edge_labels_repair(edge_distance)

##############ANIMACJA##################
path = [start_point] #lista sciezki algorytmu

def animate(frame):#przyjmuje jako arg nr klatki animacji
    if frame < 3: return

    fig.clear() 

    if len(path) == len(G.nodes): #wrocenie na pocztek -> path ma juz wszystkie node
        G.edges[path[-1],path[0]]['color'] = 'green' #pomalowanie krawedzi
        G.edges[path[-1],path[0]]['width'] = 6 #pogrubienie krawedzi
        nx.draw(G, pos=pos, with_labels=True, 
                edge_color=[G.edges[edge]['color'] for edge in G.edges()],
                node_color=[G.nodes[node]['color'] for node in G.nodes()],
                width=[G.edges[edge]['width'] for edge in G.edges()])

        if wartosc: nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_distance)
        print((path[-1],path[0])) #debug

        result = 0 #wynik koncowy
        for x in path: #sumowanie
            index_x = path.index(x)
            if x == path[-1]: 
                result = result + edge_distance_anim[path[-1],path[0]]
                break
            result = result + edge_distance_anim[x, path[index_x+1]]

        print(f"Laczna droga: {result}") #wyswietlenei wyniku
   
    else:
        min_edge_key = min([key for key in edge_distance_anim.keys() #znalezienie krawedzi ktora nalezy pomalowac
                            if key[0] == path[-1] and key[1] not in path], 
                           key=edge_distance_anim.get)

        G.edges[min_edge_key]['color'] = 'green' #pomalowanie krwedzi
        G.nodes[min_edge_key[1]]['color'] = "green" #pomalowanie node
        G.edges[min_edge_key]['width'] = 6 #pogrubienie krawedzi

        path.append(min_edge_key[1]) #dodanie node do sciezki

        print(min_edge_key) #debug

        nx.draw(G, pos=pos, with_labels=True, 
            edge_color=[G.edges[edge]['color'] for edge in G.edges()],
            node_color=[G.nodes[node]['color'] for node in G.nodes()],
            width=[G.edges[edge]['width'] for edge in G.edges()])
        if wartosc: nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_distance)

ani = animation.FuncAnimation(fig, animate, frames=len(G.nodes)+3, interval=300, repeat=False)
#fig - obraz do animacji
#func - funkcja która bêdzie wywo³ywana na ka¿dym kroku animacji i generuje kolejne klatki
#frames - okresla klatki ktore maja byc rysowane, animacja sklada sie z frames = ... klatek
#interval - czas jednej klatki
#repeat - brak zakonczenia po jednym cyklu

plt.show()