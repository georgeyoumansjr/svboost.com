from collections import Counter
import re
import pandas as pd
from pytube import Search

def frequency_by_video_tags(videos)->list:
    tags = get_tag_list_by_each_video(videos)
    end = tags.copy()
    aux = tags[0]
    result = []
    cont = 0
    while tags != []:
        for tag_list in tags:
            for word in tag_list:
                for aux_word in aux:
                    cont = cont +1
                    if word in aux_word.lower():
                        result.append(word)
                        break
        aux = tags.pop(0)

    result = dict(Counter(result))
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    result = to_list(result)
    return result


def frequency_by_video_description(videos)->list:
    
    descriptions = get_description_list_by_each_video(videos)

    result = []
    mirror = []
    df = pd.DataFrame(descriptions)
    df.dropna()
    for word in descriptions:
        try:
            aux = df.copy()
            df1 = aux[aux[0].str.contains(word)]
            if word not in mirror and len(word) > 3:
                result.append((word, len(df1.index)))
                mirror.append(word)
        except:
            print()

    result = sorted(result, key=lambda x: x[1], reverse=True)
    total_size = len(result)
    slice_number = int(total_size*0.07)
    if slice_number > 30:
        slice_number = 30
    result = result[0:slice_number]
    result = to_list(result)
    return result

def to_list(word_list) -> list:
    result = []
    for word in word_list:
        result.append(word[0])

    return result

def get_tag_list_by_each_video(video_list) -> list:
    result = []
    for video in video_list:
        tag_list = []
        for tag in video.keywords:
            tag_list.append(tag)
        result.append(tag_list)

    return result

from config import config
def get_description_list_by_each_video(video_list) -> list:
    result = []
    f = open(config.ROOT+"/stopwords.txt", "r", encoding="utf-8")
    stopwords = eval(f.read())

    for video in video_list:
        if video.description is not None:
            for word in video.description.split(" "):
                try:
                    word = re.sub('[^a-zA-Z0-9]+', '', word)
                    ###HERE COMES THE STOPWORDS
                    if not word in stopwords:
                        if word != '':
                            result.append(word.lower())
                except:
                    print()

    return result
