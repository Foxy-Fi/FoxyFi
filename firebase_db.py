import pyrebase
import requests
import json
import pandas as pd
from datetime import date, datetime
import dash_bootstrap_components as dbc

# ADD YOUR FIREBASE KEY CONFIGURATION HERE
firebaseConfig = {
    'apiKey': '',
    'authDomain': '',
    'projectId': '',
    'storageBucket': '',
    'messagingSenderId': '',
    'appId': '',
    'measurementId': '',
    'databaseURL': ''
}


# Function to always initialize DB connection and return auth and db for usage
def initialize_firebase_db():
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
    return auth, db


def sign_up(db_init, session):
    if session['pwd'] == session['conf_pwd']:
        try:
            db_init.auth.create_user_with_email_and_password(session['email'], session['pwd'])
            return True
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            error = error.replace('_', ' ')
            return 'ERROR: {}'.format(error)
    else:
        return 'pwd mismatch'


def sign_in(db_init, session):
    try:
        auth_token = db_init.auth.sign_in_with_email_and_password(session['email'], session['pwd'])
        session['auth_token'] = auth_token
        session['idToken'] = auth_token['idToken']
        session['pwd'] = None
        return True
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error = error.replace('_', ' ')
        return 'ERROR: {}'.format(error)


# RESET USER CLASS DATA + SESSION POP
def reset_user_session(session):
    [session.pop(key) for key in list(session.keys())]


def reset_add_trade_class(session):
    session['trade_type'] = None
    session['symbol'] = None
    session['qty'] = None
    session['stock_price'] = None
    session['strikes'] = []
    session['expiration'] = None
    session['price'] = None
    session['comment'] = None
    session['legs'] = 0


def check_if_user_exists(db_init, session):
    user = db_init.db.child("users").order_by_key().equal_to(session['username']).get()
    if not user.val():
        return True
    else:
        return False


def get_username_email(db_init, session):
    data = db_init.db.child("users").order_by_key().equal_to(str(session['login_user']).lower()).get().val()
    if data:
        df = pd.DataFrame(data, columns=data.keys()).T
        email = df['email'][0]
        session['email'] = email
        return True
    else:
        return False


def check_if_email_verified(db_init, session):
    check = db_init.auth.get_account_info(session['idToken'])['users'][0]['emailVerified']
    return check


def check_last_login(db_init, session):
    last_login = db_init.auth.get_account_info(session['idToken'])['users'][0]['lastRefreshAt']
    return last_login


def reset_password(db_init, session):
    try:
        db_init.auth.send_password_reset_email(session['email'])
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error = error.replace('_', ' ')
        print('ERROR: {}'.format(error))


def refresh_idToken(db_init, session):
    token = db_init.auth.refresh(session['auth_token']['refreshToken'])
    session['idToken'] = token['idToken']


def add_new_user(db_init, session):
    new_user = {
        'badges': '',
        'bio': '',
        'losses': 0,
        'premium_overall': 0,
        'premium_ytd': 0,
        'ranking': 0,
        'score': 0,
        'username': session['login_user'],
        'email': session['email'],
        'wins': 0,
        'number_of_trades': 0,
        'access_type': 'foxy',
        'last_login': 'DATE HERE',
        'login_streak': 1
    }

    try:
        db_init.db.child('users').child(session['login_user']).set(new_user, session['idToken'])
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error = error.replace('_', ' ')
        print('ERROR: {}'.format(error))


def get_number_of_trades(db_init, session):
    try:
        user_data = db_init.db.child("users").order_by_key().equal_to(session['username']).get().val()
        number_of_trades = user_data[session['username']]['number_of_trades']
        return number_of_trades
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error = error.replace('_', ' ')
        print(error)
        print('error from user profile db loader')
        return 0


def add_new_trade(db_init, session):
    refresh_idToken(db_init, session)
    update_user_access_badge(db_init, session)

    user_score = db_init.db.child("users").child(session['username']).child('score').get().val() + 100
    db_init.db.child('users').child(session['username']).update({'score': user_score}, session['idToken'])

    eligible_cb_trades = ['CASH SECURED PUT', 'SHORT NAKED PUT']
    number_of_trades = int(get_number_of_trades(db_init, session)) + 1
    total_num_trades = db_init.db.child("total_num_trades").get().val() + 1
    if session['price'] is None:
        cost_basis = float(session['qty']) * float(session['stock_price'])
    elif session['trade_type'] in eligible_cb_trades: #THIS WILL REQUIRE ADDITIONAL LOGIC CUZ OF NEW STRIKES FORMAT
        cost_basis = session['strikes'][1:]
        cost_basis = cost_basis[:-1]
        cost_basis = float(cost_basis)
        cost_basis = float(cost_basis) - float(session['price'])
    else:
        cost_basis = 'N/A'
    try:
        new_trade_data = {
            'input_date': datetime.now().strftime("%d/%b/%y, %H:%M:%S"),
            'trader': session['username'],
            'trade_type': session['trade_type'],
            'symbol': session['symbol'],
            'qty': session['qty'],
            'stock_price': session['stock_price'],
            'strikes': session['strikes'],
            'expiration': session['expiration'],
            'price': session['price'],
            'comment': session['comment'],
            'closing_price': 0,
            'cost_basis': cost_basis,
            'pnl': 0,
            'closing_comment': '',
            'closing_date': 'N/A',
            'avg_trade_length': 0,
        }
        db_init.db.child('users').child(session['username']).child('trades').push(new_trade_data, session['idToken'])
        db_init.db.child('all_trades').push(new_trade_data, session['idToken'])
        db_init.db.child('users').child(session['username']).update({'number_of_trades': number_of_trades}, session['idToken'])
        db_init.db.update({'total_num_trades': total_num_trades}, session['idToken'])
    except Exception as e:
        print(e)


def get_user_data(db_init, username):
    try:
        list_trade_lenghts = list(db_init.db.child("users").child(str(username)).child('avg_trade_length').get().val().values())
        avg_trade_length = int(sum(list_trade_lenghts) / len(list_trade_lenghts))
    except:
        avg_trade_length = 0
    try:
        user_data = db_init.db.child("users").order_by_key().equal_to(username).get().val()
        if user_data:
            if 'followers' in user_data[username]:
                followers = len(user_data[username]['followers'])
                follower_list = 'FOLLOWERS: ' + ', '.join(user_data[username]['followers'].values())
            else:
                followers = 0
                follower_list = []
            if 'following' in user_data[username]:
                following = len(user_data[username]['following'])
                following_list = 'FOLLOWING: ' + ', '.join(user_data[username]['following'].values())
            else:
                following = 0
                following_list = []

            user = {
                'access_type': user_data[username]['access_type'],
                'username': user_data[username]['username'],
                'badges': user_data[username]['badges'],
                'bio': user_data[username]['bio'],
                'followers': followers,
                'followers_list': follower_list,
                'following': following,
                'following_list': following_list,
                'wins': user_data[username]['wins'],
                'losses': user_data[username]['losses'],
                'avg_trade_length': avg_trade_length,
                'premium_overall': user_data[username]['premium_overall'],
                'premium_ytd': user_data[username]['premium_ytd'],
                'score': user_data[username]['score'],
                'ranking': user_data[username]['ranking'],
                'number_of_trades': user_data[username]['number_of_trades']
            }
            return user
        else:
            return {}
    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error = error.replace('_', ' ')
        print(error)
        print('error from user profile db loader')
        return None


def all_trades_data(db_init):
    try:
        all_trades = db_init.db.child('all_trades').get().val()
        if not all_trades is None:
            df = pd.DataFrame(all_trades, columns=all_trades.keys()).T
            df['input_date'] = pd.to_datetime(df['input_date'])
            df = df.sort_values(by=['input_date'], ascending=False)
            df['input_date'] = df['input_date'].dt.strftime('%d-%b-%y %H:%M:%S')
            df = df.rename({'closing_price': 'CLOSE',
                            'comment': 'NOTES',
                            'expiration': 'EXPIRATION',
                            'input_date': 'INPUT DATE',
                            'cost_basis': 'C.B.',
                            'pnl': 'PnL',
                            'price': 'OPEN',
                            'qty': 'QTY',
                            'strikes': 'STRIKES',
                            'symbol': 'SYMBOL',
                            'trade_type': 'TRADE',
                            'trader': 'USERNAME',
                            'stock_price': 'STOCK PRICE',
                            'closing_date': 'CLOSE DATE',
                            'closing_comment': 'CLOSE COMMENT',
                            'avg_trade_length': 'TRADE LENGTH',
                            'user_comments': 'USER COMMENTS'}, axis=1)
            df = df.head(200)
            try:
                df.loc[df['OPEN'].isna(), 'OPEN'] = df['STOCK PRICE']
            except:
                pass
            try:
                df = df[['USERNAME',
                         'INPUT DATE',
                         'TRADE',
                         'SYMBOL',
                         'QTY',
                         'EXPIRATION',
                         'STRIKES',
                         'OPEN',
                         'CLOSE',
                         'C.B.',
                         'PnL',
                         'NOTES',
                         'CLOSE DATE',
                         'CLOSE COMMENT',
                         'TRADE LENGTH',
                         'USER COMMENTS']]
            except Exception as e:
                print(e)
                df = df[['USERNAME',
                         'INPUT DATE',
                         'TRADE',
                         'SYMBOL',
                         'QTY',
                         'EXPIRATION',
                         'STRIKES',
                         'OPEN',
                         'CLOSE',
                         'C.B.',
                         'PnL',
                         'NOTES',
                         'CLOSE DATE',
                         'CLOSE COMMENT',
                         'TRADE LENGTH']]
            return df
        else:
            cols = {'USERNAME': [], 'INPUT DATE': [], 'TRADE': [], 'SYMBOL': [], 'QTY': [], 'EXPIRATION': [], 'STRIKES': [],
                    'OPEN': [], 'CLOSE': [], 'C.B.': [], 'PnL': [], 'NOTES': [], 'CLOSE DATE': [], 'CLOSE COMMENT': [], 'TRADE LENGTH': []}
            df = pd.DataFrame(data=cols)
            return df

    except requests.HTTPError as e:
        error_json = e.args[1]
        error = json.loads(error_json)['error']['message']
        error = error.replace('_', ' ')
        print(error)
        print('error from user trades dataframe db loader')
        return pd.Dataframe()


def update_user_data(db_init, session, user_datapoint, new_value):
    db_init.db.child('users').child(session['username']).update({user_datapoint: new_value}, session['idToken'])


def update_user_win_loss_number(db_init, session, pnl):
    user_wins =  db_init.db.child("users").child(session['username']).child('wins').get().val()
    user_losses = db_init.db.child("users").child(session['username']).child('losses').get().val()
    user_premium_overall = db_init.db.child("users").child(session['username']).child('premium_overall').get().val() + float(pnl)
    user_premium_ytd = db_init.db.child("users").child(session['username']).child('premium_ytd').get().val() + float(pnl)
    user_score = db_init.db.child("users").child(session['username']).child('score').get().val()
    if float(pnl) > 0:
        user_wins += 1
        user_score = int(user_score) + 250
        db_init.db.child('users').child(session['username']).update({'wins': user_wins}, session['idToken'])
        db_init.db.child('users').child(session['username']).update({'score': user_score}, session['idToken'])
    elif float(pnl) < 0:
        user_losses += 1
        db_init.db.child('users').child(session['username']).update({'losses': user_losses}, session['idToken'])
    db_init.db.child('users').child(session['username']).update({'premium_overall': user_premium_overall}, session['idToken'])
    db_init.db.child('users').child(session['username']).update({'premium_ytd': user_premium_ytd}, session['idToken'])


def update_trade_data(db_init, session, tradeid, trade_datapoint, new_value):
    db_init.db.child('all_trades').child(tradeid).update({trade_datapoint: new_value}, session['idToken'])


def update_pnl_stats(db_init, session, new_value):
    if float(new_value) > 0:
        total_profit = round(float(db_init.db.child("overall_profit").get().val()) + float(new_value), 2)
        db_init.db.update({'overall_profit': total_profit}, session['idToken'])
    elif float(new_value) < 0:
        total_loss = round(float(db_init.db.child("overall_loss").get().val()) + float(new_value), 2)
        db_init.db.update({'overall_loss': total_loss}, session['idToken'])

    total_pnl = round(float(db_init.db.child("overall_pnl").get().val()) + float(new_value), 2)
    db_init.db.update({'overall_pnl': total_pnl}, session['idToken'])


def get_user_trades(db_init, username):
    user_trades = db_init.db.child("users").child(username).child('trades').get().val()
    df = pd.DataFrame(user_trades, columns=user_trades.keys()).T
    return df


def update_user_access_badge(db_init, session):
    user_access = db_init.db.child("users").child(session['username']).child('access_type').get().val()
    user_badges = db_init.db.child("users").child(session['username']).child('badges').get().val()

    if user_access == 'foxy':
        if '🦊' not in user_badges:
            user_badges = user_badges + '🦊'
            db_init.db.child('users').child(session['username']).update({'badges': user_badges}, session['idToken'])


def get_foxyfi_stats(db_init):
    users_data = db_init.db.child("users").get().val()
    total_num_trades = db_init.db.child("total_num_trades").get().val()
    total_num_patreons = db_init.db.child("patreons").get().val()
    df = pd.DataFrame(users_data, columns=users_data.keys()).T
    number_of_users = {'number_of_users': len(df.index),
                       'total_num_trades': total_num_trades,
                       'patreons': total_num_patreons}
    return number_of_users


def get_foxyfi_pnl_stats(db_init):
    total_profit = round(float(db_init.db.child("overall_profit").get().val()), 2)
    total_loss = round(float(db_init.db.child("overall_loss").get().val()), 2)
    total_pnl = round(float(db_init.db.child("overall_pnl").get().val()), 2)
    pnl_stats = {
        'total_profit': total_profit,
        'total_loss': total_loss,
        'total_pnl': total_pnl
    }
    return pnl_stats


def follow_user(db_init, user, session):
    link = '/user=' + user
    try:
        try:
            users_followers = list(db_init.db.child("users").child(user).child('followers').get().val().values())
        except:
            users_followers = []
        if str(session['username']) not in users_followers and str(session['username']) != str(user):
            db_init.db.child('users').child(str(user)).child('followers').set({str(session['username']): str(session['username'])}, session['idToken'])
            db_init.db.child('users').child(str(session['username'])).child('following').set({str(user): str(user)}, session['idToken'])
            return dbc.Alert(f"You are now following {user}!", color='success'), dbc.Button('Close', className='rounded-pill', id='message_dynamic_close', href=link, external_link=True)
        else:
            return dbc.Alert(f"Oops! You are not able to follow {user}!", color='danger'), dbc.Button('Close', className='rounded-pill', id='message_dynamic_close', href=link, external_link=True)
    except Exception as e:
        return dbc.Alert(f"Oops! Something went wrong!\nPlease relog!", color='danger'), dbc.Button('Close', className='rounded-pill', id='message_dynamic_close', href=link, external_link=True)


def unfollow_user(db_init, user, session):
    link = '/user=' + user
    try:
        try:
            users_followers = list(db_init.db.child("users").child(user).child('followers').get().val().values())
        except:
            users_followers = []
        if str(session['username']) in users_followers and str(session['username']) != str(user):
            db_init.db.child("users").child(str(user)).child('followers').child(str(session['username'])).remove(session['idToken'])
            db_init.db.child("users").child(str(session['username'])).child('following').child(str(user)).remove(session['idToken'])
            return dbc.Alert(f"You have unfollowed {user}!", color='warning'), dbc.Button('Close', className='rounded-pill', id='message_dynamic_close', href=link, external_link=True)
        else:
            return dbc.Alert(f"Oops! You are not able to follow {user}!", color='danger'), dbc.Button('Close', className='rounded-pill', id='message_dynamic_close', href=link, external_link=True)
    except Exception as e:
        return dbc.Alert(f"Oops! Something went wrong!\nPlease relog!", color='danger'), dbc.Button('Close', className='rounded-pill', id='message_dynamic_close', href=link, external_link=True)
