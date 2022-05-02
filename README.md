### To run:

Command line is "python3 app.py [directoryOfInputFiles]" or "python3 app.py -f [directoryOfInputFiles]"
To start up the server: "python3 app.py"
### Team roles:
Pre-Processing - Chase Jamieson

Hashing/Fingerprinting & Visual - Tracy Hotchkiss & Vinh Duong

Winnowing - Trevor Holland 

### To set up the environment
Using Current Ubuntu long term support:
sudo apt install git
sudo apt install python3-pip
sudo apt install python3-flask
pip3 install -r frozen-requirements.txt


### To run the flask application
On the command line do "flask run" in the main directory


### Steps to run main file:

Run demo.py and verify part output like this:

```python
+-------------------------+-----------------+
| doc_id Pair             | File Similarity |
+-------------------------+-----------------+
| doc2 - inputFile.py     |      74.36      |
| doc2 - databaseFile1.py |      74.36      |
| doc1 - databaseFile2.py |      74.36      |
| doc3 - inputFile.py     |       47.2      |
| doc3 - databaseFile1.py |       47.2      |
| doc1 - databaseFile3.py |       47.2      |
| doc3 - databaseFile2.py |      29.91      |
| doc2 - databaseFile3.py |      29.91      |
| doc5 - databaseFile4.py |      17.07      |
| doc4 - databaseFile5.py |      17.07      |
| doc5 - databaseFile2.py |      14.53      |
| doc2 - databaseFile5.py |      14.53      |
| doc5 - inputFile.py     |      10.83      |
| doc5 - databaseFile1.py |      10.83      |
| doc1 - databaseFile5.py |      10.83      |
| doc5 - databaseFile3.py |       8.33      |
| doc3 - databaseFile5.py |       8.33      |
| doc4 - databaseFile3.py |       1.22      |
| doc3 - databaseFile4.py |       1.22      |
| doc4 - inputFile.py     |       0.0       |
| doc4 - databaseFile2.py |       0.0       |
| doc4 - databaseFile1.py |       0.0       |
| doc2 - databaseFile4.py |       0.0       |
| doc1 - databaseFile4.py |       0.0       |
+-------------------------+-----------------+
 ```
 docId and similarity between input file
