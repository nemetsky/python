with open("sh_ip_int_br.txt") as f:
    for line in f:
        line_list = line.split()
        if line_list:
            intf, ip, *_ = line_list
            if intf[-1].isdigit():
                print(intf, ip)
                
########################################

access_config = {
    'FastEthernet0/12': 10,
    'FastEthernet0/14': 11,
    'FastEthernet0/16': 17
}
for intf, vlan in access_config.items():        # for item in access_config.items():
    print(intf, vlan)                           #    intf, vlan = item
                                                #    print(intf, vlan)
########################################

for vlan, mac, _, intf in table:                # где table - это список списков 
    print(f"{vlan:10},{mac:20},{intf}")
