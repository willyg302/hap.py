import json
import urllib

from types import MethodType

from token import API_KEY


BLOCKSPRING_URL = 'https://sender.blockspring.com/api/blocks/{}?api_key={}'

API = {
	'image': {
		'block': 'd54a2e2c28aebab4fe079ff547cea495',
		'description': 'Tells you what your image (URL) is all about',
		'schema': ['img']
	},

	'fake_data': {
		'block': 'ba5ea3851f6617d1ce8addc0f99443e6',
		'description': 'Choose number of rows and get a spreadsheet of fake data.',
		'schema': ['fake_row_count']
	},

	'jeannie': {
		'block': '37181aa2e94bb56df1444d9eb5d1d62f',
		'description': 'Blockspring API for the Jeannie voice assistant API',
		'schema': ['message']
	}
}


class Blockspring:

	def __init__(self, key):
		self.key = key

	def call(self, f, d):
		if set(API[f]['schema']) != set(d.keys()):
			return
		url = BLOCKSPRING_URL.format(API[f]['block'], self.key)
		resp = urllib.urlopen(url, urllib.urlencode(d)).read()
		return resp


for k, v in API.iteritems():
	def make_f(k):
		def f(self, d):
			return self.call(k, d)
		return f
	setattr(Blockspring, k, MethodType(make_f(k), None, Blockspring))


cat = 'http://upload.wikimedia.org/wikipedia/commons/2/22/Turkish_Van_Cat.jpg'
bs = Blockspring(API_KEY)

#print bs.fake_data({'fake_row_count': ''})
#print bs.image({'img': cat})
print bs.jeannie({'message': 'Find donuts near me'})
