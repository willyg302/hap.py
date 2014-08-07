import unittest

from hap import *
from token import API_KEY


# @TODO: Mock this so it doesn't hit the network so much.
class TestWatch(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		Blockspring.load_from_file('blocks.json')
		cls.bs = Blockspring(API_KEY)
		cls.b = Block('sha512').block_id('72c4ba2569d21b7b115c8236ea8c636d').description('sha512 of a message').schema(['msg'])

	def test_block_gets(self):
		self.assertEqual(self.b.block_id(), '72c4ba2569d21b7b115c8236ea8c636d')
		self.assertEqual(self.b.description(), 'sha512 of a message')
		self.assertEqual(self.b.schema(), ['msg'])

	def test_register(self):
		self.b = self.b.register()
		self.assertIsInstance(self.b, Block)
		resp = self.bs.sha512({'msg': 'Hello world!'})
		self.assertEqual(resp, 'f6cde2a0f819314cdde55fc227d8d7dae3d28cc556222a0a8ad66d91ccad4aad6094f517a2182360c9aacf6a3dc323162cb6fd8cdffedb0fe038f55e85ffb5b6')

	def test_basic_function(self):
		resp = self.bs.base64({'msg': 'Hello world!'})
		self.assertEqual(resp, 'SGVsbG8gd29ybGQh')

	def test_keyword_args(self):
		resp = self.bs.base64(msg='Hello world!')
		self.assertEqual(resp, 'SGVsbG8gd29ybGQh')


if __name__ == '__main__':
	unittest.main()


#cat = 'http://upload.wikimedia.org/wikipedia/commons/8/8d/President_Barack_Obama.jpg'

#print bs.fake_data({'fake_row_count': ''})
#print bs.image({'img': cat})
#print bs.tree({'_levels': '10', '_trunk': '$', '_leaves': 'w'})
#print bs.jeannie(message='Hello world!')
#print bs.tree(_levels='10', _trunk='|', _leaves='v')
