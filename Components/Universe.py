
# Main database
dat = []
# Min and max star coordinates
minx, maxx, miny, maxy = 10000, 0, 10000, 0
# Screen to space scale, min and max as points, range of coordinates
skl, minxy, maxxy, fxy = 1.0, (1,1), (1,1), (1,1)
# View mode
mode = 4

class Universe:

  def __init__(self):
    self.planets = []