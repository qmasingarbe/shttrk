# coding: utf-8
from pprint import pprint #better print
from shttrk import * #lib shottracker

shttrk = shttrk("https://tracker.isartintra.com", "q.masingarbe", "yzq332")
pprint(shttrk.getAssetInfo(7153))


### TODO #### 7312
# updater tag en fonction de rrender / shotgun
# updater la miniature en fonction d'un dossier
# playblast direct sur shot
# set la durée en fonction d'un nombre de frame




'''
#compter combien de com par personne dans le project indique
projectId = 72
stat={}

#initialiser la connexion
trackerIsart = shttrk("https://tracker.isartintra.com", "q.masingarbe", "yzq332")

#recuperer un dict d'assets
assets = trackerIsart.getAssetsSimple(projectId)
print "Found {0} assets in project {1}".format(len(assets),projectId)
print "Starting counting coms ..."

#compter les com
for asset in assets: #iterer sur chaque asset
	assetId = assets[asset] #recuperer son id
	coms = trackerIsart.getComSimple(assetId) #recuperer les coms de cet asset
	for com in coms: #iterer sur chaque com
		if com[0] in stat:
			stat[com[0]]+=1
		else:
			stat[com[0]]=1

#printer proprement les stat
pprint(stat)
'''