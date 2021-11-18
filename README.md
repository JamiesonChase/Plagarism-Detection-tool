### Team roles:
Pre-Processing - Chase Jamieson

Hashing/Fingerprinting & Visual - Tracy Hotchkiss & Vinh Duong

Winnowing - Trevor Holland 

### Steps to run demo2 file:
``` 
pip install pyminifier 
```
Then change `__init__.py` pyminifier file (middle click on "import pyminifier"). replace that file with [this](https://github.com/liftoff/pyminifier/blob/master/pyminifier/__init__.py) one.

Run demo.py and verify part output like this:

```python
+--------+-------------------------+
| doc_id | inputFile.py Similarity |
+--------+-------------------------+
|  doc1  |          100.00         |
|  doc2  |          63.20          |
|  doc3  |          47.20          |
|  doc4  |           0.00          |
|  doc5  |          10.40          |
+--------+-------------------------+
 ```
 docId and similarity between input file
