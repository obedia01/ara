# coding: utf8
import getpass
from base64 import b64encode

user = input("Select User ")
pw = getpass.getpass("Select Password ")

auth=user  + ':' + pw
byt=auth.encode('utf-8')
basestring=b64encode(byt)
print (basestring.decode('utf-8'))

file = open('credentials', 'w+')
file.write(basestring.decode('utf-8'))
file.close();

with open('credentials','r') as file1:
	lecture=file1.read().replace('\n','')

print (lecture)
