# coding: utf-8
###############
# shttrk example : change thumbnails from folder (matching file name & asset name)
###############

from shttrk import * #lib shottracker
import os

# initialize variable
projectId = 72 # CHANGE HERE #
folderPath = "C:/Users/Quentin/Desktop/testShttrk" # CHANGE HERE # folder containing thumbnails

# initialize connection
trackerIsart = shttrk("https://tracker.isartintra.com", "q.masingarbe", "*****") # CHANGE HERE #

# get assets in project
assets = trackerIsart.getAssetsSimple(projectId)

#get files in folder
files = os.listdir(folderPath)

for oneFile in files: #iterate on files
	if os.path.isfile(os.path.join(folderPath,oneFile)): #file check
		for asset in assets: #iterate on assets
			if asset.lower() == os.path.splitext(oneFile)[0].lower(): #match assets and files
				print "Updating thumbnail in {0}".format(asset)
				trackerIsart.updateThumbnail(assets[asset], os.path.join(folderPath,oneFile))
				break