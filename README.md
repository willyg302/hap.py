![hap.py](https://rawgit.com/willyg302/hap.py/master/hap-logo.svg "Life is better when you're laughing.")

---

A cheerful interface for [Blockspring](https://api.blockspring.com/) APIs

## 30-second Quick Start

Fire up a Python interpreter.

1. First, import some things and create a Blockspring instance.

   ```python
   >>> API_KEY = '<YOUR API KEY HERE>'
   >>> from hap import *
   >>> b = Blockspring(API_KEY)
   ```

2. Let's say we want to do a Google reverse image search. The first thing we need to do is find a block that will do this.

   ```python
   >>> f = Blockfinder().sort('top').tag('image-processing').fetch(API_KEY).query('reverse')
   ```

   What we've done is fetched all blocks with the `image-processing` tag, sorted by all-time top rating. Then we've searched these results for blocks that have "reverse" in the name.

3. Now let's create and register our block!

   ```python
   >>> f.get_block(API_KEY, 0, 'imgsearch').register()
   {'description': u"Enter a URL of an image, get Google's best guess to what that image is, and links to direct matches.", 'schema': [u'image_url'], 'id': u'5a1b66ef208007c51a45fda220dbe8db', 'name': u'Reverse Image Search'}
   ```

   At this point our `Blockfinder` instance still contains more than one block, so we grab the first one (at index `0`) and name it `imgsearch`. Don't forget to `register()` your block, that's important!

4. It's time to call it!

   ```python
   >>> b.imgsearch(image_url='http://cdn.hitfix.com/photos/5621843/Grumpy-Cat.jpg')
   '{"best_search": "grumpy cat", "direct_matches": "[\'http://www.grumpycats.com/\', \'http://en.wikipedia.org/wiki/Grumpy_Cat\', \'http://www.hitfix.com/comedy/the-internet-lies-peter-dinklage-sadly-did-not-take-a-selfie-with-grumpy-cat\', \'http://www.3news.co.nz/entertainment/grumpy-cat-has-hit-her-terrible-twos-2014040611\', \'http://www.3news.co.nz/entertainment/grumpy-cat-sells-out-2013091811\', \'http://www.butterflybeauty.tips/2014/07/tiny-cat-grumpy-cat-and-now-sad-cat.html\', \'http://coffeeticks.my/this-cat-has-gathered-over-5-million-likes-on-facebook/\']"}'
   ```

Yes, it was really that easy.

## Usage

You can safely do `from hap import *`. This imports the three classes `Block`, `Blockfinder`, and `Blockspring`.
