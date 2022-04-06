# -*- coding: utf-8 -*-
# ftpcfg - reading cfg
import json
configfile='ftp.json'
class FTPConfigException(Exception):
 pass
class FTPjsconf:
 data = {}
 tls_enabled = 0
 tls_force = 0
 tls_cert = ""
 tls_key = ""
 fails2ban = 0
 bantype = ""
 bantime = 0
 bancooldown = 0
 anonymous = 0
 integrity_check = 0
 integrity_alg = ""
 default_dir = "files"
 motd = "FTPEnstein"
 port = 0
 max_cons = 50
 max_cons_per_ip = 25
 pwhash=""
 def __init__(self,home):
  allowed_pw_values=('none','sha256','sha3-512','sha3-256','sha3-384')
  def bc(s):
   return bool(int(s))
  fpath = home+configfile
  d = json.load(open(fpath,'r'))
  print("Reading "+fpath)
  # security object
  s = d['security']
  tls = s['tls']
  self.tls_enabled = bc(tls['enabled'])
  self.tls_force = bc(tls['force'])
  self.tls_cert = tls['cert']
  self.tls_key = tls['key']
  self.fails2ban = int(s['fails_before_punishment'])
  self.bancooldown = int(s['fails_cooldown_min'])
  self.bantime = int(s['punishment_time'])
  self.bantype = s['punishment']
  self.anonymous = bc(s['allow_anonymous_rdonly'])
  self.pwhash = s['pw_hash_algorithm']
  if not self.pwhash in allowed_pw_values:
   raise FTPConfigException('Invalid pw_hash_algorithm field value:'+self.pwhash+'.Possible values:'+','.join(['{}']*len(allowed_pw_values)).format(*allowed_pw_values))
  # integrity check object
  i = d['integrity_check']
  self.integrity_check = i['enabled']
  self.integrity_alg = i['algorithm']
  # everything else
  self.default_dir = d['ftp_default_dir']
  self.motd = d['motd']
  self.port = int(d['port'])
  self.max_cons = int(d['max_connections'])
  self.max_cons_per_ip = int(d['max_connections_per_ip'])