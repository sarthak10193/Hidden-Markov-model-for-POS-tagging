# Hidden-Markov-model-for-POS-tagging
Using an HMM model [viterbi Algorithm] to predict part of speech tags for Senteces in Catalan language

Training data: catalan_corpus_train_tagged.txt
Test data: dev_raw.txt 
Once the raw data is pos tagged it can be evaluated using the labelled dev_tagged.txt

running the HMMLearn3.py generates the model in json format in a text file
Then running the decode file, the generated model is read in and to tag the dev_raw.txt

# Detailed Desciption

Data

A set of training and development data will be made available as a compressed ZIP archive on Blackboard. The uncompressed archive will have the following format:

A file with tagged training data in the word/TAG format, with words separated by spaces and each sentence on a new line.
A file with untagged development data, with words separated by spaces and each sentence on a new line.
A file with tagged development data in the word/TAG format, with words separated by spaces and each sentence on a new line, to serve as an answer key.

Notes

Slash character. The slash character ‘/’ is the separator between words and tags, but it also appears within words in the text, so be very careful when separating words from tags. To make life easy, all tags in the data are exactly two characters long.
Smoothing and unseen words and transitions. You should implement some method to handle unknown vocabulary and unseen transitions in the test data, otherwise your programs won’t work. The unknown vocabulary problem is familiar from your naive Bayes classifier. The unseen transition problem is more subtle: you may find that the test data contains two adjacent unambiguous words (that is, words that can only have one part-of-speech tag), but the transition between these tags was never seen in the training data, so it has a probability of zero; in this case the Viterbi algorithm will have no way to proceed. The reference solution will use add-one smoothing on the transition probabilities and no smoothing on the emission probabilities; for unknown tokens in the test data it will ignore the emission probabilities and use the transition probabilities alone. You may use more sophisticated methods which you implement yourselves.
Runtime efficiency. Vocareum imposes a limit on running times, and if a program takes too long, Vocareum will kill the process. Your program therefore needs to run efficiently. Run times for the reference solution are approximately 2 seconds for running hmmlearn.py on the training data and 5 seconds for running hmmdecode.py on the development data, running on a MacBook Pro from 2012.


The learning program will be invoked in the following way:

> python hmmlearn3.py /path/to/input

The argument is a single file containing the training data; the program will learn a hidden Markov model, and write the model parameters to a file called hmmmodel.txt. The format of the model is up to you, but it should contain sufficient information for hmmdecode3.py to successfully tag new data.

The tagging program will be invoked in the following way:

> python hmmdecode3.py /path/to/input

The argument is a single file containing the test data; the program will read the parameters of a hidden Markov model from the file hmmmodel.txt, tag each word in the test data, and write the results to a text file called hmmoutput.txt in the same format as the training data.

