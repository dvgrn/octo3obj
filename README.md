# octo3obj

This repo contains the relevant files for a new version of the octohash database.

The code for generating the 7-byte hashes (encoded as 9 bytes of searchable ASCII text, with spaces as separators) is slightly different between the octohash database and ths new octo3obj database.

The octo3obj data files are quite a bit larger than octohash data files, because the octohash database was an enumeration of all arrangements of up to two common small constructible objects inside a 12x12 bounding box -- whereas octo3obj is a similar enumeration of up to three of a more limited set of objects inside 11x11.

The objects in question are blinker, block, and beehive, plus some constellations of those objects that can be constructed by two colliding gliders:  half blockade, bi-block, and teardrop.

To run an octo3obj search, clone this repository, then select a search pattern in Golly and run find-by-octo3-Python3.py from the /code subfolder.  The script will search through hashes of the first 360 ticks of each collision, and will return any matches.

The seven-byte hashes are long enough that there are few or no hash collisions in the database (I haven't found any yet).  If a pattern occurs in any orientation, anywhere in the octo3obj database, the search script will reliably find it in a few seconds.

However, the match must be exact:  the search will completely fail to find a matching pattern if, for example, it's a perfect match except for a dying spark off to one side that will disappear in a few generations.  To find this kind of thing, it's usually best to search for an N-generation descendant of the pattern you actually want.  You may have to sort through a few false positives, but you'll also pick up the options that include temporary dying sparks.

