
import tweepy as tw
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import nltk 
import string
import re
import os
import pickle




#modle traning 

def load_data():
    data = pd.read_csv('/Users/nidhivanjare/Documents/GitHub/Final-Year-Project/training_dataset_new.csv')
    return data

# convert to dataframe
df = load_data()

# remove links
df['Tweets'] = df['Tweets'].apply(lambda x: re.split('https:\/\/.*', str(x))[0])

# remove emoji
df2 = df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))

df2['Tweets'] = df2['Tweets'].str.replace('(@\w+.*?)',"" , regex=True)
df2['Tweets'] = df2['Tweets'].str.replace('(#\w+.*?)',"" ,regex=True)

# print df
pd.set_option("display.max_colwidth", None)
pd.set_option('display.max_rows', df2.shape[0]+1)
df2

#Droping Duplicate values 
df2.drop_duplicates(subset ="Tweets",
                     keep = False, inplace = True)
df2.head(10)

# sns.countplot(x = 'Output', data = df2)
# plt.show()


#WordCloud Visualisation 


# df2['Output'] = df2['Output'].astype(str).astype(int)
# df2.dtypes

# from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
# # Start with one review:
# df_Related = df2[df2['Output']==1]
# df_notRelated = df2[df2['Output']==0]
# tweet_All = " ".join(review for review in df2.Tweets)
# tweet_Realted = " ".join(review for review in df_Related.Tweets)
# tweet_notRelated = " ".join(review for review in df_notRelated.Tweets)

# # Create and generate a word cloud image:
# wordcloud_ALL = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(tweet_All)
# wordcloud_Realted = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(tweet_Realted)
# wordcloud_notRelated = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(tweet_notRelated)


# fig, ax = plt.subplots(3, 1, figsize  = (30,30))
# # Display the generated image:
# ax[0].imshow(wordcloud_ALL, interpolation='bilinear')
# ax[0].set_title('All Tweets', fontsize=30)
# ax[0].axis('off')

# ax[1].imshow(wordcloud_Realted, interpolation='bilinear')
# ax[1].set_title('Tweets Related to a Problem in Thane ',fontsize=30)
# ax[1].axis('off')

# ax[2].imshow(wordcloud_notRelated, interpolation='bilinear')
# ax[2].set_title('Tweets Not Realted to Problems for Thane',fontsize=30)
# ax[2].axis('off')
# plt.show()

# Pre-processing text data

# 1. Remove punctuations
# 2. Tokenization - Converting a sentence into list of words
# 3. Remove stopwords
# 4. Lammetization/stemming - Tranforming any form of a word to its root word


import nltk
nltk.download('omw-1.4')

def remove_punct(text):
    text  = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text

df2['Tweet_punct'] = df2['Tweets'].apply(lambda x: remove_punct(x))
df2.head(10)


def tokenization(text):
    text = re.split('\W+', text)
    return text

df2['Tweet_tokenized'] = df2['Tweet_punct'].apply(lambda x: tokenization(x.lower()))
df2.head()

import nltk
nltk.download('stopwords')
stopword = nltk.corpus.stopwords.words('english')

def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text
    
df2['Tweet_nostopwords'] = df2['Tweet_tokenized'].apply(lambda x: remove_stopwords(x))
df2.head(10)

import nltk
ps = nltk.PorterStemmer()

def stemming(text):
    text = [ps.stem(word) for word in text]
    return text

df2['Tweet_stemmed'] = df2['Tweet_nostopwords'].apply(lambda x: stemming(x))
df2.head()


import nltk
nltk.download('wordnet')
wn = nltk.WordNetLemmatizer()

def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text

df2['Tweet_lemmatized'] = df2['Tweet_nostopwords'].apply(lambda x: lemmatizer(x))
df2.head()


## Vectorisation


# Cleaning data in single line through passing clean_text in the CountVectorizer


def clean_text(text):

    text_lc = "".join([word.lower() for word in text if word not in string.punctuation]) # remove puntuation
    # print(text_lc)

    text_rc = re.sub('[0-9]+', '', text_lc)
    # print(text_rc)

    tokens = re.split('\W+', text_rc)    # tokenization
    # print(tokens)

    text = [ps.stem(word) for word in tokens if word not in stopword]  # remove stopwords and stemming
    # print(text)
    
    return text

countVectorizer = CountVectorizer(analyzer=clean_text) 
countVector = countVectorizer.fit_transform(df2['Tweets'])

# print(countVectorizer.get_feature_names())


print('{} Number of tweets has {} words'.format(countVector.shape[0], countVector.shape[1]))
#print(countVectorizer.get_feature_names())


count_vect_df = pd.DataFrame(countVector.toarray(), columns=countVectorizer.get_feature_names())
count_vect_df.head()

##Model Training and Testing

# split into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df2['Tweets'], df2['Output'], random_state=1)
print('Number of rows in the total set: {}'.format(df2.shape[0]))
print('Number of rows in the training set: {}'.format(X_train.shape[0]))
print('Number of rows in the test set: {}'.format(X_test.shape[0]))

# Instantiate the CountVectorizer method
count_vector = CountVectorizer()
# Fit the training data and then return the matrix
training_data = count_vector.fit_transform(X_train)
# Transform testing data and return the matrix. Note we are not fitting the testing data into the CountVectorizer()
testing_data = count_vector.transform(X_test)

from sklearn.naive_bayes import MultinomialNB
naive_bayes = MultinomialNB()
naive_bayes.fit(training_data, y_train)

predictions = naive_bayes.predict(testing_data)
# print(predictions)


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
print('Accuracy score: ', format(accuracy_score(y_test, predictions)))
print('Precision score: ', format(precision_score(y_test, predictions , pos_label='1')))
print('Recall score: ', format(recall_score(y_test, predictions , pos_label='1')))
print('F1 score: ', format(f1_score(y_test, predictions ,pos_label='1')))



# Save the vectorizer
vec_file = 'vectorizer.pickle'
pickle.dump(count_vector, open(vec_file, 'wb'))

loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))



# Saving the model 
# Save the trained model as a pickle string.
saved_model = pickle.dumps(naive_bayes)
 
# Load the pickled model
naive_bayes_from_pickle = pickle.loads(saved_model)
 
# Use the loaded pickled model to make predictions
# naive_bayes_from_pickle.predict(X_test)




# lst = [
#        ['we should meet at ghodbunder road']
#        ,['There is a new restaurant in Manpada'] 
#        ,['Let us celebrate Diwali in Vasant Vihar area'] 
#        ,['I have to give my ielts exam at Wagale estate.']
#        ,['Why are you dancing near kasarvadavali?'] 
#        ,['I am a teacher at Vasant Vihar high school and the students are very mischievious'] #this is giving wrong ..idk why 
#        ,['How can I go to Khopat ST stand?']
#        ,['I am vising thane today']] 
# df = pd.Series( (v[0] for v in lst) )

# trial = count_vector.transform(df)
# # print(trial)

# prediction_trial = naive_bayes_from_pickle.predict(trial)
# print(prediction_trial)


# lst1 = [['Traffic is crazy']
#        ,['Going out today']
#        ,['What is wrong with the wi-fi in this locality']
#        ,['Party..yayay'],['Life is unfair']
#        ,['Hospitals running low on staff']
#        ,['Children going to school']
#        ,['Cant sleep']
#        ,['Heavy rainfall in the city']
#        ,['I have a problem in my family']
#        ,['There are no proper streetlights in this city TMC should take action']
#         ,['This is how citizens respect traffic laws in Mumbai. + No Helmet+ Wrong Side Driving'],['RT This is how citizens respect traffic laws in Mumbai No Helmet Wrong Side Driving Not expecting any action on this']] 

# str3 = 'There are no proper streetlights in this city TMC should take action'
# lst1 = [[str3]]
# df = pd.Series( (v[0] for v in lst1) )
# print(df)
# trial = loaded_vectorizer.transform(df)
# print(trial)
# prediction_trial = naive_bayes_from_pickle.predict(trial)
# print(prediction_trial)
