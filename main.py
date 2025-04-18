import matplotlib.pyplot as plt
import networkx as nx

"""
GRAFOS
vertice x
aresta (x,y)

Ordenado -> Direcionado
Cíclico -> Repetir nó 

Completo -> Clique

Hamiltoniano -> chega ao destino independente
Eureoliano -> passa por todos
"""

class Grafo:

    def __init__(self, vertices, arestas, orientado = False):
        self.vertices = vertices
        self.arestas = arestas
        self.orientado = orientado
        self.content = []
        self.clear()

    # Total de vertices
    def n(self):
        return len(self.vertices)

    # Total de arestas
    def e(self):
        return len(self.arestas)

    def clear(self):
        print("Inicializando limpeza...")
        temp = []
        for vertice in self.vertices:
            if vertice not in temp:
                temp.append(vertice)
        self.vertices = temp
        temp = []
        if not self.orientado:
            for aresta in self.arestas:
                if aresta not in temp and (aresta[1], aresta[0]) not in temp:
                    temp.append(aresta)
            self.arestas = temp

    # Coleta as conexões do nó
    def vertices_conectados(self, vertice):
        r = []
        if self.orientado:
            for i in self.arestas:
                if i[0] == vertice:
                    r.append(i[1])
        else:
            for i in self.arestas:
                if i[0] == vertice:
                    if i[1] not in r:
                        r.append(i[1])
                elif i[1] == vertice:
                    if i[0] not in r:
                        r.append(i[0])
        return r

    # Coleta as conexões do nó
    def conexoes(self, vertice):
        r = []
        if self.orientado:
            for i in self.arestas:
                if i[0] == vertice:
                    r.append(i)
        else:
            for i in self.arestas:
                if i[0] == vertice and i not in r:
                    r.append(i)
                elif i[1] == vertice and i not in r:
                    r.append((i[1],i[0]))
        return r

    # Passa por todos os vértices do grafo uma única vez, sem repetir.
    def hamiltoniano(self, x, y):
        print(f"__________________Hamiltoniano_({x}->{y})__________________")
        self.content = []
        self.__hamiltoniano_rec(x, y, [x])
        print("Possible_paths: ", self.content)
        print("_____________________________________________________________")

    def __hamiltoniano_rec(self, x, y, current_path: list):
        if x == y:
            if len(current_path) == len(self.vertices):
                tem_ciclo = current_path[0] in self.vertices_conectados(current_path[-1])
                ciclo_info = "Tem ciclo" if tem_ciclo else "Não tem ciclo"
                print(f"Encontrado[{current_path}] <- {ciclo_info}")
                self.content.append(current_path.copy())
        else:
            for vertice in self.vertices_conectados(x):
                if vertice not in current_path:
                    current_path.append(vertice)
                    print(f"({x}->{vertice})", end=' ')
                    print(">", end=' ')
                    self.__hamiltoniano_rec(vertice, y, current_path)
                    print("<", end=' ')
                    current_path.pop()

    # Percorre todas as arestas do grafo exatamente uma vez
    def euleriano(self, x, y):
        print(f"__________________Euleriano_({x}->{y})__________________")
        self.content = []
        self.__euleriano_rec(x, y, [])
        print("Possible_paths: ", self.content)
        print("_____________________________________________________________")

    def __euleriano_rec(self, x, y, current_path: list):
        if len(current_path) == len(self.arestas):
            tem_circuito = current_path[0][0] == current_path[len(current_path) - 1][1]
            circuito_info = "Tem circuito" if tem_circuito else "Não tem circuito"
            print(f"Encontrado[{current_path}] <- {circuito_info}")
            self.content.append(current_path.copy())
        else:
            for conexao in self.conexoes(x):
                if conexao not in current_path and (conexao[1], conexao[0]) not in current_path:
                    current_path.append(conexao)
                    print(conexao, end='>')
                    self.__euleriano_rec(conexao[1], y, current_path)
                    print(end='<')
                    current_path.pop()

    def status(self):
        print("Vertices: ", self.vertices, "->", self.n())
        print("Arestas: ", self.arestas, "->", self.e())

    def draw(self):
        g = nx.Graph()
        g.add_nodes_from(self.vertices)
        g.add_edges_from(self.arestas)

        pos = nx.spring_layout(g)  # layout automático
        nx.draw(g, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=1500, font_size=15)
        plt.title("Representação do Grafo")
        plt.show()

if __name__ == '__main__':
    vertices = [3, 5, 10, 20]
    arestas = [(3,10), (10,20), (20,5), (10,5), (3,5), (5,10)]

    g = Grafo(vertices, arestas)
    g.status()
    g.hamiltoniano(3, 10)
    g.euleriano(5,10)
    g.draw()
