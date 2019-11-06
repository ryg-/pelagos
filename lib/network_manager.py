import json
import logging

logging.basicConfig(format='%(asctime)s | %(name)s | %(message)s',
                    level=logging.DEBUG)


data_file = ''


def load_data_file():
#    data = []
    with open(data_file) as json_file:
        data = json.load(json_file)
    return data

def get_option(opt_name):
    return load_data_file()[opt_name]

def get_nodes():
    return load_data_file()['nodes']
    
def get_node_by_name(name, exception=True):
    for n in load_data_file()['nodes']:
        logging.debug('Process node: ' + n['node'])
        if n['node'] == name:
            return n
    if exception:
        raise Exception("Node [{}] not found".format(name))
    return ""

