from flask import request, jsonify, redirect, Blueprint
from .getreport import frequency_by_video_tags
from .getreport import frequency_by_video_description
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from db.db import db
from db.user import User
import openai
from pytube import Search

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


@blueprint.route("/get-keyword_research-info",  methods=['GET'])
@login_required
def get_keyword_research_info():
    global search_by_keyword_result

    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        suggestions = Search(keyword).completion_suggestions
        json_data = jsonify(suggestions)

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
        videos = Search(keyword).results
        tags = frequency_by_video_tags(videos)
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
        return redirect('/pricing_page')
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        try:
            keywords = str(request.args['keywords'])
        except:
            keywords = ''
        try:
            if keywords != '':
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Write a video description about "+keyword+ " with these keywords: "+keywords,
                    max_tokens=1000,
                    temperature=0.9,
                    n=3)
            else:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="Write a video description about "+keyword,
                    max_tokens=1000,
                    temperature=0.9,
                    n=3)
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
        except Exception as e:
            print(e)
            db.session.rollback()
            return 'error'
    else:
        return "missing value in request"


@blueprint.route("/get-description-report", methods=['GET'])
@login_required
def get_description_report():
    global search_by_keyword_result

    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        videos = Search(keyword).results
        descriptions = frequency_by_video_description(videos)
        json_data = jsonify(descriptions)

        return json_data
    else:
        return "missing value in request"

