# find-by-octo3.py
# Dave Greene, 17 June 2022 (Golly Python3)

import golly as g
import hashlib

searchfiles = "new-09x11-vanish-hashes.txt"
searchlist = searchfiles.split(",")
basepath = "C:/path/to/3obj/hashes/"

NUMLINES = 4652759
# diehard TL+block, in 11x11-vanish-hashes
# 6bo$5b3o$2o2bobobo$2ob3ob3o$4bobobo$5b3o$6bo!
# this p2 object
# 2ob2o$2ob2o$8b2o$7bo2bo$8b2o2$2bo7b2o$2bo7bobo$2bo7bo!
# turns into this p2 object:
# 12b2o$12b2o17bo$21bo8bobo$20bobo6bo2bo$21b2o7b2o$12b2o$11bobo$12bo19b2o$31bo2bo$32b2o3$13b2o$13b2o3$6bo9b3o$5bobo27b2o$5bobo27b2o$6bo2$b2o7b2o15b2o$o2bo5bo2bo14b2o30bo$b2o7b2o47bo$54b2o3bo$6bo46bo2bo$5bobo46b2o$5bobo24b3o$6bo$11b3o16bo5bo$30bo5bo$30bo5bo2$33b2o$19bo12bo2bo$18bobo12b2o$18bobo$19bo2$14b2o$13bo2bo$14b2o2$19bo13b3o$18bobo$18bobo$19bo!
# this dying spark
# 5b2o$3b5o$ob4obo$3o3b3o$3b2ob3o$6o$ob4o2bo$5bo2bo$5b2o!
# shows up only once in the database (so far).

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
  # The original implementation used paste operations into a Golly universe.
  # The first attempt to switch to sorting outside of Golly contained a bug, so hashes weren't orientation-independent.
  # All fixed now!
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

g.setalgo("HashLife")
g.setrule("B3/S23")

g.fitsel()
r = g.getselrect()
if r==[]:
  r = g.getrect()
  if r==[0]:
    g.exit("No pattern found to search for.")

count = NUMLINES
outptr = 0
pat = g.getcells(r)

g.addlayer()  # do tests in a new layer, then put results there
hash = getocto3(pat)
g.new("Output")
g.putcells(pat,-pat[0]-128,-pat[1])

for fingerprintfile in searchlist:
  with open(basepath+fingerprintfile, "r") as f:
    for line in f:
      count -= 1
      if hash in line:
        matchingpat = line[:line.index(" ")]
        g.putcells(g.parse(matchingpat),outptr*64,0)
        outptr+=1
        g.fit()
        g.update()
      if count % 1000 == 0:
        g.show("Searching.  Lines remaining: " + str(count/1000) + "K lines.")
plural = "" if outptr==1 else "s"
g.show("Found " + str(outptr) + " line" + plural + " matching " + hash + " in " + str(NUMLINES) + " lines of the octo3obj database.")
