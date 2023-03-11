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
        return 'not enough tokens'
    if 'keyword' in request.args:
        keyword = str(request.args['keyword'])
        keywords = str(request.args['keywords'])
        emoji = request.args['emoji']
        
        try:
            prompt="give me a video description about "+keyword
            if keywords != '':
                prompt += " with these keywords: "+keywords
            if emoji:
                prompt += " and include some emojies"
            
            response = openai.ChatCompletion.create(
                max_tokens=1000,
                temperature=0.9,
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "You are my assistant who writes youtube video descriptions."},
                        {"role": "user", "content": prompt}
                    ],
                n=3,
                )
            # decrease user's tokens
            user.token_amount -= 5
            db.session.commit()

            json_data={}
            json_data['1'] = response['choices'][0]['message']['content']
            json_data['2'] = response['choices'][1]['message']['content']
            json_data['3'] = response['choices'][2]['message']['content']
            json_data = jsonify(json_data)
            return json_data
        except Exception as e:
            print(e)

            #db.session.rollback()
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

