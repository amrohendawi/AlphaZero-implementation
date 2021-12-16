# Usage main.py -ai1 dummy -ai2 human -notimeout -show
# ai can be dummy, human, alphazero, (alphazero_x)
# only dummy works in this branch for now

def getFloat(argv,key,defaultValue):
	ret = defaultValue
	if key in sys.argv:
		ind = sys.argv.index(key)
		if ind+1 < len(sys.argv):
			ret = float(sys.argv[ind+1])
	return ret

def getString(argv, key, defaultValue):
	ret = defaultValue
	if key in sys.argv:
		ind = sys.argv.index(key)
		if ind+1 < len(sys.argv):
			ret = sys.argv[ind+1]
	return ret
	



import sys

import gamemanager as gm
from ai_dummy import ai_dummy
from ai_base import ai_base

if "-help" in sys.argv:
	print("Usage: ")
	print("     main.py -ai1 ai -ai2 ai -show")
	print("")
	print("Arguments:")
	print("     -ai1, -ai2 xx  : defines which kind of ai plays, xx can be dummy for now")
	print("     -show          : plots board after every turn with matplotlib")
	print("     -help          : shows help")
	print("     -delay xx      : delay in seconds after every turn, minimum 0.0")
	print("")
	print("Example: \"py main.py -ai1 dummy -ai2 dummy -show\"")
	print("")
	exit()

ai1 = ai_base(0)
ai2 = ai_base(1)
show = False

ai1name = getString(sys.argv, "-ai1","base")
if(ai1name == "dummy"):
	ai1 = ai_dummy(0)

ai2name = getString(sys.argv, "-ai2","base")
if(ai2name == "dummy"):
	ai2 = ai_dummy(1)

dly = getFloat(sys.argv, "-delay", 1.0)

if "-show" in sys.argv:
	show = True

game = gm.Manager(ai1, ai2, show, delay = dly)
game.run()
