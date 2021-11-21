import hashlib
from time import time
import random
import pandas as pd

# (private) constants
__PASSWORDS_TABLE_PATH = "./user_data/passwords_table.csv"
__MESSAGES_TABLE_PATH = "./user_data/messages_table.csv"



def create_user(username, password):
    df = __get_passwords_table()
    row = pd.DataFrame([(username, hash_password(password), 0)], columns=["username", "hashed_password", "last_login_time"]) 
    df = df.append(row)
    __store_passwords_table(df)


def get_passhash(username):
    df = __get_passwords_table()
    return df[df.username==username].hashed_password.to_list()[0]


def set_password(username, password):
    pass



# TODO: retrieve sender and timestamp info, not just content, maybe make a Message class
def get_users_inbox(receiver):
    df = __get_messages_table()
    return df[df.receiver==receiver].message.to_list()



def refresh_last_login(username):
    df = __get_passwords_table()
    df.loc[df.username == username, 'last_login_time'] = time()
    __store_passwords_table(df)


def get_last_login(username):
    df = __get_passwords_table()
    return float(df.set_index("username").at[username, "last_login_time"])



def send_message(sender, receiver, message, time):

    # TODO: error of some sort
    if not user_exists(sender) or not user_exists(receiver):
        return 

    # TODO: redirect user to login
    if not session_expired(sender):
        return False

    # append new message to table    
    df = __get_messages_table()    
    row = pd.DataFrame( [(time, sender, receiver, message)] , columns=["timestamp", "sender", "receiver", "message"])
    df = df.append(row)
    __store_messages_table(df)
    
    return True




def user_exists(username):
    """
    Checks if a username is taken.
    """

    df = __get_passwords_table()
    return (df.username==username).sum() != 0 


def hash_password(password):
    h = hashlib.sha1(password.encode("utf-8")).hexdigest()
    return h



# TODO: improve rule to determine if user is logged in
def session_expired(username):

    # in seconds
    last_time = get_last_login(username)
    current_time = time()

    # 5 minutes
    if current_time - last_time < 300:
        return True

    return False    



def generate_session_id():
    return random.randint(0 , 1000000000)


def set_session_id(username, new_session_id):

    """
    Sets a user's new session id.
    """

    df = __get_passwords_table()
    df.loc[df.username == username, 'session_id'] = new_session_id
    __store_passwords_table(df)



def get_session_id(username):
    """
    Get a user's current session id.
    """

    df = __get_passwords_table()
    return df.loc[df.username == username, 'session_id'].to_list()[0]




# ----------PRIVATE FUNCTIONS-------------:


def __get_passwords_table():

    """
    Load the passwords table.
    """
    try:
        # read the table from a csv
        return pd.read_csv(__PASSWORDS_TABLE_PATH)
    except:
        # initialize a new empty passwords table if file not found
        return __create_passwords_table()



def __create_passwords_table():
    return pd.DataFrame([], columns=["username", "hashed_password", "last_login_time", "session_id"])



# TODO: add RSA encryption
def __create_messages_table():
    return pd.DataFrame([], columns=["timestamp","sender", "receiver", "message"])


def __get_messages_table():
      try:
        # read the table from a csv
        return pd.read_csv(__MESSAGES_TABLE_PATH)
      except:
        # initialize a new empty messages table if file not found
        return __create_messages_table()



def __store_passwords_table(df):
    """
    Store the passwords table.
    Arguments: passwords dataframe.
    """
    df.to_csv(__PASSWORDS_TABLE_PATH, index=False)


def __store_messages_table(df):
    df.to_csv(__MESSAGES_TABLE_PATH, index=False)


