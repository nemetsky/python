from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template_routers.txt')

with open('routers.yaml') as f:
    routers = yaml.safe_load(f)                 
    for router in routers:                                       
        filename = router['hostname']+'_conf.txt'
        with open(filename, 'w') as f:
            f.write(template.render(router))