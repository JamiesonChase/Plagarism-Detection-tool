Preprocessing tool, comments and newline will be stripped. Variables and functions will be renamed.

## Example

### Before
```c

/*Group: Antonio Maniscalco, Chase Jamieson, Josh Sedig
* CS460 Assignment_1
* Instructor: Dr. Xuechen Zhang
* my-uniq.c file
* */

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

void parse(FILE *fp);

int main(int argc, char **argv) {
    FILE *fp;
    int i;
    if (argc == 1) {
        parse(stdin); //read through stdin
        return 1;
    }
    for (i = 1;i<argc;i++) { //iterate through each command line argument
     if ((fp = fopen(argv[i],"r")) != NULL) {
        parse(fp);
        fclose(fp);
     }
     else { //error if file cannot be opened
        printf("my-uniq: cannot open file\n");
        exit(1);
    }
  }
}
//parse through for adjecent duplicate lines
void parse(FILE *fp) {
    char current[500];
    char next[500];

    while(fgets(next, 500, fp) != NULL) {
        if (strcmp(current, next) != 0) {
            printf("%s",next); //if different
            strcpy(current,next); //current line checking updated
        }

    }
  current[0]='\0'; //reset current so doens't filter next files
}
```
### Stripped
```c
void parse(FILE *fp);
int main(int argc, char **argv) {
    FILE *fp;
    int i;
    if (argc == 1) {
        parse(stdin); 
        return 1;
    }
    for (i = 1;i<argc;i++) { 
     if ((fp = fopen(argv[i],"r")) != NULL) {
        parse(fp);
        fclose(fp);
     }
     else { 
        printf("my-uniq: cannot open file\n");
        exit(1);
    }
  }
}
void parse(FILE *fp) {
    char current[500];
    char next[500];
    while(fgets(next, 500, fp) != NULL) {
        if (strcmp(current, next) != 0) {
            printf("%s",next); 
            strcpy(current,next); 
        }
    }
  current[0]='\0'; 
}
```
### Processed
```c
void F(FILE *V);
int F(int V, char **V) {
    FILE *V;
    int V;
    if (V == 1) {
        V(V); 
        return 1;
    }
    for (V = 1;V<V;V++) { 
     if ((V = V(V[V],SSS)) != NULL) {
        V(V);
        V(V);
     }
     else { 
        V(SSSS);
        V(1);
    }
  }
}
void F(FILE *V) {
    char V[500];
    char V[500];
    while(V(V, 500, V) != NULL) {
        if (V(V, V) != 0) {
            V(SSS,V); 
            V(V,V); 
        }
    }
  V[0]=SSS; 
}
```

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
