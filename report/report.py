from flask import Blueprint, render_template
from flask import request, jsonify, redirect
from .getreport import filter_video_by_id
from .getreport import filter_video_by_id_keyword
from .getreport import get_videos_statistics
from .getreport import report_by_channel
from .getreport import report_by_keyword
from .getreport import report_by_video
from .getreport import frequency_by_video_tags
from .getreport import frequency_by_video_description
from flask import Flask
from markupsafe import escape
from .scraper import *
import logging
import threading
import queue
import time
from .getreport import get_suggestions
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from .getreport import get_suggestions_webscraper
from db.db import db
from db.user import User
import uuid
import calendar
import openai


blueprint = Blueprint('report', __name__,
                        template_folder='../',
                        static_url_path='/static',
                        static_folder='../static')

videos_info = []
video_info = []
search_by_keyword_result = []
templates_path = "report/templates/"


# --------------------------------------------
# ---------------- REPORT -------------------
# --------------------------------------------

@blueprint.route("/get-videos-info", methods=['GET'])
@login_required
def get_videos_info():
    global videos_info
    if 'channel_id' in request.args and "quantity" in request.args:
        channel_id = str(request.args['channel_id'])
        quantity = int(request.args['quantity'])
        rep = report_by_channel(channel_id, quantity)
        videos_info = get_videos_statistics(rep)
        json_data = jsonify(videos_info)
        return json_data
    else:
        return "missing value in request"

@blueprint.route("/get-video-info", methods=['GET'])
@login_required
def get_video_info():
    global video_info

    if 'video_id' in request.args:
        video_id = str(request.args['video_id'])
        video_info = report_by_video(video_id)
        json_data = jsonify(video_info['items'][0])
        return json_data
    else:
        return "missing value in request"

@blueprint.route("/get-keyword_research-info",  methods=['GET'])
@login_required
def get_keyword_research_info():
    global search_by_keyword_result

    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        suggestions_result = get_suggestions(keyword)
        json_data = jsonify(suggestions_result)

        return json_data
    else:
        return "missing value in request"

@blueprint.route("/get-tag-report", methods=['GET'])
@login_required
def get_tag_report():
    global search_by_keyword_result

    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        #language = str(request.args['language'])
        search_by_keyword_result = report_by_keyword(keyword)
        tags = frequency_by_video_tags(search_by_keyword_result)
        json_data = jsonify(tags)

        return json_data
    else:
        return "missing value in request"

@blueprint.route("/get-description-builder-keywords", methods=['GET'])
@login_required
def get_description_builder_keywords():
    
    global search_by_keyword_result
    user = User.query.filter_by(id=current_user.id).first()
    if user.token_amount < 5:
        redirect('/pricing_page')
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])

        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="Write a video description about "+keyword,
                max_tokens=1000,
                temperature=0.9,
                n=3,
            )
            # decrease user's tokens
            user.token_amount -= 5
            db.session.commit()
            json_data={}
            json_data['1'] = response['choices'][0]['text']
            json_data['2'] = response['choices'][1]['text']
            json_data['3'] = response['choices'][2]['text']

            #search_by_keyword_result = report_by_keyword(keyword)
            #bdes = frequency_by_video_description(search_by_keyword_result)
            json_data = jsonify(json_data)

            return json_data
        except:
            db.session.rollback()
            return 'there is an error'
    else:
        return "missing value in request"


@blueprint.route("/get-description-report", methods=['GET'])
@login_required
def get_description_report():
    global search_by_keyword_result

    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        search_by_keyword_result = report_by_keyword(keyword)
        descriptions = frequency_by_video_description(search_by_keyword_result)
        json_data = jsonify(descriptions)

        return json_data
    else:
        return "missing value in request"


@blueprint.route("/get-videos-report", methods=['GET'])
@login_required
def get_videos_report():
    global videos_info

    if 'video_id' in request.args:
        video_id = str(request.args['video_id'])
        video = filter_video_by_id(videos_info, video_id)
        return render_template(templates_path+"video-report.html", video= video[0])
    else:
        return "missing value in request"

@blueprint.route("/get-video-report", methods=['GET'])
@login_required
def get_video_report():
    global video_info
    return render_template(templates_path+"video-report.html", video= video_info['items'][0])


@blueprint.route("/get-keyword-video-report", methods=['GET'])
@login_required
def get_keyword_video_report():
    global search_by_keyword_result
    if 'video_id' in request.args:
        video_id = str(request.args['video_id'])

        video = filter_video_by_id_keyword(search_by_keyword_result['items'], video_id)
        if video:
            video = report_by_video(video['id']['videoId'])
            return render_template(templates_path+"video-report.html", video=video['items'][0])
        else:
            return render_template("index.html")
    else:
        return "missing value in request"

@blueprint.route('/search/<search_term>')
def get_search_term_by_keyword(search_term: str):
  que = queue.Queue()
  x = threading.Thread(target=lambda q, arg1: q.put(get_search_suggestions(arg1)), args=(que, search_term))
  x.start()
  x.join()
  result = que.get()
  #time.sleep(30)
  return jsonify(keywords = result)

@blueprint.route("/get-keyword-suggestions-webscraper",  methods=['GET'])
@login_required
def get_keyword_suggestions_webscraper():

    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        suggestions_result = get_suggestions_webscraper(keyword)
        json_data = jsonify(suggestions_result)
        return json_data
    else:
        return "missing value in request"
