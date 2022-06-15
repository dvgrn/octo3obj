import golly as g
import hashlib

infnames = """09x11-p2.txt
09x11-stable.txt
09x11-vanish.txt
10x10-p2.txt
10x10-stable.txt
10x10-vanish.txt
11x11-p2.txt
11x11-stable.txt
11x11-vanish.txt
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
  testpats = []
  if clist == []:
    minstr="[]"
  else:
    for orientation in [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
      # calling g.evolve() slows down processing a lot, but without this step, coordinates aren't sorted into canonical order
      # testpat = g.evolve(g.transform(clist,0,0,orientation[0],orientation[1],orientation[2],orientation[3]),0)
      testpat_chunks = list(chunks(clist, 2))
      testpat_chunks.sort(key=lambda l:(l[1], l[0]))
      mcc = min(testpat_chunks)  # notice this is the first ON cell in this orientation of pattern, NOT the upper left corner of the pattern's bounding box! ####
      sortedpatlist = [[x[0]-mcc[0],x[1]-mcc[1]] for x in testpat_chunks]
      testpats.append(sortedpatlist)
    minstr = min([str(pat) for pat in testpats])
  return get9char(minstr)

g.setalgo("HashLife")
g.setrule("B3/S23")
count = 0
for i in range(len(infnames)):
  with open("C:/Users/greedd/Desktop/3obj/final/" + infnamelist[i],"r") as f:
    with open("C:/Users/greedd/Desktop/3obj/hashes/" + infnamelist[i].replace(".txt","-hashes.txt"),"w") as f2:
      all = f.readlines()
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
        count+=1
        f2.write(s+"\n")