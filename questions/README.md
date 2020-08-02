# Questions
An AI to answer questions
```
$ python questions.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning , classification and regression.

$ python questions.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python questions.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
```
## Screencast
[![Project 6b: Questions](https://img.youtube.com/vi/EsQNLzHgrjQ/0.jpg)](https://youtu.be/EsQNLzHgrjQ)

## Background
Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions. Among the more famous question answering systems is Watson, the IBM computer that competed (and won) on Jeopardy!. A question answering system of Watson’s accuracy requires enormous complexity and vast amounts of data, but in this problem, we have designed a very simple question answering system based on inverse document frequency.

This question answering system performs two tasks: document retrieval and passage retrieval. Our system have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval first identifies which document(s) are most relevant to the query. Once the top documents are found, the top document(s) are subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

How do we find the most relevant documents and passages? To find the most relevant documents, project have used tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Once it finds the most relevant documents, there many possible metrics for scoring passages, but a combination of inverse document frequency and a query term density measure is used.

More sophisticated question answering systems might employ other strategies (analyzing the type of question word used, looking for synonyms of query words, lemmatizing to handle different forms of the same word, etc.) but this project limited to being simple.

## Understanding
In corpus, each text file contains the contents of a Wikipedia page. The goal of the project is to write AI that can find sentences from these files that are relevant to a user’s query.

In `questions.py`, the global variable `FILE_MATCHES` specifies how many files should be matched for any given query. The global variable `SENTENCES_MATCHES` specifies how many sentences within those files should be matched for any given query. If we set each of these values to 1: the AI will find the top sentence from the top matching document as the answer to our question. 

In the main function, we first load the files from the corpus directory into memory (via the `load_files` function). Each of the files is then tokenized (via `tokenize`) into a list of words, which then allows us to compute inverse document frequency values for each of the words (via `compute_idfs`). The user is then prompted to enter a query. The `top_files` function identifies the files that are the best match for the query. From those files, sentences are extracted, and the top_sentences function identifies the sentences that are the best match for the query.

The `load_files` function accepts the name of a directory and returns a dictionary mapping the filename of each .txt file inside that directory to the file’s contents as a string.

The `tokenize` function accepts a document (a string) as input, and returns a list of all of the words in that document, in order and lowercased.

The `compute_idfs` function accepts a dictionary of documents and return a new dictionary mapping words to their IDF (inverse document frequency) values.

The `top_files` function does given a `query` (a set of words), `files` (a dictionary mapping names of files to a list of their words), and `idfs` (a dictionary mapping words to their IDF values), returns a list of the filenames of the the n top files that match the query, ranked according to tf-idf.

The `top_sentences` function does given a `query` (a set of words), `sentences` (a dictionary mapping sentences to a list of their words), and `idfs` (a dictionary mapping words to their IDF values), returns a list of the n top sentences that match the query, ranked according to IDF.