import networkx as nx
import random
import numpy as np
import time
import sys

#######SETUP####################################

#Pobranie od uzytkownika ilosc wierzcholkow

for nodes in range(12, 26, 1):
    G = nx.Graph()#tworzenie grafu

    for t in range(nodes):
        G.add_node(t)#dodanie wierzcholkow

    pos = nx.random_layout(G) #zapisanie pozycji losowych

    def distance(x, y) -> int: #zwraca dystans miedzy 2 nodes
        pos_x = pos[x]
        pos_y = pos[y]
        return np.linalg.norm(pos_x - pos_y)

    for x in range(nodes-1):
        for y in range(x+1, nodes):
            G.add_edge(x,y,dis = distance(x,y))#dodanie krawedzi kazdy z kazdym wraz z roznica odleglosci

    def edge_labels_repair(edge): #dodanie krawdzi odwrotych ((1,2) -> (2,1))
        edge_new = edge.copy()
        for x in edge:
            edge_new[x[1],x[0]] = edge_new[x[0],x[1]]
        return edge_new

    #distance
    #slownik: (node1, node2) = distance ...
    edge_distance = nx.get_edge_attributes(G, 'dis')

    #dodanie krawedzi odwrotnych
    edge_dis= edge_labels_repair(edge_distance)

    #start point
    start_point = random.randint(0,len(G.nodes)) #losowanie punktu startowego

    #debug
    print(f"Ilosc Node: {nodes}, Starting Node: {start_point}")

    print("\n###ALGORYTM_NAJBLIZSZEGO_SASIADA###\n")

    path = [start_point] #droga z elementem startowym
    result = 0 #laczny dystans

    time.sleep(1)

    #Time start
    start = time.time() * 1000

    for n in range(nodes):
        if len(path) == len(G.nodes):
            #dla zakonczenia

            result = 0 #wynik koncowy
            for x in path: #sumowanie
                if x == path[-1]: 
                    result = result + edge_dis[tuple((x, path[0]))]
                    break
                result = result + edge_dis[x, path[path.index(x) + 1]]

            #Time stop
            stop = time.time() * 1000

            print(f"Droga: {path}")
            print(f"Laczna droga: {result}, Czas: {stop - start}") #wyswietlenie wyniku
            print(f"Zlozonosc pamiecowa: {sys.getsizeof(result) + sys.getsizeof(path)}\n")

        else:
            #dla kazdego innego przypadku

            #znalezienie klucza (node1, node2) ktorego krawedz ma 
            #najmniejsza odleglosc i zaczyna sie od ostatniego znaku w path[] i 
            #node2 nie nalezy w path[]
            min_edge_key = min([key for key in edge_dis.keys()
                                if key[0] == path[-1] and key[1] not in path], 
                               key=edge_dis.get)

            path.append(min_edge_key[1]) #dodanie node do sciezki

            #print(min_edge_key) #debug

    if len(list(G.nodes)) < 12:

        print("\n###ALGORYTM_DOKlADNY###\n")
        import itertools

        min_result = 100 #najlepsze rozwiazanie

        vertices = list(G.nodes) #lista wierzcholkow
        vertices.remove(start_point) #wyrzucenie wierzcholka startowego

        #Time start
        start_2 = time.time() * 1000

        for path in list(itertools.permutations(vertices)): #dla kazdej permutacji (drogi)

            path = (start_point,) + path #dodanie do drogi wierzcholka poczatkowego na poczatek listy
            result_2 = 0 #obecna dlugosc drogi

            for x in path: #obliczenie lacznej drogi dla danego path
                if x == path[-1]: 
                    result_2 = result_2 + edge_dis[tuple((x,path[0]))]
                    break
                result_2 = result_2 + edge_dis[tuple((x,path[path.index(x) + 1]))]

            if min_result > result_2: 
                min_result = result_2
                result_path = path

        #Time stop
        stop_2 = time.time() * 1000

        print(f"Droga: {result_path}")
        print(f"Laczna droga: {min_result}, Czas: {stop_2 - start_2}") #wyswietlenei wyniku
        print(f"Zlozonosc pamieciowa: {sys.getsizeof(list(itertools.permutations(vertices))) + sys.getsizeof(min_result) + sys.getsizeof(result_2)}\n")
        print(f"Dokladnosc algorytmu zachlannego: {100-(((result - min_result) / min_result) * 100)}%")

input()

