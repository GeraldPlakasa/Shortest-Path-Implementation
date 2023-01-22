"""
    PROGAM SIMULASI PENCARIAN SEDERHANA
    Copyright@2021 - abdiansah@unsri.ac.id
"""

import pygame
import collections
import numpy as np

class UI:
    __screen = None
    __map = None
    __alg = None
    __width, __height = 640*2, int(480*1.5)
    __running = True
    __enemy = None
    __enemypos = [15, 15]
    __player = None
    __playerpos = [95, 95]
    __path = []

    def __init__(self, peta, alg):
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__map = peta
        self.__alg = alg
        self.__set_props()

    def __set_field(self):
        myfont = pygame.font.SysFont('Comic Sans MS', 15)
        a2d_map = self.__map.get_2d_map()
        y = 0
        for i in range(self.__map.get_baris()):
            x = 0
            for j in range(self.__map.get_kolom()):
                if str(a2d_map[i][j]) == '#' :

                    pygame.draw.rect(self.__screen, "#cccccc",(x, y, 80, 80))
                    pygame.draw.rect(self.__screen, "#000000",(x, y, 80, 80),1)
                    textsurface = myfont.render(str(a2d_map[i][j]), False, (0, 0, 0))
                    self.__screen.blit(textsurface,(x+65,y+55))
                else:
                    pygame.draw.rect(self.__screen, "#000000",(x, y, 80, 80),1)
                    textsurface = myfont.render(str(a2d_map[i][j]), False, (0, 0, 0))
                    self.__screen.blit(textsurface,(x+65,y+55))
                x += 80
            y += 80
        self.__screen.blit(self.__enemy, self.__enemypos)
        self.__screen.blit(self.__player, self.__playerpos)

    def __set_props(self):
        a1d_map = self.__map.get_1d_map()
        a1d_map_koor = list(self.__map.get_1d_map_koor())

        self.__enemy = pygame.image.load("enemy.png")
        self.__enemy = pygame.transform.smoothscale(self.__enemy, (50, 50))
        idx = np.where(a1d_map == "P")
        posisi = a1d_map_koor[idx[0][0]]

        x = 15 + (80*posisi[0])
        y = 15 + (80*posisi[1])
        self.__enemypos = [x,y]

        self.__player = pygame.image.load("player.png")
        self.__player = pygame.transform.smoothscale(self.__player, (50, 50))
        
        idx = np.where(a1d_map == "T")
        posisi = a1d_map_koor[idx[0][0]]

        x = 15 + (80*posisi[0])
        y = 15 + (80*posisi[1])
        x, y = y, x 
        self.__playerpos = [x,y]
    
    def __search(self):
        x = 15 + (80*self.__map.get_kolom())
        myfont = pygame.font.SysFont('Arial', 60)
        textsurface = myfont.render("Proses", False, (0, 0, 0))
        self.__screen.blit(textsurface,(x+125,30))

        for i in range(len(self.__path)-1):
            # self.__draw_line(self.__path[i], self.__path[i+1])
            if i > 0 :
                self.__draw_circle(self.__path[i])

            if i < int((len(self.__path)*30)/100):
                textsurface = myfont.render('.', False, (0, 0, 0))
            elif i < int((len(self.__path)*60)/100):
                textsurface = myfont.render('..', False, (0, 0, 0))
            else:
                textsurface = myfont.render('...', False, (0, 0, 0))

            self.__screen.blit(textsurface,(x+275,30))

            pygame.time.wait(70)
            pygame.display.update()
            pygame.time.wait(70)
        return True

    def __bsf(self):
        return self.__alg.bfs(self.__map.ambil_graf(), (0, 0))
    
    def __dsf(self):
        return self.__alg.dfs(self.__map.ambil_graf(), (0, 0))

    def __get_path_final(self, path):
        path_nilai = self.__map.ambil_path_nilai(path)

        path_akhir = []
        for p in path_nilai:
            if p == 'T':
                path_akhir.append(p)
                break
            path_akhir.append(p)

        idx = path_nilai.index("T")
        path_akhir_koor = [path[i] for i in range(idx+1)]
        return path_akhir_koor

    def __draw_line(self, awal, tujuan):
        x1 = 35 + (80*awal[0])
        y1 = 35 + (80*awal[1])
        x1, y1 = y1, x1
        p1 = [x1,y1]
        x2 = 35 + (80*tujuan[0])
        y2 = 35 + (80*tujuan[1])
        x2, y2 = y2, x2
        p2 = [x2,y2]
        pygame.draw.line(self.__screen, "#d63413", p1, p2, 2)

    def __draw_circle(self, titik):
        x = 40 + (80*titik[0])
        y = 40 + (80*titik[1])
        x, y = y, x
        p1 = [x,y]
        pygame.draw.circle(self.__screen, "#cfcfcf", p1, 20)

    def __set_button_bsf(self):
        x = 15 + (80*self.__map.get_kolom())
        button = pygame.Rect(x+90, 20, 145, 50)
        myfont = pygame.font.SysFont('Arial', 20)
        textsurface = myfont.render("Search BSF", False, (0, 0, 0))
        self.__screen.blit(textsurface,(x+115, 30))
        return button

    def __set_button_dsf(self):
        x = 15 + (80*self.__map.get_kolom())
        button = pygame.Rect(x+90, 90, 145, 50)
        myfont = pygame.font.SysFont('Arial', 20)
        textsurface = myfont.render("Search DSF", False, (0, 0, 0))
        self.__screen.blit(textsurface,(x+115, 100))
        return button

    # def __bsf_search(self, graph, root):
    #     visited, queue = set(), collections.deque([root])
    #     visited.add(root)
    #     path = []
    #     i = 0

    #     while queue:
    #         vertex = queue.popleft()
    #         path.append(vertex)
    #         if len(path) > 1:
    #             self.__draw_line(self.__path[i], self.__path[i+1])
    #             pygame.time.wait(100)
    #             pygame.display.update()
    #             pygame.time.wait(100)
    #         for neighbour in graph[vertex]:
    #             if neighbour not in visited:
    #                 visited.add(neighbour)
    #                 queue.append(neighbour)
    #         i += 1
    #     return True

    # def __draw_graf(self):
    #     x = 15 + (80*self.__map.get_kolom())
    #     myfont = pygame.font.SysFont('Comic Sans MS', 15)
    #     textsurface = myfont.render("0,0", False, (0, 0, 0))
    #     pygame.draw.circle(self.__screen, "#d63413", (x+312, 32), 20, 2)
    #     self.__screen.blit(textsurface,(x+300,20))

    def run(self):

        search_done = True
        # path = self.__bsf()
        # self.__path = self.__get_path_final(path)
        alg_pilihan = "-"

        while(self.__running):
            self.__screen.fill("#ffffff")
            self.__set_field()
            # self.__draw_graf()
            if alg_pilihan == 'bsf':
                path = self.__bsf()
            elif alg_pilihan == 'dsf':
                path = self.__dsf()
            else:
                path = []

            if not search_done:
                self.__path = self.__get_path_final(path)
                search_done = self.__search()
                # search_done = self.__bsf_search(self.__map.ambil_graf(),(0, 0))
            button_bsf = self.__set_button_bsf()
            button_dsf = self.__set_button_dsf()
            pygame.draw.rect(self.__screen, "#000000", button_bsf, 2, 3)
            pygame.draw.rect(self.__screen, "#000000", button_dsf, 2, 3)
            
            pygame.display.flip()
            # pygame.time.wait(1000)
            # self.__screen.fill("#d63413")
            # pygame.display.update()
            # pygame.time.wait(1000)
            

            for event in pygame.event.get():
                # event saat tombol exit diklik
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button

                    if button_bsf.collidepoint(mouse_pos):
                        search_done = False
                        alg_pilihan = 'bsf'

                    if button_dsf.collidepoint(mouse_pos):
                        search_done = False
                        alg_pilihan = 'dsf'