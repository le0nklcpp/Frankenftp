# -*- coding: utf-8 -*-
##FTP project - load users
#
# loadadmins - loads user configs and writes into list users [[name,password,directory]]
DEFAULT_FTP_DIR="./files"
configfile='ftp-users.ini'
def loadadmins(path):
 users=[]
 fpath = path + configfile
 f=open(fpath,'r')
 print("Reading "+fpath)
 s=f.readline()
 for s in f:
  l=parsestr(s)
  if l: 
   if len(l)<2:
    print("ftpusers.py: failed to parse string:\"",s,"\" - Not enough arguments")
   else:
    if len(l)<3:
     l.append(DEFAULT_FTP_DIR)
    users.append(l)
 return users
def parsestr(s):
 # removing spaces
 if not s:
  return 0
 ln=s.strip()
 ln=ln.strip(' ')
 if ln[0]==';':
  return 0
 quote=1
 words=[]
 cstr=""
 g_strings=0
 for i in range(len(ln)):
  if (ln[i]=='\"' or ln[i]=='\'') and not quote:
   quote=1
   cstr=cstr.strip(' ')
   words.append(cstr)
   cstr=""
  elif  not (ln[i]=='\"' or ln[i]=='\''):
   cstr+=ln[i]
  elif quote:
   quote=0
 return words
