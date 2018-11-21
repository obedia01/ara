import json
from subprocess import call
from pathlib import Path
import time
import argparse

# Déclaration des paramètres
file_restart_relay="file_restart_relay.cmd"
file_credentials="credentials"
file_message_error="message_error.txt"
trouve=False
timestr = "\n-----------------------Check at "+ time.strftime("%Y%m%d-%H%M%S")+ "-----------------\n"


# Déclaration des URL
url1='http://ara-webservice.itp.echonet:80/datamanagement/a/AgentGroup?'
url2='http://ara-webservice.group.echonet'
# 
hfile_message_error=open(file_message_error,"a+")
hfile_message_error.write(timestr)

# Récupération des arguments
parser = argparse.ArgumentParser(description='Give arguments to check RELAY')
parser.add_argument('RELAY')
parser.add_argument('PROD')

args = parser.parse_args()

argument1=args.RELAY
argument2=args.PROD

# argument1 est le nom logique du serveur RELAY (exemple: RELAY_1A)
#argument1='RELAY_1B'

# argument2 indique l'environnement de Production: PROD-1 ou PROD-2
#argument2='PROD-1'

# test du premier argument
if argument1=='':
	message_error="The first argument is not provided"+"\n"
	hfile_message_error.write(message_error)
	raise ValueError(message_error)

# Test du second argument
if argument2=='PROD-1':
	url=url1
	indice_RELAY=[1,2,3,5]
elif argument2=='PROD-2':
	url=url2
	indice_RELAY=[4]
else:
	message_error="The second argument is not either PROD-1 or PROD-2"+"\n"
	hfile_message_error.write(message_error)
	raise ValueError(message_error)


# Récupération du fichier de credentials
path_credentials=Path(file_credentials)
if path_credentials.is_file():
	with open(file_credentials,'r') as file1:
		authARA=file1.read().replace('\n','')
else:
	message_error="The credentials file does not exist: "+file_credentials+"\n"
	hfile_message_error.write(message_error)
	raise ValueError(message_error)

# Récupération du résultat de l'appel au WS : statut des agents du serveur RELAY
#str='{"list":[{"host":"RELAY_1A_1","reachable":false},{"host":"RELAY_1A_2","reachable":true},{"host":"RELAY_1A_3","reachable":true} ]}'
str='{"list":[{"reachable":true,"osType":"WINDOWS","serverGroups":[{"categoryName":"Nexus FGAT","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"Nexus FGAT","id":"22399486"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"},{"categoryName":"RELAY_1_4","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"RELAY_1_4","id":"40353341"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"}],"usageCount":"315","state":"PRE_RUN","agentId":"fgat_nexus_1a","serverIP":"10.244.232.68","name":"RELAY_1A_4","description":"Automatically added","id":"23341384"},{"reachable":false,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"}],"usageCount":"0","state":"PRE_RUN","agentId":"RELAY_1B_4","serverIP":"10.244.233.64","name":"RELAY_1B_4","description":"Automatically added","id":"40467167"},{"reachable":false,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"Nexus FGAT II","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"Nexus FGAT II","id":"33784305"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - CARDIF","parentCategoryId":"12431856","categoryContext":"AUTHORIZATION","name":"ALL - CARDIF","id":"23398460"},{"categoryName":"RELAY_2_3","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"RELAY_2_3","id":"40353249"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"}],"usageCount":"6","state":"PRE_RUN","agentId":"fgat_nexus_11A","serverIP":"10.244.232.71","name":"RELAY_2A_3_TO_BE_DELETED","description":"Automatically added","id":"27040941"},{"reachable":true,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"},{"categoryName":"RELAY_2_4","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"RELAY_2_4","id":"40353353"}],"usageCount":"248","state":"PRE_RUN","agentId":"RELAY_2A_4","serverIP":"10.244.232.71","name":"RELAY_2A_4","description":"Automatically added","id":"40504897"},{"reachable":true,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"RELAY_TEST","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"RELAY_TEST","id":"81019948"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"}],"usageCount":"2","state":"PRE_RUN","agentId":"RELAY_2B_4","serverIP":"10.244.233.66","name":"RELAY_2B_4","description":"Automatically added","id":"40465520"},{"reachable":false,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - BNL","parentCategoryId":"4112313","categoryContext":"AUTHORIZATION","name":"ALL - BNL","id":"41233974"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - IRB","parentCategoryId":"32808930","categoryContext":"AUTHORIZATION","name":"ALL - IRB","id":"32809861"},{"categoryName":"ALL - CARDIF","parentCategoryId":"12431856","categoryContext":"AUTHORIZATION","name":"ALL - CARDIF","id":"23398460"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"}],"usageCount":"0","state":"PRE_RUN","agentId":"RELAY_2B_5","serverIP":"10.244.233.66","name":"RELAY_2B_5","description":"Automatically added","id":"40465517"},{"reachable":true,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"},{"categoryName":"RELAY_3_4","parentCategoryId":"26","categoryContext":"ARTIFACT_GETTER","name":"RELAY_3_4","id":"40353408"}],"usageCount":"277","state":"PRE_RUN","agentId":"RELAY_3A_4","serverIP":"10.244.232.72","name":"RELAY_3A_4","description":"Automatically added","id":"40460416"},{"reachable":true,"osType":"WINDOWS","serverGroups":[{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - ARA","parentCategoryId":"2198225","categoryContext":"AUTHORIZATION","name":"ALL - ARA","id":"39943537"},{"categoryName":"ALL - FGAT","parentCategoryId":"176369","categoryContext":"AUTHORIZATION","name":"ALL - FGAT","id":"22595629"}],"usageCount":"0","state":"PRE_RUN","agentId":"RELAY_3B_4","serverIP":"10.244.233.67","name":"RELAY_3B_4","description":"Automatically added","id":"40445428"}]}'
#print (str)
# Chargement de l'objet json
jData=json.loads(str)

# Ouverture du fichier de commande
hfile_commande=open(file_restart_relay,"w+")
file_content=''

# Fermeture du fichier de comessages d erreur
hfile_message_error.close()

# Parcours de l'objet json pour récupérer la liste des services Windows à relancer
for key in jData:
	if key=='list':
		jData2=jData[key]
		for key1 in jData2:
			if key1['reachable']==False:
				for i in indice_RELAY:
					if key1['name']==argument1+"_"+format(i):
						trouve=True
						file_content=file_content+"\necho Demarrage du service Nolio Agent "+format(i)+" >>"+file_message_error+"\n"
						file_content=file_content+"sc start \"Nolio Agent "+format(i)+"\" >>"+file_message_error+"\n"
						print("sc start Nolio Agent {0}".format(i))
# Génération du fichier de commandes de redémarrage des serveurs RELAY
hfile_commande.write(file_content)	

# Fermeture du fichier de commandes de redémarrage des serveurs RELAY
hfile_commande.close()

# appel du fichier de commandes de redémarrage des serveurs RELAY
if trouve==True:
	call(["cmd","/c",file_restart_relay])
					