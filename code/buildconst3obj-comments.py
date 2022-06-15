# build-constellation-v15.py

import golly as g
from time import sleep
from glife.text import make_text

enable_table_output = 1

MAXOBJ=3
xsize,ysize=11,11

outfile = "C:/Users/greedd/Desktop/3obj/3obj-11x11-comments.txt"

# Python function to convert a cell list to RLE
# Author: Nathaniel Johnston (nathaniel@nathanieljohnston.com), June 2009.
#           DMG: Refactored slightly so that the function input is a simple cell list.
#                No error checking added.
#                TBD:  check for multistate rule, show appropriate warning.
#           AJP: Replace g.evolve(clist,0) with Python sort
#           DMG: switch to chunked coordinate input
# --------------------------------------------------------------------
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def giveRLE(clist_chunks):
    # clist_chunks = list (chunks (g.evolve(clist,0), 2))
    # clist_chunks = list(chunks(clist, 2))
    clist_chunks.sort(key=lambda l:(l[1], l[0]))
    mcc = min(clist_chunks)
    rl_list = [[x[0]-mcc[0],x[1]-mcc[1]] for x in clist_chunks]
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
    
    return rle_res+"!"


def getinp(s):
###########################
  temp=g.getcell(x,y)
  g.setcell(x,y,5)
  g.show(s+"Ptr:"+str(ptr)+" x:" +str(x)+" y:"+str(y))
  g.fit()
  g.update()
  g.setcell(x,y,temp)
  # return
  k=g.getevent()
  count=0
  while k=="":
    sleep(.01)
    k=g.getevent()
    count+=1
  if k=="key q none": g.exit()
  return
###########################



patdict={}
objs=["2o$2o!", # block
      "b2o$o2bo$b2o!","bo$obo$obo$bo!", # beehive
      "2o$2o2b2o$4b2o!","b2o$b2o3$2o$2o!","4b2o$2o2b2o$2o!","2o$2o3$b2o$b2o!", # half blockade
      "2ob2o$2ob2o!", "2o$2o2$2o$2o!", # bi-block
      "bo$obo$obo$bo3$6b2o$5bo2bo$6b2o!","6b2o$5bo2bo$6b2o3$bo$obo$obo$bo!","b2o$o2bo$b2o3$7bo$6bobo$6bobo$7bo!","7bo$6bobo$6bobo$7bo3$b2o$o2bo$b2o!", # teardrop
      "bo$3o$bo!"]  # and last but not least, the weird case -- blinkers
objlist=[]
for i in range(len(objs)):
  # normalize so that the first ON cell in the list is always (0,0)
  templist=g.parse(objs[i])
  objlist+=[g.transform(templist,-templist[0],-templist[1])]
numobjs=len(objlist)
zonelist=[]
for item in objlist:
  g.setrule("B12345678/S012345678")
  neighbors=g.evolve(item,1)
  g.setrule("B2345678/S012345678")
  zone=g.evolve(neighbors,1)
  zonelist+=[zone]    # includes cells for object also

g.setrule("LifeHistory")
# it's now very obvious that this was a bad idea -- objects that extend outside the frame should be caught with a separate check
nearlist=[[i,j] for i in range(-4,xsize+4) for j in range(-4,ysize+4) if i<0 or i>=xsize or j<0 or j>=ysize] # customized to catch teardrops
count,x,y,ptr,filledlist,searchlist=0,0,0,0,[],[]
while y==0 or len(searchlist)>0:
  overlap=([x,y] in nearlist)
  # place current object
  #############################################
  if overlap==0:
    # g.show(str(ptr))
    obj=g.transform(objlist[ptr],x,y)
    objpairs=[[obj[i],obj[i+1]] for i in range(0,len(obj),2)]
    for item in objpairs:
      if item in nearlist:
        overlap=1
        break
    if overlap==0:
      zone=g.transform(zonelist[ptr],x,y)
      zonepairs=[[zone[i],zone[i+1]] for i in range(0,len(zone),2)]
      for item in zonepairs:
        if item in filledlist:
          overlap=2
          break
      if overlap==0:
        g.new("TestPage")
        newptr,newx,newy=ptr+1,x,y
        if newptr>=len(objlist): newptr,newx=0,newx+1
        if newx>=xsize-1: newptr,newx,newy=0,0,y+1
        searchlist.append([newx,newy,newptr,nearlist[:],filledlist[:]]) # add next state to search to the stack
        nearlist+=zonepairs
        filledlist+=objpairs
        for i,j in nearlist: g.setcell(i,j,2)
        minx, maxx, miny, maxy = 999,-999,999,-999
        for i,j in filledlist:
          g.setcell(i,j,1)
          if i<minx:minx=i
          elif i>maxx:maxx=i
          if j<miny: miny=j
          elif j>maxy: maxy=j          
        # Take a snapshot of the current successful placement
        # [e.g., successful if two objects placed, etc.]
        if minx==0 and miny==0:
          keystr=str(1000+(maxx+1)*(maxy+1))[1:]+" "+str(maxx+1)+"x"+str(maxy+1)
          if keystr not in patdict: patdict[keystr]=[]
          if filledlist not in patdict[keystr]: patdict[keystr]+=[filledlist[:]]
        # Now continue searching from where we are
        count+=1
        if count%100==0:
          g.show(str(count))
          g.update()        
        ptr,x=0,x+4
      else:  # the neighbor zone for this object overlaps some already placed object
        ptr+=1
        if ptr>=len(objlist): ptr,x=0,x+1
    else: # the object itself overlaps some already placed object's neighborhood
      ptr+=1
      if ptr>=len(objlist): ptr,x=0,x+1
  else:
    ptr,x=0,x+1
  if x>=xsize-1: ptr,x,y=0,0,y+1
  if y>=ysize-1 or len(searchlist)>=MAXOBJ:
    # we've reached the end of the frame.
    # Time to clear the last placed object, go back to that x,y
    if searchlist==[]:
      g.new("TestPage")
      g.exit("Search is complete.")
    x,y,ptr,nearlist,filledlist=searchlist.pop()
# no point in looking at configurations with no object on the first line
g.new("TestPage")
outstr="Total count = " + str(count)
t=make_text(outstr,"mono")
g.putcells(t,0,-20)

f=open(outfile,"w")
for item in sorted(patdict):
  y=0
  t = make_text(item + " ("+str(len(patdict[item]))+")","mono")
  outstr+="\n" + item + " ("+str(len(patdict[item]))+")"
  g.putcells(t,x-6,y)
  y+=30
  # g.note(item)
  f.write("# CATEGORY size=" + item + "\n")
  for pat in patdict[item]:
    blinkercenters = []
    for i,j in pat:
      if [i-1,j] in pat and [i+1,j] in pat and [i,j-1] in pat and [i,j+1] in pat:
        blinkercenters+=[[i,j]]
    if len(blinkercenters)>0:
      if len(blinkercenters)==1:
        i,j = blinkercenters[0]
        patphase1=[coord for coord in pat if coord not in [[i-1,j],[i+1,j]]]
        f.write(giveRLE(patphase1)+"\n")
        if enable_table_output == 1:
            for cell in patphase1:
              g.setcell(cell[0]+x,cell[1]+y,1)
            y+=20
      elif len(blinkercenters)==2:
        i,j = blinkercenters[0]
        m,n = blinkercenters[1]
        patphase1=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m,n-1],[m,n+1]]]
        patphase2=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m-1,n],[m+1,n]]]
        f.write(giveRLE(patphase1)+"\n")
        f.write(giveRLE(patphase2)+"\n")
        if enable_table_output == 1:        
            for cell in patphase1:
                g.setcell(cell[0]+x,cell[1]+y,1)
            y+=20
            for cell in patphase2:
              g.setcell(cell[0]+x,cell[1]+y,1)
            y+=20
      elif len(blinkercenters)==3:
          i,j = blinkercenters[0]
          m,n = blinkercenters[1]
          o,p = blinkercenters[2]
          patphase1=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m,n-1],[m,n+1],[o-1,p],[o+1,p]]]
          patphase2=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m,n-1],[m,n+1],[o-1,p],[o+1,p]]]
          patphase3=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m-1,n],[m+1,n],[o-1,p],[o+1,p]]]
          patphase4=[coord for coord in pat if coord not in [[i-1,j],[i+1,j],[m-1,n],[m+1,n],[o-1,p],[o+1,p]]]
          f.write(giveRLE(patphase1)+"\n")
          f.write(giveRLE(patphase2)+"\n")
          f.write(giveRLE(patphase3)+"\n")
          f.write(giveRLE(patphase4)+"\n")
          if enable_table_output == 1:        
              for cell in patphase1:
                  g.setcell(cell[0]+x,cell[1]+y,1)
              y+=20
              for cell in patphase2:
                g.setcell(cell[0]+x,cell[1]+y,1)
              y+=20
              for cell in patphase3:
                g.setcell(cell[0]+x,cell[1]+y,1)
              y+=20
              for cell in patphase4:
                g.setcell(cell[0]+x,cell[1]+y,1)
              y+=20
      else:
        g.note("The general case with more than three blinkers is not yet handled in this code.  Skipping this configuration.")
    else:
      f.write(giveRLE(pat)+"\n")
      if enable_table_output == 1: 
          for cell in pat:
            g.setcell(cell[0]+x,cell[1]+y,1)
          y+=20
  f.flush()  # file ends up empty if I don't do this before the script ends
  x+=100
f.close()