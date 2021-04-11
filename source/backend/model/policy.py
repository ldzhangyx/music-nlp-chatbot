import sys
sys.path.insert(0, r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot")

from database import database_op as op
from source.backend.model.lyrics.generate import generate_lyrics_wrapper
from source.backend.model.melody_chord.generate import generate_music_warpper

database_url = r"C:\Users\ldzha\OneDrive\AIM\music-nlp-chatbot\log.sqlite3"

actions = {
    1: 'waiting for more information', # not available
    2: 'generate melody with full info',
    3: 'require music keywords',
    4: 'revise melody',
    5: 'generate lyrics with full info',
    6: 'require keywords',
    7: 'require genre',
    8: 'revise lyrics',
    9: 'error'
}

def action(current_state, keywords, session_id):

    # check the table
    creation_table = {'genre': "",
                      'keywords': "",
                      'note_num': None,
                      'note_var': None,
                      'rhyrhm_var': None,
                      'melody_generated': None,
                      'lyrics_generated': None
                      }
    [_, creation_table['note_num'], creation_table['note_var'], \
        creation_table['rhythm_var'], creation_table['genre'], \
        creation_table['keyword'], creation_table['melody_generated'], \
        creation_table['lyrics_generated']] = op.check_table(database_url, 'CREATION', session_id)

    # fill the table if keywords are not null
    if current_state == 1: # generate melody
        keyword = keywords['keywords_music']
        if len(keyword) > 0: # success
            music_path = generate_music_warpper(keyword) #
            # op.creation_logging_update(database_url, session_id, '')
            return_action = [actions[2], music_path]
        else: # fail
            return_action = actions[3]
    elif current_state == 2: # revise melody
        keyword = keywords['keywords_music']
        if len(keyword) > 0: # success
            music_path = generate_music_warpper(keyword)
            return_action = actions[4]
    elif current_state == 3: # generate lyrics
        creation_table['keywords'] = keyword = keywords['keywords_lyrics']
        creation_table['genre'] = genre = keywords['genre_lyrics']
        if creation_table['keywords'] != "" and creation_table['genre'] != "":
            lyrics = generate_lyrics_wrapper(genre, keyword)
            op.creation_logging_update(database_url, session_id, 'keyword', creation_table['keywords'])
            op.creation_logging_update(database_url, session_id, 'genre', creation_table['genre'])
            return_action = [actions[5], lyrics]
        elif creation_table['keywords'] == "":
            return_action = actions[6]
        else:
            return_action = actions[7]
    elif current_state == 4: # resive lyrics
        creation_table['keywords'] = keyword = keywords['keywords_lyrics']
        creation_table['genre'] = genre = keywords['genre_lyrics']
        lyrics = generate_lyrics_wrapper(genre, keyword)
        op.creation_logging_update(database_url, session_id, 'keyword', creation_table['keywords'])
        op.creation_logging_update(database_url, session_id, 'genre', creation_table['genre'])
        return_action = [actions[8], lyrics]
    else:
        return_action = actions[9]
    # generate or require more messages (not available)

    return return_action


def return_message(return_action):
    messages = list()
    info = ""
    if isinstance(return_action, list):
        info = return_action[1]
        return_action = return_action[0]
    if return_action == 1:
        messages.append('We need more information.')
    if return_action == 2:
        messages.append('We have succeed to generate a piece of music.')
        messages.append('Player has been updated!')
    if return_action == 3:
        messages.append('Okay.')
        messages.append('It seems that we need some descriptions for the melody.')
    if return_action == 4:
        messages.append('Succeed!')
        messages.append('We have just revised the melody.')
    if return_action == 5:
        messages.append('Great. How about the lyrics below:')
        messages.appand(info)
        info = ""
    if return_action == 6:
        messages.append('I think we need some information about the keywords of the lyrics.')
    if return_action == 7:
        messages.append('How is your opinion about the genre of the lyrics?')
    if return_action == 8:
        messages.append('Okay. We have revised the lyrics for you:')
        messages.append(info)
        info = ""
    if return_action == 9:
        messages.append('Sorry, but some internal error happens.')
    # pass
    return " * ".join(messages), info
