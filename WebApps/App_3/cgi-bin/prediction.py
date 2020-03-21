import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle as pkl

def textProcessing(documents):
    tokens = []
    for i in range(len(documents)):
        tokens.append(word_tokenize(documents['Review'].iloc[i].lower()))

    eng_stopwords = stopwords.words("english")
    eng_stopwords.extend([',', '.', '!', '@', '#', '?', '-'])

    main_words = []
    for i in range(len(tokens)):
        words = []
        for token in tokens[i]:
            if token not in eng_stopwords:
                words.append(token)
        main_words.append(words)

    wnet = WordNetLemmatizer()

    for i in range(len(main_words)):
        for j in range(len(main_words[i])):
            main_words[i][j] = wnet.lemmatize(main_words[i][j], pos='v')

    for i in range(len(main_words)):
        main_words[i] = " ".join(main_words[i])

    return main_words


def testReview(review):
    test_df = pd.DataFrame({"Review": [review]})
    test_words = textProcessing(test_df)
    with open('nb.pkl', 'rb') as file:
        nb = pkl.load(file)

    with open('tfidf.pkl', 'rb') as file:
        tfidf = pkl.load(file)

    test_vector = tfidf.transform(test_words).toarray()
    pred = nb.predict(test_vector)
    return pred