from ezsnmp import Session
from pprint import pprint

#ip = '10.11.10.211'
ip = '10.20.11.32'

session = Session(hostname=ip, community='CDUro', version=2)

output_number_sw_object = session.get('1.3.6.1.4.1.89.53.8.0')
output_pid_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.13')
output_sn_object = session.walk('1.3.6.1.2.1.47.1.1.1.1.11')
output_sfp_pid_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.10')
output_sfp_sn_object = session.walk('1.3.6.1.4.1.35265.1.23.53.1.1.1.6')

number_sw = int(output_number_sw_object[0].value)
output_pid = []
output_sn = []
output_sfp_pid = []
output_sfp_sn = []
out_dict = {}

for i in range(1,number_sw+1):
    out_dict[i] = []

for item in output_sn_object:
    #oid = item.oid + '.' + item.index
    output_sn.append((item.index, item.value))
for item in output_pid_object:
    output_pid.append((item.index, item.value))

result_module = list(zip(output_pid, output_sn))

for pid, sn in result_module:
    if pid[1] != '':
        list1 = [pid[1], sn[1]]
        index = int(pid[0])
        if index in range(67108864,134217728):
            out_dict[1].append(list1)
        elif index in range(134217728,201326592):
            out_dict[2].append(list1)

for item in output_sfp_sn_object:
    output_sfp_sn.append((item.index, item.value))
for item in output_sfp_pid_object:
    output_sfp_pid.append((item.index, item.value))

result_sfp = list(zip(output_sfp_pid, output_sfp_sn))

if result_sfp[0][0][1] != None:
    for sfp_pid, sfp_sn in result_sfp:
        list1 = [sfp_pid[1], sfp_sn[1]]
        index = int(sfp_pid[0])
        if index <= 156:
            out_dict[1].append(list1)
        elif index in range(157,313):
            out_dict[2].append(list1)
        elif index in range(313,469):
            out_dict[3].append(list1)
        elif index in range(469,625):
            out_dict[4].append(list1)
pprint(out_dict)
