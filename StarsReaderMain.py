import sys, math, cmath, json
import numpy as np, pygame as pg
#from pygame.locals import *
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

#constants
# Screen size
WINSIZE = [1600, 1600]
# Center of screen
WINCENTER = [800, 800]
#mpath = r'C:\Users\User\Documents\KN\Dos\Stars!\Games\Hgserati\Hgserati.map'
#mpath = r'C:\Users\User\Documents\KN\Dos\Stars!\Games\testbed\testbed.map'
#mpath = r'\\ZYKRONOS\Stars!\GAMES\AC4RAND.MAP'
mpath = r'C:\Users\Nihil\OneDrive\Dos\Stars!\Games\AC1\AC1.map'
ppath = r'C:\Users\Nihil\OneDrive\Dos\Stars!\Games\AC1\AC1.p2'
clrs = {
  "habg":(0,255,0),
  "habgb":(0,130,0),
  "haby":(255,255,0),
  "habyb":(130,130,0),
  "habr":(255,0,0),
  "habrb":(130,0,0),
  "scany":(130,130,0),
  "scanr":(130,0,0),
  "Nanite":(255,255,0),
  "Hiserat":(255,0,0),
  "Hawk":(0,255,0),
  "House Cat":(0,0,255),
  "Valadiac":(255,255,0),
  "Crusher":(255,0,255),
  "Rush'n":(0,255,255),
  "Golem":(130,0,0)
  }

# Main database
dat = []
# Min and max star coordinates
minx, maxx, miny, maxy = 10000, 0, 10000, 0
# Screen to space scale, min and max as points, range of coordinates
skl, minxy, maxxy, fxy = 1.0, (1,1), (1,1), (1,1)
# Inputs: Mouse position
mpos = (WINCENTER[0], WINCENTER[1])
safegates = []
unsafegates = []
bestgates = []

def space2screen(x, y):
    return math.floor(skl * (x - minx)),  WINSIZE[1] - math.floor(skl * (y - miny))
def screen2space(sx, sy):
    return math.floor(sx / skl + minx),  math.floor((WINSIZE[1] - sy) / skl + miny)

class Star:
  #i, x, y, n = 0, 0, 0, ""
  #sx, sy, xy = 0.0, 0.0, 0+0j
  #owner, starbase, reportage, pop, value = "", "", 0, 0, 0.0
  def __init__(self, n):
    # ID, Space X, Space Y, Name
    self.i:int = n[0]
    self.x:int = n[1]
    self.y:int = n[2]
    self.n:str = n[3]
  def screen(self):
    # Screen X, Screen Y, Screen point as complex
    s2s = space2screen(self.x, self.y)
    self.sx:int = s2s[0]
    self.sy:int = s2s[1]
    self.xy:complex = (complex(self.sx, self.sy))
  def pla(self, n):
    if self.n != n[0]: return
    self.owner     :str = n[1]
    self.starbase  :str = n[2]
    self.reportage :int = n[3]
    self.pop       :int = n[4]
    if n[5] == "":
      print("Error! No value for", self.n)
    else:
      self.value     :float = (float)(n[5][:-1])/100.0
    self.production :str = n[6]
    self.mines :int = n[7]
    self.factories:int = n[8]
    self.defperc:float = 0.0 if n[9] == "" else (float)(n[9][:-1])/100.0
    self.siron:int = n[10]
    self.sbora:int = n[11]
    self.sgerm:int = n[12]
    self.ironmr:int = n[13]
    self.boramr:int = n[14]
    self.germmr:int = n[15]
    self.ironmc:int = n[16]
    self.boramc:int = n[17]
    self.germmc:int = n[18]
    self.res:int = n[19]
    self.grav:str = n[20]
    self.temp:str = n[21]
    self.rad:str = n[22]
    self.gravo:str = n[23]
    self.tempo:str = n[24]
    self.rado:str = n[25]
    self.terra:float = 0.0 if n[26] == "" else (float)(n[26][:-1])/100.0
    if len(n) == 27: return
    self.cap:int = n[27]
    self.scan:int = n[28]
    self.pen:int = n[29]
    self.driver:int = n[30]
    self.warp:int = n[31]
    self.route:int = n[32]
    self.gaterange:int = (int)(n[33])
    self.gatemass:int = n[34]
    self.pctdmg:int = n[35]

    #self.safegates:Star = []
    #self.unsafegates:Star = []
    self.numsafegates:int = 0
    self.numunsafegates:int = 0
    self.rangefromhw:float = 0.0
    self.head:Star = None
    self.rangefromhead:float = 0.0




  def __str__(self):
    return (f'#{self.i}, {self.x}, {self.y}, {self.n}; {self.sx}, {self.sy}, {self.xy}')
  def dbugpla(self):
    print(f'#{self.i}, {self.n}; {self.owner}, {self.starbase}, {self.reportage}, {self.pop}, {self.value}')
# Homeworld
hw:Star = None
sel:Star = None

def loadmap(hwname):
  global dat, hw
  global minx, maxx, miny, maxy
  global skl, minxy, maxxy, fxy
  print("Minx =",minx)
  with open(mpath) as f:
    # Read off the headers.
    l = f.readline()
    p = ()
    while len(l)>2:
      # Each line is i,x,y,n.
      l = f.readline()
      p = l[:-1].split('\t')
      if len(p)==4:
        for v in range(len(p)-1):
          if p[v].isnumeric():
            p[v]=int(p[v])
        # Grow the viewport as we load.
        if minx > p[1]: minx = p[1]
        if miny > p[2]: miny = p[2]
        if maxx < p[1]: maxx = p[1]
        if maxy < p[2]: maxy = p[2]
        dat.append(Star(p))
        if dat[-1].n == hwname:
          hw = dat[-1]
  maxx += minx - 1000
  minx = 1000
  maxy += miny - 1000
  miny = 1000
  skl = min(WINSIZE[0] / (maxx - minx), WINSIZE[1] / (maxy - miny))
  for p in dat:
    p.screen()
  for v in range(5):
    print(dat[v])
  print(hw)
  print(dat[-1])
  print("X=(",minx,"-",maxx,") Y=(",miny,"-",maxy,")")
  minxy, maxxy, fxy = (minx, miny), (maxx, maxy), (maxx-minx, maxy-miny)
  print("Fxy=",fxy)
  print("XY=(",(maxx-minx)/2,",",(maxy-miny)/2,")")

def loadpfile():
  global dat
  with open(ppath) as f:
    # Read off the headers.
    l = f.readline()
    h = l[:-1].split('\t')
    p = ()
    while len(l)>2:
      l = f.readline()
      p = l[:-1].split('\t')
      if len(p) >= 27:
        i = searchmap(p[0])
        dat[i].pla(p)
    
    #My planets
    race = hw.owner
    myplanets = []
    for x in dat:
      try:
        if x.owner != race: continue
      except AttributeError:
        continue
      d = math.sqrt((x.x-hw.x)**2 + (x.y-hw.y)**2)
      x.rangefromhw = d
      myplanets.append(x)
    myplanets = sorted(myplanets, key=lambda p:p.rangefromhw)

    #Stargates
    for i,x in enumerate(myplanets):
      r = x.gaterange
      r = 832 if r == 800 else 311 if r == 300 else r
      for y in myplanets[i+1:]:
        d = math.sqrt((x.x-y.x)**2 + (x.y-y.y)**2)
        if d < r:
          safegates.append((x, y, r))
          x.numsafegates += 1
          y.numsafegates += 1
          if y.head is None:
            pass
        elif d < 5*r:
          unsafegates.append((x, y, r))
          x.numunsafegates += 1
          y.numunsafegates += 1
    print(f'Safe gates: {len(safegates)}')
    print(f'Unsafe gates: {len(unsafegates)}')
    unbestgates = safegates[:]
    heads = [hw]
    head = hw
    hw.head = hw
    for tier in range(1):
      for x,y,r in safegates:
        if x.i == head.i and y.head is None:
          y.head = x
          bestgates.append((x, y, r))

    myplanets = sorted(myplanets, key=lambda p:p.numsafegates)
    for i,x in enumerate(myplanets):
      print(f'#{i} {x.n} at {x.rangefromhw}ly from hw, {x.numsafegates} safe gates' + '' if x.head is None else f', {x.rangefromhead}ly from {x.head.n}')

    
def searchmap(n) -> int:
  for p in dat:
    if p.n == n:
      return p.i - 1
  return -1

def draw_stars(screen, mode):
  "used to draw (and clear) the stars"
  "Lifted from pygame.examples.stars"
  white = 255, 240, 200
  color = white
  c, r = white, 0
  for p in dat:
    try:
      v = p.value
      #color = white
    except AttributeError:
      v = 0
      #color = (255,0,255)
    try:
      t = p.terra
      #color = white
    except AttributeError:
      t = 0
      #color = (255,0,255)
    if v > 0:
      try:
        c, r = clrs[p.owner], v * 20
        pg.draw.circle(screen, c, (p.sx, p.sy), r)
      except KeyError:
        pass
      c, r = clrs["habgb"], v * 18
      pg.draw.circle(screen, c, (p.sx, p.sy), r)
      c, r = clrs["habg"], v * 15
      pg.draw.circle(screen, c, (p.sx, p.sy), r)
    elif v < 0:
      if t > 0:
        try:
          c, r = clrs[p.owner], t * 20
          pg.draw.circle(screen, c, (p.sx, p.sy), r)
        except KeyError:
          pass
        c, r = clrs["habyb"], t * 18
        pg.draw.circle(screen, c, (p.sx, p.sy), r)
        c, r = clrs["haby"], t * 15
        pg.draw.circle(screen, c, (p.sx, p.sy), r)
      else:
        try:
          c, r = clrs[p.owner], v/-0.45 * 20
          pg.draw.circle(screen, c, (p.sx, p.sy), r)
        except KeyError:
          pass
        c, r = clrs["habrb"], v/-0.45 * 18
        pg.draw.circle(screen, c, (p.sx, p.sy), r)
        c, r = clrs["habr"], v/-0.45 * 15
        pg.draw.circle(screen, c, (p.sx, p.sy), r)
    else:
      for x in [-1,0,1]:
        for y in [-1,0,1]:
          pos = (int(p.sx+x), int(p.sy+y))
          #val = 
          screen.set_at(pos, (0,255,0) if p.n == hw.n else color)

clrs16 = [(0,0,0),(0,0,128),(0,128,0),(0,128,128),
  (128,0,0),(128,0,128),(128,128,0),(170,170,170),
  (85,85,85),(0,0,255),(0,255,0),(0,255,255),
  (255,0,0),(255,0,255),(255,255,0),(255,255,255)]
def divide_stars(screen, n):
  print("Dividing stars at ", hw)
  color = clrs16[12]
  for x in [-1,0,1]:
    for y in [-1,0,1]:
      pos = (int(hw.sx+x), int(hw.sy+y))
      screen.set_at(pos, color)
  excl = {}#100,89, 107,117,128,105,86,77,98,78, 101,74,69,65,63,70,61,58,50}
  s = [e for e in dat if e.i not in excl]
  s = sorted(s, key=lambda p:(-cmath.phase(hw.xy-p.xy)))
  n=min(n,16)
  for v in range(n):
    vv=int(len(s)/n*v)
    print(s[vv])
    ep = (s[vv].sx+(s[vv].sx-hw.sx)*10,s[vv].sy+(s[vv].sy-hw.sy)*10)
    pg.draw.line(screen, clrs16[v], (hw.sx,hw.sy), ep)
  subdat = [[] for i in range(n)]
  for v in range(1,len(s)):
    vv = int(math.floor(v/len(s)*n))
    subdat[vv].append(s[v])
  for v in range(n):
    s = sorted(subdat[v], key=lambda p:(abs(hw.xy-p.xy)))
    startpoint = (int(hw.sx), int(hw.sy))
    for vv in range(len(s)):
      endpoint = (s[vv].sx,s[vv].sy)
      pg.draw.line(screen, clrs16[15], startpoint, endpoint)
      startpoint = endpoint[:]

def Delaunay_stars(screen):
  points = []
  for p in dat:
    points.append([int(p.sx),int(p.sy)])
  arr = np.array(points)
  tri = Delaunay(arr)
  print(points[:10])
  plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
  plt.plot(points[:,0], points[:,1], 'o')
  plt.show()

def Shortest_path(screen, hw, n):
  print(hw)
  color = 255,0,0
  for x in [-1,0,1]:
    for y in [-1,0,1]:
      pos = (int(hw.sx+x), int(hw.sy+y))
      screen.set_at(pos, color)
  #excl = {100,89, 107,117,128,105,86,77,98,78, 101,74,69,65,63,70,61,58,50}
  #s = [e for e in dat if e[0] not in excl]
  #s = sorted(s, key=lambda p:(-cmath.phase(h[6]-p[6])))

def findnearest(pos):
  x, y = screen2space(pos[0], pos[1])
  mini, mind = -1, 10000
  for i, p in enumerate(dat):
    d = math.sqrt((x - p.x)**2 + (y - p.y)**2)
    if d < mind:
      mind = d
      mini = i
  if mini == -1: return None
  return dat[mini]

def draw_heartbeats(screen):
  v = searchmap("Dowding")
  p = dat[v]
  pg.draw.circle(screen, (64,0,0), (p.sx, p.sy), 312*skl)
  v = searchmap("Spittle")
  p = dat[v]
  pg.draw.circle(screen, (64,0,0), (p.sx, p.sy), 312*skl)
  v = searchmap("Tsagigla'lal")
  p = dat[v]
  pg.draw.circle(screen, (64,0,0), (p.sx, p.sy), 312*skl)
  v = searchmap("Nirvana")
  p = dat[v]
  pg.draw.circle(screen, (128,0,0), (p.sx, p.sy), 312*skl)
  pg.draw.circle(screen, (128,128,0), (hw.sx, hw.sy), 312*skl)
  pg.draw.circle(screen, (128,64,0), (hw.sx, hw.sy), 312/300*800*skl, 5)
  v = searchmap("Trog")
  p = dat[v]
  pg.draw.circle(screen, (130,0,255), (p.sx, p.sy), 600*skl, 5)


def draw_gates(screen):
  for g in unsafegates:
    color = (255, 130, 0) if g[0].gaterange > 0 and g[1].gaterange > 0 else (130, 0, 130)
    #pg.draw.line(screen, color, (g[0].sx, g[0].sy), (g[1].sx, g[1].sy))
  for g in safegates:
    #if g[1].head is not None: continue
    color = (130, 255, 0) if g[0].gaterange > 0 and g[1].gaterange > 0 else (130, 255, 130)
    pg.draw.line(screen, color, (g[0].sx, g[0].sy), (g[1].sx, g[1].sy))
  for g in bestgates:
    color = (0, 0, 255) if g[0].gaterange > 0 and g[1].gaterange > 0 else (130, 130, 255)
    #pg.draw.line(screen, color, (g[0].sx, g[0].sy), (g[1].sx, g[1].sy))



def draw_screen(screen):
  black = 20, 20, 40
  screen.fill(black)
  draw_heartbeats(screen)
  draw_gates(screen)
  draw_stars(screen, 4)
  pg.draw.line(screen, (255,0,0), (hw.sx, hw.sy), mpos)
  if sel:
    pg.draw.line(screen, (130,0,130), (sel.sx, sel.sy), mpos)
  #divide_stars(screen, 100, 8)#422#304
  #Delaunay_stars(screen)
  #Shortest_path(screen, 23, 8)


def main():
  "This is the starfield code"
  "Lifted from pygame.examples.stars"
  #create our starfield
  loadmap("Klaupaucius")
  loadpfile()
  clock = pg.time.Clock()
  #initialize and prepare screen
  pg.init()
  screen = pg.display.set_mode(WINSIZE)
  pg.display.set_caption("Stars!calc by Nihil K'ri")

  #main game loop
  done = 0
  global mpos
  print("Game loop begins")
  while not done:
    for e in pg.event.get():
      if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
        done = 1
        break
      elif e.type == pg.MOUSEMOTION:
          if 0 < e.pos[0] < WINSIZE[0] and 0 < e.pos[1] < WINSIZE[1]:
              mpos = e.pos
      elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
        #WINCENTER[:] = list(e.pos)
        sel = findnearest(e.pos)
        print(f'{sel.n} selected!')

    pg.display.set_caption(f'({hw.sx}, {hw.sy}) - ({mpos[0]}, {mpos[1]})')
    draw_screen(screen)
    pg.display.update()
    clock.tick(60)
  print("Game loop ends")
  print(hw.__dict__)
  pg.quit()


def Aaron():
  for c in range(3, 37, 1):
    kt = 100 + 3 * 25 + c * 3 + (36-c) * 100
    cu = 140 * c * kt
    #cu/(kt+x) >= 1612
    #cu >= 1612 * (kt+x)
    #cu >= (1612 * kt + 1612 * x)
    #cu - 1612 * kt >= (1612 * x)
    #(cu - 1612 * kt)/1612 >= x
    x = math.floor((cu - 1612 * kt)/1612)
    print(f'{c:2} cloaks weigh {kt:5,}kt with {cu:7,}cu, supporting {x:6,}kt more')

# if python says run, then we should run
if __name__ == '__main__':
  main()
  #Aaron()