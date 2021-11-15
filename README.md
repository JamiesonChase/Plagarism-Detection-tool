### Team roles:
Pre-Processing - Chase Jamieson

Hashing/Fingerprinting & Visual - Tracy Hotchkiss & Vinh Duong

Winnowing - Trevor Holland 

### Steps to run demo file:
``` 
pip install pyminifier 
```
Then change `__init__.py` pyminifier file (middle click on "import pyminifier"). replace that file with [this](https://github.com/liftoff/pyminifier/blob/master/pyminifier/__init__.py) one.

Run demo.py and verify part output like this:

```python
{512: {'doc1': [5], 'doc2': [9]},
 517: {'doc1': [5], 'doc2': [9]},
 518: {'doc1': [5], 'doc2': [9]},
 580: {'doc1': [5], 'doc2': [9]},
 595: {'doc1': [5], 'doc2': [9]},
 610: {'doc1': [4], 'doc2': [8]},
 630: {'doc1': [5], 'doc2': [9]},
 632: {'doc1': [1, 2], 'doc2': [1, 2]},
 638: {'doc1': [2, 3, 4], 'doc2': [2, 3, 6, 7, 8]},
 644: {'doc2': [2, 3, 6, 7]},
 654: {'doc1': [2]},
 656: {'doc1': [6, 7], 'doc2': [10, 11]},
 ```
 Here we have an inverted index with hash values as keys and DocID,line numbers as values.
