"""
    PROGAM SIMULASI PENCARIAN SEDERHANA
    Copyright@2021 - abdiansah@unsri.ac.id
"""

import collections
import numpy as np
from ui import UI

class Map:

    __file_map = ''
    __baris = 0
    __kolom = 0
    __a2d_map = None
    __a1d_map = None
    __a1d_map_koor = []
    __graf = None
    tes = []

    def __init__(self):
        print('')

    # fungsi buat map dari dalam file menjadi list
    def buat_map(self, file_map):
        self.__file_map = file_map
        self.__baris, self.__kolom = self.__get_dimensi(file_map)

        f_map = open(file_map)
        a_map = f_map.read()
        a_map = [a for a in a_map if a != '\n']
        a_map = np.array(a_map)
        # map versi 1 dimensi
        self.__a1d_map = a_map
        # map versi 2 dimensi
        self.__a2d_map = a_map.reshape(self.__baris, self.__kolom)

    def tampilkan_map(self):
        print(f'File Map\t: {self.__file_map}')
        print(f'Ukuran Map\t: {self.__baris} X {self.__kolom} - (baris x kolom)')
        print(f'{self.__a2d_map}\n')

    def __get_dimensi(self, file_map):
        f_map = open(file_map)
        a_map = f_map.read().split()
        baris = len(a_map)
        kolom = len(a_map[0])
        return (baris, kolom)

    def ambil_nilai(self, no_baris, no_kolom):
        return self.__a2d_map[no_baris, no_kolom]

    def ambil_path_nilai(self, path):
        return [self.ambil_nilai(n[0], n[1]) for n in path]

    def __valid_koordinat(self, no_baris, no_kolom):
        if (no_baris >=0) and (no_baris < self.__baris) and (no_kolom >=0) and (no_kolom < self.__kolom):
            return True
        else:
            return False

    def __ambil_tetangga(self, no_baris, no_kolom):
        tetangga = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ((no_baris + i) != no_baris) or ((no_kolom + j) != no_kolom):
                    nbt, nkt = (no_baris+i, no_kolom+j) # nbt:nomor_baris_tetangga, nbk:no_kolom_tetangga
                    if self.__valid_koordinat(nbt, nkt):
                        if self.ambil_nilai(nbt, nkt) != '#':
                            tetangga.append((nbt, nkt))
        return tetangga

    def buat_graf(self):
        self.__graf = {}
        b, k = (0, 0)
        for b in range(self.__baris):
            for k in range(self.__kolom):
                if self.ambil_nilai(b, k) != '#':
                    tetangga = self.__ambil_tetangga(b, k)
                    self.__graf[(b, k)] = tetangga  # {'0': ['1', '2', '3'], '1': ['0', '2']}

    def tampilkan_graf_koordinat(self):
        print(f'Tampilan Graf Koordinat')
        for key in self.__graf:
            print(f'{key} : {self.__graf[key]}')

    def tampilkan_graf_nilai(self):
        print(f'Tampilan Graf Nilai')
        for key in self.__graf:
            node = map.ambil_nilai(key[0], key[1])
            tetangga = [map.ambil_nilai(v[0], v[1]) for v in self.__graf[key]]
            print(f'{node} : {tetangga}')

    def set_map_koor(self):
        for r in range(len(self.__a2d_map)):
            for c in range(len(self.__a2d_map[r])):
                self.__a1d_map_koor.append([r, c])

    def set_new_graf(self, path):

        graf = self.__graf.copy()
        keys = graf.keys()
        keys_removed = []

        for key in keys:
            if key not in path:
                keys_removed.append(key)

        for key in keys_removed:
            graf.pop(key)

        for k in keys_removed:
            for a in graf:
                if k in graf[a]:
                    graf[a].remove(k)

        self.__graf = graf

    def ambil_graf(self):
        return self.__graf

    def get_baris(self):
        return self.__baris

    def get_kolom(self):
        return self.__kolom

    def get_2d_map(self):
        return self.__a2d_map

    def get_1d_map(self):
        return self.__a1d_map

    def get_1d_map_koor(self):
        return self.__a1d_map_koor

class Algoritme:

    def __init__(self):
        print('')

    # BFS algorithm (sumber: https://www.programiz.com/dsa/graph-bfs)
    def bfs(self, graph, root):
        visited, queue = set(), collections.deque([root])
        visited.add(root)
        path = []

        while queue:
            vertex = queue.popleft()
            path.append(vertex)
            for neighbour in graph[vertex]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
        return path

    # DFS algorithm 
    # (sumber: https://rinagustiana.medium.com/implementasi-depth-first-search-dfs-dan-breadth-first-search-bfs-pada-python-62afe680925d)
    # code dari sumber + modifikasi
    def dfs(self, graph, node, visited=None):
        if visited is None:
            visited = []
        
        if node not in visited:
            visited.append(node)
            for neighbour in graph[node]:
                self.dfs(graph, neighbour, visited)
        return visited

    def backt(self, graph, node, visited=None):
        
        if visited is None:
            visited = []
        if node not in visited:
            visited.append(node)
            if node == (0,0):
                self.tes.append(visited)
                visited.pop(node)
            for neighbour in graph[node]:
                self.dfs(graph, neighbour, visited)
        return visited

if __name__ == '__main__':

    peta = Map()
    peta.buat_map('map-004.txt')

    peta.set_map_koor()

    peta.buat_graf()

    alg = Algoritme()
    # graf = peta.ambil_graf()

    # print('Hasil penelusuran algoritme BFS')
    # path = alg.dfs(graf, (0, 0))    # posisi mulai (P) di koordinat (0,0)

    # print(f'Path Koord.\t: {path}')

    # path_nilai = peta.ambil_path_nilai(path)
    # print(f'Path Nilai\t: {path_nilai}')

    # path_akhir = []
    # for p in path_nilai:
    #     if p == 'T':
    #         path_akhir.append(p)
    #         break
    #     path_akhir.append(p)
    # print(f'Path Akhir\t: {path_akhir}')

    # idx = path_nilai.index("T")
    # path_akhir_koor = [path[i] for i in range(idx+1)]

    # print(f'Path Akhir Koor\t: {path_akhir_koor}\n')

    # map.set_new_graf(path_akhir_koor
    # back = alg.dfs(graf, (0, 0))
    # print(back)
    # print(map.tes)

    ui = UI(peta, alg)
    ui.run()