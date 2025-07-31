network = input("Введите IP-сеть в формате X.X.X.X/X: ")

index = network.find("/")
address = network[:index]
mask = int(network[index+1:])
list_oct = address.split(".")
mask_bin = "1" * mask + "0" * (32-mask)
list_mask = [mask_bin[0:8], mask_bin[8:16], mask_bin[16:24], mask_bin[24:32]]

# address_bin = bin(int(list_oct[0]))[2:] + bin(int(list_oct[1]))[2:] + bin(int(list_oct[2]))[2:] + bin(int(list_oct[3]))[2:08]
# закоментированная строка переводит в двочный формат, но не добавляет нули впереди слагаемых

address_bin_host = "{:08b}".format(int(list_oct[0])) + "{:08b}".format(int(list_oct[1])) + "{:08b}".format(int(list_oct[2])) + "{:08b}".format(int(list_oct[3]))

address_bin_net = address_bin_host[:int(mask)] + "0" * (32-mask)
list_bin_net = [address_bin_net[0:8], address_bin_net[8:16], address_bin_net[16:24], address_bin_net[24:32]]
oct_net1 = int(list_bin_net[0], 2)
oct_net2 = int(list_bin_net[1], 2)
oct_net3 = int(list_bin_net[2], 2)
oct_net4 = int(list_bin_net[3], 2)

template_output_net = """
Network:
{0:<10}{1:<10}{2:<10}{3:<10}
{0:08b}  {1:08b}  {2:08b}  {3:08b}

Mask:
/{4:}
{5:<10}{6:<10}{7:<10}{8:<10}
{9:<10}{10:<10}{11:<10}{12:<10}
"""

print(template_output_net.format(oct_net1, oct_net2, oct_net3, oct_net4, 
    mask, list_mask[0], list_mask[1], list_mask[2], list_mask[3], int(list_mask[0], 2), int(list_mask[1], 2), int(list_mask[2], 2), int(list_mask[3], 2)))