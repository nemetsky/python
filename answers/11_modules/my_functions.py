from pprint import pprint

def parse_cdp_neighbors(string):
    cdp_dict = {}
    line_list = string.split("\n")
    for s in line_list:
        if ">" in s:
            hostname = s.split(">")[0]
        elif s[-1:].isdigit():                   # мое условие проверят последний символ в строке
            s_list = s.split()
            device = s_list[0]
            local_intf = s_list[1] + s_list[2]
            remote_intf = s_list[-2] + s_list[-1]
            key = (hostname, local_intf)
            cdp_dict[key] = device, remote_intf
    return cdp_dict
    
if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        pprint(parse_cdp_neighbors(f.read()))