# coding: utf-8
###############
# shttrk example : clone assets from shotgun project to shottracker project (with thumbnails & tags)
###############

import shotgun_api3 #lib shotgun
import shttrk #lib shottracker
import urllib #lib to download from web
import os
import pprint

sgProjectId = 167 # CHANGE HERE # id of shotgun project to clone from
stProjectId = 25 # CHANGE HERE # id of shottracker project to clone assets into

sg = shotgun_api3.Shotgun("https://#########.shotgunstudio.com",login="#########",password="#########") # CHANGE HERE # connect to shotgun
st = shttrk.shttrk("http://#########", "#########", "#########") # CHANGE HERE # connect to shottracker

# checking thumbnail download directory
if not os.path.exists('D:/SGtoSTtemp'):
    os.makedirs('D:/SGtoSTtemp')

#####################################
# download infos from shotgunstudio #
#####################################
print "--- SHOTGUN ---"
# requests to shotgun
assets = sg.find('Asset',[['project','is', {'type': 'Project','id': sgProjectId}]],['id','code','description','image','sg_status_list','sg_asset_type']) #get a list of dict, each dict contains the infos asked for an asset
print "Found {0} assets in SG project {1}".format(len(assets),sgProjectId)

# sorting unique assets tags
assetType = []
assetStatus = []
i=0
for asset in assets:
	i+=1
	if asset['sg_asset_type'] not in assetType:
		assetType.append(asset['sg_asset_type'])
	if asset['sg_status_list'] not in assetStatus:
		assetStatus.append(asset['sg_status_list'])
	if asset['image']: #if thumbnail available
		print "Downloading thumbnail {0}/{1} : {2}".format(i,len(assets),asset['code'])
		urllib.urlretrieve (asset['image'], "D:/SGtoSTtemp/{0}.jpg".format(asset['code'])) #download thumbnail in temp location

pprint.pprint(assetType)
pprint.pprint(assetStatus)

################################
# create assets in shottracker #
################################
print "--- SHOTTRACKER ---"
allTags = st.getAllTagsSimple(stProjectId) #get all tags in shottracker

# create non existent simple tags
for eachAssetType in assetType:
	if eachAssetType not in allTags.keys():
		print "Creating tag {0}".format(eachAssetType)
		print st.createTag(stProjectId,eachAssetType)

# create or update complexe tag sg_status
if 'sg_status' in allTags.keys():
	print st.deleteTag(allTags['sg_status']) #delete existing asset named sg_status
data = {'type':2, 'name':'sg_status', 'id':stProjectId}
i=0
for status in assetStatus:
	data['values['+str(i)+'][n]']=status.upper()
	data['values['+str(i)+'][v]']=i
	data['values['+str(i)+'][c]']='#ffcc00'
	i+=1
print "Updating sg_status tag"
print st.postEncode('/json/add-tag.php',data)

allTags = st.getAllTagsSimple(stProjectId) #update tag list

#create assets
stAssets = st.getAssetsSimple(stProjectId)
for asset in assets:
	# asset creation, name, description
	if asset['code'] not in stAssets:
		newAsset = st.createAsset(stProjectId,asset['code'],description=asset['description'])
		print "Asset {0} created on ShotTracker".format(asset['code'])
		stAssets = st.getAssetsSimple(stProjectId)
		newAssetId = stAssets[asset['code']]
	else:
		newAssetId = stAssets[asset['code']]
	# add thumbnail
	if asset['image']: #if thumbnail available
		print st.updateThumbnail(newAssetId,"D:/SGtoSTtemp/{0}.jpg".format(asset['code']))
		print "Thumbnail updated on {0}".format(asset['code'])
	# add tag type
	if asset['sg_asset_type']:
		print st.addTag(newAssetId,allTags[asset['sg_asset_type']])
		print "Tag updated on {0}".format(asset['code'])
	# add tag status
	if asset['sg_status_list']:
		print st.addTag(newAssetId,allTags['sg_status'])
		print st.updateTag(newAssetId,allTags['sg_status'],assetStatus.index(asset['sg_status_list']))
		print "sg_status updated on {0}".format(asset['code'])


#########
# Clean #
#########
import shutil
shutil.rmtree('D:/SGtoSTtemp')
print "Temp directory deleted"