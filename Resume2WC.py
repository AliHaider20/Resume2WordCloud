import PyPDF2 as pdread
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
import spacy
import matplotlib.pyplot as plt
from geotext import GeoText

# Downloading the required NLTK corpuses
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("averaged_perceptron_tagger")

stops = set(stopwords.words("english")) # Fecthing list of stop words 

file = open(r"C:\Users\Ali & Alifia's Home\Desktop\Resume_Haider_Ali.pdf", "rb")
reader = pdread.PdfReader(file) # PDF reader object
pages = reader.pages # Extracting pages

wn = nltk.WordNetLemmatizer() # Initializing WordNet Lemmatizer
months = ["jan", "january", "feb", "february", "march", "april", "apr", "may", "june", "july", "aug", "august",
        "sept", "september", "nov", "november", "dec", "december"]

wn = nltk.WordNetLemmatizer()


def extract_required_words(pages, extra_words):
    """
    Extracts all the required words for the wordcloud
    """

    words = []
    locations =  []

    for i in range(len(pages)):
        words.extend(reader.pages[i].extract_text().split(" "))
    words = [word for word in words if word not in months]
    geo = GeoText(" ".join(words))
        
    for i in geo.cities + geo.countries:
        locations.extend(i.split(" "))

    words = word_tokenize(" ".join(words))

    words = [wn.lemmatize(word) for word in words]

    words = [word for word in words if word not in locations ]
    words = [word.lower() for word in words if word not in months]
    words = [word for word in words ]

    final_words = []
    for word in words:
        # Consider word with length grater than 2, not a stopwords, is not numeric, and not a punctuation
        if (
            (word not in stops)
            and (len(word) > 2)
            and (word.isalpha())
            and (word not in punctuation)
        ):
            final_words.append(word)

    final_words = [
        word
        for word, tag in nltk.pos_tag(final_words)
        if (tag == "NN" or tag == "NNS" or tag == "RB") # Extracting words using prepositions tagging from NLTK
        # NN: common singular nouns, NNS: common, plural nouns, RB: Adverb
    ]
    return final_words


if __name__ == "__main__":
    extra_words = []
    while True:
        word = input("Enter the extra word you want to remove or press Enter: ")
        if word:
            extra_words.append(word)
        else:
            break

    remove_words = []

    final_words = extract_required_words(pages, extra_words)
    wordcloud = WordCloud(
        width=1000,
        height=300,
        background_color="white",
        # stopwords = stopwords,
        min_font_size=10,
    )
    
    final_words = final_words[3:]
    wordcloud.generate(" ".join(final_words))

    plt.axis('off')
    plt.imshow(wordcloud, cmap="magma")
    plt.show()
