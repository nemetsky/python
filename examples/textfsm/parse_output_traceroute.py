# ======================================================
# Пример 1

import sys
import textfsm
from pprint import pprint
from tabulate import tabulate


output1 = """
c3845-inet-1#traceroute 192.168.0.17

Type escape sequence to abort.
Tracing the route to 192.168.0.17

  1 172.16.0.2 16 msec 12 msec 12 msec
  2 10.10.10.10 16 msec 12 msec 20 msec
  3 192.168.0.17 20 msec 24 msec 20 msec
c3845-inet-1#

"""

with open("traceroute.template") as f:
    fsm = textfsm.TextFSM(f)
    result = fsm.ParseText(output)

print(fsm.header)
print(result)    

# ======================================================
# Пример 2

template = sys.argv[1]
output_file = sys.argv[2]

with open(template) as f, open(output_file) as output:
    fsm = textfsm.TextFSM(f)
    header = fsm.header                                 # заголовки (переменные из шаблона)
    result = fsm.ParseText(output.read())
    pprint(result)
    print(tabulate(result, headers=header))             # красивый вывод