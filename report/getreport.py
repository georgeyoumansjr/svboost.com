import os
import googleapiclient.discovery
import googleapiclient.errors
import asyncio
from collections import Counter
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from config.config import YOUTUBE_API_KEY
import requests
from .scraper import get_search_suggestions

def rank(search_result, keyword) -> list:
    video_id_list = get_videos_from_search_by_keyword_result(search_result)
    videos = get_videos_information(video_id_list)
    tags = get_tag_list_from_video(videos)
    tags = clustering(tags, keyword)
    return tags


def frequency_by_video_tags(search_result)->list:
    video_id_list = get_videos_from_search_by_keyword_result(search_result)
    videos = get_videos_information(video_id_list)
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


def frequency_by_video_description(search_result)->list:
    video_id_list = get_videos_from_search_by_keyword_result(search_result)
    videos = get_videos_information(video_id_list)
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
    result = result[0:slice_number]
    result = to_list(result)
    return result

def to_list(word_list) -> list:
    result = []
    for word in word_list:
        result.append(word[0])

    return result

def get_tag_list_from_video(video_list) -> list:
    result = []
    for video in video_list['items']:
        if 'tags' in video['snippet']:
            for tag in video['snippet']['tags']:
                result.append(tag)

    return result

def get_tag_list_by_each_video(video_list) -> list:
    result = []
    for video in video_list['items']:
        tag_list = []
        if 'tags' in video['snippet']:
            for tag in video['snippet']['tags']:
                tag_list.append(tag)
            result.append(tag_list)

    return result

from config import config
def get_description_list_by_each_video(video_list) -> list:
    result = []
    f = open(config.ROOT+"/stopwords.txt", "r", encoding="utf-8")
    stopwords = eval(f.read())

    for video in video_list['items']:
        if 'description' in video['snippet']:
            for word in video['snippet']['description'].split(" "):
                try:
                    word = re.sub('[^a-zA-Z0-9]+', '', word)
                    ###HERE COMES THE STOPWORDS
                    if not word in stopwords:
                        if word != '':
                            result.append(word.lower())
                except:
                    print()

    return result

#WARNING - There might be some problems in the first 'if' block
def get_videos_from_search_by_keyword_result(search_by_keyword_result) -> list:
    result = []
    for video in search_by_keyword_result['items']:
        if 'videoId' not in video['id']:
            pass
        elif video['id']['videoId'] is not None:
            result.append(video['id']['videoId'])

    return result


#get video from list by its id
def filter_video_by_id(videos, video_id):
    return [v for v in videos if v["id"] == video_id]

#WARNING - this function seems a lot with the 'filter_video_by_id' function,
#investigate more about it
def filter_video_by_id_keyword(videos, video_id):
    for v in videos:
        try:
            if v["id"]['videoId'] == video_id:
                return v
            elif v["id"]['videoId'] == 'undefined':
                return False
        except:
            print("key error")

#WARNING - too implicit what is going on in here
#This is supposed to extract the statics from each video
def get_videos_statistics(uploaded_videos_information):
    #List of videos id
    videos = []
    for video_list in uploaded_videos_information.values():
        if type(video_list) is list:
            for video_info in video_list:
                videos.append(video_info)

    return videos

#Makes api call using channel id to retrieve its information
def get_channel_by_id(channel_id):
    #get the youtube channels
    request = youtube.channels().list(
        part = "contentDetails,statistics",
        id = channel_id
    )
    response = request.execute()
    return response

#Makes api call using video id to get its information
def get_video_by_id(video_id):
    #get the youtube channels
    request = youtube.videos().list(
        part = "snippet,contentDetails,statistics",
        id = video_id
    )
    response = request.execute()
    return response

#Makes api call to search a given keyword inputted by the user
#Remember to make the maxresult available for the user to choose.
def get_search_by_keyword(search_key):
    #get the youtube channels
    request = youtube.search().list(
        part = "snippet",
        maxResults=25,
        q = search_key,
        type = 'video',
        regionCode ='US'
    )
    response = request.execute()
    return response

#WARNING - this function seems a lot like 'get_channel_by_id' function,
#investigate more later
def get_uploaded_videos_from_channel(channel, quantity):
    #get the videos uploaded in the channel (the recent ones)
    uploads_id = channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    request = youtube.playlistItems().list(
        part = "id,contentDetails",
        playlistId = uploads_id,
        maxResults = quantity
    )
    response = request.execute()
    return response

#WARNING - this name is complicated, better to look for other one
def get_video_id_list_from_channel(uploaded_videos_information):
    #List of videos id
    videos = []
    for video_list in uploaded_videos_information.values():
        if type(video_list) is list:
            for video_info in video_list:
                videos.append(video_info['contentDetails']['videoId'])

    return videos

#Makes API call to retrieve information about the video
def get_videos_information(videos_id):
    #get videos information
    request = youtube.videos().list(
            part = "snippet,contentDetails,statistics",
            id = ",".join(videos_id)
        )
    response = request.execute()

    return response

#Basically gets the most recent videos from channel by its id
def report_by_channel(channel_id: str = '', quantity: int = 5):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    global youtube
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

    response = get_channel_by_id(channel_id = channel_id)
    response = get_uploaded_videos_from_channel(channel = response, quantity = quantity)
    video_id_list = get_video_id_list_from_channel(response)
    response = get_videos_information(videos_id = video_id_list)

    return response

#get video information by using its id
def report_by_video(video_id: str = ''):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    global youtube
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

    response = get_video_by_id(video_id = video_id)

    return response

#Get the result from a search by keyword
def report_by_keyword(key: str = ''):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    global youtube
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=YOUTUBE_API_KEY)

    response = get_search_by_keyword(search_key = key)

    return response

#This function will group the most frequent words up to 50 words in the resulting group
def clustering(tags, keyword):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(tags)

    true_k = 1
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)

    print("Top terms per cluster:")
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    clusters = []
    for i in range(true_k):
        for ind in order_centroids[i, :10]:
            clusters.append(terms[ind])

    return style_tags(clusters)

def style_tags(tags):
    result = []
    for tag in tags:
        result.append(tag)

    return " ".join(result)

def get_suggestions(search_term):
    language = "en"
    region = "us"

    url = 'https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&hl='+language+'&gl='+region+'&q='+search_term+'&gs_rn=64&ds=yt'

    resp = requests.get(url)
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    a = str(resp.content)
    startidx = a.find('(')
    endidx = a.rfind(')')

    new_list = []
    result = eval(a[startidx + 1:endidx])
    for lis in result[1]:
        new_list.append(lis[0])

    return new_list

def get_suggestions_webscraper(search_term):
    result = get_search_suggestions(search_term)

    return result
