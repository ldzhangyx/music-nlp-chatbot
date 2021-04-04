import sys
sys.path.insert(0, r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot")

from database import database_op as op
from source.backend.model import intention_analysis
import json
import keyword_extractor
import policy
import yaml

# global yaml_data
# with open(r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\settings.yaml",'r') as f:
#     yaml_data = yaml.load(f)

# database_url = yaml_data['database_url']

global database_url
database_url = r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\log.sqlite3"

global current_state

def controller(post_json):
    post_json = json.loads(post_json)
    # TODO: 是否考虑常驻？这与上下文密切相关
    session_id = post_json['id']
    timestamp = post_json['timestamp']
    message = post_json['content']

    # 日志增加表项
    op.message_logging(database_url, session_id, message, timestamp, is_user = True)
    # op.creation_table_logging('log.sqlite3', session_id, )

    # 意图分析
    if(len(message) > 50): # audio blob文件
        # audio detection?
        intention = "sound detected."
    else:
        intention = intention_analysis.intention_analysis_bag_of_words(message)
        keywords = keyword_extractor.keyword_extractor(message)

    # 状态转移
    # current state
    transfer_state = intention_analysis.state_transfer(intention)

    # 模型计算
    return_action, return_policy = policy.action(transfer_state, keywords)

    # 生成回复
    return_message = policy.return_message(return_action)

    # 日志增加表项
    op.message_logging(database_url, session_id, return_message, timestamp, is_user = False)
    # op.creation_table_logging('log.sqlite3', session_id, )

    # 回复
    return return_message

