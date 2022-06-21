# find-by-octo3.py
# Dave Greene, 17 June 2022 (Golly Python3)
import golly as g
import hashlib

searchfiles = "new-to6x11-vanish-hashes.txt,new-to7x11-vanish-hashes.txt,new-to8x11-vanish-hashes.txt,new-to9x11-vanish-hashes.txt," + \
              "new-09x11-vanish-hashes.txt,new-10x10-vanish-hashes.txt,new-11x11-vanish-hashes.txt," + \
              "new-to6x11-stable-hashes.txt,new-to6x11-p2-hashes.txt,new-to8x11-stable-hashes.txt,new-11x11-p2-part1-hashes.txt,new-11x11-p2-part2-hashes.txt," + \
              "new-to9x11-stable-part1-hashes.txt,new-to9x11-stable-part2-hashes.txt," + \
              "new-to8x11-p2-hashes.txt,new-09x11-stable-part1-hashes.txt,new-09x11-stable-part2-hashes.txt,new-10x10-p2-hashes.txt,new-10x10-stable-hashes.txt," + \
              "new-to9x11-p2-part1-hashes.txt,new-to9x11-p2-part2-hashes.txt,new-11x11-stable-part1-hashes.txt,new-11x11-stable-part2-hashes.txt," + \
              "new-to7x11-stable-hashes.txt,new-to7x11-p2-hashes.txt,new-09x11-p2-part1-hashes.txt,new-09x11-p2-part2-hashes.txt"
searchlist = searchfiles.split(",")
basepath = "C:/path/to/3obj/hashes/"

NUMLINES = 2637764 # TODO: get the new number, update

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
