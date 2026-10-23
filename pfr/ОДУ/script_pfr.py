import json
import netmiko
import yaml
import re
import sys
from pprint import pprint

def send_config_commands(device, config_commands):
    with netmiko.ConnectHandler(**device) as ssh:
        result = ssh.send_config_set(config_commands)
        result += ssh.send_command_timing("commit")
        result += ssh.send_command_timing("confirm")
    return result

def send_show_command(device, command):
    with netmiko.ConnectHandler(**device) as ssh:
        output = ssh.send_command(command)
        return output

def main():
    path = "/opt/scripts"
    template_commands = [
        "route-map IMPORT_EBGP",
        "rule {number}",
        "action set local-preference {lp}",
    ]
    show_command = "show bgp ipv4 unicast"
    mask = r"(?P<branch>RDU-\d) (?P<channel>(?:t|r)tk) (?P<state>good|bad)"
    with open(f"{path}/state_channels.json") as f:
        current_topology = json.load(f)
    new_topology = current_topology.copy()
    try:
        for line in sys.stdin:
            if not line:
                break
            with open(f"{path}/devices_rt.yaml") as f:
                devices = yaml.safe_load(f)
            message = re.search(mask, line.strip())
            if message:
                branch, channel, new_state = message.groups()
                current_state = current_topology[branch][channel]["state"]
                if current_state == new_state:
                   pass
                else:
                    for dev in devices:
                        bgp_table = send_show_command(dev, show_command)
                    new_topology[branch][channel]["state"] = new_state
                    if channel == 'ttk':
                        prefix = current_topology[branch]['prefix_ttk']
                        if prefix in bgp_table:
                            new_topology[branch][channel]['bgp'] = 'up'
                        else:
                            new_topology[branch][channel]['bgp'] = 'down'

                        num_rule = current_topology[branch]['map_corp_prefix']['rule']
                        if new_state == 'bad' and current_topology[branch]['rtk']['state'] == 'bad':
                            lp = '350'
                            num_rule = current_topology[branch]['map_off_prefix']['rule']
                            new_topology[branch]['map_off_prefix']['lp'] = lp                         
                        elif new_state == 'good' and current_topology[branch]['rtk']['state'] == 'bad':
                            lp = '500'
                            num_rule = current_topology[branch]['map_off_prefix']['rule']
                            new_topology[branch]['map_off_prefix']['lp'] = lp  
                        elif new_state == 'bad':
                            lp = '300'
                            new_topology[branch]['map_corp_prefix']['lp'] = lp
                        elif new_state == 'good':
                            lp = '450'
                            new_topology[branch]['map_corp_prefix']['lp'] = lp

                    elif channel == 'rtk':
                        prefix = current_topology[branch]['prefix_rtk']
                        if prefix in bgp_table:
                            new_topology[branch][channel]['bgp'] = 'up'
                        else:
                            new_topology[branch][channel]['bgp'] = 'down'

                        num_rule = current_topology[branch]['map_off_prefix']['rule']
                        if new_state == 'bad' and current_topology[branch]['ttk']['state'] == 'bad':
                            lp = '450'
                            num_rule = current_topology[branch]['map_corp_prefix']['rule']
                            new_topology[branch]['map_corp_prefix']['lp'] = lp
                        elif new_state == 'good' and current_topology[branch]['ttk']['state'] == 'bad':
                            lp = '300'
                            num_rule = current_topology[branch]['map_corp_prefix'] ['rule']
                            new_topology[branch]['map_corp_prefix']['lp'] = lp
                        elif new_state == 'bad':
                            lp = '500'
                            new_topology[branch]['map_off_prefix']['lp'] = lp 
                        elif new_state == 'good':
                            lp = '350'
                            new_topology[branch]['map_off_prefix']['lp'] = lp 

                    commands_variable_dict = {'number': num_rule, 'lp': lp}
                    commands = [cmd.format(**commands_variable_dict) for cmd in template_commands]
                    for dev in devices:
                        result = send_config_commands(dev, commands)
                    with open(f"{path}/state_channels.json", "w") as f:
                        json.dump(new_topology, f, indent=4)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

