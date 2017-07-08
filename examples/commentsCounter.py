# coding: utf-8
###############
# shttrk example : count the number of comments for each people on a project
###############

from shttrk import * #lib shottracker
from pprint import pprint #better print

# initialize variable
projectId = 72 # CHANGE HERE #
stat={}

# initialize connection
trackerIsart = shttrk("https://tracker.isartintra.com", "q.masingarbe", "******") # CHANGE HERE #

# get assets dictionnary
assets = trackerIsart.getAssetsSimple(projectId)

print "Found {0} assets in project number {1}".format(len(assets),projectId)
print "Starting counting coms ..."

# counting comments
for asset in assets: #iterate on assets
	assetId = assets[asset] #get asset id
	coms = trackerIsart.getComSimple(assetId) #get comments of this asset
	for com in coms: #iterate on comments
		if com[0] in stat:
			stat[com[0]]+=1
		else:
			stat[com[0]]=1

#pretty print stats
pprint(stat)