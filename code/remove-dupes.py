# remove-dupes.py
# version 2:  corrected a problem with the hash function

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
outfnames = """new-11x11-vanish.txt
new-09x11-p2.txt
new-09x11-stable.txt
new-09x11-vanish.txt
new-10x10-p2.txt
new-10x10-stable.txt
new-10x10-vanish.txt
new-11x11-p2.txt
new-11x11-stable.txt
new-to6x11-p2.txt
new-to6x11-stable.txt
new-to6x11-vanish.txt
new-to7x11-p2.txt
new-to7x11-stable.txt
new-to7x11-vanish.txt
new-to8x11-p2.txt
new-to8x11-stable.txt
new-to8x11-vanish.txt
new-to9x11-p2.txt
new-to9x11-stable.txt
new-to9x11-vanish.txt"""
outfnamelist = outfnames.split("\n")

chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma

def get9char(inputstr):
  h = hashlib.sha1()
  h.update(inputstr.encode())
  i = 0  # convert first seven bytes of SHA1 digest to an integer
  for char in h.digest()[:7]:
    i = i*256 + char
  s = ""
  while len(s)<9:
    d = i//90
    r = i - d*90
    s = chardict[r] + s
    i = (i - r) // 90   
  return s

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def getocto3(clist):
  testpats = []
  if clist == []:
    minstr="[]"
  else:
    testpat_chunks = list(chunks(clist, 2))  # start with the un-transformed pattern, look for something lexicographically smaller
    testpat_chunks.sort(key=lambda l:(l[1], l[0]))
    firstx, firsty = testpat_chunks[0][0],testpat_chunks[0][1]
    minstr = str([[coord[0]-firstx,coord[1]-firsty] for coord in testpat_chunks])
    for orientation in [[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
      # calling g.evolve() slows down processing a lot, but without this step, coordinates aren't sorted into canonical order
      testpat = g.transform(clist,0,0,orientation[0],orientation[1],orientation[2],orientation[3])
      testpat_chunks = list(chunks(testpat, 2))
      testpat_chunks.sort(key=lambda l:(l[1], l[0]))
      # g.note("Before canonicalization: " + str(testpat_chunks))  ###############
      # notice this is the first ON cell in this orientation of pattern, NOT the upper left corner of the pattern's bounding box! ####
      firstx, firsty = testpat_chunks[0][0],testpat_chunks[0][1]
      sortedpatstr = str([[coord[0]-firstx,coord[1]-firsty] for coord in testpat_chunks])
      # g.note(sortedpatstr)
      if sortedpatstr<minstr: minstr = sortedpatstr
  return get9char(minstr)  

# Voice of Experience:  don't start collecting hashes until this definitely returns all the same hash value...
# s = getocto3(g.parse("3o$o$bo!"))+"\n"+getocto3(g.parse("3o$2bo$bo!"))+"\n"+ \
#     getocto3(g.parse("bo$o$3o!"))+"\n"+getocto3(g.parse("bo$2bo$3o!"))+"\n"+ \
#     getocto3(g.parse("o$obo$2o!"))+"\n"+getocto3(g.parse("2bo$obo$b2o!"))+"\n"+ \
#     getocto3(g.parse("b2o$obo$2bo!"))+"\n"+getocto3(g.parse("2o$obo$o!"))+"\n"
# g.note(s)
# g.exit()

s=""
for i in range(len(datalist)):
  with open("C:/Users/greedd/Desktop/3obj/output/" + datalist[i],"r") as f:
    with open("C:/Users/greedd/Desktop/3obj/new/" + outfnamelist[i],"w") as f2:
      # in theory, matches can only happen inside a given file, so the lookup dictionary can be reset here
      dupedict = {}
      count = 0
      matchcount = 0
      exactmatchcount = 0
      all = f.readlines()[1:-1]
      for item in all:
        pat = g.parse(item[:-1])
        h = getocto3(pat)
        if h in dupedict:
          if dupedict[h]==item[:-1]:
            matchcount+=1
            exactmatchcount+=1
          else:
            # g.new("")
            # g.putcells(pat)
            # g.putcells(g.parse(dupedict[h]),32, 0)
            # g.fit()
            # g.update()
            # g.note("Same but not...")
            matchcount +=1
        else:
          dupedict[h]=item[:-1]
          if count %100 == 0:
            g.show(datalist[i] + ": " + datalist[i] + ": Total count=" + str(count) + ", total matches=" + str(matchcount) + ", exact matches=" + str(exactmatchcount))
          count+=1
          f2.write(item)
      s += datalist[i] + ":  total count=" + str(count) + ", total matches=" + str(matchcount) + ", exact matches=" + str(exactmatchcount) + "\n"
g.note(s)
g.setclipstr(s)
