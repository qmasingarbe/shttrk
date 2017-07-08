# coding: utf-8
###############
# shttrk example : python script for maya; post viewport screenshot in selected asset
###############

import maya.cmds as cmds
from shttrk import * #lib shottracker
import os
import re #regular expression

# connect to shottracher
shotTracker = shttrk("https://tracker.isartintra.com", "q.masingarbe", "******") # CHANGE HERE #

# update asset list when changing project
def projectChange(project):
    assets = shotTracker.getAssetsSimple(projects[project]) #list project's assets
    listOldAssets = cmds.optionMenu('dropdownMenuAsset', q=True, itemListLong=True) #get old list of assets
    if listOldAssets:
        cmds.deleteUI(listOldAssets) #empty list from old assets
    for asset in sorted(assets): #put new assests in dropdown menu
        cmds.menuItem(p='dropdownMenuAsset', label=asset)

# take and post a screenshot
def postScreenshot(arg):
    # take a screenshot
    xRes = cmds.getAttr('defaultResolution.width')
    yRes = cmds.getAttr('defaultResolution.height')
    currentFrame = int(cmds.currentTime(q=True))
    cmds.playblast(format='image', filename='D:/mayaScreenshot',sequenceTime=False, clearCache=True, viewer=False, showOrnaments=False, offScreen=True, percent=100, compression='jpg', quality=100, widthHeight=(xRes,yRes), fr=[currentFrame])
    
    # upload the screenshot
    assetName = cmds.optionMenu("dropdownMenuAsset",q=True, v=True) #query asset name
    assets = shotTracker.getAssetsSimple(projects[cmds.optionMenu('dropdownMenuProject',q=True, v=True)]) #query assets list
    for asset in assets: #iterate on assets to find asset id
        if asset == assetName: 
            idComment = shotTracker.postCom(assets[asset],'Screenshot from maya scene: {0}'.format(cmds.file(q=True, sceneName=True))) #post comment with text
            shotTracker.postFile(re.search(':(\d*)', idComment).group(1), 'D:/mayaScreenshot.0000.jpg') #attach screenshot to previously posted comment
            break
            
    # delete screenshot on local drive
    print "Clean file"
    os.remove("D:/mayaScreenshot.0000.jpg")


#window creation
if cmds.window("screenShhtrk", exists = True): #check if window open
    cmds.deleteUI("screenShhtrk")
cmds.window("screenShhtrk", title="Screenshot to shotTracker", sizeable=True, rtf=True) #window
cmds.columnLayout("leLayout", adj=True, cat=("both",10)) #layout

cmds.optionMenu("dropdownMenuProject",label="Choose a project :", cc=projectChange) #dropdown menu projects
projects = shotTracker.getProjects() #list projects
for project in sorted(projects):
    cmds.menuItem(label=project)
cmds.setParent("leLayout")

cmds.optionMenu("dropdownMenuAsset",label="Choose an asset :") #dropdown menu assets
assets = shotTracker.getAssetsSimple(projects[cmds.optionMenu('dropdownMenuProject',q=True, v=True)])
for asset in sorted(assets):
    cmds.menuItem(label=asset)
cmds.setParent("leLayout")

cmds.button("Post a screenshot", command=postScreenshot) #button post
cmds.setParent("leLayout")

cmds.showWindow("screenShhtrk")