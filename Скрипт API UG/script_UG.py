
import xmlrpc.client

from pprint import pprint

server = "192.168.1.208"
user = "Admin"
password = "1"

server = xmlrpc.client.ServerProxy("http://192.168.1.208:4040/rpc", verbose=False)

res = server.v2.core.login(user, password, {})
auth_token = res['auth_token']

fw_rules = server.v1.firewall.rules.list(auth_token, 0, 100, {})
pprint(fw_rules)

server.v2.core.logout(auth_token)