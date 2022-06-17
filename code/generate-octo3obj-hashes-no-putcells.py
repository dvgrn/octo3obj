import golly as g
import hashlib
import itertools

sourcepath, targetpath = "C:/path/to/3obj/new/", "C:/path/to/3obj/hashes/"
infnames = """new-09x11-p2-part1.txt
new-09x11-p2-part2.txt
new-09x11-stable-part1.txt
new-09x11-stable-part2.txt
new-09x11-vanish.txt
new-10x10-p2.txt
new-10x10-stable.txt
new-10x10-vanish.txt
new-11x11-p2-part1.txt
new-11x11-p2-part2.txt
new-11x11-stable-part1.txt
new-11x11-stable-part2.txt
new-11x11-vanish.txt
new-to6x11-p2.txt
new-to6x11-stable.txt
new-to6x11-vanish.txt
new-to7x11-p2.txt
new-to7x11-stable.txt
new-to7x11-vanish.txt
new-to8x11-p2.txt
new-to8x11-stable.txt
new-to8x11-vanish.txt
new-to9x11-p2-part1.txt
new-to9x11-p2-part2.txt
new-to9x11-stable-part1.txt
new-to9x11-stable-part2.txt
new-to9x11-vanish.txt"""
infnamelist = infnames.split("\n")

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
# s = getocto3(g.parse("3o$o$bo!"))+"\n"+getocto3(g.parse("3o$2bo$bo!"))+"\n"+ \
#     getocto3(g.parse("bo$o$3o!"))+"\n"+getocto3(g.parse("bo$2bo$3o!"))+"\n"+ \
#     getocto3(g.parse("o$obo$2o!"))+"\n"+getocto3(g.parse("2bo$obo$b2o!"))+"\n"+ \
#     getocto3(g.parse("b2o$obo$2bo!"))+"\n"+getocto3(g.parse("2o$obo$o!"))+"\n"
# g.note(s)
# g.exit()

for i in range(len(infnames[:1])):
  with open(sourcepath + infnamelist[i],"r") as f:
    with open(targetpath + infnamelist[i].replace(".txt","-hashes.txt"),"w") as f2:
      all = f.readlines()
      count = len(all)
      for item in all:
        s = item[:-4]+"! "
        pat = g.parse(s)
        for ticks in range(360):  # arbitrarily chosen due to the length of the longest vanish reactions I saw in a partial survey
          h = getocto3(pat)+" "
          if s.find(" "+h)!=-1:
            s+=h  # add the repeating hash at the end to show the repetition period
            break
          s+=h
          pat = g.evolve(pat,1)
        if count %10 == 0:
          g.show(infnamelist[i] + ":  Total count=" + str(count))
          f.flush()
        count-=1
        f2.write(s+"\n")
