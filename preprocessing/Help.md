First Draft for preprocessing tool, comments and newline will be stripped. Variables and functions will be renamed.

## Example

<table border="0">
 <tr>
    <td><b style="font-size:30px">Before </b></td>
    <td><b style="font-size:30px">After </b></td>
 </tr>
 <tr>
   <td><pre>
  <code>
# This is a test function with junk comments

def main():
 a = addNum(1,2)  #addition
 b = addNum(3,4)  #more addition
 c = a + b
 print(a," + ", b, " = ", c)

 #bala blah blah

def addNum(x,y): #function
 return x+y

main()
  </code>
</pre></td>
   <td><pre>
  <code>
 def fun1():
 var1 = fun2(1,2) 
 var2 = fun2(3,4) 
 var3 = var1 + var2
 print(var1," + ", var2, " = ", var3)
def fun2(var4,var5): 
 return var4+var5
fun1()
  </code>
</pre></td>
 </tr>
</table>

## Installation:
First pyminifer needs to be installed. Verify using version 2.2, might have to install directly from github [repo](https://github.com/liftoff/pyminifier).

```
pip install pyminifer
```

## Running
download files into same directory and run the program with:

```
python process.py test.py
```

Two new files will be created and directory will contain:


| Files  | Description |
| ------------- | ------------- |
| process.py  | processing file  |
| test.py  | same testfile  |
| test.py_Stripped | testfile stripped of blank lines and comments |
| test.py_Processed | testfile stripped and variables renamed |
