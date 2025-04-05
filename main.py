from nlp.textastic import Textastic

foxn1 = Textastic()
foxn1.load_text('foxnews_conservative.txt')
print(foxn1.data['bigramcount'])

foxn1.compare_num_words('bigramcount')