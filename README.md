![hap.py](https://rawgit.com/willyg302/hap.py/master/hap-logo.svg "Life is better when you're laughing.")

---

A cheerful interface for [Blockspring](https://api.blockspring.com/) APIs

## Usage

You can safely do `from hap import *`. This imports the two classes `Block` and `Blockspring`.

### Register an API

The first thing you're going to want to do is register an API to the Blockspring class. There are several ways to do so.

1. Configure it as a `Block`

   ```python
   Block('sha512').block_id('72c4ba2569d21b7b115c8236ea8c636d').description('sha512 of a message').schema(['msg']).register()
   ```

2. Load it as a Python dictionary

   ```python
   Blockspring.load({
       'sha512': {
           'block_id': '72c4ba2569d21b7b115c8236ea8c636d',
           'description': 'sha512 of a message',
           'schema': ['msg']
       }
   })
   ```

   This method can accept several blocks at once.

3. Load blocks from a JSON file

   ```python
   Blockspring.load_from_file('myblocks.json')
   ```

   In this case, the JSON is formatted exactly like the dictionary you would pass to `Blockspring.load()`.

In all cases, the `schema` consists of a list of values the API expects (the keys for the data that you pass to Blockspring).

### Call an API

Now that you've registered your API, you can call it!

```python
API_KEY = ''  # Your API key here
resp = Blockspring(API_KEY).sha512({'msg': 'Hello world!'})
print resp  # Prints f6cde2a...
```

Wait, whaaaaat?! Was it really that easy? Rest assured, it was.
