#!/usr/bin/python3

from tkinter import Tk, Canvas, Toplevel, Scale, Label, Entry, HORIZONTAL
from random import randint
from sys import argv

def generate_random_color():
    return "#%02x%02x%02x" % tuple(randint(0, 255) for _ in range(3))

def generate_color_list(players_cnt):
    if players_cnt == 2:
        return ["red", "blue"]
    return [generate_random_color() for _ in range(players_cnt)]

min_ms, max_ms = 1, 200

if "--help" in argv:
    print(f"Usage:\n {argv[0]} log.txt ms font wait\n log.txt - text file with game log,\n ms - time in milliseconds between two steps in visualization,\n font - score font,\n wait - time before visualization")
    exit(0)
if len(argv) == 5:
    path = argv[1]
    ms = int(argv[2])
    scfont = int(argv[3])
    wait = int(argv[4])
    if ms < min_ms or ms > max_ms:
        print(f"ms = {ms} violates the range [{min_ms}, {max_ms}]")
        exit(0)
else:
    print(f"Incorrect option\nUse {argv[0]} --help to view usage information")
    exit(1)

f = open(path, "r")
t, n, p, k, a = map(int, f.readline().split())
a //= 2

def get_cell(x, y):
    return (-y + a, x + a)

tab = [[0 for _ in range(2 * a + 1)] for _ in range(2 * a + 1)]
for i in range(2 * a + 1):
    arr = list(map(int, f.readline().split()))
    for j in range(2 * a + 1):
        tab[i][j] = arr[j]

wall_color = "black"
colors = generate_color_list(k)
scores = [0 for _ in range(k)]
ids = [-1 for _ in range(k)]

master = Tk()
master.title("Визуализация")
W, H = master.winfo_screenwidth() * 0.9, master.winfo_screenheight() * 0.9
W = min(W, H)
H = W
cnv = Canvas(master=master, width=W, height=H)

scores_master = Toplevel(master)
scores_master.title("Счёт")

SW, SH = W * 0.3, H

scr = Canvas(scores_master, width=SW, height=SH)

mixc, miyc, maxc, mayc = W / 100, H / 100, W - W / 100, H - H / 100
cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
dx, dy = (maxc - mixc) / (2 * n + 1), (maxc - mixc) / (2 * n + 1)
ddx, ddy = dx / 10, dy / 10

def get_crds(x, y):
    return (cx + dx * x, cy - dy * y)

def fill(x, y, col):
    fx, fy = get_crds(x, y)
    cnv.create_rectangle(fx - dx / 2 + ddx, fy - dy / 2 + ddy, fx + dx / 2 - ddx, fy + dy / 2 - ddy, outline=col, fill=col)

def redraw(tsize):
    global dx, dy, ddx, ddy, ids
    cnv.delete("all")
    dx = (maxc - mixc) / (2 * tsize + 1)
    dy = (mayc - miyc) / (2 * tsize + 1)
    ddx, ddy = dx / 10, dy / 10
    for i in range(-tsize - 1, tsize + 1):
        x, y = get_crds(i, i)
        cnv.create_line(x + dx / 2, miyc, x + dx / 2, mayc)
        cnv.create_line(mixc, y - dy / 2, maxc, y - dy / 2)
    for x in range(-tsize, tsize + 1):
        for y in range(-tsize, tsize + 1):
            i, j = get_cell(x, y)
            color = None
            if tab[i][j] == -1:
                color = wall_color
            elif tab[i][j] > 0:
                color = colors[tab[i][j] - 1]
            if color:
                fill(x, y, color)

def redraw_score(select_best=False):
    scr.delete("all")
    pa = SH / 100
    wi, he = SW / 2, scfont * 2
    scr.create_line(SW / 2 - wi / 2, pa, SW / 2 - wi / 2, pa + he * k)
    scr.create_line(SW / 2 + wi / 2, pa, SW / 2 + wi / 2, pa + he * k)
    x = SW / 2 - wi / 2
    y = pa
    scr.create_line(x, y, x + wi, y)
    best_score = max(scores)
    for i in range(k):
        if scores[i] < best_score or not select_best:
            scr.create_text(x + wi / 2, y + he / 2, text=str(scores[i]), fill=colors[i], font=("Helvetica", scfont))
        else:
            scr.create_rectangle(x, y, x + wi, y + he, fill="black")
            scr.create_text(x + wi / 2, y + he / 2, text=str(scores[i]), fill="white", font=("Helvetica", scfont))
        y += he
        scr.create_line(x, y, x + wi, y)


def process():
    global ts
    inp = list(map(int, f.readline().split()))
    if inp[0] > 0:
        num, x, y = inp[0], inp[1], inp[2]
        i, j = get_cell(x, y)
        tab[i][j] = num
        fill(x, y, colors[num - 1])
        scores[num - 1] += 1
        redraw_score()
    elif inp[0] == -1:
        ts += 1
        redraw(ts)
        ni = list(map(int, f.readline().split()))
        while ni[0] != -1:
            x, y = ni[1], ni[2]
            i, j = get_cell(x, y)
            tab[i][j] = -1
            fill(x, y, wall_color)
            ni = list(map(int, f.readline().split()))
    elif inp[0] == -2:
        ni = list(map(int, f.readline().split()))
        while ni[0] != -2:
            num, x, y = ni[0], ni[1], ni[2]
            i, j = get_cell(x, y)
            if tab[i][j] > 0:
                scores[tab[i][j] - 1] -= 1
            tab[i][j] = num
            scores[num - 1] += 1
            fill(x, y, colors[num - 1])
            ni = list(map(int, f.readline().split()))
        redraw_score()
    else:
        redraw_score(select_best=True)
        return
    ms = speed.get()
    cnv.after(ms, process)

lsp = Label(scores_master, text="Speed")

speed = Scale(scores_master, from_=max_ms, to=min_ms, orient=HORIZONTAL)
speed.set(ms)

lsp.pack()
speed.pack()

cnv.pack()
scr.pack()

ts = n
redraw(n)
redraw_score()
cnv.after(wait, process)

cnv.mainloop()