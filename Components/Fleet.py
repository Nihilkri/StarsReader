class Fleet:
  def __init__(self, nrace, nname:str, nships:list=None):
    from Components import Race
    self.race:Race.Race = nrace
    self.name:str = nname
    self.maxfuel:int = 0
    self.maxcargo:int = 0
    if nships is None:
      print("Warning! No ships provided for fleet", self.name)
      self.ships = []
    else:
      from Components import Ship
      self.ships:list[tuple[Ship.Ship, int]] = nships
      for ship, num in self.ships:
        self.maxfuel += ship.maxfuel * num
        self.maxcargo += ship.maxcargo * num
    self.fuel:int = self.maxfuel

  def add_ship(self, nship, nnum):
    self.ships.append((nship, nnum))
    self.maxfuel += nship.maxfuel * nnum
    self.maxcargo += nship.maxcargo * nnum
    self.fuel += nship.maxfuel * nnum

  def remove_ship(self, ship):
    if ship in self.ships:
      self.ships.remove(ship)
  def get_ships(self):
    return self.ships
  def __str__(self):
    return f"Fleet: {self.name}, Ships: {len(self.ships)}"

  def initCargo(self, nfuel:int=0, niron:int=0, nbora:int=0, ngerm:int=0, ncols:int=0):
    self.fuel:int = nfuel
    self.iron:int = niron
    self.bora:int = nbora
    self.germ:int = ngerm
    self.cols:int = ncols
  def cargo(self):
    return self.fuel, self.iron , self.bora , self.germ , self.cols
  def cargomass(self):
    return self.iron + self.bora + self.germ + self.cols
  def emptymass(self):
    return sum([ship.mass * num for ship, num in self.ships])
  def mass(self):
    return self.emptymass() + self.cargomass()