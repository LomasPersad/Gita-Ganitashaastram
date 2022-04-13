# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from matplotlib import rc
# import matplotlib.image as mpimg
import seaborn as sns
from wordcloud import WordCloud,STOPWORDS
import re
import json
import collections
from nltk.probability import FreqDist
import nltk
# from indic_transliteration import sanscript
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory
# https://fonts.google.com/specimen/Eczar?subset=devanagari#standard-styles



#------Extract sections from large datafile

def get_data(nam):
    f = open(nam)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()
    return data

def get_verses():
    # Opening JSON file
    f = open('LP_dataset_english.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    # Closing file
    f.close()

    # Iterating through the chapters
    # list
    # for i in data['chapters']:
    #     print(data['chapters'][i]['name'])
    V=['a']*640
    indx=0
    BG_total = pd.DataFrame(columns=['Chapter','Verse','Sanskrit','Transliteration'])
    # Iterating through the verses
    for i in data['chapters']:
        for v in data['verses'][i]:
            # print(data['verses'][str(i)][str(v)]['text'].replace('।।\* ।।',' '))
            print('chapter{} and verse{}'.format(i,v))
            tmp=data['verses'][str(i)][str(v)]['text'].replace('|',' ') #remove symbol
            tmp = tmp.replace('।', ' ')#remove symbol
            tmp = re.sub(r'\d+', '', tmp) #remove number
            V[indx]=tmp
            # Store in dataframe
            translit=data['verses'][str(i)][str(v)]['transliteration']
            BG_total=BG_total.append({'Chapter': i, 'Verse': v, 'Sanskrit': tmp, 'Transliteration': translit},ignore_index = True)

            indx+=1


    # print(indx)
    # data_file = open("LP_verses.json", "w", encoding="utf-8")
    # json.dump(V, data_file, ensure_ascii=False)
    BG_total.to_csv('BG_dataframe.csv')

def compile_stopwords_list_frequency(text, freq_percentage=0.02):

    words = nltk.tokenize.word_tokenize(text)
    freq_dist = FreqDist(word.lower() for word in words)
    words_with_frequencies = [(word, freq_dist[word]) for word in freq_dist.keys()]
    sorted_words = sorted(words_with_frequencies, key=lambda tup: tup[1])
    length_cutoff = int(freq_percentage*len(sorted_words))
    stopwords = [tuple[0] for tuple in sorted_words[-length_cutoff:]]
    return stopwords


# df.to_csv(file_name, sep='\t', encoding='utf-8')


#-----------------------main code
#--------redo getverse
# get_verses()

#---------------------ANALYSE Sanskrit
# Opening JSON file
# f = open('LP_verses.json')
# Verses = json.load(f)
# f.close()
# ---------------OLD way
# Verses=get_data('LP_verses.json')
# df_verses = pd.DataFrame(Verses)
# df_verses.rename(columns ={0:'hindi'}, inplace = True)
# ----------------OLD way

# nltk.download('punkt')

BGdata= pd.read_csv('BG_dataframe.csv') # ['Chapter','Verse','Sanskrit','Transliteration']


# --------------Barchart #------plot chapter-verse#
"""
#get data
data=get_data('LP_dataset_english.json') # all data
plt_vers = pd.DataFrame(columns=['chpt','Verse_count'])

alist = []
for i in data['chapters']:
    num=data['chapters'][str(i)]['verses_count']
    print('Chapter {} has {} verses'.format(i, num))

    new_list={'chpt': int(i), 'Verse_count': int(num)}
    alist.append(new_list)
    # plt_vers = plt_vers.append({'chpt': int(i), 'Verse_count': int(num)},
    #                            ignore_index=True)
    # plt_vers[n]=num
    # n+=1
Chpt_versecount=pd.DataFrame.from_records(alist) #create table

# Setting the dimensions of the figure
plt.figure(figsize=(15,5), frameon=False)
# plt.rc('font', family='Open Sans')
plt.tick_params(labelsize=11, length=6, width=2)
# Passing the data to plot
# sns.countplot(plt_vers)
my_image = plt.imread('plots/BG2.jpg')
ax=sns.barplot(x='chpt', y='Verse_count', data=Chpt_versecount)
for container in ax.containers:
    ax.bar_label(container,weight='bold')
    # ax.text(
    #     bar.get_x() + bar.get_width() / 2,
    #     bar.get_height() + 0.3,
    #     round(bar.get_height(), 1),
    #     horizontalalignment='center',
    #     color=bar_color,
    #     weight='bold'
    # )
# plt.imshow(img, extent=[110, 40, 110, 400], aspect='auto')
plt.imshow(my_image,
         aspect=ax.get_aspect(),
         extent= ax.get_xlim() + ax.get_ylim(),
         zorder=1, alpha=0.6)
ax=sns.barplot(x='chpt', y='Verse_count', data=Chpt_versecount)
plt.xlabel("Chapter number", fontsize=16, fontname='Nimbus sans')
plt.ylabel("Number of Verses", fontsize=16, fontname='Nimbus sans')
# Displaying the plot
plt.tight_layout()
plt.show()
# plt.savefig('plots/BG_verse_count.png')
"""

#<---------------Transliteration section
df_verses = BGdata.apply(lambda row: row['Transliteration'].strip().split(), axis=1)
data1 = []
for row in df_verses:
    temp = []
    for words in row:
        if len(words)>2:
            temp.append(words)
    data1.append(temp)
data_flat1 = [item for sublist in data1 for item in sublist]
# Getting to know the most prominent 10 words used across the documen
# as per my knowledge of this holy document it makes sense to see these results because of the words used such as भारत, अर्जुन, कर्म, ज्ञानं.
top_10_translit = [i[0] for i in sorted(dict(collections.Counter(data_flat1)).items(), key=lambda k: k[1], reverse=True)[:20]]
print(top_10_translit)

# stopwords = compile_stopwords_list_frequency(data_flat1)
# stopwords.remove("holmes")
# stopwords.remove("watson")

#plot world cloud- generate for all, then each chapter
wordfreq1 = collections.Counter(data_flat1)
text = data_flat1
fig = plt.figure(figsize=(20,10), facecolor='k')
wordcloud = WordCloud(width=1300, height=600,max_words=2000,font_path='/home/ubuntu/Downloads/Eczar/Eczar-VariableFont_wght.ttf').generate(str(text))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.show()



#<--------------hindi section
#get common words df_verses.head()
df_verses = BGdata.apply(lambda row: row['Sanskrit'].strip().split(), axis=1)
data = []
for row in df_verses:
    temp = []
    for words in row:
        if len(words)>2:
            temp.append(words)
    data.append(temp)
data_flat = [item for sublist in data for item in sublist]

# Getting to know the most prominent 10 words used across the documen
# as per my knowledge of this holy document it makes sense to see these results because of the words used such as भारत, अर्जुन, कर्म, ज्ञानं.
top_10 = [i[0] for i in sorted(dict(collections.Counter(data_flat)).items(), key=lambda k: k[1], reverse=True)[:20]]
print(top_10)

stopword=open('hindi-tokenizer-master/stopwords.txt','r')
stop_words=[]
# pre-process stopword
for i in stopword:
    i = re.sub('[\n]', '', i)
    stop_words.append(i)
    stopwords = set(stop_words)


#plot world cloud- generate for all, then each chapter
wordfreq = collections.Counter(data_flat)
text = data_flat
fig = plt.figure(figsize=(20,10), facecolor='k')
wordcloud = WordCloud(width=1300, height=600,max_words=2000,font_path='/home/ubuntu/Downloads/Yatra_One/YatraOne-Regular.ttf',stopwords = stopwords).generate(str(wordfreq))
plt.imshow(wordcloud,interpolation='bilinear')
plt.axis("off")
plt.show()

# /home/ubuntu/Downloads/lohit_devanagari/Lohit-Devanagari.ttf