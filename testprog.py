import json
from subprocess import call
from pathlib import Path
import time

# Déclaration des paramètres
file_restart_relay="file_restart_relay.cmd"
file_credentials="credentials"
file_message_error="message_error.txt"
trouve=False
timestr = "\nCheck at "+ time.strftime("%Y%m%d-%H%M%S")+ "\n"

# 
hfile_message_error=open(file_message_error,"a+")
hfile_message_error.write(timestr)

# Déclaration des URL
url1='http://ara-webservice.itp.echonet:80/datamanagement/a/AgentGroup?'
url2='http://ara-webservice.group.echonet'

# Récupération des arguments
# argument1 est le nom logique du serveur RELAY (exemple: RELAY_1A)
argument1='RELAY_1A'

# argument2 indique l'environnement de Production: PROD-1 ou PROD-2
argument2='PROD-1'

# test du premier argument
if argument1=='':
	message_error="The first argument is not provided"+"\n"
	hfile_message_error.write(message_error)
	raise ValueError(message_error)

# Test du second argument
if argument2=='PROD-1':
	url=url1
elif argument2=='PROD-2':
	url=url2
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
str='{"list":[{"host":"RELAY_1A_1","reachable":false},{"host":"RELAY_1A_2","reachable":true},{"host":"RELAY_1A_3","reachable":true} ]}'
print (str)
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
				for i in [1,2,3,4,5]:
					if key1['host']==argument1+"_"+format(i):
						trouve=True
						file_content=file_content+"\necho Demarrage du service Nolio Agent "+format(i)+" >>"+file_message_error+"\n"
						file_content=file_content+"sc start Nolio Agent "+format(i)+" >>"+file_message_error+"\n"
						print("sc start Nolio Agent {0}".format(i))
# Génération du fichier de commandes de redémarrage des serveurs RELAY
hfile_commande.write(file_content)	

# Fermeture du fichier de commandes de redémarrage des serveurs RELAY
hfile_commande.close()

# appel du fichier de commandes de redémarrage des serveurs RELAY
if trouve==True:
	call(["cmd","/c",file_restart_relay])
					