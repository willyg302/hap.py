import json
import urllib

from types import MethodType


__all__ = ['Block', 'Blockspring']


BLOCKSPRING_URL = 'https://sender.blockspring.com/api/blocks/{}?api_key={}'


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
