# -*- coding: utf-8 -*-
import pyftpdlib
from pyftpdlib.servers import FTPServer as srv
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import TLS_FTPHandler
import os.path
import ftpusers
# main function
def main():
 users=ftpusers.loadadmins()
 print("FTPServer")
 print('Loaded list of {0} users'.format(len(users)))
 authorizer = DummyAuthorizer()
 for i in users:
  if not os.path.exists(i[2]) or not os.path.isdir(i[2]):
   i[2] = default_ftp_dir
  authorizer.add_user(i[0],i[1],i[2],perm='elradfmw')
 handler=TLS_FTPHandler
 handler.certfile='ftpuser.pem'
 handler.keyfile='ftpuserkey.pem'
 handler.authorizer=authorizer
 handler.banner='Python FTP server'
 address=('','22545')
 server=srv(address,handler)
 server.max_cons = 100
 server.max_cons_per_ip = 10
 server.serve_forever()
if __name__=="__main__":
 main()
