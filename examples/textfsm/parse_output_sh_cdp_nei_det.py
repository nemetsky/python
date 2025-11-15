"""
c3845-inet-1#sh cdp nei detail
-------------------------
Device ID: c3845-inet-2.cisco.com
Entry address(es):
  IP address: 172.16.0.2
Platform: Cisco 3725,  Capabilities: Router Switch IGMP
Interface: FastEthernet1/0,  Port ID (outgoing port): FastEthernet1/0
Holdtime : 139 sec

Version :
Cisco IOS Software, 3700 Software (C3725-ADVENTERPRISEK9-M), Version 12.4(15)T14, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Tue 17-Aug-10 12:08 by prod_rel_team

advertisement version: 2
VTP Management Domain: ''
Duplex: full

-------------------------
..........
..........
..........

"""

Value Required nei_hostname (\S+)           # Required - указываем обязательно для записи в Record нужна проматченная переменная nei_hostname (на случай если у соседа в выводе несколько IP нашлось, то у второго IP уже не будет в записи hostname)
Value nei_ip (\S+)
Value ios (\S+)

Start
 ^Device ID: ${nei_hostname}
 ^ +IP address: ${nei_ip}
 ^Cisco IOS Software,.+, Version${ios}, -> Record         # Record только в конце указываем после последней переменной, чтобы записались все переменные
# ^-+ -> Record                                           # Как вариант Record делать когда дошли в выводе до '-------------------------', так как это означает конец соседа

