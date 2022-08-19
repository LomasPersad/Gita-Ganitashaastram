# Script to clean and arrange data that was scrapped
import pandas as pd
import numpy as np
import json


#test sync
def get_versesV2():
    # Opening JSON file
    # f = open('LP_dataset_english.json')
    # # returns JSON object as
    # # a dictionary
    # data = json.load(f)
    # # Closing file
    # f.close()

    # sans_data = pd.read_csv('/home/ubuntu/Documents/Gita/Gita-Ganitashaastram/Sans.csv') #NVME drive
    sans_data = pd.read_csv('/home/ubuntu/Documents/Gita_Ganitashaastram.io/Sans.csv') #USB drive


    # Iterating through the chapters
    # list
    # for i in data['chapters']:
    #     print(data['chapters'][i]['name'])
    V=['a']*640
    indx=0
    BG_total = pd.DataFrame(columns=['Chapter','Verse','Sanskrit'])
    # Iterating through the verses
    for i in range(len((sans_data))):
            # print(data['verses'][str(i)][str(v)]['text'].replace('।।\* ।।',' '))
            # print(sans_data['Sans'][i])
            temp =sans_data["Sans"][i].replace("'",'').replace(",",'').replace("[", "").replace("]",'')
            temp=temp.split('||')

            if len(temp)==3: #one verse
                print(temp[0])
                # V=temp[0]
                # V_n=temp[1]
                print(temp[1])
            elif len(temp)>3:
                # rng=np.arange(0,len(temp),1)
                V = temp[0:len(temp):2]
                V_n=temp[1:len(temp):2]
                print(lp)



            # ?-------- to do. seperate sanskrit verses in two. match each sanskrit word to corresponding transliteration


            # ele = Transliteration.find_all(text=True)
            # print('chapter{} and verse{}'.format(i,v))
            # tmp=data['verses'][str(i)][str(v)]['text']
            # tmp = tmp.replace('।', ' ')#remove symbol
            # tmp = re.sub(r'\d+', '', tmp) #remove number
            # V[indx]=tmp
            # Store in dataframe

            # BG_total=BG_total.append({'Chapter': i, 'Verse': v, 'Sanskrit': tmp},ignore_index = True)
            #
            # indx+=1



    # BG_total.to_csv('BG_dataframev2_organized.csv')



if __name__ == "__main__":
    #-----------------------main code
    #--------redo getverse -save csv
    get_versesV2()
    # print(BGdata['Sanskrit'])
    # # print(BGdata['Transliteration'][0])
    # BGdata.loc[BGdata['Chapter'] == 1, 'Transliteration'].iloc[0]


