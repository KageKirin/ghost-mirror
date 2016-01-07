#!/usr/local/bin/python

import requests
import json
import os
import sys
import yamlconfig


config = yamlconfig.load_config_yaml('config.yml')

#config stuff
ghost_config = config['ghost']
headers = ghost_config['headers']
params = ghost_config['params']
ghost_url = ghost_config['url']

outDir = config['output']['local_dir']

## TODO adjust to blog api
postsUrl = ghost_url + ''	#/posts/
tagsUrl = ghost_url + ''	#/tags/
usersUrl = ghost_url + ''	#/users/

indexUrl = ghost_url
postUrl = postsUrl + '/%(id)s/'			#/posts/:id/ or /posts/slug/:slug
tagUrl = tagsUrl + '/tag/%(id)s/'		#/tags/:id/ or /tags/slug/:slug
userUrl = usersUrl + '/author/%(id)s/'	#/users/:id/ or /users/slug/:slug

indexPath = 'index.json'
postPath = 'posts/slug/%(slug)s.json'
tagPath = 'tags/slug/%(slug)s.json'
userPath = 'users/slug/%(slug)s.json'



def fetchFromGhost(id, slug, url):
	print 'fetching %(id)s [%(slug)s] from %(url)s' % {'id': id, 'slug': slug, 'url': url }
	fetchResponse = requests.get(url, headers = headers, params = params)
	return fetchResponse.json()


def dumpJsonFile(data, filepath):
	path = os.path.join(outDir, filepath)
	print 'writing to', path

	pathDir = os.path.dirname(path)
	if not os.path.exists(pathDir):
		try:
			os.makedirs(pathDir)
		except OSError:
			print 'error creating', pathDir

	with open(path, 'w') as fd:
		fd.write(json.dumps(data))


def fetchAndDump(dataCollection, targetUrlParam, targetPathParam):
	for dataSet in dataCollection:
		fetchData = fetchFromGhost(dataSet['id'], dataSet['slug'], targetUrlParam % {'id': dataSet['slug']})
		dumpJsonFile(fetchData, targetPathParam % {'slug': dataSet['slug']})



def main(argv):
	indexResponse = requests.get(indexUrl, headers = headers, params = params)
	indexData = indexResponse.json()
	dumpJsonFile(indexData, indexPath)

	print 'posts'
	fetchAndDump(indexData['posts'], postUrl, postPath)
	print 'tags'
	fetchAndDump(indexData['tags'], tagUrl, tagPath)
	print 'users'
	fetchAndDump(indexData['users'], userUrl, userPath)


if __name__ == "__main__":
    main(sys.argv)
