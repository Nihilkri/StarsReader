
from math import ceil, floor


#Defs = {"SDI": 1.0, "Missile": 2.0, "Laser": 2.4, "Planet": 3.0, "Neutron": 3.8}
Defs = {"SDI": 0.99, "Missile": 1.99, "Laser": 2.39, "Planet": 2.99, "Neutron": 3.79}
Bombs = {}

def LoadBombs():
  global Bombs
  path = 'Bombs.csv'
  with open(path) as f:
    # Read off the headers.
    l = f.readline()
    h = l[:-1].split('\t')
    p = ()
    while len(l)>2:
      l = f.readline()
      p = l[:-1].split('\t')
      if len(p) >= 2:
        Bombs[p[0]] = {h[i]:(float(p[i]) if p[i].find('.')>-1 else (int(p[i]) if p[i].isdigit() else p[i])) for i in range(0, len(h))}


def Bomb(title:str, deft:str, instn:int|tuple[int, int, int], pop:int, ships:int, bombs:list[tuple[str, int]], years:int = 1, invpop:int = 0, invthresh:int = 0, isatkWM:bool = False, isdefIS:bool = False):
  try:
    facn, minen, defn = instn
  except:
    facn, minen, defn = 0, 0, instn
  defop = ceil(min(defn, pop / 2500))
  print(f"{title:>87} against {pop:>9,} population, {facn:>4} factories, {minen:>4} mines, and {defop:>3}/{defn:>3} {deft} defenses.")
  # Save original values.
  ofacn, ominen, odefn, opop, oships = facn, minen, defn, pop, ships
  for year in range(1, years + 1):
    if pop == 0:
      print(f"Year {year:>2}: No population left to bomb.")
      break

    # Save original values.
    yfacn, yminen, ydefn, ypop, yships = facn, minen, defn, pop, ships
    defop = ceil(min(defn, pop / 2500))
    killpercs, killmins = [], []
    killperc, killmin = 0, 0
    killbuilds = []
    killbuild = 0
    buildkills = 0

    # Calculate the defences for normal/LBU bombing.
    defpop:float = (1.0 - ((1.0 - (Defs[deft] * 0.01)) ** defop))
    killpercs, killmins = [], []
    killperc, killmin = 0, 0
    for bomb in bombs:
      if Bombs[bomb[0]]["Smart"] == 1: continue
      killpercs.append(Bombs[bomb[0]]["Kill"] * 0.01 * bomb[1] * ships)
      killmins.append(Bombs[bomb[0]]["Min"] * bomb[1] * ships)
    killperc = sum(killpercs)
    killmin = sum(killmins)
    popkills = killperc * (1.0 - defpop)
    popkills = floor(popkills * 1000.0) * 0.0001
    minpopkills = killmin * (1.0 - defpop)
    minpopkills = floor(minpopkills * 1000.0) * 0.0001
    popkilled = floor(max(popkills * pop, minpopkills) * 0.01) * 100.0
    pop -= floor(popkilled)

    # Destroy buildings.
    defbuild:float = (1.0 - ((1.0 - (Defs[deft] * 0.01)) ** defop)) * 0.5
    killbuilds = []
    killbuild = 0
    buildkills = 0
    for bomb in bombs:
      if Bombs[bomb[0]]["Smart"] == 1: continue
      killbuilds.append(Bombs[bomb[0]]["Destroy"] * 10 * bomb[1] * ships)
    killbuild = sum(killbuilds)
    buildkills = floor(killbuild * (1.0 - defbuild))

    # Smart Bombing.
    defsmart:float = (1.0 - ((1.0 - (Defs[deft] * 0.005)) ** defop))
    killpercs = []
    killperc = 1.0
    for bomb in bombs:
      if Bombs[bomb[0]]["Smart"] == 0: continue
      killpercs.append((1.0 - Bombs[bomb[0]]["Kill"] * 0.01) ** (bomb[1] * ships))
      killperc *= killpercs[-1]
    popkills = (1.0 - killperc) * (1.0 - defsmart)
    popkills = floor(popkills * 1000.0) * 0.001
    popkilled = floor(popkills * pop * 0.01) * 100.0
    pop -= floor(popkilled)

    # Defences are recalculated after smart bombing.
    totbuildings = facn + minen + defn
    killbuildperc = buildkills / totbuildings if totbuildings > 0 else 1.0
    facn = max(0, facn - floor(facn * killbuildperc))
    minen = max(0, minen - floor(minen * killbuildperc))
    defn = max(0, defn - floor(defn * killbuildperc))
    defop = ceil(min(defn, pop / 2500))

    print(f"Year {year:>2}: ", end="")
    pop = int(max(0, floor(pop * 0.01) * 100.0))
    defop = ceil(min(defn, pop / 2500))
    print(f"{ypop - pop:>9,} ({(ypop - pop)/ypop*100.0:>5.1f}%) colonists are killed and ", end="")
    print(f"{yfacn - facn + yminen - minen + ydefn - defn:>5} buildings are destroyed by this fleet. ", end="")
    print(f"{pop:>9,} population, {facn:>4} factories, {minen:>4} mines, and {defop:>3}/{defn:>3} defenses remain.")

    # Waypoint 1 Invasions.
    definv:float = (1.0 - ((1.0 - (Defs[deft] * 0.01)) ** defop)) * 0.75
    atk = invpop * (1.0 - definv)
    atkb = 1.1 * (1.0 + 0.5 * isatkWM)
    defb = 1.0 + isdefIS
    if atk * atkb > pop * defb:
      popi = int((atk - pop * defb / atkb) / 100.0) * 100
      if popi >= invthresh:
        r = int(popi / 2500 + min(floor(popi/10000*25), facn)*1.5)
        print(f"Year {year:>2}: The fleet successfully invades and kills {pop:>9,} colonists, leaving {popi:>9,} invaders remaining, producing {r} resources.")

        #pop = 0
        #break


  print("======================")

def Bombing():
  LoadBombs()
  c16 = [("Cherry", 16)]
  c12n04 = [("Cherry", 12), ("Neutron",  4)]
  c08n08 = [("Cherry",  8), ("Neutron",  8)]
  c04n12 = [("Cherry",  4), ("Neutron", 12)]
  n16 = [("Neutron", 16)]
  e16 = [("Enriched", 16)]
  hw = ("Laser", (2500, 1500, 100), 1000000)
  #hw = ("Laser", 100, 1000000)
  inv = (10, 486800, 212500)
  print()
  Bomb("16 ships of 16 Cherries"             , *hw, 16, c16   , *inv)
  #Bomb("16 ships of 12 Cherries,  4 Neutrons", *hw, 16, c12n04, *inv)
  Bomb("16 ships of  8 Cherries,  8 Neutrons", *hw, 16, c08n08, *inv)
  #Bomb("16 ships of  4 Cherries, 12 Neutrons", *hw, 16, c04n12, *inv)
  Bomb("16 ships of 16 Neutrons"             , *hw, 16,    n16, *inv)
  #Bomb("8 ships of 16 Neutrons"              , *hw,  8,    n16, *inv)
  #Bomb("1000 ships of 16 Neutrons"              , *hw,  1000,    n16, *inv)
  Bomb("128 ships of 2 LBU17s", *hw, 128, [("LBU17", 2)], 5, 2100000, 0)
  Bomb("96 ships of 2 LBU32s", *hw, 96, [("LBU32", 2)], 5, 2100000, 0)
  #Bomb("90 ships of 2 Cherries", *hw, 90, [("Cherry", 2)], 5, 2000000, 0)

# if python says run, then we should run
if __name__ == '__main__':
  Bombing()