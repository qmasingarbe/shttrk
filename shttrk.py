####	SHTTRK	  ####
# Python library to connect to shottracker
# v1.1 - 2017
######################

import requests #connect to shottracker
import re #parse results
import HTMLParser #parse html
parser = HTMLParser.HTMLParser()

class shttrk():
	def __init__(self, url, login, password):
		s = requests.Session() #request object
		s.get(url) #ping url (add verify=False if problem in local connection)
		s.post(url+'/index.php', data={'login': login, 'password': password }) #connect
		self.session = s
		self.url = url

	######	  UTILITY	  ######
	def postEncode(self,json,dataDict):
		response = self.session.post(self.url+json, data=dataDict)
		response = response.text.encode('utf8')
		return response


	######	  PROJECT	  ######
	def getProjects(self): #dict
		#download html homepage
		response=self.session.get(self.url+'/index.php')
		response=response.text.encode('utf8')
		#find list of projects in html
		match=re.findall("<OPTION role='0' value='(\d*)'.*>(.*)<\/option>",response)
		#faire un dict et inverser key value
		response= {value: key for key, value in dict(match).iteritems()}
		return response

	######	  ASSETS	  ######
	def getAssets(self, project): #LIST recuperer list des assets et de leurs info en dict
		if type(project)=="int":
			project=str(project)
		#requete des assets
		response=self.session.get(self.url+'/json/get-items.php?id='+str(project))
		#json to list
		return response.json()

	def getAssetsSimple(self, project): #DICT recuperer simplement dictionnaire des assets et leurs id
		response=self.getAssets(project)
		data={}
		for asset in response:
			data[asset['name']]=asset['id']
		return data

	def getAssetsInBin(self,project): #LIST recuperer list des assets correspondant au tag POUBELLE et leurs info en dict
		#verifier le numero de projet
		if type(project)=="int":
			project=str(project)
		#requete des assets 
		response=self.session.post(self.url+'/json/get-items.php?id='+str(project), data={'tags[]': 0 , 'sort': 1 })
		#json to list
		return response.json()

	def createAsset(self,project,name,description='',length='0'): #CREER un nouveau asset a partir de son nom
		name=str(name)
		length=str(length)
		return self.postEncode('/json/create-item-info.php',{'name': name, 'length': length, 'decription': description, 'id_project': project })

	def deleteAsset(self,asset): #DELETE un asset en fonction de son id
		if type(asset)=="int":
			asset=str(asset)
		return self.postEncode('/json/delete-item.php',{'id':asset})

	######    ASSET INFO    ######
	def getAssetInfo(self,assetId):
		response=self.session.post(self.url+'/json/get-details.php?id='+str(assetId))
		data = response.json()
		del data['comments']
		return data

	def updateInfo(self,asset,name=False,length=False,description=False,storage=False):
		assetInfo = self.getAssetInfo(asset)
		if name:
			name = assetInfo['name']
		if length==False:
			length = assetInfo['length']
		if description==False:
			description = assetInfo['description']
		if storage==False:
			storage = assetInfo['storage']
		return self.postEncode('/json/save-item-info.php',{'id':asset,'name':name,'length':str(length),'description':description,'storage':storage})

	def updateThumbnail(self,asset,pathToFile):
		response = self.session.post(self.url+'/upload-vignette.php?id='+str(asset),files={'file': open(pathToFile,'rb')})
		response = response.text.encode('utf8')
		return response


	######	  COMMENTS	######
	def getCom(self,asset): #LIST recuperer list des com dun asset et de leurs info en dict
		#verifier le numero asset
		if type(asset)=="int":
			asset=str(asset)
		#requete des detail de asset
		response=self.session.get(self.url+'/json/get-details.php?id='+str(asset))
		#json to list
		data = response.json()
		return data['comments']

	def getComSimple(self,asset): #LIST recuperer simplement list avec com en text et nom et id
		response=self.getCom(asset)
		data=[]
		#garder les bon donnees dans un tableau
		for com in response:
			#retirer les balises html du text
			leCom=re.sub('<[^>]*>','',parser.unescape(com['text']))
			#test=leCom.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2022", "'")
			#leCom=test.encode("latin1").decode("latin1")
			data.append([com['firstname']+' '+com['lastname'],leCom,com['id_comment']])
		return data

	def postCom(self,asset,text,user=1): #poster un commentaire !!! default user to first user !!!
		return self.postEncode('/json/save-item-comment.php',{'id_item': asset, 'text': text,'id_user': user})

	def updateCom(self,com,newtext): #changer le contenu d'un commentaire ! fonctionne sur les commentaires de tout le monde !
		return self.postEncode('/json/update-comment.php',{'id':com,'text':newtext})

	def deleteCom(self,com): #supprimer un commentaire
		return self.postEncode('/json/delete-comment.php',{'id': com})

	######	  LIKE	  ######
	def likeCom(self,com): #mettre un +1
		return self.postEncode('/json/like-comment.php',{'id-comment':com})

	def dislikeCom(self,com): #enlever le +1
		return self.postEncode('/json/dislike-comment.php',{'id-comment':com})

	######	  COMMENTS ATTACHEMENTS	  ######
	def postFile(self,com,pathToFile): #attacher un file a un commentaire
		response = self.session.post(self.url+'/upload-attach.php?id='+str(com),files={'file': open(pathToFile,'rb')})
		response = response.text.encode('utf8')
		return response

	def deleteFile(self, asset, com, fileId): #deleter un file a partir de l'id du file
		response = self.session.get(self.url+'/json/get-details.php?id='+str(asset))
		data = response.json() #convertir le json en dict
		reponse=False
		for comment in data['comments']: #iterer sur le com
			if comment['id_comment']==str(com): #chercher le bon com
				for fichier in comment['files']: #iterer sur le files du com
					splitting=fichier['file'].split('/')
					if splitting[len(splitting)-1]==fileId: #chercher le bon file dans le com
						response = self.session.post(self.url+'/json/update-comment.php', data={'id': com, 'text': comment['text'], 'delete-attach[]': fichier['id']}) #supprimer le file
						response = response.text.encode('utf8')
						break;
					else:
						response=False
				break;
			else:
				response=False
		return response

	#####     TAGS     #####
	def getAllTags(self,project): #recuperer tous les tags dispo sur un projet
		response=self.session.post(self.url+'/json/get-tags.php', data={'id': project})
		data = response.json()
		response=data["generic"]+data["specific"] #assembler les tags en une list
		return response

	def getAllTagsSimple(self,project): #recuperer dict nom et id des tags
		response=self.getAllTags(project)
		data={}
		for tag in response:
			data[tag['name']]=tag['id']
		return data

	def createTag(self,projectId,name): #creer un simple tag pour le projet
		return self.postEncode('/json/add-tag.php',{'type':100, 'name':str(name),'id':projectId})

	def deleteTag(self,tagId): #supprimer un tag sur tout le projet
		return self.postEncode('/json/delete-tag.php',{'id':tagId})

	def addTag(self,assetId,tagId): #ajouter un tag sur asset (tagId 0 pour mettre a la poubelle)
		return self.postEncode('/json/add-tag-item.php',{'id-tag':tagId,'id-item':assetId})

	def findSpecificTagId(self,assetId,tagId):
		assetInfo = self.getAssetInfo(assetId)
		idSpecific=False
		for tag in assetInfo['tags']:
			if tag['id_tag']==str(tagId):
				idSpecific = tag['id']
				break;
		return idSpecific

	def removeTag(self,assetId,tagId):
		idSpecific = self.findSpecificTagId(assetId,tagId)
		if idSpecific:
			response = self.postEncode('/json/remove-tag-item.php',{'id':idSpecific})
		else:
			response = "Pas de tag correspondant"
		return response

	def updateTag(self,assetId, tagId, state):
		if type(state)=='int':
			idSpecific = self.findSpecificTagId(assetId,tagId)
			if idSpecific:
				response = self.postEncode('/json/update-tag-item.php',{'id':idSpecific,'value':str state)})
			else:
				response = "Pas de tag correspondant"
		else:
			response =  "Etat n'est pas un nombre"
		return response