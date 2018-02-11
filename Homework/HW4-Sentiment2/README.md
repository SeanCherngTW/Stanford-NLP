# HW4-Sentiment2

#### Run
```
$ python BooleanNaiveBayes.py -f ../data/imdb1
$ python NaiveBayesWithNegationFeature.py -f ../data/imdb1
```

#### Result of Boolean Naive Bayes
```
[INFO]	Performing 10-fold cross-validation on data set:	../data/imdb1
[INFO]	Fold 0 Accuracy: 0.505000
[INFO]	Fold 1 Accuracy: 1.000000
[INFO]	Fold 2 Accuracy: 1.000000
[INFO]	Fold 3 Accuracy: 1.000000
[INFO]	Fold 4 Accuracy: 1.000000
[INFO]	Fold 5 Accuracy: 1.000000
[INFO]	Fold 6 Accuracy: 1.000000
[INFO]	Fold 7 Accuracy: 1.000000
[INFO]	Fold 8 Accuracy: 1.000000
[INFO]	Fold 9 Accuracy: 1.000000
[INFO]	Accuracy: 0.950500
```

#### Result of Naive Bayes with Negation Features
```
[INFO]	Performing 10-fold cross-validation on data set:	../data/imdb1
[INFO]	Fold 0 Accuracy: 0.760000
[INFO]	Fold 1 Accuracy: 0.960000
[INFO]	Fold 2 Accuracy: 1.000000
[INFO]	Fold 3 Accuracy: 0.990000
[INFO]	Fold 4 Accuracy: 0.990000
[INFO]	Fold 5 Accuracy: 0.990000
[INFO]	Fold 6 Accuracy: 0.995000
[INFO]	Fold 7 Accuracy: 1.000000
[INFO]	Fold 8 Accuracy: 1.000000
[INFO]	Fold 9 Accuracy: 0.995000
[INFO]	Accuracy: 0.968000
```