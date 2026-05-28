import math
class Ship:
  def __init__(self, nfleet, nname:str, nemptymass:int, nmaxcargo:int=0):
    from Components import Fleet
    self.fleet:Fleet.Fleet = nfleet
    from Components import Race
    self.race:Race.Race = self.fleet.race
    self.name:str = nname
    self.emptymass:int = nemptymass
    self.maxcargo:int = nmaxcargo

  def initCombat(self, narmor:int, nshield:int, nbaseinit:int, ncomps:tuple, njams:tuple, *nweapons:list):
    self.armor:int = narmor
    self.shield:int = nshield
    self.baseinit:int = nbaseinit
    self.comps:tuple = ncomps
    self.jams:tuple = njams
    self.weapons:list = nweapons
    for i, w in enumerate(self.weapons):
      w.slot = i
      w.Initiative += self.baseinit + 1 * self.comps[0] + 2 * self.comps[1] + 3 * self.comps[2]
      if w.Type == "Torpedo" or w.Type == "Missile":
        w.Accuracy = math.floor(10000.0 * (1.0 - (1.0 - w.BaseAccuracy) *
                            (1.0 - 0.2) ** self.comps[0] *
                            (1.0 - 0.3) ** self.comps[1] *
                            (1.0 - 0.5) ** self.comps[2])) / 10000.0

  def initEngine(self, nengine, nnumengine:int, nmaxfuel:int, njets:int=0, nover:int=0):
    self.engine = nengine
    self.numengine:int = nnumengine
    self.maxfuel:int = nmaxfuel
    self.mj:int = njets
    self.ot:int = nover

  def cargo(self):
    ratio = 0 if self.maxcargo == 0 else self.maxcargo / self.fleet.maxcargo
    return tuple([math.floor(x * ratio) for x in self.fleet.cargo()])
  def cargomass(self):
    return 0 if self.maxcargo == 0 else self.maxcargo / self.fleet.maxcargo * self.fleet.cargomass()
  def mass(self):
    return self.emptymass + self.cargomass()

  def __hash__(self):
    return hash((self.name, self.owner))
  def __eq__(self, other):
    return (self.name, self.owner) == (other.name, other.owner)
  def __ne__(self, other):
    # Not strictly necessary, but to avoid having both x==y and x!=y
    # True at the same time
    return not(self == other)