import nltk
import sys
import os
import string
import math

#nltk.download('punkt')
#nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 10


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)

def get_file_content(file):
    """
    Read the content of the file
    """
    content = ""
    with open(file, encoding="utf8") as f: 
        content = f.read()

    return content

def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result={}

    # loop through each file in directory
    for filename in os.listdir(directory):
        result[filename] = get_file_content(os.path.join(directory,filename))

    return result

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    result=[]

    tokens = nltk.word_tokenize(document)
    stop_words = set(nltk.corpus.stopwords.words('english'))

    def remove_punctuation(s):
        for c in string.punctuation:
            s=s.replace(c,"")
        return s

    # loop through each token in tokens
    for token in tokens:
        # turn token into lower case and remove punctuation
        word = remove_punctuation(token.lower())

        # in word is non blank and is not in stop words list then add to result
        if len(word) > 0 and word not in stop_words:
            result.append(word)

    return result

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    result = {}
    total_no_of_documents = len(documents)

    # loop through all word lists
    for words_list in documents.values():
        # for each word in word list
        for word in words_list:
            # check if the word already exists in results
            # i.e its idf is already calculated before
            # if yes skip
            if word not in result:

                no_documents_word_contain = 0
                word_idf = 0
                
                # find occurrance of the word in each document
                for values in documents.values():
                    if word in values:
                        no_documents_word_contain += 1

                # calculate the idf value of word
                word_idf = math.log(total_no_of_documents/no_documents_word_contain)
                # add to result
                result[word] = word_idf

    return result

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    document_score = {}

    # loop thru each file
    for document, word_list in files.items():
        score = 0
        # for each word in query
        for query_word in query:

            # if the query word exists in the document word list
            if query_word in word_list:
                # term frequency
                tf = word_list.count(query_word)
                # inverse document frequency
                idf = idfs[query_word]
                # td-idf value calculation
                tf_idf = tf * idf
                # add to score of document
                score += tf_idf

        # record the document score        
        document_score[document] = score
    
    result = []
    counter = 0

    # sort the documents by best score
    for document, score in sorted(document_score.items(), key=lambda item: item[1], reverse=True):
        if counter < n:
            result.append(document)
        counter += 1

    return result

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = {}

    for sentence, sentence_words in sentences.items():
        score = 0

        # number of words in query that matches with sentence words
        matching_words = 0
        words_in_sentence = len(sentence_words)

        # for each word in query
        for query_word in query:
            # if the query word exists in sentence's words
            if query_word in sentence_words:
                # calculating matching word measure
                score += idfs[query_word]
                matching_words += 1
        
        # calculate sentence's query term density measure
        qtd = matching_words / words_in_sentence
        # record sentence's score as Tuple of (matching word measure, query term density)
        sentence_score[sentence] = (score, qtd)

    result=[]
    counter = 0
    # sort the sentences by best score
    for sentence, score in sorted(sentence_score.items(), key=lambda item: item[1], reverse=True):
        if counter < n:
            result.append(sentence)
        counter += 1
    
    return result

if __name__ == "__main__":
    main()
