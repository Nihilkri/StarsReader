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
  def screen(self, s2s):
    # Screen X, Screen Y, Screen point as complex
    self.sx:int = s2s[0]
    self.sy:int = s2s[1]
    self.xy:complex = (complex(self.sx, self.sy))
  def pla(self, n):
    if self.n != n[0]: return
    self.ownerstr  :str = n[1]
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
    print(f'#{self.i}, {self.n}; {self.ownerstr}, {self.starbase}, {self.reportage}, {self.pop}, {self.value}')
