#!/usr/bin/env python

# from https://forum.kicad.info/t/python-script-for-setting-initial-size-and-visibility-of-all-module-references-values/617
 
from pcbnew import *
pcb = GetBoard()
moduleCount = 0
for aModule in pcb.GetModules():
	aModule.Reference().SetVisible(False)
	#aModule.Reference().SetHeight(1000000)
	#aModule.Reference().SetWidth(1000000)
	aModule.Value().SetVisible(False)
	#aModule.Value().SetHeight(1000000)
	#aModule.Value().SetWidth(1000000)
	moduleCount = moduleCount + 1

mc_str = str(moduleCount)
print('TextFormat script updated the text of '+mc_str+' Modules.')
print('[Board: '+pcb.GetFileName()+']')