# find-full-participation-collisions-v3.py
#   v1: first working version, very slow
#   v2: deal with smaller chunks of constellations, remove most duplicates, check for the rest
#   v3: move LONG_ENOUGH back up to 65536, skip stabilizations with populations repeating after 60 not just after 12

import golly as g

# this script doesn't add a new layer, so it will overwrite whatever's in the current Golly universe

WIDTH = 11
HEIGHT = 11
LONG_ENOUGH = 65536

g.setrule("B3/S23")

# the next three lines are just a standard Python trick to figure out where the script is saved
import os
import sys
defaultfolder = os.path.abspath(os.path.dirname(sys.argv[0]))

# Change the next line to a hard-coded path if you don't want to have to
#   choose the constellations.txt file every time you run the script

constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11B-11x11reduced.txt"

output_fname = "C:/path/to/3obj/11x11B-collisions-for-11x11-3obj-1G-stable.txt"
output2_fname = "C:/path/to/3obj/11x11B-collisions-for-11x11-3obj-1G-p2.txt"
output3_vanish_fname = "C:/path/to/3obj/11x11B-collisions-for-11x11-3obj-1G-vanish.txt"
output4_unusual_fname = "C:/path/to/3obj/11x11B-collisions-for-11x11-3obj-1G-long.txt"

# Ran the following one at a time to verify results.  TODO: refactor to work from a list of filenames
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11-to-06x11reduced.txt"
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11-to-07x11reduced.txt"
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11-to-08x11reduced.txt"
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11-to-09x11reduced.txt"
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11-09x11reduced.txt"
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11-10x10reduced.txt"
# constellation_fname = "C:/path/to/3obj/11x11groups/3obj-11x11A-11x11reduced.txt"

# Python function to convert a cell list to RLE
# Author: Nathaniel Johnston (nathaniel@nathanieljohnston.com), June 2009.
#           DMG: Refactored slightly so that the function input is a simple cell list.
#                No error checking added.
#                TBD:  check for multistate rule, show appropriate warning.
#           AJP: Replace g.evolve(clist,0) with Python sort
#           DMG: switch input to multistate, and -- just for this script -- don't return the trailing "!"
# --------------------------------------------------------------------

def coords(l):
    for i in range(0, len(l)-1, 3):
        yield l[i:i+2]

def giveRLEfrommultistate(clist):
    clist_coords = list(coords(clist))
    # g.note(str(clist) + "\n" + str(clist_coords))
    # g.exit()
    clist_coords.sort(key=lambda l:(l[1], l[0]))
    mcc = min(clist_coords)
    rl_list = [[x[0]-mcc[0],x[1]-mcc[1]] for x in clist_coords]
    rle_res = ""
    rle_len = 1
    rl_y = rl_list[0][1] - 1
    rl_x = 0
    for rl_i in rl_list:
        if rl_i[1] == rl_y:
            if rl_i[0] == rl_x + 1:
                rle_len += 1
            else:
                if rle_len == 1: rle_strA = ""
                else: rle_strA = str (rle_len)
                if rl_i[0] - rl_x - 1 == 1: rle_strB = ""
                else: rle_strB = str (rl_i[0] - rl_x - 1)
                
                rle_res = rle_res + rle_strA + "o" + rle_strB + "b"
                rle_len = 1
        else:
            if rle_len == 1: rle_strA = ""
            else: rle_strA = str (rle_len)
            if rl_i[1] - rl_y == 1: rle_strB = ""
            else: rle_strB = str (rl_i[1] - rl_y)
            if rl_i[0] == 1: rle_strC = "b"
            elif rl_i[0] == 0: rle_strC = ""
            else: rle_strC = str (rl_i[0]) + "b"
            
            rle_res = rle_res + rle_strA + "o" + rle_strB + "$" + rle_strC
            rle_len = 1
            
        rl_x = rl_i[0]
        rl_y = rl_i[1]
    
    if rle_len == 1: rle_strA = ""
    else: rle_strA = str (rle_len)
    rle_res = rle_res[2:] + rle_strA + "o"
    
    return rle_res     # +"!"
# --------------------------------------------------------------------
glider = g.parse("3o$o$bo!")

# backup way for the script to work:  have user choose a text file containing constellations
if constellation_fname == "C:/users/{USERNAME}/Desktop/constellations.txt":  # don't edit the path in this line
   constellation_fname = g.opendialog("Open constellation list", "Text files (*.txt)|*.txt", \
                                      defaultfolder, "constellations.txt", False)
   if constellation_fname == "": g.exit("No constellation list found.  Script has exited.")

if output_fname == "C:/users/{USERNAME}/Desktop/output-collisions.rle":  # don't edit the path in this line
   output_fname = g.savedialog("Pick a place for the output file", "RLE files (*.rle)|*.rle", \
                                      defaultfolder, "output-collisions.rle", False)
   if output_fname == "": g.exit("No output filename provided.  Script has exited.")

# create empty output files to append results to
outf=open(output_fname, "w")
outf.write("x = 0, y = 0, rule = B3/S23\n")
out2f=open(output2_fname, "w")
out2f.write("x = 0, y = 0, rule = B3/S23\n")
out3f=open(output3_vanish_fname, "w")
out3f.write("x = 0, y = 0, rule = B3/S23\n")
out4f=open(output4_unusual_fname, "w")
out4f.write("x = 0, y = 0, rule = B3/S23\n")
x, y, count, match = 0, 0, 0, 0
s = ""
rlecount = 0

with open (constellation_fname,"r") as f:
  rledata = f.readlines()
for rlestr in rledata:
  rlecount += 1
  if rlestr.startswith("#"):
    continue
  pat = g.parse(rlestr.replace("\n",""))
  mindiag, maxdiag, maxy = 99999,-99999, 0
  for i in range(0,len(pat),2):
    diag = pat[i]-pat[i+1]
    if diag<mindiag: mindiag = diag
    if diag>maxdiag: maxdiag = diag
    if pat[i+1]>maxy: maxy = pat[i+1]

  g.setrule("Interaction-test")
  g.new("Pre-test")
  g.putcells(pat, x, y)

  # find out if this constellation contains p2 stuff or not...
  testclist=str(g.getcells(g.getrect()))
  g.run(1)
  phases = 1 if str(g.getcells(g.getrect())) == testclist else 2
  # s += str(rlecount) + "," + str((maxdiag + 5 + HEIGHT + 2 - (mindiag - 5 + HEIGHT + 2)) * phases) + "\n"
  
  for lane in range(mindiag - 5 + HEIGHT + 2, maxdiag + 5 + HEIGHT + 2):
    for phase in range(0,phases):
      # this time, set up each pattern in state 3, with the appropriate phase of glider in state 1
      g.setrule("Interaction-prep")
      g.new("Test")
      g.putcells(pat, x, y)
    
      # use the Interaction-prep rule to change the pattern to the "not touched by the glider yet" State 3
      g.run(1) 
      count += 1

      # Make Golly update the screen every now and then
      if count % 100 == 0:
        g.show("Matches so far: " + str([match,count]) + " from " + str(rlecount) + " target patterns.")
        g.fit()
        g.update()
        outf.flush()
        out2f.flush()
        out3f.flush()
        out4f.flush()
      g.setrule("Interaction-test")
      g.run(phase)
      #  g.putcells(glider, lane, HEIGHT + 2)  ### "lane" was originally defined in relation to the full bounding box of the constellation enumeration
      g.putcells(glider, lane - HEIGHT + maxy + 1, maxy + 3)  ### this saves some time evolving the glider to cross guaranteed empty space
      
#    g.fit()
#    g.update()
#    c = g.getevent()
#    while c != "key c none":
#      c = g.getevent()
#    c = ""

      # run the pattern until the tick before the glider collides with something
      refpop = g.getpop()
      curpop = refpop
      skip = 0
      while curpop == refpop:
        r = g.getrect()  # it's easiest (though not fastest) to do this every time because there may be blinkers on the edges
        if r[1]<-5: # could be -1 because of a blinker on the top edge, 
          skip = 1  # but by -5 the glider has passed all the way through the constellation without affecting anything
          break
        canonpat = g.getcells(g.getrect())
        g.run(1)
        curpop = g.getpop()  # yes, it's a string. The comparison will still work.
      
      if not skip:
        # now check and make sure that every object in the constellation is potentially affected by the collision
        g.new("Closest approach")
        g.putcells(canonpat)

        g.run(LONG_ENOUGH)
        afterpat = g.getcells(g.getrect())
        afterpatstates = afterpat[2::3]
        p = g.getpop()
        g.run(60)
        unusual_osc = (p != g.getpop())
        # g.update()
        # g.note(str(afterpatstates))
        if 3 in afterpatstates:
          continue  # some live cells were left after trimming, meaning they didn't interact at all
        else:
          rle = giveRLEfrommultistate(canonpat).replace("\n","")
          if 1 not in afterpatstates:
            # we'll still want these for octo3obj results, but not for things like splitter and OTT searches
            out3f.write(rle+"50$\n") # pattern was empty or contained only leftover state-2 induction cells
          else:
            if phases==2:
              out2f.write(rle + "50$\n")
            else:
              outf.write(rle + "50$\n")
            match+=1        
            # write to an additional location if it's something weird
            if unusual_osc:
               rle = giveRLEfrommultistate(canonpat).replace("\n","")
               out4f.write(rle + "1000$\n")
            # g.note("Found something with a population period that isn't a factor of 60...")

# just for the record, make the output file into valid RLE
outf.write("!")
out2f.write("!")
out3f.write("!")
out4f.write("!")
outf.close()
out2f.close()
out3f.close()
out4f.close()
# g.open(output_fname)
g.show("Count: " + str(count))
