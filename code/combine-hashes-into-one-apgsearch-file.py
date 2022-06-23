# combine-hashes-into-one-apgsearch-file.py
# for details on running these kinds of files through apgsearch, see
#   https://conwaylife.com/wiki/Tutorials/Catagolue_stdin_symmetry
# -- or for the census results for these particular octo3obj files, see
#   https://conwaylife.com/forums/viewtopic.php?p=147468#p147468
# 3331973 lines in combined non-vanish files

import golly as g

files = "new-to6x11-stable.txt,new-to7x11-stable.txt,new-to8x11-stable.txt," + \
        "new-to9x11-stable-part1.txt,new-to9x11-stable-part2.txt," + \
        "new-09x11-stable-part1.txt,new-09x11-stable-part2.txt,new-10x10-stable.txt," + \
        "new-11x11-stable-part1.txt,new-11x11-stable-part2.txt," + \
        "new-to6x11-p2.txt,new-to7x11-p2-part1.txt,new-to7x11-p2-part2.txt,new-to8x11-p2.txt," + \
        "new-to9x11-p2-part1.txt,new-to9x11-p2-part2.txt," + \
        "new-09x11-p2-part1.txt,new-09x11-p2-part2.txt,new-10x10-p2.txt," + \
        "new-11x11-p2-part1.txt,new-11x11-p2-part2.txt"
fileslist=files.split(",")
fout = open("C:/Users/greedd/Desktop/3obj/apgsearch.txt", "w")
count = 0

for item in fileslist:
  with open("C:/Users/greedd/Desktop/3obj/new/" + item, "r") as f:
    all = f.readlines()
    for item in all:
      fout.write("x = 0, y = 0, rule = B3/S23\n")
      fout.write(item.replace("50$","!"))  # this replacement is important -- 
                                           # apgsearch will basically lock up if each RLE isn't terminated correctly
      count += 1
      if count % 10000 == 0 : g.show(str(count))
