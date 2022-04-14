""" This file is part of Frankenftp - pyftpdlib-based FTP server

    Frankenftp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Frankenftp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Frankenftp.  If not, see <https://www.gnu.org/licenses/>.
"""
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
