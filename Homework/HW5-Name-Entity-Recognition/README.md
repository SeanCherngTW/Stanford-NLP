# HW4-Sentiment2

#### Run
```
$ cd python
$ mkdir classes
$ javac *.java org/json/*.java -d classes
$ python NER.py ../data/train ../data/dev [-print]

Use [-print] to print the real answers and your guesses of the test set.
```

#### Result
```
precision = 0.898910411622276
recall = 0.8105895196506551
F1 = 0.8524684270952928
```