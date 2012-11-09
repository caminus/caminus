#!/usr/bin/env python
# Prints out python code from a working Material.java from bukkit.
# https://github.com/Bukkit/Bukkit/raw/master/src/main/java/org/bukkit/Material.java
import re
f = open('Material.java')

dataMatch = re.compile("([A-Z][A-Z0-9_]+)\((.*)\),")
print "ITEMS = ["
for line in f.readlines():
  line = line.strip()
  matches = dataMatch.search(line)
  if matches:
    name = matches.group(1)
    params  = matches.group(2).split(',')
    id = int(params.pop(0))
    try:
      stack = int(params.pop(0))
    except:
      stack = 64
    try:
      durability = int(params.pop(0))
    except:
      durability = 0
    print "  {"
    print "    'name': '%s',"%(name)
    print "    'id': %d,"%(id)
    print "    'stack': %d,"%(stack)
    print "    'durability': %d,"%(durability)
    print "  },"
print "]"
