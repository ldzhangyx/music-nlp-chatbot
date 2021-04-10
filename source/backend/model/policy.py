import sys
sys.path.insert(0, r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot")

from database import database_op as op

actions = {
    1: 'waiting for more information', # not available
    2: 'generate melody with full info',
    3: 'generate melody with part info',
    4: 'revise melody',
    5: 'generate lyrics with full info',
    6: 'generate lyrics with part info',
    7: 'revise lyrics'
}

def action(current_state, keywords, session_id):


    # check the table


    # fill the table if keywords are not null

    # generate or require more messages (not available)

    return return_action

def return_message(return_action):
    return actions[1]
    # pass

