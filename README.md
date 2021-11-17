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
|  doc2  |          76.62          |
|  doc3  |          72.73          |
|  doc4  |           6.49          |
|  doc5  |          35.06          |
+--------+-------------------------+
 ```
 docId and similarity between input file
