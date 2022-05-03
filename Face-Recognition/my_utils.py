import yaml
import os 

def getConfig(yaml_file='./data/config.yml', path=''):
	yaml_file = os.path.join(path, yaml_file)
	with open(yaml_file, 'r') as file:
		cfgs = yaml.load(file, Loader=yaml.FullLoader)
	return cfgs

def updateConfig(yaml_file='./data/config.yml', path=''):
	yaml_file = os.path.join(path, yaml_file)
	cfgs = getConfig(yaml_file)
	cfgs['currentMember'] += 1

	with open(yaml_file, 'w') as file:
		yaml.dump(cfgs, file)

