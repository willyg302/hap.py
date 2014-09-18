import unittest
import json

from hap import *
from token import API_KEY


# @TODO: Mock this so it doesn't hit the network so much.
class TestHappy(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.bs = Blockspring(API_KEY)
		cls.b = Block('sha512').id('72c4ba2569d21b7b115c8236ea8c636d').fetch(API_KEY).register()

	def test_block(self):
		self.assertIsInstance(self.b, Block)
		resp = self.bs.sha512({'msg': 'Hello world!'})
		self.assertEqual(resp, 'f6cde2a0f819314cdde55fc227d8d7dae3d28cc556222a0a8ad66d91ccad4aad6094f517a2182360c9aacf6a3dc323162cb6fd8cdffedb0fe038f55e85ffb5b6')

	def test_block_gets(self):
		self.assertEqual(self.b.id(), '72c4ba2569d21b7b115c8236ea8c636d')
		self.assertEqual(self.b.name(), 'sha512')
		self.assertEqual(self.b.schema(), ['msg'])
		self.assertEqual(self.b.description(), 'sha512 of a message')

	def test_blockspring_tags(self):
		l = json.loads(self.bs.tags())
		self.assertIsInstance(l, list)
		for prop in ['name', 'count', 'description']:
			self.assertIn(prop, l[0])


if __name__ == '__main__':
	unittest.main()
