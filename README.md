# Overview
Frankenftp is easy to setup and configure pyftpdlib-based FTP server with some features and additions, useful or not.
You can specify path to your configs directory by using --config command-line argument.
# WARNING
DO NOT USE IT SINCE IT IS NOT READY, AND A FEW OPTIONS LISTED IN FTP.JSON ARE NOT IMPLEMENTED
## Configurations
See ftp.json to understand what works and can be configured now:
|Option      |JSON field  |Description|
|------------|------------|-----------|
|TLS protocol|security:tls|           |
|Password hashing|security:pw_hash_algorithm|Set this option to store only password checksums in ftp-users.ini(I need to implement something better than just checksum)|
|Anonymous read-only|security:allow_anonymous_rdonly|Anonymous read-only user with access to ftp_default_dir|
|Anonymous default directory|ftp_default_dir|specify default directory for anonymous user access|
|Port|port|Server port|
|Passive ports|open_ports|Assign passive ports for access through firewall(you need to open these ports)|
||max_connections|0 = unlimited|
||max_connections_per_ip|0 = unlimited|

User info is stored in ftp-users.ini file in this format:

"username" "password" "directory"

Optionally, you can restrict user access to read-only by specifying permissions:

"username" "password" "directory" "r"

Only accepted permissions are

rw - read-write

r - read-only

# Everything else IS NOT IMPLEMENTED

- files integrity check
- brute-force protection
- Actual password hashing algorythm(Using checksums is not good)
