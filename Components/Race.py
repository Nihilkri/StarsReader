

class Race:
  def __init__(self, nracename:str, nraceplural:str=None, nprt:str=None, nlrt:list=None, nclr:tuple=None):
    self.racename:str = nracename
    self.raceplural:str = (nracename + "s") if nraceplural is None else nraceplural
    self.prt = "" if nprt is None else nprt
    self.lrt = [] if nlrt is None else nlrt
    self.clr = (255, 255, 255) if nclr is None else nclr

  def WizHab(self, nmingrav:float, nmaxgrav:float, nmintemp:int, nmaxtemp:int, nminrad:int, nmaxrad:int, ngrowth:float):
    self.mingrav:float = nmingrav
    self.maxgrav:float = nmaxgrav
    self.mintemp:int = nmintemp
    self.maxtemp:int = nmaxtemp
    self.minrad:int = nminrad
    self.maxrad:int = nmaxrad
    self.growth:float = ngrowth

  def WizEcon(self, nwizpopeff:int=1000, nwizfacres:int=10, nwizfaccost:int=10, nwiznumfacs:int=10, nwizfacgerm:bool=False, nwizmineeff:int=10, nwizminecost:int=5, nwiznummines:int=10):
    self.wizpopeff:int = nwizpopeff
    self.wizfacres:int = nwizfacres
    self.wizfaccost:int = nwizfaccost
    self.wiznumfacs:int = nwiznumfacs
    self.wizfacgerm:bool = nwizfacgerm
    self.wizmineeff:int = nwizmineeff
    self.wizminecost:int = nwizminecost
    self.wiznummines:int = nwiznummines

    self.popeff:float = 1.0 / nwizpopeff
    self.facres:float = nwizfacres / 10.0
    self.faccost:int = nwizfaccost
    self.numfacs:int = nwiznumfacs / 10000.0
    self.facgerm:int = 3 if nwizfacgerm else 4
    self.mineeff:float = nwizmineeff / 10.0
    self.minecost:int = nwizminecost
    self.nummines:int = nwiznummines / 10000.0

  def WizTechs(self, nwizenergy:float=1.0, nwizweapons:float=1.0, nwizpropulsion:float=1.0, nwizconstruction:float=1.0, nwizelectronics:float=1.0, nwizbiotech:float=1.0, nwiztech3:bool=False):
    self.wizenergy:float = nwizenergy
    self.wizweapons:float = nwizweapons
    self.wizpropulsion:float = nwizpropulsion
    self.wizconstruction:float = nwizconstruction
    self.wizelectronics:float = nwizelectronics
    self.wizbiotech:float = nwizbiotech
    self.wiztech3:bool = nwiztech3
    self.initTechs()
  def initTechs(self):
    t = {
      "HE":(0, 0, 0, 0, 0, 0), "SS":(0, 0, 0, 0, 5, 0), "WM":(1, 5, 1, 0, 0, 0), "CA":(1, 1, 1, 0, 0, 6),
      "IS":(0, 0, 0, 0, 0, 0), "SD":(0, 0, 2, 0, 0, 2), "PP":(4, 0, 0, 0, 0, 0), "IT":(0, 0, 5, 5, 0, 0),
      "AR":(0, 0, 0, 0, 0, 0), "JoAT":(3, 3, 3, 3, 3, 3)}
    self.energy:int = max(t[self.prt][0], (4 if self.prt=="JoAt" else 3) if (self.wizenergy==1.75 and self.wiztech3) else 0)
    self.weapons:int = max(t[self.prt][1], (4 if self.prt=="JoAt" else 3) if (self.wizweapons==1.75 and self.wiztech3) else 0) + (1 if "IFE" in self.lrt else 0) + (1 if "CE" in self.lrt else 0)
    self.propulsion:int = max(t[self.prt][2], (4 if self.prt=="JoAt" else 3) if (self.wizpropulsion==1.75 and self.wiztech3) else 0)
    self.construction:int = max(t[self.prt][3], (4 if self.prt=="JoAt" else 3) if (self.wizconstruction==1.75 and self.wiztech3) else 0)
    self.electronics:int = max(t[self.prt][4], (4 if self.prt=="JoAt" else 3) if (self.wizelectronics==1.75 and self.wiztech3) else 0)
    self.biotech:int = max(t[self.prt][5], (4 if self.prt=="JoAt" else 3) if (self.wizbiotech==1.75 and self.wiztech3) else 0)
  def initTechs(self, nenergy:int=0, nweapons:int=0, npropulsion:int=0, nconstruction:int=0, nelectronics:int=0, nbiotech:int=0):
    self.energy:int = nenergy
    self.weapons:int = nweapons
    self.propulsion:int = npropulsion
    self.construction:int = nconstruction
    self.electronics:int = nelectronics
    self.biotech:int = nbiotech

  def initFleets(self, nfleets:list = None):
    self.fleets:list = [] if nfleets is None else nfleets
