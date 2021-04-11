# -*- coding: utf-8 -*-
import pyftpdlib
import ftpcfg
from pyftpdlib.servers import FTPServer as srv
from pyftpdlib.authorizers import DummyAuthorizer
import os.path
import ftpusers

confp = './'
def main():
 print('FTPEnstein')
 config = ftpcfg.FTPjsconf(confp)
 print('Read json config')
 users=ftpusers.loadadmins()
 print('Loaded list of {0} users'.format(len(users)))
 authorizer = DummyAuthorizer() # TODO: write your own authorizer
 print('Initialized authorizer')
 for i in users:
  if not os.path.exists(i[2]) or not os.path.isdir(i[2]):
   i[2] = config.default_dir
  authorizer.add_user(i[0],i[1],i[2],perm='elradfmw')
 # Anonymous read-only user
 if config.anonymous:
   print('Adding read-only anonymous user')
   authorizer.add_anonymous(config.default_dir,perm='elr')
 if config.tls_enabled:
  print('TLS enabled')
  from pyftpdlib.handlers import TLS_FTPHandler
  handler=TLS_FTPHandler
  handler.certfile=config.tls_cert
  handler.keyfile=config.tls_key
  handler.tls_control_required = handler.tls_data_required = config.tls_force
  handler.authorizer=authorizer
 else:
  print('TLS disabled')
  from pyftpdlib.handlers import FTPHandler
  handler = FTPHandler
 handler.banner='Python FTP server'
 address=('',config.port)
 server=srv(address,handler)
 server.max_cons = config.max_cons
 server.max_cons_per_ip = config.max_cons_per_ip
 server.serve_forever()
if __name__=="__main__":
 main()
