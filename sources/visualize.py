#!/usr/bin/env python3

from tkinter import Tk, Canvas, Toplevel, Scale, Label, Entry, HORIZONTAL
from random import randint
from sys import argv
from threading import Thread
from signal import signal, SIGINT
from colorsys import hls_to_rgb

class VisualizerTk(Thread):
    def generate_random_color(self, p, pp):
        c2 = [p / pp, 0.5, 1]
        c2 = hls_to_rgb(*c2)
        c2 = list(map(lambda x: int(255.9* x), c2))
        return "#%02x%02x%02x" % tuple(map(int, c2))

    def generate_color_list(self, players_cnt):
        if players_cnt == 2:
            return ["red", "blue"]
        return [self.generate_random_color(_, players_cnt) for _ in range(players_cnt)]
    
    def get_cell(self, x, y):
        return (-y + self.a, x + self.a)

    def get_crds(self, x, y):
        return (self.cx + self.dx * x, self.cy - self.dy * y)

    def fill(self, x, y, col):
        fx, fy = self.get_crds(x, y)
        self.cnv.create_rectangle(fx - self.dx / 2 + self.ddx, fy - self.dy / 2 + self.ddy, fx + self.dx / 2 - self.ddx, fy + self.dy / 2 - self.ddy, outline=col, fill=col)

    def redraw(self, tsize):
        self.cnv.delete("all")
        self.dx = (self.maxc - self.mixc) / (2 * tsize + 1)
        self.dy = (self.mayc - self.miyc) / (2 * tsize + 1)
        self.ddx, self.ddy = self.dx / 10, self.dy / 10
        for i in range(-tsize - 1, tsize + 1):
            x, y = self.get_crds(i, i)
            self.cnv.create_line(x + self.dx / 2, self.miyc, x + self.dx / 2, self.mayc)
            self.cnv.create_line(self.mixc, y - self.dy / 2, self.maxc, y - self.dy / 2)
        for x in range(-tsize, tsize + 1):
            for y in range(-tsize, tsize + 1):
                i, j = self.get_cell(x, y)
                color = None
                if self.tab[i][j] == -1:
                    color = self.wall_color
                elif self.tab[i][j] > 0:
                    color = self.colors[self.tab[i][j] - 1]
                if color:
                    self.fill(x, y, color)

    def redraw_score(self, select_best=False):
        self.scr.delete("all")
        pa = self.SH / 100
        wi, he = self.SW / 2, self.scfont * 2
        self.scr.create_line(self.SW / 2 - wi / 2, pa, self.SW / 2 - wi / 2, pa + he * self.k)
        self.scr.create_line(self.SW / 2 + wi / 2, pa, self.SW / 2 + wi / 2, pa + he * self.k)
        x = self.SW / 2 - wi / 2
        y = pa
        self.scr.create_line(x, y, x + wi, y)
        best_score = max(self.scores)
        for i in range(self.k):
            if self.scores[i] < best_score or not select_best:
                self.scr.create_text(x + wi / 2, y + he / 2, text=str(self.scores[i]), fill=self.colors[i], font=("Helvetica", self.scfont))
            else:
                self.scr.create_rectangle(x, y, x + wi, y + he, fill="black")
                self.scr.create_text(x + wi / 2, y + he / 2, text=str(self.scores[i]), fill="white", font=("Helvetica", self.scfont))
            y += he
            self.scr.create_line(x, y, x + wi, y)


    def process(self):
            num, x, y = inp[0], inp[1], inp[2]
            i, j = self.get_cell(x, y)
            self.tab[i][j] = num
            self.fill(x, y, self.colors[num - 1])
            self.scores[num - 1] += 1
            self.redraw_score()
        elif inp[0] == -1:
            self.ts += 1
            self.redraw(self.ts)
            ni = list(map(int, self.file.readline().split()))
            while ni[0] != -1:
                x, y = ni[1], ni[2]
                i, j = self.get_cell(x, y)
                self.tab[i][j] = -1
                self.fill(x, y, self.wall_color)
                ni = list(map(int, self.file.readline().split()))
        elif inp[0] == -2:
            ni = list(map(int, self.file.readline().split()))
            while ni[0] != -2:
                num, x, y = ni[0], ni[1], ni[2]
                i, j = self.get_cell(x, y)
                if self.tab[i][j] > 0:
                    self.scores[self.tab[i][j] - 1] -= 1
                self.tab[i][j] = num
                self.scores[num - 1] += 1
                self.fill(x, y, self.colors[num - 1])
                ni = list(map(int, self.file.readline().split()))
            self.redraw_score()
        else:
            self.redraw_score(select_best=True)
            return
        ms = self.speed.get()
        self.cnv.after(ms, self.process)

    def space_handler(self, event):
        if not self.check:
            self.check = True
            self.process()

    def exit(self):
        self.master.quit()
        self.master.update()
    
    def run(self):
        self.min_ms, self.max_ms = 1, 200
        if "--help" in argv:
            print(f"Usage:\n {argv[0]} log.txt [ms [scfont]]")
            self.exit()
        if len(argv) in {2, 3, 4}:
            self.path = argv[1]
            self.ms = (self.min_ms + self.max_ms) / 2 if len(argv) == 2 else int(argv[2])
            self.scfont = 18 if len(argv) <= 3 else int(argv[3])
            if not self.min_ms <= self.ms <= self.max_ms:
                print(f"ms violates [{self.min_ms}, {self.max_ms}]\n")
                self.exit()
        else:
            print(f"Incorrect option\nUse {argv[0]} --help to view usage information")
            self.exit()

        self.file = open(self.path, "r")
        self.t, self.n, self.p, self.k, self.a = map(int, self.file.readline().split())
        self.a //= 2
        self.tab = [[0 for _ in range(2 * self.a + 1)] for _ in range(2 * self.a + 1)]
        for i in range(2 * self.a + 1):
            arr = list(map(int, self.file.readline().split()))
            for j in range(2 * self.a + 1):
                self.tab[i][j] = arr[j]

        self.wall_color = "black"
        self.colors = self.generate_color_list(self.k)
        self.scores = [0 for _ in range(self.k)]
        self.ids = [-1 for _ in range(self.k)]

        self.master = Tk()
        self.master.title("Визуализация")
        self.W, self.H = self.master.winfo_screenwidth() * 0.9, self.master.winfo_screenheight() * 0.9
        self.W = min(self.W, self.H)
        self.H = self.W
        self.cnv = Canvas(master=self.master, width=self.W, height=self.H)

        self.scores_master = Toplevel(self.master)
        self.scores_master.title("Счёт")

        self.SW, self.SH = self.W * 0.3, self.H

        self.scr = Canvas(self.scores_master, width=self.SW, height=self.SH)

        self.mixc, self.miyc, self.maxc, self.mayc = self.W / 100, self.H / 100, self.W - self.W / 100, self.H - self.H / 100
        self.cx, self.cy = (self.mixc + self.maxc) / 2, (self.miyc + self.mayc) / 2
        self.dx, self.dy = (self.maxc - self.mixc) / (2 * self.n + 1), (self.maxc - self.mixc) / (2 * self.n + 1)
        self.ddx, self.ddy = self.dx / 10, self.dy / 10

        self.lsp = Label(self.scores_master, text="Speed")

        self.speed = Scale(self.scores_master, from_=self.max_ms, to=self.min_ms, orient=HORIZONTAL)
        self.speed.set((self.min_ms + self.max_ms) / 2)

        self.lsp.pack()
        self.speed.pack()

        self.cnv.pack()
        self.scr.pack()

        self.ts = self.n
        self.redraw(self.n)
        self.redraw_score()

        self.check = False
        self.master.bind("<space>", self.space_handler)
        self.cnv.mainloop()

def sigint_handler(sig, frame):
    app.exit()

app = VisualizerTk()

signal(SIGINT, sigint_handler)

app.start()
