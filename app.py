# -*- coding: utf-8 -*-
from layouts.html_layouts import *
from layouts.add_trade_modal_dynamic_layout import *
from layouts.modals import *
from classes import *
from firebase_db import *
from dataframe import *

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from flask import session
from datetime import datetime, timedelta
import json

external_stylesheets = [
    'https://use.fontawesome.com/releases/v5.15.4/css/all.css',
    'https://use.fontawesome.com/releases/v5.15.4/css/v4-shims.css',
    dbc.themes.SLATE
]

# INITIATE CLASSES
db_init = FirebaseDB()

app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets,
                meta_tags=
                    [
                        {
                            'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'
                        }
                    ]
                )
server = app.server
app.css.config.serve_locally=True
app.server.secret_key = b'' # create your own secret key (randomized string of characters)
app.server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=55)
app.title = 'FoxyFi'
app.layout = html.Div(
    [
        dcc.Store(id='memory'),
        dcc.Location(id='url', refresh=False),
        html.Link(
            rel='stylesheet',
            href='/static/stylesheet.css'
        ),

        html.Div(
            [
                # NAV BAR
                html.Div(
                    nav_bar()
                ),
                # HEADER
                dbc.Row(
                    header_content(),
                style={'margin-top': '-0.7rem'}),
                html.Br(),

                # MAIN BODY
                dbc.Row(
                    [
                        # LEFT COLUMN
                        dbc.Col(
                            [
                                dbc.Card(
                                    # html.Div(main_site_stats(get_number_of_users(db_init)), id='website_main_stats'),
                                    dbc.Col(html.A(html.Img(src=app.get_asset_url('logo.png'),
                                                     className='image_logo'), href='/'),
                                            style={'text-align': 'center'}),
                                    color='#1e222d'
                                ),
                                html.Br(),
                                dbc.Card(
                                    html.Div(id='user_profile_section'),
                                    id='user_profile_card',
                                    className='',
                                    color='#1e222d'
                                )
                            ],
                            xs=12, sm=12, md=12, lg=3, xl=3,
                        ),

                        dbc.Col(
                            [
                                html.Div(id='main_content')
                            ],
                            xs=12, sm=12, md=12, lg=9, xl=9
                        ),
                        html.Div(id='table_row')
                    ]
                ),
            ],
        ),
        login_modal(),
        signup_modal(),
        pwd_reset_modal(),
        reset_pwd_conf_modal(),
        logout_conf_modal(),
        new_trade_modal(),
        add_trade_conf_modal(),
        add_trade_fail_modal(),
        message_login_modal_success(),
        message_siginup_modal_success(),
        message_modal_fail(),
        message_modal_dynamic(),
        close_trade_modal(),
        edit_user_modal(),
        comment_modal()
    ],
    id='parent_id',
    className='mobile_margin'
)


# CALLBACK CONTROLLING THE OPENING AND CLOSING OF THE LOGIN MODAL
@app.callback(
    [Output('login_modal', 'is_open'),
     Output('message_login_success_text', 'children'),
     Output('message_login_modal_success', 'is_open'),
     Output('login_alert', 'children')],
    [Input('login_btn', 'n_clicks'),
     Input('login_submit', 'n_clicks')],
    [State('login_email', 'value'),
     State('login_password', 'value')],
)
def toggle_login_modal(n1, n2, email, password):
    if n1:
        return True, no_update, no_update, no_update

    elif n2:
        if email is None or password is None:
            empty_field_alert = dbc.Alert('Please make sure all fields are filled in before signing up!', color="danger", duration=4000)
            return True, no_update, False, empty_field_alert
        else:
            session['login_user'] = str(email).lower().replace("\t", "").replace(" ", "")
            session['pwd'] = str(password).replace("\t", "").replace(" ", "")
            session['username'] = str(session['login_user']).lower()

            user_exists = get_username_email(db_init, session)

            if user_exists:
                sign_in_return = sign_in(db_init, session)
                if sign_in_return != 'ERROR: INVALID PASSWORD' and sign_in_return != 'ERROR: TOO MANY ATTEMPTS TRY LATER : Access to this account has been temporarily disabled due to many failed login attempts. You can immediately restore it by resetting your password or you can try again later.' and sign_in_return:
                    session['username'] = str(session['login_user']).lower()
                    reset_add_trade_class(session)
                    email_verification = check_if_email_verified(db_init, session)
                    if not email_verification:
                        reset_user_session(session)
                        msg_content = dbc.Alert([html.P('Sorry!'),
                                       html.Br(),
                                       html.P('You must verify your e-mail before signing in!')],
                                  color='danger')
                        return False, msg_content, True, no_update
                    else:
                        msg_content = dbc.Alert('Welcome back {}!'.format(session['username']), color='success')
                        return False, msg_content, True, no_update
                elif sign_in_return == 'ERROR: INVALID PASSWORD':
                    reset_user_session(session)
                    msg_content = dbc.Alert('Whoops! Wrong password! Please try again!', color='danger')
                    return False, msg_content, True, no_update
                elif sign_in_return == 'ERROR: TOO MANY ATTEMPTS TRY LATER : Access to this account has been temporarily disabled due to many failed login attempts. You can immediately restore it by resetting your password or you can try again later.':
                    reset_user_session(session)
                    msg_content = dbc.Alert('Whoops! You tried too many attempts! Access to this account has been temporarily disabled due to many failed login attempts. You can immediately restore it by resetting your password or you can try again later.', color='danger')
                    return False, msg_content, True, no_update
            else:
                reset_user_session(session)
                msg_content = dbc.Alert('Username not recognized!', color='danger')
                return False, msg_content, True, no_update


# CALLBACK CONTROLLING THE OPENING/CLOSE OF THE SIGN UP MODAL
@app.callback(
    [Output('signup_modal', 'is_open'),
     Output('message_signup_success_text', 'children'),
     Output('message_signup_modal_success', 'is_open'),
     Output('signup_alert', 'children')],
    [Input('signup_btn', 'n_clicks'),
     Input('signup_submit', 'n_clicks')],
    [State('signup_email', 'value'),
     State('signup_username', 'value'),
     State('signup_password', 'value'),
     State('confirm_signup_password', 'value')]
)
def toggle_signup_modal(n1, n2, email, username, password, password_confirm):
    if n1:
        return True, no_update, no_update, no_update

    elif n2:
        if email is None or username is None or password is None or password_confirm is None:
            empty_field_alert = dbc.Alert('Please make sure all fields are filled in before signing up!', color="danger", duration=4000)
            return True, no_update, False, empty_field_alert
        else:
            session['email'] = str(email).lower().replace("\t", "").replace(" ", "")
            session['login_user'] = str(username).lower().replace("\t", "").replace(" ", "")
            session['pwd'] = str(password).replace("\t", "").replace(" ", "")
            session['conf_pwd'] = str(password_confirm).replace("\t", "").replace(" ", "")
            session['username'] = str(session['login_user']).lower()

            non_eligible_usernames = ['foxyfi', 'foxifi', 'foxify', 'foxifi',
                                      'f0xyfi', 'f0xyfy', 'f0x1f1', 'f0x1fy',
                                      'f0x1fi', 'fox1f1', 'fox1fi', 'foxif1']
            if check_if_user_exists(db_init, session) is True and not any(
                    str(session['login_user']).lower() in unallowed_username for unallowed_username in non_eligible_usernames):
                singup_return = sign_up(db_init, session)
            else:
                reset_user_session(session)
                msg_content = dbc.Alert('Username already taken, chose another one!', color='danger')
                return False, msg_content, True, no_update
            if singup_return != 'ERROR: WEAK PASSWORD : Password should be at least 6 characters' and singup_return:
                signin_return = sign_in(db_init, session)
                db_init.auth.send_email_verification(session['idToken'])
                add_new_user(db_init, session)
                if signin_return is True:
                    msg_content = dbc.Alert([html.P('Welcome and thanks for signing up {}!'.format(session['login_user'])),
                                          html.Br(),
                                          html.P('Your username has been temporarily reserved for you!'),
                                          html.Br(),
                                          html.P('Please verify your e-mail to finish your registration!')],
                                            color='success')
                    [session.pop(key) for key in list(session.keys())]
                    reset_user_session(session)
                    return False, msg_content, True, no_update
            elif singup_return == 'ERROR: WEAK PASSWORD : Password should be at least 6 characters':
                msg_content = dbc.Alert('ERROR: WEAK PASSWORD : Password should be at least 6 characters!', color='danger')
                return False, msg_content, True, no_update
            else:
                reset_user_session(session)
                msg_content = dbc.Alert('Whoops!..Something went wrong! Please try again!', color='danger')
                return False, msg_content, True, no_update


# CALLBACK CONTROLLING THE OPENING AND CLOSING OF THE RESET PASSWORD MODAL
@app.callback(
    Output('reset_pwd_modal', 'is_open'),
    [Input('url', 'pathname')]
)
def reset_pwd(pathname):
    if pathname == '/pwd-reset':
        return True
    else:
        return False


# CALLBACK FOR USER PWD RESET EMAIL DATA CLASS STORAGE
@app.callback(
    Output('reset_pwd_submit', 'children'),
    [Input('reset_pwd_email', 'value')]
)
def login_user_data(email):
    session['email'] = str(email).lower().replace("\t", "").replace(" ", "")
    return no_update


# CALLBACK CONTROLLING THE OPENING AND CLOSING OF THE RESET PASSWORD CONFIRMATION MODAL
@app.callback(
    Output('reset_pwd_conf_modal', 'is_open'),
    [Input('url', 'pathname')]
)
def reset_pwd(pathname):
    if pathname == '/pwd-reset-send':
        if not session['email'] is None:
            reset_password(db_init, session)
            reset_user_session(session)
            return True
        else:
            return False
    else:
        return False


# CALLBACK FOR THE ROUTING OF THE NAV BAR AND LOGIN/SIGN IN SECTION (incl. SESSION COOKIE CREATION UPON AUTH)
@app.callback(
    Output('url', 'pathname'),
    [Input(f'navitem_1', 'n_clicks'),
     Input(f'navitem_2', 'n_clicks'),
     Input(f'navitem_3', 'n_clicks'),
     Input(f'navitem_4', 'n_clicks'),
     Input(f'navitem_5', 'n_clicks'),
     Input(f'navitem_6', 'n_clicks'),
     # Input(f'navitem_7', 'n_clicks'),
     Input(f'navitem_8', 'n_clicks')],
)
def url_router(n1, n2, n3, n4, n5, n6, n8):
    paths = {
        'navitem_1': '/',
        'navitem_2': '/learning-centre',
        'navitem_3': '/ticker=spy',
        'navitem_4': '/FAQ',
        'navitem_5': '/statistics',
        'navitem_6': '/youtube',
        'navitem_7': '/patreon-discord',
        'navitem_8': '/contact',
        'navitem_9': '/buymeacoffee',
    }
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id in list(paths.keys()):
            return paths[button_id]
        else:
            return '/'


# CALLBACK FEEDING THE CONTENT TO THE HEADER (LOGIN /SIGN IN/ LOGOUT BUTTONS)
@app.callback(
    Output('login_signup_section', 'children'),
    [Input('url', 'pathname')]
)
def signup_buttons_output(pathname):
    if 'idToken' in session:
        return logout_header_buttons()
    else:
        return logon_header_buttons()


# CALLBACK CONTROLLING THE CONTENT OUTPUT TO THE MAIN SECTION OF THE PAGE
@app.callback(
    Output('main_content', 'children'),
    [Input('url', 'pathname')]
)
def main_content_output(pathname):
    path_content = {
        '/learning-centre': learning_page(),
        '/FAQ': faq_page(),
        '/youtube': youtube_page(),
        '/patreon-discord': patreon_page(),
        '/contact': contact_page(),
        # '/buymeacoffee': 'BUY ME A COFFEE LINK',
    }

    if 'idToken' in session:
        main_page = home_page_user(all_trades_data(db_init))
    else:
        main_page = home_page(all_trades_data(db_init))

    if pathname == '/':
        return main_page
    elif any(path in pathname for path in ['/user=', '/follow=', '/unfollow=']):
        user = pathname.replace(pathname.split('=')[0], "")[1:]
        if '💬 ' in str(user):
            user = str(user)[2:]
        return user_view(get_user_data(db_init, user), all_trades_data(db_init))
    elif any(path in pathname for path in ['/tradeid=', '/comment=']):
        if '/tradeid=' in pathname:
            tradeid = pathname.replace("/tradeid=", "")
        elif '/comment=' in pathname:
            tradeid = pathname.replace("/comment=", "")
        return trade_view(tradeid, all_trades_data(db_init))
    elif '/ticker=' in pathname:
        ticker = pathname.replace('/ticker=', '')
        return ticker_view(ticker, all_trades_data(db_init))
    elif '/close-trade=' in pathname:
        tradeid = pathname.replace("/close-trade=", "")
        return trade_view(tradeid, all_trades_data(db_init))
    elif '/edituser=' in pathname:
        return user_view(get_user_data(db_init, session['username']), all_trades_data(db_init))
    elif '/statistics' in pathname:
        return stats_view(get_foxyfi_stats(db_init), get_foxyfi_pnl_stats(db_init))
    else:
        for path, content in path_content.items():
            if pathname == path:
                return content
    return home_page(all_trades_data(db_init))


# CALLBACK CONTROLLING HOMEPAGE TAB CONTENT
@app.callback(
    Output('main_tab_content', 'children'),
    [Input('url', 'pathname'),
     Input('home_page_tabs', 'active_tab')]
)
def home_page_tab_content(pathname, active_tab):
    if pathname == '/':
        if active_tab == 'all_trades_tab':
            df = all_trades_data(db_init).head(40)
            return html.Div(data_frame(df), className='df_div')
        elif active_tab == 'my_trades_tab':
            df = all_trades_data(db_init)
            df = df.loc[df['USERNAME'] == session['username']]
            return html.Div(data_frame(df), className='df_div')
    else:
        return no_update


# CALLBACK CONTROLLING LEARNING PAGE TAB CONTENT
@app.callback(
    Output('learning_page_content', 'children'),
    [Input('url', 'pathname'),
     Input('learning_select', 'value')]
)
def learing_page_content(pathname, selection):
    if pathname == '/learning-centre':
        if selection in learning_content.keys():
            content_title = learning_content[selection]['title']
            content_text = learning_content[selection]['text']
        else:
            content_title = 'Comming SOON!'
            content_text = 'THE ENTIRELY DIFFERENT LEARNING SECTION'
        return container(content_title, content_text)
    else:
        return no_update


# CALLBACK CONTROLLING FAQ PAGE TAB CONTENT
@app.callback(
    Output('FAQ_page_content', 'children'),
    [Input('url', 'pathname'),
     Input('FAQ_select', 'value')]
)
def FAQ_page_content(pathname, selection):
    if pathname == '/FAQ':
        if selection in faq_content.keys():
            content_title = faq_content[selection]['title']
            content_text = faq_content[selection]['text']
        else:
            content_title = 'Comming SOON!'
            content_text = 'THE ENTIRELY DIFFERENT LEARNING SECTION'
        return container(content_title, content_text)
    else:
        return no_update


# CALLBACK CONTROLLING THE OPENING AND CLOSING OF THE LOGOUT CONFIRMATION MODAL (incl. SESSION COOKIE REMOVAL)
@app.callback(
    Output('logout_modal', 'is_open'),
    [Input('url', 'pathname')]
)
def logout_conf_modal(pathname):
    if pathname == '/logout':
        [session.pop(key) for key in list(session.keys())]
        reset_user_session(session)
        return True
    else:
        return False


# CALLBACK FEEDING THE CONTENT OUTPUT TO THE USER SECTION (LOGGED IN AND LOGGED OUT)
@app.callback(
    Output('user_profile_section', 'children'),
    [Input('url', 'pathname')],
)
def user_section_output(pathname):
    if 'idToken' in session:
        return user_profile(get_user_data(db_init, session['username']))
    else:
        reset_add_trade_class(session)
        return user_container_not_logged()


# CALLBACK CONTROLLING OPENING AND CLOSING OF NEW TRADE MODAL
@app.callback(
     Output('newtrade_modal', 'is_open'),
     [Input('url', 'pathname')],
     [State('newtrade_modal', 'is_open')]
)
def add_trade_modal(pathname, is_open):
    if pathname in ['/', '/add-trade-submit']:
        return False
    elif pathname == '/add-trade-1':
        return not is_open
    else:
        return is_open


# CALLBACK FEEDING CONTENT OUTPUTS TO NEW TRADE MODAL
@app.callback(
    [Output('newtrade_header', 'children'),
     Output('new_trade_inputs', 'children'),
     Output('new_trade_buttons', 'children'),
     Output('trade_preview', 'children')],
    [Input('url', 'pathname')],
)
def add_trade_modal(pathname):
    if pathname == '/add-trade-1':
        title = 'TRADE TYPE'
        return add_trade_back(pathname, title), trade_type(), stage_1_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-2':
        title = 'TICKER'
        return add_trade_back(pathname, title), add_trade_symbol(), stage_2_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-3':
        title = 'QUANTITY'
        return add_trade_back(pathname, title), add_trade_qty(), stage_3_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-4':
        if session['trade_type'] in ['LONG POSITION', 'SHORT POSITION']:
            title = 'STOCK PRICE'
            return add_trade_back(pathname, title), add_stock_price(session), stage_stocks_buttons(), trade_preview(pathname, session)
        else:
            title = 'STRIKES'
            return add_trade_back(pathname, title), add_trade_strikes(session), stage_4_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-5':
        title = 'EXPIRATION DATE'
        return add_trade_back(pathname, title), add_trade_expiry(), stage_5_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-6':
        title = 'PRICE'
        return add_trade_back(pathname, title), add_trade_price(), stage_6_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-7':
        title = 'NOTES'
        return add_trade_back(pathname, title), add_trade_comment(), stage_7_buttons(), trade_preview(pathname, session)
    elif pathname == '/add-trade-stocks':
        title = 'NOTES'
        return add_trade_back(pathname, title), add_trade_comment(), stage_7_buttons(), trade_preview(pathname, session)
    else:
        return '', '', '', ''


# CALLBACK FOR DYNAMIC FILL FOR TRADE TYPE PREVIEW
@app.callback(
    [Output('trade_type_profile', 'children')],
    [Input('trade_type', 'value')]
)
def trade_type_preview(value):
    trade_legs = {'CASH SECURED PUT': 1,
                  'COVERED CALL': 1,
                  'PUT CREDIT SPREAD': 2,
                  'CALL CREDIT SPREAD': 2,
                  'PUT DEBIT SPREAD': 2,
                  'CALL DEBIT SPREAD': 2,
                  'LONG NAKED CALL': 1,
                  'LONG NAKED PUT': 1,
                  'SHORT NAKED CALL': 1,
                  'SHORT NAKED PUT': 1,
                  'LONG STRANGLE': 2,
                  'SHORT STRANGLE': 2,
                  'LONG STRADDLE': 2,
                  'SHORT STRADDLE': 2,
                  'SYNTHETIC LONG': 2,
                  'SYNTHETIC SHORT': 2,
                  'JADE LIZARD': 3,
                  'PMCC': 2,
                  'IRON CONDOR': 4,
                  'IRON BUTTERFLY': 4}
    if value is not None:
        for trade_type, legs in trade_legs.items():
            if value == trade_type:
                session['legs'] = legs
        session['trade_type'] = value.upper()
        return [value.upper()]
    else:
        return PreventUpdate


# CALLBACK FOR DYNAMIC FILL FOR SYMBOL PREVIEW
@app.callback(
    Output('symbol_profile', 'children'),
    [Input('trade_symbol', 'value')]
)
def trade_symbol(value):
    if value is not None:
        session['symbol'] = value.upper()
        return [value.upper()]


# CALLBACK FOR DYNAMIC FILL OF QTY PREVIEW
@app.callback(
    Output('qty_profile', 'children'),
    [Input('trade_qty', 'value'),]
)
def trade_qty(value):
    if value is not None:
        session['qty'] = value
        return [str(value).upper()]


# CALLBACK FOR DYNAMIC FILL OF STOCK PRICE PREVIEW
@app.callback(
    Output('stock_price_profile', 'children'),
    [Input('trade_stock_price', 'value')]
)
def stock_price(value):
    if value is not None:
        session['stock_price'] = value
        return [str(value).upper()]
    else:
        return ''


# CALLBACK FOR DYNAMIC FILL OF 1 STRIKES PREVIEW
@app.callback(
    Output('strikes_profile_1', 'children'),
    [Input('trade_strike_1', 'value'),
     Input('trade_strike_1', 'placeholder')]
)
def strikes_1(value, placeholder):
    if value is not None:
        strikes = option_identification(value, placeholder)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    else:
        return ''


# CALLBACK FOR DYNAMIC FILL OF 2 STRIKES PREVIEW
@app.callback(
    Output('strikes_profile_2', 'children'),
    [Input('trade_strike_2_1', 'value'),
     Input('trade_strike_2_1', 'placeholder'),
     Input('trade_strike_2_2', 'value'),
     Input('trade_strike_2_2', 'placeholder')]
)
def strikes_2(value_1, placeholder_1, value_2, placeholder_2):
    if None not in (value_1, value_2):
        strikes = option_identification(value_1, placeholder_1) + ' ' + option_identification(value_2, placeholder_2)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    elif value_1 is not None:
        strikes = option_identification(value_1, placeholder_1)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    else:
        return ''


# CALLBACK FOR DYNAMIC FILL OF 3 STRIKES PREVIEW (JADE LIZARD ONLY)
@app.callback(
    Output('strikes_profile_3', 'children'),
    [Input('trade_strike_3_1', 'value'),
     Input('trade_strike_3_1', 'placeholder'),
     Input('trade_strike_3_2', 'value'),
     Input('trade_strike_3_2', 'placeholder'),
     Input('trade_strike_3_3', 'value'),
     Input('trade_strike_3_3', 'placeholder')]
)
def strikes_3(value_1, placeholder_1, value_2, placeholder_2, value_3, placeholder_3):
    if None not in (value_1, value_2, value_3):
        strikes = option_identification(value_1, placeholder_1) + ' ' + option_identification(value_2, placeholder_2) + ' ' + option_identification(value_3, placeholder_3)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    elif None not in (value_1, value_2):
        strikes = option_identification(value_1, placeholder_1) + ' ' + option_identification(value_2, placeholder_2)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    elif value_1 is not None:
        strikes = option_identification(value_1, placeholder_1)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    else:
        return ''


# CALLBACK FOR DYNAMIC FILL OF 4 STRIKES PREVIEW
@app.callback(
    Output('strikes_profile_4', 'children'),
    [Input('trade_strike_4_1', 'value'),
     Input('trade_strike_4_1', 'placeholder'),
     Input('trade_strike_4_2', 'value'),
     Input('trade_strike_4_2', 'placeholder'),
     Input('trade_strike_4_3', 'value'),
     Input('trade_strike_4_3', 'placeholder'),
     Input('trade_strike_4_4', 'value'),
     Input('trade_strike_4_4', 'placeholder')]
)
def strikes_4(value_1, placeholder_1, value_2, placeholder_2, value_3, placeholder_3, value_4, placeholder_4):
    if None not in (value_1, value_2, value_3, value_4):
        strikes = option_identification(value_1, placeholder_1) + ' ' + \
                  option_identification(value_2, placeholder_2) + ' ' + \
                  option_identification(value_3, placeholder_3) + ' ' + \
                  option_identification(value_4, placeholder_4)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    elif None not in (value_1, value_2, value_3):
        strikes = option_identification(value_1, placeholder_1) + ' ' + \
                  option_identification(value_2, placeholder_2) + ' ' + \
                  option_identification(value_3, placeholder_3)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    elif None not in (value_1, value_2):
        strikes = option_identification(value_1, placeholder_1) + ' ' + option_identification(value_2, placeholder_2)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    elif value_1 is not None:
        strikes = option_identification(value_1, placeholder_1)
        session['strikes'] = str(strikes).upper()
        return [str(strikes).upper()]
    else:
        return ''


# CALLBACK FOR DYNAMIC SHOW OF STRIKES PREVIEW
@app.callback(
    [Output('strikes_profile_1', 'style'),
     Output('strikes_profile_2', 'style'),
     Output('strikes_profile_3', 'style'),
     Output('strikes_profile_4', 'style')],
    [Input('url', 'pathname')],
    State('newtrade_modal', 'is_open')
)
def strikes_show(pathname, is_open):
    show = {'display': 'initial'}
    not_show = {'display': 'none'}
    if pathname in ('/add-trade-4', '/add-trade-5', '/add-trade-6', '/add-trade-7') and is_open:
        if session['legs'] == 1:
            return show, not_show, not_show, not_show
        elif session['legs'] == 2:
            return not_show, show, not_show, not_show
        elif session['legs'] == 3:
            return not_show, not_show, show, not_show
        elif session['legs'] == 4:
            return not_show, not_show, not_show, show
        else:
            return not_show, not_show, not_show, not_show
    else:
        return not_show, not_show, not_show, not_show


# CALLBACK FOR DYNAMIC FILL OF EXPIRATION PREVIEW
@app.callback(
    Output('expiry_date_profile', 'children'),
    [Input('trade_expiration', 'date')]
)
def trade_expiration(date):
    from datetime import datetime
    if date is not None:
        session['expiration'] = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%b-%y')
        return [datetime.strptime(date, '%Y-%m-%d').strftime('%d-%b-%y')]


# CALLBACK FOR DYNAMIC FILL OF OPTION PRICE PREVIEW
@app.callback(
    Output('price_profile', 'children'),
    [Input('trade_price', 'value')]
)
def trade_price(value):
    if value is not None:
        session['price'] = str(value).upper()
        return [str(value).upper()]


# CALLBACK FOR DYNAMIC FILL OF COMMENT PREVIEW
@app.callback(
    Output('comment_profile', 'children'),
    [Input('trade_comment', 'value')]
)
def trade_comment(value):
    if value is not None:
        session['comment'] = str(value).upper()
        return [str(value).upper()]


# CALLBACK FROM ADD TRADE SUBMIT CONFIRMATION
@app.callback(
    [Output('add_trade_conf_modal', 'is_open'),
     Output('add_trade_fail_modal', 'is_open')],
    [Input('url', 'pathname')]
)
def trade_submit_conf_modal(pathname):
    if pathname == '/add-trade-submit':
        if session['trade_type'] is not None:
            add_new_trade(db_init, session)
            reset_add_trade_class(session)
            return True, False
        else:
            return False, True
    else:
        return False, False
#
#
# CALLBACK ENSURING THAT when path is '/' new_trade session data gets reset
@app.callback(
    Output('parent_id', 'children'),
    [Input('url', 'pathname')]
)
def reset_new_trade_class(pathname):
    if pathname == '/':
        reset_add_trade_class(session)
    return no_update


@app.callback(Output('stage1_submit_btn', 'children'),
              [Input('trade_type', 'value')])
def ticker_search_btn(trade_type):
    if trade_type != '' and trade_type is not None:
        return dbc.Button("Next", id="addtrade_next_1", href='/add-trade-2', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("Next", id="addtrade_next_1", href='/add-trade-2', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}, disabled=True)


@app.callback(Output('stage2_submit_btn', 'children'),
              [Input('trade_symbol', 'value')])
def ticker_search_btn(trade_symbol):
    if trade_symbol != '' and trade_symbol is not None:
        return dbc.Button("Next", id="addtrade_next_2", href='/add-trade-3', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("Next", id="addtrade_next_2", href='/add-trade-3', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}, disabled=True)


@app.callback(Output('stage3_submit_btn', 'children'),
              [Input('trade_qty', 'value')])
def ticker_search_btn(trade_qty):
    if trade_qty != '' and trade_qty is not None:
        return dbc.Button("Next", id="addtrade_next_3", href='/add-trade-4', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("Next", id="addtrade_next_3", href='/add-trade-4', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}, disabled=True)


@app.callback(Output('stage5_submit_btn', 'children'),
              [Input('trade_expiration', 'date')])
def ticker_search_btn(trade_expiration):
    if trade_expiration != '' and trade_expiration is not None:
        return dbc.Button("Next", id="addtrade_next_5", href='/add-trade-6', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("Next", id="addtrade_next_5", href='/add-trade-6', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}, disabled=True)


@app.callback(Output('stage6_submit_btn', 'children'),
              [Input('trade_price', 'value')])
def ticker_search_btn(trade_price):
    if trade_price != '' and trade_price is not None:
        return dbc.Button("Next", id="addtrade_next_6", href='/add-trade-7', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("Next", id="addtrade_next_6", href='/add-trade-7', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}, disabled=True)


@app.callback(Output('stage7_submit_btn', 'children'),
              [Input('trade_comment', 'value')])
def ticker_search_btn(trade_comment):
    if trade_comment != '' and trade_comment is not None:
        return dbc.Button("SUBMIT", id="addtrade_submit", href='/add-trade-submit', className='me-1 btn-block', n_clicks=0,  # href to change and trigger func to create trade and retoute to /
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("SUBMIT", id="addtrade_submit", href='/add-trade-submit', className='me-1 btn-block', n_clicks=0,  # href to change and trigger func to create trade and retoute to /
                   style={'margin': '0.5rem'}, disabled=True)


@app.callback(Output('stagestocks_submit_btn', 'children'),
              [Input('trade_stock_price', 'value')])
def ticker_search_btn(trade_comment):
    if trade_comment != '' and trade_comment is not None:
        return dbc.Button("Next", id="addtrade_next_stocks", href='/add-trade-stocks', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'})
    else:
        return dbc.Button("Next", id="addtrade_next_stocks", href='/add-trade-stocks', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}, disabled=True)


# # CALLBACK RETURNING THE VALUE OF SELECTED ROW IN TRADES TABLE
# @app.callback(Output('table_row', 'children'),
#               [Input('trades_table', 'active_cell')],
# )
# def update_div(active_cell):
#     print("active_cell: ", active_cell)
#     if active_cell is not None:
#         row = db_init.trades_data.iloc[[active_cell.get("row")]]
#         print("row: ", row)


@app.callback(Output('ticker_search_btn_col', 'children'),
              [Input('ticker_search', 'value')])
def ticker_search_btn(search_val):
    if search_val != '' and search_val is not None:
        href_link = '/ticker=' + search_val
        return dbc.Button('GO', href=href_link, id='ticker_search_btn', style={'display': 'inline-block'}, className="me-1")
    else:
        return dbc.Button('GO', id='ticker_search_btn', style={'display': 'inline-block'}, className="me-1", disabled=True)


@app.callback(Output('close_trade_modal', 'is_open'),
              [Input('url', 'pathname')],
              [State('close_trade_modal', 'is_open')])
def close_trade(pathname, is_open):
    if '/close-trade=' in pathname:
        return not is_open
    else:
        return False


@app.callback([Output('close_trade_btn_area', 'children'),
               Output('open_price_val', 'children'),
               Output('qty_val', 'children'),
               Output('symbol_val', 'children'),
               Output('trade_type_val', 'children')],
              [Input('url', 'pathname')],
              [State('price_view', 'children'),
               State('qty_view', 'children'),
               State('symbol_view', 'children'),
               State('trade_type_view', 'children')])
def close_trade_btn(pathname, open_price, qty, symbol, trade_type):
    if '/close-trade=' in pathname:
        tradeid = pathname.replace("/close-trade=", "")
        link = '/tradeid=' + str(tradeid)
        return [dbc.Button('CLOSE', id='close_trade_close_modal', color='danger', href=link, external_link=True)], open_price , qty, symbol, trade_type
    else:
        return no_update


@app.callback(Output('pnl_val', 'children'),
              [Input('close_price_input', 'value')],
              [State('price_view', 'children'),
               State('qty_view', 'children'),
               State('trade_type_view', 'children')])
def set_closing_pnl(close_price, open_price, qty, trade_type):
    exceptions = ['LONG POSITION', 'SHORT POSITION']
    long_options = ['PUT DEBIT SPREAD', 'CALL DEBIT SPREAD',
                    'LONG NAKED CALL', 'LONG NAKED PUT',
                    'LONG STRANGLE', 'LONG STRADDLE',
                    'SYNTHETIC LONG', 'SYNTHETIC SHORT']
    if trade_type in exceptions:
        if trade_type == 'LONG POSITION':
            pnl = round((float(close_price) * int(qty)) - (float(open_price) * int(qty)), 2)
        else:
            pnl = round((float(open_price) * int(qty)) - (float(close_price) * int(qty)), 2)
    else:
        if trade_type in long_options:
            pnl = round((float(close_price) * int(qty) * 100) - (float(open_price) * int(qty) * 100), 2)
        else:
            pnl = round((float(open_price) * int(qty) * 100) - (float(close_price) * int(qty) * 100), 2)
    if pnl > 0:
        return html.P(pnl, id='pnl_value_view', style={'color': '#7EFE76', 'font-weight': 'bold'})
    elif pnl < 0:
        return html.P(pnl, id='pnl_value_view', style={'color': '#FE7676', 'font-weight': 'bold'})
    else:
        return html.P(pnl, id='pnl_value_view')


@app.callback(Output('close_trade_success', 'children'),
              [Input('close_trade_submit', 'n_clicks'),
               Input('url', 'pathname')],
              [State('pnl_value_view', 'children'),
               State('close_price_input', 'value'),
               State('close_trade_text_area', 'value'),
               State('date_open_view', 'children')])
def close_trade_submmit(n, pathname, pnl_value, close_price, closing_note, date_open):
    if n and '/close-trade=' in pathname:
        try:
            date_open_trade = datetime.strptime(date_open, '%d-%b-%y %H:%M:%S')
            date_now = datetime.now()
            trade_lenght = (date_now - date_open_trade).days
            if trade_lenght < 1:
                trade_lenght = 1
            tradeid = pathname.replace("/close-trade=", "")
            update_trade_data(db_init, session, tradeid, 'pnl', round(float(pnl_value),2))
            update_trade_data(db_init, session, tradeid, 'closing_price', round(float(close_price),2))
            update_trade_data(db_init, session, tradeid, 'closing_date', datetime.now().strftime("%d-%b-%y, %H:%M:%S"))
            update_trade_data(db_init, session, tradeid, 'closing_comment', str(closing_note).upper())
            update_trade_data(db_init, session, tradeid, 'avg_trade_length', int(trade_lenght))
            db_init.db.child('users').child(session['username']).child('avg_trade_length').push(int(trade_lenght), session['idToken'])
            update_pnl_stats(db_init, session, round(float(pnl_value), 2))
            update_user_win_loss_number(db_init, session, round(float(pnl_value),2))
            return dbc.Alert("Trade closed!", color="success", duration=4000)
        except Exception as e:
            return dbc.Alert('Oops! Something went wrong!\nPlease relog and try again.', color="danger", duration=4000)


@app.callback(Output('edit_user_modal', 'is_open'),
              [Input('url', 'pathname')],
              [State('edit_user_modal', 'is_open')])
def edit_user(pathname, is_open):
    if '/edituser=' in pathname:
        return not is_open
    else:
        return False


@app.callback([Output('bio_text_area', 'value'),
               Output('close_user_edit_btn_area', 'children')],
              [Input('url', 'pathname')])
def bio_text_value(pathname):
    if '/edituser=' in pathname:
        link = '/user=' + str(session['username'])
        user_data = get_user_data(db_init, session['username'])
        return user_data['bio'], [dbc.Button('CLOSE', color='danger', href=link, external_link=True)]
    else:
        return no_update


@app.callback(Output('user_update_success', 'children'),
              [Input('edituser_submit', 'n_clicks')],
              [State('bio_text_area', 'value')])
def update_bio(n, bio_value):
    if n:
        try:
            update_user_data(db_init, session, 'bio', bio_value)
            return dbc.Alert("Your bio has been updated!", color="success", duration=4000)
        except Exception as e:
            return dbc.Alert('Oops! Something went wrong!\nPlease relog.', color="danger", duration=4000)


@app.callback([Output('message_modal_dynamic', 'is_open'),
               Output('message_modal_dynamic_text', 'children'),
               Output('message_modal_dynamic_button', 'children')],
              [Input('url', 'pathname')],
              [State('message_modal_dynamic', 'is_open')])
def follow_unfollow_user(pathname, is_open):
    if '/follow=' in pathname:
        user = pathname.replace("/follow=", "")
        msg, btn = follow_user(db_init, user, session)
        return True, msg, btn
    elif '/unfollow=' in pathname:
        user = pathname.replace("/unfollow=", "")
        msg, btn = unfollow_user(db_init, user, session)
        return True, msg, btn
    else:
        return False, no_update, no_update


@app.callback(Output('comment_trade_modal', 'is_open'),
              [Input('url', 'pathname')],
              [State('comment_trade_modal', 'is_open')])
def comment_trade(pathname, is_open):
    if '/comment=' in pathname:
        return not is_open
    else:
        return False


@app.callback([Output('comment_submmit_btn_area', 'children')],
              [Input('url', 'pathname')])
def comment_close_btn(pathname):
    if '/comment=' in pathname:
        trade_id = pathname.replace(pathname.split('=')[0], "")[1:]
        link = '/tradeid=' + str(trade_id)
        return [dbc.Button('CLOSE', color='danger', href=link, external_link=True)]
    else:
        return no_update


@app.callback([Output('comment_submmit_success', 'children'),
               Output('hide_comment_btn_id', 'style')],
              [Input('comment_submit', 'n_clicks')],
              [State('url', 'pathname'),
               State('comment_area', 'value')])
def submmit_comment(n, pathname, comment_text):
    if n:
        if comment_text is not None and str(comment_text) != '':
            trade_id = pathname.replace(pathname.split('=')[0], "")[1:]
            comment = {
                'user': session['username'],
                'datetime': datetime.now().strftime("%d-%b-%y, %H:%M:%S"),
                'comment_text': str(comment_text)
            }
            try:
                db_init.db.child("all_trades").child(str(trade_id)).child('user_comments').push(comment, session['idToken'])
                msg = dbc.Alert(f"Comment submmited!", color='success')
            except:
                msg = dbc.Alert(f"Oops! Something went wrong!\nPlease try again later!", color='danger')
            return msg, {'display': 'none'}
        else:
            return dbc.Alert(f"Oops! You submmited an empty comment!\nPlease write something and try again!", color='danger', duration=4000), {'display': ''}
    else:
        return no_update, {'display': ''}

# App instantiation
if __name__ == '__main__':
    app.run_server(debug=False)
