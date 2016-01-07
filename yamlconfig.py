#!/usr/bin/python

import yaml

def load_config_yaml(filename):
	return yaml.safe_load(open(filename))
