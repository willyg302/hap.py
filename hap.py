import os
import json
import urllib

from types import MethodType


__all__ = ['Block', 'Blockfinder', 'Blockspring']


BLOCKSPRING_URL = 'https://sender.blockspring.com/api/blocks/{}?api_key={}'
BASE_BLOCKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blocks.json')


class Block(dict):

	def __init__(self, name):
		self._name = name

	def __getattr__(self, k):
		if k in ['id', 'name', 'schema', 'description']:
			def wrapped_f(v=None):
				if v is None:
					return self[k]
				self[k] = v
				return self
			return wrapped_f
		raise AttributeError('Method "{}" not recognized!'.format(k))

	def fetch(self, key):
		data = json.loads(Blockspring(key).get_block(block_id=self.id()))
		return self.name(data['name']).schema(data['schema']).description(data['description'])

	def register(self):
		Blockspring.register(self._name, self)
		return self


class Blockfinder(list):

	def __init__(self):
		self._sort = ''
		self._tag = ''

	def sort(self, _sort):
		self._sort = _sort
		return self

	def tag(self, _tag):
		self._tag = _tag
		return self

	def fetch(self, key, sort=None, tag=None):
		self.extend(json.loads(Blockspring(key).blockception(sort=sort or self._sort, tag=tag or self._tag)))
		return self

	def query(self, s=''):
		self[:] = [e for e in self if s in e['name'].lower()]
		return self

	def get_block(self, key, index, name):
		if index < 0 or index >= len(self):
			raise RuntimeException('Invalid block index!')
		return Block(name).id(self[index]['id']).fetch(key)


class Blockspring:

	def __init__(self, key):
		self.key = key
		# Load the base blocks we need to work
		Blockspring.load_from_file(BASE_BLOCKS)

	def call(self, f, config, data):
		if set(config['schema']) != set(data.keys()):
			return
		url = BLOCKSPRING_URL.format(config['id'], self.key)
		resp = urllib.urlopen(url, urllib.urlencode(data)).read().strip()
		return resp

	@classmethod
	def register(cls, name, config):
		def make_f(k):
			def f(self, d=None, **kwargs):
				return self.call(k, config, d or kwargs)
			return f
		setattr(cls, name, MethodType(make_f(name), None, cls))

	@staticmethod
	def load(blocks):
		for k, v in blocks.iteritems():
			Blockspring.register(k, v)

	@staticmethod
	def load_from_file(filename):
		with open(filename) as f:
			Blockspring.load(json.load(f))
