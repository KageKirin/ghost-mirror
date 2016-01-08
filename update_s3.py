import os
import sys
import s3
import yaml

with open('config.yml', 'r') as fi:
    config = yaml.load(fi)



'''
connection = s3.S3Connection(**config['s3'])
storage = s3.Storage(connection)

#assert storage.bucket_exists(config['s3']['default_bucket'])

for bucket in storage.bucket_list():
    print bucket.name, bucket.creation_date
'''

'''
import tinys3

connection = tinys3.Connection(config['s3']['access_key_id'], config['s3']['secret_access_key'])
'''


import simples3
s = simples3.S3Bucket(
    config['s3']['default_bucket'],
    config['s3']['access_key_id'],
    config['s3']['secret_access_key']
    )
print s

s.put("testfile", "test content")
