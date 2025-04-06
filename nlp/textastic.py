

"""
File: textastic.py

Description: A reusable, extensible framework
for comparitive text analysis designed to work
with any arbitrary collection of related documents.

"""


from collections import Counter, defaultdict
import re 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.sankey import Sankey
import networkx as nx
import plotly.graph_objects as go
from itertools import chain


class Textastic:

    def __init__(self):
        """ Contructor """
        self.data = defaultdict(dict)
        self.stop_words = set()

    def load_stop_words(self, stopfile):
        with open(stopfile, 'r') as f:
            self.stop_words = set(word.strip().lower() for word in f.readlines())

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

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Create a Sankey diagram showing the relationship between text sources and words.
        
        Parameters:
        - word_list: Optional list of specific words to include
        - k: If word_list is None, include the top k words from each document
        
        Returns:
        - Displays a Sankey diagram
        """
        # Get wordcount data
        wordcount_data = self.data['wordcount']
        
        # Get document labels
        doc_labels = list(wordcount_data.keys())
        
        # If no specific words provided, get top k words from each document
        if word_list is None:
            # Get top k words from each document
            all_top_words = set()
            for doc, counter in wordcount_data.items():
                top_words = [word for word, _ in counter.most_common(k)]
                all_top_words.update(top_words)
            word_list = list(all_top_words)
        
        # Create sources, targets, and values for Sankey diagram
        sources = []
        targets = []
        values = []
        
        # Create a mapping of labels to indices
        doc_indices = {doc: i for i, doc in enumerate(doc_labels)}
        word_indices = {word: i + len(doc_labels) for i, word in enumerate(word_list)}
        
        # Create the links
        for doc, counter in wordcount_data.items():
            doc_idx = doc_indices[doc]
            for word in word_list:
                if word in counter and counter[word] > 0:
                    word_idx = word_indices[word]
                    sources.append(doc_idx)
                    targets.append(word_idx)
                    values.append(counter[word])
        
        # Create labels for the nodes
        node_labels = doc_labels + word_list
        
        # Create the Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])
        
        # Conservative vs. Liberal color scheme
        conservative_color = 'rgba(178, 34, 34, 0.4)'  # Dark red with opacity
        liberal_color = 'rgba(30, 144, 255, 0.4)'      # Dodger blue with opacity
        
        # Determine colors for links based on source document (conservative or liberal)
        link_colors = []
        for source in sources:
            doc = doc_labels[source]
            # Assumption: Conservative documents have 'conservative' in their name
            if 'conservative' in doc.lower():
                link_colors.append(conservative_color)
            # Assumption: Liberal documents have 'liberal' in their name
            elif 'liberal' in doc.lower():
                link_colors.append(liberal_color)
            else:
                link_colors.append('rgba(128, 128, 128, 0.4)')  # Gray for others
        
        # Add colors to the links
        fig.data[0].link.color = link_colors
        
        # Update the layout
        fig.update_layout(
            title_text="Text-to-Word Sankey Diagram: Conservative vs. Liberal Language",
            font_size=10,
            height=800
        )
        
        fig.show()   


