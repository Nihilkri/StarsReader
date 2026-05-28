import random, math

WeaponData:dict = {}
def LoadWeapons():
  global WeaponData
  path = 'Weapons.csv'
  with open(path) as f:
    # Read off the headers.
    l = f.readline()
    h = l[:-1].split('\t')
    p = ()
    while len(l)>2:
      l = f.readline()
      p = l[:-1].split('\t')
      if len(p) >= 2:
        WeaponData[p[0]] = {h[i]:int(p[i]) if p[i].isdigit() else p[i] for i in range(0, len(h))}


class Weapon:
  def __init__(self, nweapon:str, nstack:int):
     self.Name:str = WeaponData[nweapon]["Name"]
     self.Energy:int = WeaponData[nweapon]["Energy"]
     self.Weapons:int = WeaponData[nweapon]["Weapons"]
     self.Propulsion:int = WeaponData[nweapon]["Propulsion"]
     self.Construction:int = WeaponData[nweapon]["Construction"]
     self.Electronics:int = WeaponData[nweapon]["Electronics"]
     self.Biotech:int = WeaponData[nweapon]["Biotech"]
     self.Mass:int = WeaponData[nweapon]["Mass"]
     self.Resources:int = WeaponData[nweapon]["Resources"]
     self.Ironium:int = WeaponData[nweapon]["Ironium"]
     self.Boranium:int = WeaponData[nweapon]["Boranium"]
     self.Germanium:int = WeaponData[nweapon]["Germanium"]
     self.Range:int = WeaponData[nweapon]["Range"]
     self.DP:int = WeaponData[nweapon]["DP"]
     self.Initiative:int = WeaponData[nweapon]["Initiative"]
     self.BaseAccuracy:int = WeaponData[nweapon]["Accuracy"] / 100.0
     self.Accuracy:int = WeaponData[nweapon]["Accuracy"] / 100.0
     self.Type:str = WeaponData[nweapon]["Type"]
     self.Typepl:str = WeaponData[nweapon]["Type"]
     self.Typepl += "es" if self.Typepl[-1] == "o" else "s"
     self.stack:int = nstack
     self.slot:int = None
     self.fleet = None
     self.target = None


class Ship:
  def __init__(self, nname:str, narmor:int, nshield:int, ninit:int, ncomps:tuple, njams:tuple, *nweapons:list):
    self.name:str = nname
    self.armor:int = narmor
    self.shield:int = nshield
    self.init:int = ninit
    self.comps:tuple = ncomps
    self.jams:tuple = njams
    self.weapons:list = nweapons
    for i, w in enumerate(self.weapons):
      w.slot = i
      w.Initiative += self.init + 1 * self.comps[0] + 2 * self.comps[1] + 3 * self.comps[2]
      if w.Type == "Torpedo" or w.Type == "Missile":
        w.Accuracy = math.floor(10000.0 * (1.0 - (1.0 - w.BaseAccuracy) *
                            (1.0 - 0.2) ** self.comps[0] *
                            (1.0 - 0.3) ** self.comps[1] *
                            (1.0 - 0.5) ** self.comps[2])) / 10000.0




class Fleet:
  def __init__(self, nracename:str, nraceplural:str, nship:Ship, nnumber:int):
    self.racename:str = nracename
    self.raceplural:str = nraceplural
    self.ship:Ship = nship
    self.number:int = nnumber
    self.shield:int = self.ship.shield * self.number
    self.damage:int = 0
    self.numleft:int = nnumber

  def hit(self, dmg:int, type:str) -> tuple[int, int]:
    admg, sdmg, dmg = 0, 0, 0
    if self.ship.shield > 0:
      if dmg > self.ship.shield:
        dmg -= self.ship.shield
        self.ship.shield = 0
      else:
        self.ship.shield -= dmg
        return 0
    if dmg > self.ship.armor:
      dmg -= self.ship.armor
      self.ship.armor = 0
    else:
      self.ship.armor -= dmg
      return 0
    return (ddmg, sdmg)



def Battlesim():
  LoadWeapons()
  # AC1
  #jihads:list = [Weapon("Jihad Missile", x) for x in [6,6,2,2,4]]
  #firestorm:Ship = Ship("Firestorm", 3650, 800, 10, (0,6,0), (0,0,0,0), *jihads)
  #f1:Fleet = Fleet("Hiserat", "Hiserati", firestorm, 1)
  #colloidals:list = [Weapon("Colloidal Phaser", x) for x in [3]]
  #ffr2:Ship = Ship("FF R2", 175, 120, 4, (0,0,0), (0,0,0,0), *colloidals)
  #f2:Fleet = Fleet("Nanite", "Nanites", ffr2, 50)
  # Testbed
  w1:list = [Weapon("Armageddon Missile", x) for x in [6,6,2,2,4]]
  s1:Ship = Ship("Shooter", 2000, 0, 10, (0,0,0), (0,0,0,0), *w1)
  f1:Fleet = Fleet("Attacking", "Attackings", s1, 1)
  w2:list = [Weapon("Blackjack", x) for x in [1]]
  s2:Ship = Ship("Wall", 32000, 7500, 2, (0,0,0), (0,0,0,0), *w2)
  f2:Fleet = Fleet("Defending", "Defendings", s2, 2)

  print("Battlesim")
  weaps = []
  for w in f1.ship.weapons:
    w.fleet = f1
    w.target = f2
    weaps.append(w)
  for w in f2.ship.weapons:
    w.fleet = f2
    w.target = f1
    weaps.append(w)
  weaps = sorted(weaps, key=lambda w:w.slot)
  weaps = sorted(weaps, key=lambda w:w.Range)
  weaps = sorted(weaps, key=lambda w:w.Initiative, reverse=True)

  for round in range(1, 2):
    print(f"Round {round}")
    for w in weaps:
      print(f"  Init {w.Initiative}: {w.fleet.racename} {w.fleet.ship.name} fires {w.Name} x{w.stack}:")
      # Reset counters for this weapon.
      shotshit, admg, sdmg, admg1, sdmg1, admg2, sdmg2 = 0, 0, 0, 0, 0, 0, 0
      if w.Type in ["Torpedo", "Missile"]:
        # Roll each shot, count the hits.
        for i in range(1, w.stack + 1):
          if random.random() < w.Accuracy:
            shotshit += 1
        # Calculate damage.
        admg, sdmg = w.DP * shotshit / 2.0, w.DP * shotshit / 2.0 + w.DP / 8.0 * (w.stack - shotshit)


        if shotshit > 0:
          txthit = (f"{shotshit}/{w.stack} ") + (f"{w.Typepl} hit" if shotshit > 1 else f"{w.Type} hits")
        else:
          txthit = (f"{w.stack} ") + (f"{w.Typepl} miss" if w.stack > 1 else f"{w.Type} misses")
        atxt = f"{admg} damage to armor" if admg > 0 else ""
        atxt += " and " if atxt != "" and sdmg > 0 else ""
        stxt = f"{sdmg} damage to shields" if sdmg > 0 else ""
        print(f"    {txthit} with {w.Accuracy * 100.0}% accuracy, dealing {atxt}{stxt}.")
      else:
        txthit = f"{w.Typepl} hit" if w.stack > 1 else f"{w.Type} hits"
        admg, sdmg = 0, w.DP * w.stack
        atxt = f"{admg} damage to armor" if admg > 0 else ""
        atxt += " and " if atxt != "" and sdmg > 0 else ""
        stxt = f"{sdmg} damage to shields" if sdmg > 0 else ""
        print(f"    {w.stack} {txthit}, dealing {atxt}{stxt}.")
    print("")
  


# if python says run, then we should run
if __name__ == '__main__':
  Battlesim()