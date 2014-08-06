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
	},

	'tree': {
		'block': '1d888ebb91b0dd6abae2b17f3fa147d8',
		'description': 'This is a simple little script that generates ASCII trees',
		'schema': ['_levels', '_trunk', '_leaves']
	},

	'base64': {
		'block': '16e9a66177adb91f1f75cf837d27558a',
		'description': 'base64 encode of a msg',
		'schema': ['msg']
	}
}

class Block:

	def __init__(self, name):
		self.name = name

	def _get_or_set(self, k, v):
		if v is None:
			return getattr(self, k)
		setattr(self, k, v)
		return self

	def block_id(self, _block_id=None):
		return self._get_or_set('_block_id', _block_id)

	def description(self, _description=None):
		return self._get_or_set('_description', _description)

	def schema(self, _schema=None):
		return self._get_or_set('_schema', _schema)

	def register(self):
		Blockspring.register(self.name, {
			'block': self._block_id,
			'description': self._description,
			'schema': self._schema 
		})
		return self


class Blockspring:

	def __init__(self, key):
		self.key = key

	def call(self, f, config, data):
		if set(config['schema']) != set(data.keys()):
			return
		url = BLOCKSPRING_URL.format(config['block'], self.key)
		resp = urllib.urlopen(url, urllib.urlencode(data)).read()
		return resp

	@classmethod
	def register(cls, name, config):
		def make_f(k):
			def f(self, d):
				return self.call(k, config, d)
			return f
		setattr(cls, name, MethodType(make_f(name), None, cls))


for k, v in API.iteritems():
	Blockspring.register(k, v)

b = Block('sha512').block_id('72c4ba2569d21b7b115c8236ea8c636d').description('sha512 of a message').schema(['msg']).register()
print b.block_id(), b.description(), b.schema()

cat = 'http://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg'
bs = Blockspring(API_KEY)

#print bs.fake_data({'fake_row_count': ''})
#print bs.image({'img': cat})
#print bs.jeannie({'message': 'What is the weather?'})
#print bs.tree({'_levels': '10', '_trunk': '$', '_leaves': 'w'})
#print bs.base64({'msg': 'Hello world!'})
print bs.sha512({'msg': 'Hello world!'})
