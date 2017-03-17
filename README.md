# Hidden-Markov-model-for-POS-tagging
Using an HMM model [viterbi Algorithm] to predict part of speech tags for Senteces in Catalan language

Training data: catalan_corpus_train_tagged.txt
Test data: dev_raw.txt 
Once the raw data is pos tagged it can be evaluated using the labelled dev_tagged.txt

running the HMMLearn3.py generates the model in json format in a text file
Then running the decode file, the generated model is read in and to tag the dev_raw.txt
