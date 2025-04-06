from nlp.textastic import Textastic
import os

def main():
    # Create Textastic instance
    analyzer = Textastic()
    
    # Load stop words (you'll need to create this file)
    if os.path.exists('stopwords.txt'):
        analyzer.load_stop_words('stopwords.txt')
    
    # Load conservative articles
    analyzer.load_text('foxnews_conservative.txt', label='Fox News (Conservative)')
    analyzer.load_text('nationalreview_conservative.txt', label='National Review (Conservative)')
    analyzer.load_text('boundless_conservative.txt', label='Boundless (Conservative)')
    analyzer.load_text('washingtonpost_conservative.txt', label='Washington Post (Conservative)')
    analyzer.load_text('usnews_conservative.txt', label='US News (Conservative)')
    
    # Load liberal articles
    analyzer.load_text('newyorktimes_libral.txt', label='New York Times (Liberal)')
    analyzer.load_text('cityandstateny_libral.txt', label='City and State NY (Liberal)')
    analyzer.load_text('forbes_libral.txt', label='Forbes (Liberal)')
    analyzer.load_text('usatoday_libral.txt', label='USA Today (Liberal)')
    analyzer.load_text('msnbc_libral.txt', label='MSNBC (Liberal)')
    
    # Create Sankey diagram 
    analyzer.wordcount_sankey(k=8)  # Show top 8 words from each source
    
    # Create bigram visualization
    analyzer.bigram_visualization(top_n=8)
    
    # Create comparative word usage visualization 
    analyzer.comparative_word_usage(k=15)  # Compare top 15 words
    
    # analyze specific words of interest
    specific_words = ['tax', 'government', 'freedom', 'rights', 'economy', 
                      'regulation', 'policy', 'healthcare', 'education', 'climate']
    print("Generating Comparative Analysis of Policy Terms...")
    analyzer.comparative_word_usage(words=specific_words)

if __name__ == "__main__":
    main()