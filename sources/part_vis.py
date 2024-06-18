#!/usr/bin/env python3

import pygame as pg
from random import randint
from sys import argv
import colorsys
import copy

more_info = 0

START_MI_WIDTH = 200
MORE_INFO_WIDTH = 200
MAX_MORE_INFO_LINE_H = 50

W = H = 1000
WW = W + 400
HH = H
W = HH - MORE_INFO_WIDTH * more_info
H = HH - MORE_INFO_WIDTH * more_info
WL = WW - W




big_colors = [
    [
        
    ]
]

# Sum of the min & max of (a, b, c)


def generate_random_color(p, pp):
    c2 = [p / pp, 0.5, 1]
    c2 = colorsys.hls_to_rgb(*c2)
    c2 = list(map(lambda x: int(255.9* x), c2))

    return c2

def generate_color_list(players_cnt):
    if players_cnt == 2:
        return [(255, 0, 0), (0, 0, 255)]
    return [generate_random_color(_, players_cnt) for _ in range(players_cnt)]

min_ms, max_ms = 1, 200

if "--help" in argv:
    print(f"Usage:\n {argv[0]} log.txt ms font wait\n log.txt - text file with game log,\n ms - time in milliseconds between two steps in visualization,\n font - score font,\n wait - time before visualization")
    exit(0)
if len(argv) == 4:
    path = argv[1]
    speed_ms = max(0, int(argv[2]))
    scfont = int(argv[3])
else:
    print(f"Incorrect option\nUse {argv[0]} --help to view usage information")
    exit(1)

f = open(path, "r")
t, n, p, k, a = map(int, f.readline().split())
alltime = t * k
a //= 2
maxtsize = a


def get_cell(x, y):
    return (-y + a, x + a)

tab = [[0 for _ in range(2 * a + 1)] for _ in range(2 * a + 1)]
for i in range(2 * a + 1):
    arr = list(map(int, f.readline().split()))
    for j in range(2 * a + 1):
        tab[i][j] = arr[j]



colors = generate_color_list(k)

players = k

scores = [0 for _ in range(k)]

ids = [-1 for _ in range(k)]

wall_color = [0, 0, 0]

sc = pg.display.set_mode((WW, HH), pg.RESIZABLE)
sc.fill((255, 255, 255))
pg.display.update()

pg.display.set_caption("Game")

pg.init()
fn = pg.Font(None, scfont)
fnhrect = pg.Font(None, min(MAX_MORE_INFO_LINE_H, int(MORE_INFO_WIDTH / 3)))


mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
dx = (maxc - mixc) / (2 * n + 1)
dy = (mayc - miyc) / (2 * n + 1)
dx = int(dx)
dy = int(dy)
mixc = int(mixc)
miyc = int(miyc)
maxc = mixc + dx * (2 * n + 1)
mayc = miyc + dy * (2 * n + 1)
#ddx, ddy = dx / 10, dy / 10


final_score = None

def get_crds(x, y):
    return (cx + dx * x, cy - dy * y)

def fill(x, y, col):
    fx, fy = get_crds(x, y)
    if col[0] == col[1] == col[2] == 0:
        fille(x, y)
    pg.draw.rect(sc, col, (fx - dx / 2 + 1, fy - dy / 2 + 1, dx - 1, dy - 1))
    
def fille(x, y):
    fx, fy = get_crds(x, y)
    pg.draw.rect(sc, (0, 0, 0), (fx - dx / 2, fy - dy / 2, dx + 1, dy + 1), 1)

def redraw(tsize):
    global dx, dy, ddx, ddy, ids
    
    if tsize != maxtsize:
        if used == len(tts):
            tsize += 1
            for x in range(-tsize, tsize + 1):
                fille(x, -tsize)
                fille(x, +tsize)
            for y in range(-tsize, tsize + 1):
                fille(-tsize, y)
                fille(+tsize, y)
            tsize -= 1

#        i = tsize + 1
#        x, y = get_crds(i, i)
#        pg.draw.line(sc, (0, 0, 0), (x + dx / 2, miyc), (x + dx / 2, mayc), 1)
#        pg.draw.line(sc, (0, 0, 0), (mixc, y - dy / 2), (maxc, y - dy / 2), 1)
#        i = -tsize - 1
#        x, y = get_crds(i, i)
#        pg.draw.line(sc, (0, 0, 0), (x + dx / 2, miyc), (x + dx / 2, mayc), 1)
#        pg.draw.line(sc, (0, 0, 0), (mixc, y - dy / 2), (maxc, y - dy / 2), 1)
glob_graph = True
    
def redraw_score(select_best=False, graph=None):
    global MORE_INFO_WIDTH
    
    if graph is None:
        graph = glob_graph
    
    if final_score is not None:
        select_best = True
    else:
        select_best = False
        
    pg.draw.rect(sc, (255, 255, 255), (W + 2, 0, WL, H))
    
    txt = fn.render("WINNERS", True, (0, 0, 0))
    txt = pg.transform.rotate(txt, 90)
    sc.blit(txt, (W + 3, 200 - txt.get_height()))
    
    for i in range(len(scores)):
        pg.draw.circle(sc, (0, 0, 0), (W + 15, 200 + (i + 0.5) * fn.get_height()), 13)
        if select_best and final_score[i] == max(final_score):
            txt = fn.render(f"{i + 1}: " + str(scores[i]), True, colors[i])
            pg.draw.line(sc, (0, 255, 0), (W + 15 - 10, 200 + (i + 0.5) * fn.get_height() - 5), (W + 15, 200 + (i + 0.5) * fn.get_height() + 10), 5)
            pg.draw.line(sc, (0, 255, 0), (W + 15 + 10, 200 + (i + 0.5) * fn.get_height() - 10), (W + 15, 200 + (i + 0.5) * fn.get_height() + 10), 5)
        elif select_best:
            txt = fn.render(f"{i + 1}: " + str(scores[i]), True, colors[i])
            pg.draw.line(sc, (255, 0, 0), (W + 15 - 15, 200 + (i + 0.5) * fn.get_height() - 15), (W + 15 + 15, 200 + (i + 0.5) * fn.get_height() + 15), 5)
            pg.draw.line(sc, (255, 0, 0), (W + 15 + 15, 200 + (i + 0.5) * fn.get_height() - 15), (W + 15 - 15, 200 + (i + 0.5) * fn.get_height() + 15), 5)
        else:
            txt = fn.render(f"{i + 1}: " + str(scores[i]), True, colors[i])
        sc.blit(txt, (W + 30, 200 + i * fn.get_height()))
        
    if more_info:
            
        
        pg.draw.rect(sc, (255, 255, 255), (0, HH - MORE_INFO_WIDTH - 5, WW, MORE_INFO_WIDTH + 5))
    
        if graph:
            hrect = int(MORE_INFO_WIDTH / 3)
        else:
            hrect = int(MORE_INFO_WIDTH)
            
        pg.draw.rect(sc, (255, 0, 0), (10, HH - hrect + 5, WW - 20, hrect - 10), 0)
        pg.draw.rect(sc, (255, 100, 0), (15, HH - hrect + 10, (WW - 30) * used / alltime, hrect - 20), 0)
        pg.draw.rect(sc, (0, 255, 0), (15, HH - hrect + 10, (WW - 30) * ntime / alltime, hrect - 20), 0)
        pg.draw.rect(sc, (0, 0, 255), (15 + (WW - 30) * ntime / alltime - 3, HH - hrect, 6, hrect), 0)
        
        
        txt = fnhrect.render(f"{ntime}/{alltime}", True, (0, 0, 0))
        sc.blit(txt, (WW // 2 - txt.get_width() * 0.5, HH - hrect / 2 - 1 - txt.get_height() * 0.5 + 4))
        
        # draw grapth
        
        if graph:
        
            MORE_INFO_WIDTH += 5
            
            hrect = int(MORE_INFO_WIDTH * 2 / 3)
            hinfo = hrect - 10
            
            pg.draw.rect(sc, (255, 230, 200), (10, HH - MORE_INFO_WIDTH + 5, WW - 20, hinfo), 0)
            pg.draw.rect(sc, (0, 0, 255), (15 + (WW - 30) * ntime / alltime, HH - MORE_INFO_WIDTH, 1, hinfo + 10), 0)
            
            y0 = HH - MORE_INFO_WIDTH + hinfo + 5
            
            for i in range(1, used):
                for pl in range(players):
                    y1 = y0 - scoress[i - 1][pl] * hinfo / max_score
                    y2 = y0 - scoress[i][pl] * hinfo / max_score
                    pg.draw.line(sc, colors[pl], (10 + (WW - 30) * i / alltime, y1), (10 + (WW - 30) * (i + 1) / alltime, y2), 1)
            
            MORE_INFO_WIDTH -= 5
    
def draw_start_field(tsize):
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
            else:
                fille(x, y)
    redraw_score()



scoress = []
max_score = 1
images = []
tts = []
ntime = 0
used = 0

def clprocess():
    global ts, dx, dy, mixc, miyc, maxc, mayc, speed_ms, ntime, used, tab, pause, scores, final_score
    global max_score, glob_graph, W, H, WW, HH, WL, MORE_INFO_WIDTH, more_info, alltime
    
    need_inv = 0
    
    need_inv0 = 0

    if more_info == 0:
        more_info ^= 1
        need_inv0 = 1
    
        W = HH - MORE_INFO_WIDTH * more_info
        H = HH - MORE_INFO_WIDTH * more_info
        WL = WW - W
        

        mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
        cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
        dx = (maxc - mixc) / (2 * ts + 1)
        dy = (mayc - miyc) / (2 * ts + 1)
        dx = int(dx)
        dy = int(dy)
        mixc = int(mixc)
        miyc = int(miyc)
        maxc = mixc + dx * (2 * ts + 1)
        mayc = miyc + dy * (2 * ts + 1)
        
    
    if glob_graph:
        need_inv = 1
        glob_graph ^= 1
        MORE_INFO_WIDTH = (int(START_MI_WIDTH * 1 / 3) + 1 if not glob_graph else START_MI_WIDTH)
        if more_info:
            W = HH - MORE_INFO_WIDTH * more_info
            H = HH - MORE_INFO_WIDTH * more_info
            WL = WW - W
        
    
    ntime = used
    sc.fill((255, 255, 255))
    while True:
        inp = list(map(int, f.readline().split()))
        if not inp:
            break
        if inp[0] > 0:
            
            num, x, y = inp[0], inp[1], inp[2]
            i, j = get_cell(x, y)
            tab[i][j] = num
            scores[num - 1] += 1
            
            ntime += 1
            used = ntime
            images.append(copy.deepcopy(tab))
            scoress.append(copy.deepcopy(scores))
            max_score = max(max_score, max(scores))
            tts.append(ts)
            
        elif inp[0] == -1:
            ts += 1
            
            ni = list(map(int, f.readline().split()))
            while ni[0] != -1:
                x, y = ni[1], ni[2]
                i, j = get_cell(x, y)
                tab[i][j] = -1
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
                ni = list(map(int, f.readline().split()))
        else:
            break
        redraw_score(graph = False)
        pg.display.flip()
        for e in pg.event.get():
            if e.type == pg.QUIT:
                exit()
            
    if need_inv0:
        more_info ^= 1
    
        W = HH - MORE_INFO_WIDTH * more_info
        H = HH - MORE_INFO_WIDTH * more_info
        WL = WW - W
        

        mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
        cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
        dx = (maxc - mixc) / (2 * ts + 1)
        dy = (mayc - miyc) / (2 * ts + 1)
        dx = int(dx)
        dy = int(dy)
        mixc = int(mixc)
        miyc = int(miyc)
        maxc = mixc + dx * (2 * ts + 1)
        mayc = miyc + dy * (2 * ts + 1)
            
     
    if need_inv:
        glob_graph ^= 1
        MORE_INFO_WIDTH = (int(START_MI_WIDTH * 1 / 3) + 1 if not glob_graph else START_MI_WIDTH)
        
    

                
    WW = sc.get_width()
    HH = sc.get_height()
    W = HH - MORE_INFO_WIDTH * more_info
    H = HH - MORE_INFO_WIDTH * more_info
    WL = WW - W
                
    mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
    cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
    dx = (maxc - mixc) / (2 * ts + 1)
    dy = (mayc - miyc) / (2 * ts + 1)
    dx = int(dx)
    dy = int(dy)
    mixc = int(mixc)
    miyc = int(miyc)
    maxc = mixc + dx * (2 * ts + 1)
    mayc = miyc + dy * (2 * ts + 1)
    
    final_score = copy.deepcopy(scores)
    alltime = used
    
    return

def process():
    global ts, dx, dy, mixc, miyc, maxc, mayc, speed_ms, ntime, used, tab, pause, scores, final_score
    global max_score, alltime

    if ntime >= used:
        inp = list(map(int, f.readline().split()))
        if not inp:
            pause = True
            alltime = used
            final_score = copy.deepcopy(scores)
            redraw_score(select_best=True)
            return
        if inp[0] > 0:
            
            num, x, y = inp[0], inp[1], inp[2]
            i, j = get_cell(x, y)
            tab[i][j] = num
            fill(x, y, colors[num - 1])
            scores[num - 1] += 1
            redraw_score()
            
            ntime += 1
            used = ntime
            images.append(copy.deepcopy(tab))
            scoress.append(copy.deepcopy(scores))
            max_score = max(max_score, max(scores))
            tts.append(ts)
            
        elif inp[0] == -1:
            ts += 1
            
            
            mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
            cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
            dx = (maxc - mixc) / (2 * ts + 1)
            dy = (mayc - miyc) / (2 * ts + 1)
            dx = int(dx)
            dy = int(dy)
            mixc = int(mixc)
            miyc = int(miyc)
            maxc = mixc + dx * (2 * ts + 1)
            mayc = miyc + dy * (2 * ts + 1)
            
            sc.fill((255, 255, 255))
            redraw_all()
            
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

        else:
            alltime = used
            final_score = copy.deepcopy(scores)
            redraw_score(select_best=True)
        redraw(ts)
    else:
        tab = copy.deepcopy(images[ntime])
        scores = copy.deepcopy(scoress[ntime])
        ts = tts[ntime]
            
        mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
        cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
        dx = (maxc - mixc) / (2 * ts + 1)
        dy = (mayc - miyc) / (2 * ts + 1)
        dx = int(dx)
        dy = int(dy)
        mixc = int(mixc)
        miyc = int(miyc)
        maxc = mixc + dx * (2 * ts + 1)
        mayc = miyc + dy * (2 * ts + 1)
        
        
        ntime += 1
        sc.fill((255, 255, 255))
        redraw_all()

def redraw_all():
    for x in range(-ts, ts + 1):
        for y in range(-ts, ts + 1):
            fille(x, y)
            i, j = get_cell(x, y)
            if tab[i][j] == -1:
                fill(x, y, wall_color)
            else:
                if tab[i][j]:
                    fill(x, y, colors[tab[i][j] - 1])
    redraw_score()

def mouse_press(x, y):
    global pressed
    pressed = x, y

def handle_press():
    global ts, dx, dy, mixc, miyc, maxc, mayc, speed_ms, ntime, used, tab, pause, scores
    global ntime, used, tab, ts
    if pressed is None or more_info == 0:
        return
    x, y = pressed;
    if y > H - MORE_INFO_WIDTH and more_info:
        t = (x - 15) / (WW - 30)
        t = int(t * alltime)
        t = max(0, t)
        t = min(used, t)
        ntime = t
        
        
        sc.fill((255, 255, 255))
        
        
        tab = copy.deepcopy(images[ntime])
        scores = copy.deepcopy(scoress[ntime])
        ts = tts[ntime]
        
                
        mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
        cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
        dx = (maxc - mixc) / (2 * ts + 1)
        dy = (mayc - miyc) / (2 * ts + 1)
        dx = int(dx)
        dy = int(dy)
        mixc = int(mixc)
        miyc = int(miyc)
        maxc = mixc + dx * (2 * ts + 1)
        mayc = miyc + dy * (2 * ts + 1)
        
        redraw_all()
        
        if ntime == alltime:
            redraw_score(select_best=True)


def move(t):
    global ts, dx, dy, mixc, miyc, maxc, mayc, speed_ms, ntime, used, tab, pause, scores
    global ntime, used, tab, ts
    t = max(0, t)
    t = min(used, t)
    ntime = t
    
            
    mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
    cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
    dx = (maxc - mixc) / (2 * ts + 1)
    dy = (mayc - miyc) / (2 * ts + 1)
    dx = int(dx)
    dy = int(dy)
    mixc = int(mixc)
    miyc = int(miyc)
    maxc = mixc + dx * (2 * ts + 1)
    mayc = miyc + dy * (2 * ts + 1)
    
    
    sc.fill((255, 255, 255))
    
    
    tab = copy.deepcopy(images[ntime])
    ts = tts[ntime]
    scores = scoress[ntime]
    redraw_all()
    
    if ntime == alltime:
        redraw_score(select_best=True)


ts = n


#
#for i in range(-ts, ts + 1):    
#    x, y = get_crds(i, i)
#    pg.draw.line(sc, (0, 0, 0), (x + dx / 2, miyc), (x + dx / 2, mayc), 1)
#    pg.draw.line(sc, (0, 0, 0), (mixc, y - dy / 2), (maxc, y - dy / 2), 1)
#    

redraw(n)
draw_start_field(n)


images.append(copy.deepcopy(tab))
tts.append(ts)
scoress.append(copy.deepcopy(scores))
max_score = max(max_score, max(scores))
# redraw_score()

pause = True


FPS = 60
clock = pg.Clock()

while True:
    if not pause:
        process()
    
    #fx, fy = get_crds(-ts, ts)
    #ffx, ffy = get_crds(ts, -ts)
    #pg.draw.rect(sc, col, (fx - dx / 2 + 1, fy - dy / 2 + 1, dx, dy))
    
    #print(fx, fy, ffx, ffy)
    
    #pg.display.update(sc, (0,0,0), (fx - dx / 2, fy - dy / 2, ffx - fx, ffy - fy))
    
    pg.display.flip()
    

    pressed = None
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_SPACE:
                pause ^= 1
            elif e.key == pg.K_TAB:
                clprocess()
                sc.fill((255, 255, 255))
                redraw_all()
            elif e.key == pg.K_RETURN:
                more_info ^= 1
            
                W = HH - MORE_INFO_WIDTH * more_info
                H = HH - MORE_INFO_WIDTH * more_info
                WL = WW - W
                

                mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
                cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
                dx = (maxc - mixc) / (2 * ts + 1)
                dy = (mayc - miyc) / (2 * ts + 1)
                dx = int(dx)
                dy = int(dy)
                mixc = int(mixc)
                miyc = int(miyc)
                maxc = mixc + dx * (2 * ts + 1)
                mayc = miyc + dy * (2 * ts + 1)
                
                
                sc.fill((255, 255, 255))
                redraw_all()
            elif e.key == pg.K_LEFT:
                move(ntime - 1)
            elif e.key == pg.K_RIGHT:
                move(ntime + 1)
            elif e.key == pg.K_0:
                speed_ms = 0
            elif e.key == pg.K_g:
                glob_graph ^= 1
                MORE_INFO_WIDTH = (int(START_MI_WIDTH * 1 / 3) + 1 if not glob_graph else START_MI_WIDTH)
                
                if more_info:
                    W = HH - MORE_INFO_WIDTH * more_info
                    H = HH - MORE_INFO_WIDTH * more_info
                    WL = WW - W
                    

                    mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
                    cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
                    dx = (maxc - mixc) / (2 * ts + 1)
                    dy = (mayc - miyc) / (2 * ts + 1)
                    dx = int(dx)
                    dy = int(dy)
                    mixc = int(mixc)
                    miyc = int(miyc)
                    maxc = mixc + dx * (2 * ts + 1)
                    mayc = miyc + dy * (2 * ts + 1)
                    
                    
                    sc.fill((255, 255, 255))
                    redraw_all()
            elif e.key >= pg.K_1 and e.key <= pg.K_9:
                speed_ms = 10 * (1 + e.key - pg.K_1)
        if e.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            mouse_press(x, y)
        if e.type == pg.MOUSEMOTION:
            x, y = pg.mouse.get_pos()
            if e.buttons[0]:
                mouse_press(x, y)
        if e.type == pg.VIDEORESIZE:
            # There's some code to add back window content here.
            #surface = pygame.display.set_mode((q.w, q.h),
            #                                  pygame.RESIZABLE)
            WW = e.w
            HH = e.h
            W = HH - MORE_INFO_WIDTH * more_info
            H = HH - MORE_INFO_WIDTH * more_info
            WL = WW - W
            
            sc.fill((255, 255, 255))
            

            mixc, miyc, maxc, mayc = 30, 30, W - 30, H - 30
            cx, cy = (mixc + maxc) / 2, (miyc + mayc) / 2
            dx = (maxc - mixc) / (2 * ts + 1)
            dy = (mayc - miyc) / (2 * ts + 1)
            dx = int(dx)
            dy = int(dy)
            mixc = int(mixc)
            miyc = int(miyc)
            maxc = mixc + dx * (2 * ts + 1)
            mayc = miyc + dy * (2 * ts + 1)
            
            redraw_all()
    
    handle_press()
    
    if speed_ms:
        pg.time.delay(speed_ms)
    #clock.tick(FPS)
