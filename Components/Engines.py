# Screen size
WINSIZE = [1600, 1600]
# Center of screen
WINCENTER = [800, 800]
mpos = (WINCENTER[0], WINCENTER[1])
font = None
ship = None

def write(screen, text, location, color=(255,255,255)):
  screen.blit(font.render(text,True,color),location)

EngineData:dict = {}
def LoadEngines():
  global EngineData
  path = r'Data\Engines.csv'
  with open(path) as f:
    # Read off the headers.
    l = f.readline()
    h = l[:-1].split(',')
    p = ()
    while len(l)>2:
      l = f.readline()
      p = l[:-1].split(',')
      if len(p) >= 2:
        EngineData[p[0]] = {h[i]:int(p[i]) if (p[i].isdigit() or p[i][0]=='-') else p[i] for i in range(0, len(h))}

def CheapEngines():
  "What's going to happen if we use cheap engines on a long route? Let's find out by simulating the route many times and seeing how long it takes to complete."
  route = [26.93, 21.2, 15.3, 31.30, 59.48, 45.31, 44.92, 30.53, 22.14, 23.77]
  #w     = [    6,    5,    4,     6,     8,     7,     7,     6,     5,     5]
  w     = [    9,    9,    9,     9,     9,     9,     9,     9,     9,     9]
  routetime  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  routestops = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  runs = 100000
  import random
  for run in range(runs):
    y = 0
    s = 0
    for leg, odis in enumerate(route):
      dis = odis
      while dis > 0:
        if w[leg]<=6 or (w[leg]>6 and random.random() > 0.1):
          dis -= min(dis, w[leg]**2)
        else:
          s += 1
        y += 1
    routetime[y] += 1
    routestops[s] += 1
  for y in range(len(route), len(routetime)):
    if routetime[y] > 0:
      print(f"{routetime[y]/runs*100.0:7.3f}% chance for {y:2} years")
  print(f"{sum([y*routetime[y] for y in range(len(route), len(routetime))])/runs:7.3f} years average")

def CombatSpeed(ship):
  a = (ship.engine["Battle"] - 2)
  b = floor((ship.mass + ship.cargo()) // (70 * ship.numengine))
  c = ship.mj + ship.ot * 2
  return max(0.5, min(2.5, (a - b + c) * 0.25))

def FuelUsage(fleet, w:int, d:int, deliveryreturnempty:bool=False):
  fu = 0
  fuIFE = 0.85 if "IFE" in fleet.race.lrt else 1.00
  for ship, num in fleet.ships:
    if ship.engine[f"Warp {w}"] > 0:
      fuelusage = (ship.emptymass * (2 if deliveryreturnempty else 1) + ship.cargomass()) * ship.engine[f"Warp {w}"] * ship.numengine * fuIFE / 20000.0 * d * num
    else:
      fuelusage = -ship.engine[f"Warp {w}"] * d / w ** 2 * ship.numengine * num
    fu += fuelusage
  return fu

def MaxRange(fleet, w:int, deliveryreturnempty:bool=False):
  return fleet.fuel / FuelUsage(fleet, w, 1, deliveryreturnempty)

c = ((0,0,0),(0,0,128),(0,128,0),(0,128,128),
  (128,0,0),(128,0,128),(128,128,0),(170,170,170),
  (85,85,85),(0,0,255),(0,255,0),(0,255,255),
  (255,0,0),(255,0,255),(255,255,0),(255,255,255))
def DrawScreen(screen, fleet, deliveryreturnempty:bool=False):
  black = 0,0,0#20, 20, 40
  screen.fill(black)
  for w in range(1, 11):
    write(screen, f"Warp {w}", (10, -65 + w * 75), c[w])
  #write(screen, f"{fleet.name} has {fleet.fuel}mg of fuel{" and IFE" if "IFE" in fleet.race.lrt else ""}", (10, 800), (255,255,255))
  cargo = fleet.cargo()
  for x in range(WINSIZE[0]):
    for w in range(10, 0, -1):
      if x == 424 and w == 8:
        pass
      fu = 0
      cd = x
      while cd > 0:
        d = min(cd, w**2)
        fu += FuelUsage(fleet, w, d)
        cd -= d
      if deliveryreturnempty:
        fleet.initCargo(cargo[0], 0, 0, 0, 0)
        cd = x
        while cd > 0:
          d = min(cd, w**2)
          fu += FuelUsage(fleet, w, d)
          cd -= d
        fleet.initCargo(*cargo)
      if fu <= fleet.fuel:
        pg.draw.line(screen, c[w], (x, WINSIZE[1]), (x, WINSIZE[1] - min(WINSIZE[1], fu)), 1)


def ShowGraph():
  LoadEngines()
  clock = pg.time.Clock()
  #initialize and prepare screen
  pg.init()
  screen = pg.display.set_mode(WINSIZE)
  pg.display.set_caption("Stars!calc by Nihil K'ri")
  global font, ship
  font=pg.font.Font(None,100)
  race = Race.Race("Test", "Test", None, ["IFE"])
  fleet = Fleet.Fleet(race, "Test Fleet")
  ship = Ship.Ship(fleet, "Ship", 80, 250)
  ship.initEngine(EngineData["Fuel Mizer"], 1, 1400)
  fleet.add_ship(ship, 1)
  #fleet.initCargo(1400, 0, 0, 0, 0)
  fleet.initCargo(1400, 0, 0, 0, 250)
  #DrawScreen(screen, fleet, True)
  
  print(MaxRange(fleet, 8))
  print(MaxRange(fleet, 9, True))

  #main window loop
  done = 1
  global mpos
  print("Window loop begins")
  while not done:
    for e in pg.event.get():
      if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
        done = 1
        break
      elif e.type == pg.MOUSEMOTION:
          if 0 < e.pos[0] < WINSIZE[0] and 0 < e.pos[1] < WINSIZE[1]:
              mpos = e.pos
    pg.display.set_caption(f'(({mpos[0]}, {WINSIZE[1] - mpos[1]})')
    pg.display.update()
    clock.tick(60)
  print("Window loop ends")
  pg.quit()


# if python says run, then we should run
if __name__ == '__main__':
  from math import floor
  import numpy as np, pygame as pg
  import Race, Fleet, Ship

  ShowGraph()