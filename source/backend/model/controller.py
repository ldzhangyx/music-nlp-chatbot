import sys
sys.path.insert(0, r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot")

from database import database_op as op
from source.backend.model import intention_analysis
import json
from . import keyword_extractor
from . import policy
import yaml

import json
from django.http import JsonResponse

# global yaml_data
# with open(r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\settings.yaml",'r') as f:
#     yaml_data = yaml.load(f)

# database_url = yaml_data['database_url']

global database_url
database_url = r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\log.sqlite3"

def controller(post_json):
    post_json = json.loads(post_json)
    # TODO: 是否考虑常驻？这与上下文密切相关
    session_id = post_json['id']
    timestamp = post_json['timestamp']
    message = post_json['content']


    # 日志增加表项
    op.message_logging(database_url, session_id, timestamp, message, is_user=True)
    op.creation_logging_new(database_url, session_id)

    # 意图分析 NLU
    intention = intention_analysis.intention_analysis_bag_of_words(message)
    keywords_music = keyword_extractor.keyword_extractor(message)
    genres_lyrics, keywords_lyrics = keyword_extractor.keyword_extractor_lyrics(message)
    keywords = {
        'keywords_music': keywords_music,
        'genres_lyrics': genres_lyrics,
        'keywords_lyrics': keywords_lyrics
    }

    # 状态转移 DST
    # current state
    current_state = op.check_table(database_url, 'CREATION', session_id, 'state') # check table
    current_state = intention_analysis.state_transfer(intention, keywords, current_state)
    op.creation_logging_update(database_url, session_id, 'state', current_state)

    # 模型计算 POL
    return_action = policy.action(current_state, keywords, session_id)

    # 生成回复 NLG
    return_message, audio_path = policy.return_message(return_action)

    # 日志增加表项
    op.message_logging(database_url, session_id, timestamp, return_message, is_user=False)

    # 回复
    return JsonResponse({
        'message': return_message,
        'status': current_state,
        'audio_path': audio_path
    })
