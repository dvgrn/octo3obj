import golly as g
import hashlib

data = """11x11-collisions-for-11x11-3obj-1G-vanish.txt
09x11-collisions-for-11x11-3obj-1G-p2.txt
09x11-collisions-for-11x11-3obj-1G-stable.txt
09x11-collisions-for-11x11-3obj-1G-vanish.txt
10x10-collisions-for-11x11-3obj-1G-p2.txt
10x10-collisions-for-11x11-3obj-1G-stable.txt
10x10-collisions-for-11x11-3obj-1G-vanish.txt
11x11-collisions-for-11x11-3obj-1G-p2.txt
11x11-collisions-for-11x11-3obj-1G-stable.txt
to6x11-collisions-for-11x11-3obj-1G-p2.txt
to6x11-collisions-for-11x11-3obj-1G-stable.txt
to6x11-collisions-for-11x11-3obj-1G-vanish.txt
to7x11-collisions-for-11x11-3obj-1G-p2.txt
to7x11-collisions-for-11x11-3obj-1G-stable.txt
to7x11-collisions-for-11x11-3obj-1G-vanish.txt
to8x11-collisions-for-11x11-3obj-1G-p2.txt
to8x11-collisions-for-11x11-3obj-1G-stable.txt
to8x11-collisions-for-11x11-3obj-1G-vanish.txt
to9x11-collisions-for-11x11-3obj-1G-p2.txt
to9x11-collisions-for-11x11-3obj-1G-stable.txt
to9x11-collisions-for-11x11-3obj-1G-vanish.txt"""
datalist = data.split("\n")
outfnames = """11x11-vanish.txt
09x11-p2.txt
09x11-stable.txt
09x11-vanish.txt
10x10-p2.txt
10x10-stable.txt
10x10-vanish.txt
11x11-p2.txt
11x11-stable.txt
to6x11-p2.txt
to6x11-stable.txt
to6x11-vanish.txt
to7x11-p2.txt
to7x11-stable.txt
to7x11-vanish.txt
to8x11-p2.txt
to8x11-stable.txt
to8x11-vanish.txt
to9x11-p2.txt
to9x11-stable.txt
to9x11-vanish.txt"""
outfnamelist = outfnames.split("\n")

chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma

def get16char(inputstr):
  h = hashlib.sha1()
  h.update(inputstr.encode())
  i = 0  # convert first seven bytes of SHA1 digest to an integer
  for char in h.digest()[:15]:  # was 7
    i = i*256 + char
  s = ""
  while len(s)<17: # was 9
    d = i//90
    r = i - d*90
    s = chardict[r] + s
    i = (i - r) // 90   
  return s

def getoctohash(clist):
  ptr = 0
  g.new("Octotest")
  for orientation in [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
    g.putcells(clist,ptr*2048,0,*orientation)
    ptr += 1
  for j in range(8):
    g.select([2048*j-1024,-1024,2048,2048])
    g.shrink()
    r = g.getselrect()
    if r == []: r = [0,0,1,1]
    pat = g.getcells(r)
    deltax, deltay = 0, 0
    if pat != []:
      deltax, deltay = -pat[0], -pat[1]
    if j==0:
      minstr = str(g.transform(pat, deltax, deltay))
    else:
      strpat = str(g.transform(pat, deltax, deltay))
      if  strpat < minstr:
        minstr = strpat
  return " " + get16char(minstr)
  

# pat = g.parse("o$obo$2o!") # "3o$o$bo!")
# g.note(getoctohash(pat) + " *")

for i in range(len(datalist)):
  with open("C:/Users/greedd/Desktop/3obj/output/" + datalist[i],"r") as f:
    with open("C:/Users/greedd/Desktop/3obj/final/" + outfnamelist[i],"w") as f2:
      # in theory, matches can only happen inside a given file, so the lookup dictionary can be reset here
      dupedict = {}
      count = 0
      matchcount = 0
      exactmatchcount = 0
      all = f.readlines()[1:-1]
      for item in all:
        pat = g.parse(item[:-1])
        h = getoctohash(pat)
        if h in dupedict:
          if dupedict[h]==item[:-1]:
            exactmatchcount+=1
          else:
            # g.putcells(pat)
            # g.putcells(g.parse(dupedict[h]),32, 0)
            # g.fit()
            # g.update()
            matchcount +=1
            # TODO:  maybe report number of matches to a separate file?
        else:
          dupedict[h]=item[:-1]
          if count %100 ==0:
            g.show(datalist[i] + ": " + datalist[i] + ": Total count=" + str(count) + ", total matches=" + str(matchcount) + ", exact matches=" + str(exactmatchcount))
          count+=1
          f2.write(item)