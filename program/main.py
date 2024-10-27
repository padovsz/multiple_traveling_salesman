import math 
import matplotlib.collections as mp
import matplotlib.pyplot as pt
import random 

n_cities    = 71
n_caixeiros = 5

# função para criar uma matriz de coordenadas aleatórias
# desenvolvida caso não existam as coordenadas das cidades
def matriz_coordinates(number):
    coordinates = []

    for i in range(number):
        line = []
        x = random.randint(1,100)
        y = random.randint(1,100)
        line.append(x)
        line.append(y)
        coordinates.append(line)

    return coordinates

matriz_c = [ [500, 500], [731, 587], [101,  29], [249, 645], [230,  56], [986, 130], [66 , 859], [389, 311], 
             [586, 672], [787, 726], [544, 949], [13 , 154], [191, 859], [703, 639], [122, 503], [187, 910], 
             [582, 916], [653, 995], [898, 742], [730, 148], [53 , 545], [150, 458], [70 , 293], [970, 112], 
             [540, 301], [986, 233], [969,  86], [445, 721], [349, 459], [675, 127], [109, 816], [371, 141], 
             [413, 541], [189, 473], [470, 231], [837, 517], [57 , 143], [872, 328], [988, 471], [76 , 142], 
             [793, 758], [625, 780], [311, 542], [755, 356], [107, 474], [72 , 276], [710, 225], [997, 678], 
             [474, 250], [775, 632], [220, 850], [330, 818], [73 , 106], [582, 689], [483,  99], [264, 821], 
             [152, 700], [929, 976], [901, 783], [983, 421], [316, 189], [866, 396], [179, 848], [457, 154], 
             [502, 772], [521, 260], [164, 787], [378,   5], [25 , 507], [919, 420], [414, 761], [799, 421]]


# função cujo objetivo é calcular de acordo com os dados 
# da matriz de coordenadas as distâncias entre as cidades.
def matriz_distances(number, matriz): 
    distances = [] # irá armazenar todas as distâncias entre as cidades

    for i in range(number):
        line = [] # armazena as distâncias relativas a uma cidade 
        for o in range(number):
            if(o == i):
                line.append(0) # faz com que a distância entre a cidade e ela mesma seja sempre zero 
            else:
                distancia = math.sqrt( # calcula a distância euclidiana entre as cidades 
                    (matriz[i][0] - matriz[o][0])**2 + 
                    (matriz[i][1] - matriz[o][1])**2
                    )
                line.append(round(distancia)) # adiciona os números arredondados das distâncias 
        distances.append(line) 

    return distances

matriz_d = matriz_distances(n_cities, matriz_c)
print(matriz_d)

def nearest_neighbor_heuristic(startingCity):
    tour = [startingCity]
    unvisited = list (range(0,n_cities)) # lista de cidades não visitadas
    unvisited.remove(startingCity)

    while unvisited:
        next_city = min(unvisited, key = lambda candidate : matriz_d[tour[-1]][candidate]) # a função lambda deverá ser a responsável para determinar qual vai ser a cidade não visitada escolhida
        tour.append(next_city) # adiciona a cidade mais próxima ao tour para criar o caminho
        unvisited.remove(next_city) # remove da lista unvisited a próxima cidade

    return tour

def get_total_distance(tour):
    total_distance = 0 
    for i in range(n_cities - 1): # o -1 é necessário por conta que se o for tentar encontrar algum elemento que não esteja na lista , vai dar erro
        total_distance = total_distance + matriz_d[tour[i]][tour[i+1]]

    total_distance = total_distance + matriz_d[tour[-1]][tour[0]]
    return total_distance

def find_the_first_city(): # metódo para achar a cidade que serviria como a melhor cidade para iniciar o caminho
    distances = []
    cities = None 

    for i in range(cities-1): # dentro deste for, os melhores caminhos serão calculados partindo de todas as cidades e armazenados em distances 
        tour = nearest_neighbor_heuristic(i)
        distances.append(tour)
    
    smaller = distances[0]
    for o in range(len(distances)): #esse for irá comparar todas as distâncias totais referentes as diferentes opções de caminho e assim, vai determinar qual a melhor cidade para começar
        distance = get_total_distance(distances[o])
        if distance < smaller:
            cities = o
            smaller = distance 

    return cities 

def find_the_furthest_city(indiceStartingCity,unvisited): #esse metódo irá definir qual a cidade mais distante da cidade que os caixeiros começaram a sair. 
    city = 0
    distance = 0

    for i in range(len(unvisited)):
        indice = unvisited [i]
        d = matriz_d[indiceStartingCity][indice]
        if d > distance:
            city = indice
            distance = d

    return city 

def number_cities_per_caixeiro(cities, caixeiros): # determina qual será o número que cidades que cada caixeiro deve visitar
    chosen = cities - 1 
    cities_per_caixeiro = chosen // caixeiros  
    unvisited = chosen % caixeiros

    list_caixeiros = [cities_per_caixeiro] * caixeiros

    for i in range(unvisited):
        list_caixeiros[i] += 1

    return list_caixeiros

list_cities = number_cities_per_caixeiro(n_cities, n_caixeiros)
print(list_cities)  

def find_the_two_nearest_cities(indice, unvisited):
    if len(unvisited) == 1:
        return [unvisited[0], unvisited[0]]  # Retorna a mesma cidade duas vezes se houver apenas uma cidade não visitada
    else:
        distances = []
        for i in range(len(unvisited)):
            ind = unvisited[i]
            distances.append(matriz_d[indice][ind])
        sorted_distances_with_indices = sorted(enumerate(distances), key=lambda x: x[1])

        nearest_cities = []
        for city_index, distance in sorted_distances_with_indices[0:2]:
            nearest_cities.append(city_index)
        return nearest_cities


def average_between_two_cities(ind1,ind2):
    x1 = matriz_c [ind1] [0]
    x2 = matriz_c [ind2] [0]
    y1 = matriz_c [ind1] [1]
    y2 = matriz_c [ind2] [1]
    average = [] 
    mediaX = round((x1 + x2) / 2)
    mediaY = round((y2 + y1) / 2)
    average.append(mediaX)
    average.append(mediaY)
    return average

def average_between_cities(visited):
    average = []
    mediaX = 0
    mediaY = 0 
    for i in range(len(visited)-1):
        indice = visited[i]
        mediaX = mediaX + matriz_c [indice] [0]
        mediaY = mediaY + matriz_c [indice] [1]
    mediaX = round(mediaX / len(visited))
    mediaY = round(mediaY / len(visited))
    average.append(mediaX)
    average.append(mediaY)
    return average


def get_the_nearest_city(average, unvisited):
    nearest = 0
    smaller = math.inf  # declara como valor incial da várivael infinito
    
    for i in range(len(unvisited)):
        ind = unvisited [i]
        distancia = math.sqrt((average[0] - matriz_c[ind][0])**2 + (average[1] - matriz_c[ind][1])**2)
        if distancia < smaller:
            nearest = ind
            smaller = distancia  
    return nearest

def get_next_city(indice,unvisited):
    smaller = math.inf
    city = 0

    for i in range(len(unvisited)):
        ind = unvisited[i]
        d = matriz_d[indice][ind]
        if d < smaller and d != 0:
            smaller = d
            city = ind

    return city

def get_distance(ind1,ind2):
    distancia = math.sqrt( # calcula a distância euclidiana entre as cidades 
                    (matriz_c[ind1][0] - matriz_c[ind2][0])**2 + 
                    (matriz_c[ind2][1] - matriz_c[ind2][1])**2
                    )
    return distancia 
    
def create_the_path():
    unvisited = []
    totaldistance = 0
    lastcity = 0
    distribution = [] # váriavel que será responsável por informar quais cidades foram vistadas por cada caixeiro

    for i in range(n_cities): # adiciona a uma váriavel todas os indices das cidades que tem que ser visitadas 
        unvisited.append(i)
    
    unvisited.remove(0) 

    for o in range(n_caixeiros):
        number = list_cities[o]
        cities = [0]
        lastcity = 0 
        for j in range(number):
            if j == 0:
                furthest = find_the_furthest_city(lastcity,unvisited)
                next = find_the_two_nearest_cities(furthest,unvisited)
                city1 = next[0]
                city2 = next[1]
                average = average_between_two_cities(city1,city2)
                next_city = get_the_nearest_city(average,unvisited)
                cities.append(next_city)
                unvisited.remove(next_city)
                totaldistance = totaldistance + get_distance(lastcity,next_city)
                lastcity = next_city
            else:
                average = average_between_cities(cities)
                next_city = get_the_nearest_city(average, unvisited)
                cities.append(next_city)
                unvisited.remove(next_city)
                totaldistance = totaldistance + get_distance(lastcity,next_city)
                lastcity = next_city 

            if j == number-1:
                totaldistance = totaldistance + get_distance(lastcity,0)
                
        distribution.append(cities)
                
    return totaldistance, distribution


result = create_the_path()
print (result[0])
print (result[1])