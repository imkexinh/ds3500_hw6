

"""
File: textastic.py

Description: A reusable, extensible framework
for comparitive text analysis designed to work
with any arbitrary collection of related documents.

"""


from collections import Counter, defaultdict
import re 
import matplotlib.pyplot as plt



class Textastic:

    def __init__(self):
        """ Contructor """
        self.data = defaultdict(dict)

    def simple_text_parser(self, filename):
        """ For processing simple, unformatted text documents """

        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        words = re.findall(r'\b\w+\b', text.lower())
        wordcount = Counter(words)
        numwords = len(words)

        # Bigrams (meaningful sequence of 2 words)
        bigrams = zip(words, words[1:])
        bigramcount = Counter(bigrams)

        # Trigrams (meaningful sequence of 3 words)
        trigrams = zip(words, words[1:], words[2:])
        trigramcount = Counter(trigrams)

        results = {
            'wordcount': wordcount,
            'numwords': numwords,
            'bigramcount': bigramcount,
            'trigramcount': trigramcount
        }

        print("Parsed:", filename, ":", results)
        return results



    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework and
        store data extracted from the document to be used
        later in visualizations """

        results = self.simple_text_parser(filename) # default
        if parser is not None:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v




    def compare_num_words(self, metric):
        """ A very simplistic visualization that creats a bar
        chart comparing the counted of selected metric in each file.
         """

        dict = self.data[metric]
        # for words, count in dict.items():
        #     if count <= 20:
        #         continue
        #     plt.bar(count, x=words)
        # plt.show()
        print(dict.keys())

