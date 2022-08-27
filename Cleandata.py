# Script to clean and arrange data that was scrapped
import pandas as pd
import numpy as np
import json
import re


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

    for i in range(1,19):
        nm='chpt'+ str(i) +'V'
        new_nm='chpt' + str(i)
        sans_data["chptverse"]=sans_data["chptverse"].str.replace("{}.*".format(nm), new_nm, case=False, regex=True)

     # create new mega list
    Sans_data_chpt=sans_data[sans_data["chptverse"]=='chpt1']
    regular_list = ' '.join(Sans_data_chpt["Sans"])
    regular_list = regular_list.replace("[", '').replace("]", '').replace("'",'').replace(",",'')
    split_pattern=r'[0-9]+'
    test=re.split(split_pattern, regular_list)

    # test=regular_list.split('||')
    # regular_list = regular_list.str.split('||[0-9]*||', regex=True)???



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
                # print(lp)



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

def get_versesV3():
         # sans_data = pd.read_csv('/home/ubuntu/Documents/Gita/Gita-Ganitashaastram/Sans.csv') #NVME drive
        sans_data = pd.read_csv('/home/ubuntu/Documents/Gita_Ganitashaastram.io/Sans.csv')  # USB drive
        translit= pd.read_csv(r'Translit.csv')
        translit.columns=['chptverse','Translit']

        #other data
        # Gita_data = pd.read_json(r'LP_verses.json')
        Gita_data = pd.read_json(r'LP_dataset_english.json')
        # Gita_data['verses'][1]['1']['transliteration']
        # with open(r'/gita_json-master/LP_dataset_english.json', encoding='utf-8') as f:
        #      # Deserialises it
        #      json_data = json.load(f)
        #      f.close()

        # #access transliteration
        # Gita_data.iloc[0]['verses']['1']['transliteration']

        # Iterating through chapters to correct chapter names
        for i in range(1, 19):
             nm = 'chpt' + str(i) + 'V'
             new_nm = str(i)
             sans_data["chptverse"] = sans_data["chptverse"].str.replace("{}.*".format(nm), new_nm, case=False, regex=True)

        big_data=pd.DataFrame(columns=['Chapter','Verse','Sanskrit'])
        # Iterate for each chapter
        for i in range(1, 19):
            chpt_nm= str(i)
            Sans_data_chpt = sans_data[sans_data["chptverse"] == chpt_nm]
            new_chapter=clean_chpt(Sans_data_chpt)
            if i==13:
                del new_chapter[1]
            # print(new_chapter)
            data = {'Sanskrit': new_chapter,
                    'Verse': list(range(1,len(new_chapter)+1))}
            # Create Chapter DataFrame
            df = pd.DataFrame(data)
            df["Chapter"]=int(chpt_nm)

            # big_data=big_data.append(df)  # create new mega list
            big_data=pd.concat([big_data,df])

        # Work on transliteration


        return big_data



def clean_chpt(Sans_data_chpt):
    regular_list = ' '.join(Sans_data_chpt["Sans"])
    regular_list = regular_list.replace("[", '').replace("]", '').replace("'", '').replace(",", '')
    split_pattern = r'[0-9]+'
    test = re.split(split_pattern, regular_list)
    del test[-1]
    return test



    # BG_total.to_csv('BG_dataframev2_organized.csv')



if __name__ == "__main__":
    #-----------------------main code
    #--------redo getverse -save csv
    Sanskritverses=get_versesV3()
    for i in range(1, 19):
        print('Chapter {} has {} verses'.format(i,len(Sanskritverses[Sanskritverses['Chapter']==i])))

    # print(Sanskritverses[Sanskritverses['Chapter']==13])
    # print(BGdata['Sanskrit'])
    # # print(BGdata['Transliteration'][0])
    # BGdata.loc[BGdata['Chapter'] == 1, 'Transliteration'].iloc[0]


