#Poap Information 
Folder IOS contain the IOS/IOS XE configuration an poap files

#####genrate md5
from linux: <br/>
f=poap.py ; cat $f | sed '/^#md5sum/d' > $f.md5 ; sed -i "s/^#md5sum=.*/#md5sum=\"$(md5sum $f.md5 | sed 's/ .*//')\"/" $f 

from swithes:<br/>
md5sum /bootflash/poap.cfg > /bootflash/poap.cfg.md5

references:
---------
https://developer.cisco.com/docs/nx-os/#!poap/poap-poweron-auto-provisioning <br/>
https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/102x/configuration/fundamentals/cisco-nexus-9000-nx-os-fundamentals-configuration-guide-102x/m-using-poap.html <br/>
https://www.fatalerrors.org/a/0NV91jE.html <br/>

-----

requirements:
-------
DHCP Server <br/>
TFTP Server (Script server) <br/>
SCP/HTTP Server (Config and NXOS Image server) <br/>

Options:
-------
1) use switch/router(ios/ios_xe) as poap server 
2) use linux box
3) mix options 1 and 2 

config:
------
###DHCP (IOS)

IOS dhcp config sample:<br>
ip dhcp pool LAB <br/>
 network 10.0.0.0 255.255.254.0<br/>
 default-router 10.0.0.1 <br/>
 domain-name cassio.lab<br/>
 dns-server 10.0.0.1 <br/>
 option 67 ascii "poap/poap.py" <----- poap location + file name <br/>
 option 150 ip 10.0.0.1 <----- tftp server <br/>

###TFTP Server (IOS)
The router is not a fully functional TFTP server. It can only serve files for download<br/>
#####create a new folder
mkdir bootflash:poap<br/>

#####copy scp from IOS Devices 
copy  scp://root:1q2w3e4r@10.0.0.22//var/lib/tftpboot/poap.py bootflash:poap/
copy  scp://root:1q2w3e4r@10.0.0.22//var/lib/tftpboot/poap.py.md5 bootflash:poap/

#####configure tftp-server
conf t 
tftp-server bootflash:poap/poap.py
tftp-server bootflash:poap.py

###SCP Server (IOS)
#####enable scp server 
ip scp server enable

#####copy files
copy  scp://root:1q2w3e4r@10.0.0.22//var/lib/tftpboot/conf.9SH5TI5QPRA bootflash:poap/ <br/>
copy  scp://root:1q2w3e4r@10.0.0.22//var/lib/tftpboot/conf.9SH5TI5QPRA.md5 bootflash:poap/ <br/>
copy  scp://root:1q2w3e4r@10.0.0.22//var/lib/tftpboot/nxos.9.3.6.bin bootflash:poap/ <br/>
copy  scp://root:1q2w3e4r@10.0.0.22//var/lib/tftpboot/nxos.9.3.6.bin.md5  bootflash:poap/ <br/>




