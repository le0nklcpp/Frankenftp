#!/usr/bin/python3
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
import pyftpdlib
import ftpcfg
from pyftpdlib.servers import FTPServer as srv
from authorizer import ExtendedAuthorizer
from pyftpdlib.log import logger
from pyftpdlib.log import config_logging
import os
import ftpusers
import sys

confp = '.'+os.sep
def main():
 config_logging()
 os.chdir(confp) # to be sure - bad config protection. After execution
 logger.info('Frankenftp - pyftpdlib-based FTP server')
 logger.info('Changed directory:'+os.getcwd())
 config = ftpcfg.FTPjsconf(confp)
 logger.info('Read json config')
 users=ftpusers.loadadmins(confp)
 logger.info('Loaded list of {0} users'.format(len(users)))
 authorizer = ExtendedAuthorizer(config)
 logger.info('Initialized authorizer')
 for i in users:
  if not os.path.exists(i[2]) or not os.path.isdir(i[2]):
   i[2] = config.default_dir
  authorizer.add_user(i[0],i[1],i[2],perm='elradfmw')
 # Anonymous read-only user
 if config.anonymous:
   logger.warning('!!!!WARNING!!!!Adding read-only anonymous user')
   authorizer.add_anonymous(config.default_dir,perm='elr')
 if config.tls_enabled:
  logger.info('TLS enabled')
  from pyftpdlib.handlers import TLS_FTPHandler
  handler=TLS_FTPHandler
  handler.certfile=config.tls_cert
  handler.keyfile=config.tls_key
  handler.tls_control_required = handler.tls_data_required = config.tls_force
 else:
  logger.warning('!!!!WARNING!!!!TLS disabled')
  from pyftpdlib.handlers import FTPHandler
  handler = FTPHandler
 handler.authorizer=authorizer
 handler.banner=config.motd
 address=('',config.port)
 server=srv(address,handler)
 server.max_cons = config.max_cons
 server.max_cons_per_ip = config.max_cons_per_ip
 server.serve_forever()


def parseargs(argv):
 # Argument callback
 # Function returns -1 if argument expects exit
 i = 1
 def displayhelp():
  print("Usage: frankenftp [options]")
  print("Options:")
  print("--config configdir Specify config path")
  print("--help             Display help and exit")
  print("--version          Display current software version and exit")
  return True
 def printversion():
  print("Frankenftp - pyftpdlib-based FTP server")
  print("Copyright (C) le0nklcpp,2021-2022")
  print("This program is free software: you can redistribute it and/or modify\n"+\
    "it under the terms of the GNU General Public License as published by\n"+\
    "the Free Software Foundation, either version 3 of the License, or\n"+\
    "(at your option) any later version.")
  print("Pyftpdlib version: {0}".format(pyftpdlib.__ver__))
  print("Python3 version: {0}.{1}.{2}".format(sys.version_info.major,sys.version_info.minor,sys.version_info.micro))
  return True
 def setconfpath():
  nonlocal i
  i = i + 1
  if i>=len(argv):
   print("Error!Expected argument after --config")
   displayhelp()
   return True
  global confp
  confp = argv[i]
  if confp[len(confp)-1]!=os.sep:
   confp+=os.sep
  return False
 def unknownargument():
  print("Error!Unknown argument:{0}".format(sys.argv[i]))
  return True
 # Parse arguments.
 argcalls={
 '--help':displayhelp,
 '--version':printversion,
 '--config':setconfpath
 }
 while i<len(argv): # first is the script name
  func = argcalls.get(argv[i],unknownargument)
  if func():
   quit()
  i=i+1
# call main()
if __name__=="__main__":
 parseargs(sys.argv)
 main()
