from dash import html, dcc
import dash_bootstrap_components as dbc


def login_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("LOGIN", style={'font-size': '1rem'})),
            dbc.ModalBody(
                [
                    html.P('USERNAME:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='login_email', type="text", placeholder='Enter your username',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.Br(),
                    html.P('PASSWORD:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='login_password', placeholder='Enter your password',
                              type='password',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.A('Forgot your password?', style={'color': 'white', 'font-size': '10px'}, href='/pwd-reset'),
                    html.Br(),
                    html.Div(id='login_alert')
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Submit", id="login_submit", className="ms-auto rounded-pill", n_clicks=0)
            ),
        ],
        id="login_modal",
        backdrop=False,
        is_open=False,
    )


def signup_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("SIGN-UP", style={'font-size': '1rem'})),
            dbc.ModalBody(
                [
                    html.P('E-MAIL:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='signup_email', type="email", placeholder='Enter your email',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.P('CHOSE YOUR USERNAME:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='signup_username', placeholder='Enter your username',
                              type='text',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.P('PASSWORD:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='signup_password', placeholder='Enter your password',
                              type='password',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.P('CONFIRM PASSWORD:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='confirm_signup_password', placeholder='Confirm your password',
                              type='password',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.Br(),
                    html.Div(id='signup_alert')
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Submit", id="signup_submit", className="ms-auto rounded-pill", n_clicks=0)
            ),
        ],
        id='signup_modal',
        backdrop=False,
        is_open=False,
    )


def pwd_reset_modal():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("RESET YOUR PASSWORD", style={'font-size': '1rem'})),
            dbc.ModalBody(
                [
                    html.P('E-MAIL:', style={'margin': '0px 0px 5px 5px'}),
                    dbc.Input(id='reset_pwd_email', type="email", placeholder='Enter your e-mail',
                              style={'margin-bottom': '1rem',
                                     'color': 'white',
                                     'font-size': '0.8rem',
                                     'background-color': '#222'}),
                    html.Br(),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Reset", id="reset_pwd_submit", href='/pwd-reset-send', className="ms-auto rounded-pill", n_clicks=0)
            ),
        ],
        id="reset_pwd_modal",
        backdrop=False,
        is_open=False,
    )


def reset_pwd_conf_modal():
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(dbc.Alert("PASSWORD RESET E-MAIL SENT!", color='success'), style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', id='reset_pwd_conf_close', href='/', external_link=True))
        ],
        size='md',
        id='reset_pwd_conf_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def logout_conf_modal():
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalTitle("LOGOUT SUCCESS", style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', className='rounded-pill', id='logout_close', href='/', external_link=True))
        ],
        size='md',
        id='logout_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def message_login_modal_success():
    msg = dbc.Alert(color='success'),
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(id='message_login_success_text', style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', className='rounded-pill', href='/', external_link=True))
        ],
        size='md',
        id='message_login_modal_success',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def message_siginup_modal_success():
    msg = dbc.Alert(color='success'),
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(id='message_signup_success_text', style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', className='rounded-pill', href='/', external_link=True))
        ],
        size='md',
        id='message_signup_modal_success',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def message_modal_fail():
    msg = dbc.Alert(id='message_fail_text', color='danger'),
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(msg, style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', className='rounded-pill', id='message_fail_close', href='/',  external_link=True))
        ],
        size='sm',
        id='message_modal_fail',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def message_modal_dynamic():
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(id='message_modal_dynamic_text', style={'text-align': 'center'})),
            dbc.Card(id='message_modal_dynamic_button')
        ],
        size='md',
        id='message_modal_dynamic',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def new_trade_modal():
    return dbc.Modal(
        [
            dbc.ModalTitle(id='newtrade_header',
                           style={'margin': '2rem 0rem 0rem 1rem',
                                  'font-weight': 'bold',
                                  'display': 'flex',
                                  'justify-content': 'space-between'}),
            dbc.Row(
                [
                        dbc.Card(
                            [
                                dbc.Row(html.Div(id='new_trade_inputs')),
                                dbc.Row(html.Div(id='new_trade_buttons'), style={'margin-top': '1rem'}),
                            ],
                            style={'margin-bottom': '1rem'}
                        ),
                        dbc.Card(
                            id='trade_preview',
                            style={'margin-bottom': '2rem'}
                        ),
                ],
            className='add_trade_row',)
        ],
        size='lg',
        id='newtrade_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
    )


def add_trade_conf_modal():
    msg = dbc.Alert('TRADE SUBMITTED!', color="success"),
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(msg, style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', className='rounded-pill', id='add_trade_conf_close', href='/', external_link=True))
        ],
        size='sm',
        id='add_trade_conf_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def add_trade_fail_modal():
    msg = dbc.Alert('TRADE ADDITION FAILED!', color="danger"),
    return dbc.Modal(
        [
            dbc.Card(dbc.ModalBody(msg, style={'text-align': 'center'})),
            dbc.Card(dbc.Button('Close', className='rounded-pill', id='add_trade_fail_close', href='/'))
        ],
        size='sm',
        id='add_trade_fail_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
        centered=True
    )


def close_trade_modal():
    return dbc.Modal(
        [
            dbc.Row(
                [
                    dbc.Card(
                        [
                            html.H2('CLOSE TRADE:'),
                            dbc.Row([
                                dbc.Row([dbc.Col(id='symbol_val', width='auto', style={'font-size': '110%', 'color': 'white', 'font-weight': 'bold'})]),
                                dbc.Row([dbc.Col(id='trade_type_val', width='auto', style={'font-size': '110%', 'color': 'white',  'font-weight': 'bold'})]),
                                dbc.Row([dbc.Col('Open Price: $', width='auto'), dbc.Col(id='open_price_val', width='auto')]),
                                dbc.Row([dbc.Col('Qty:', width='auto'), dbc.Col(id='qty_val', width='auto')]),
                                dbc.Row([dbc.Col('PnL: $', width='auto'), dbc.Col(id='pnl_val', width='auto')]),
                                html.Div(style={'height': '1.5rem'}),
                                dbc.Label("Closing Price: $"),
                                dbc.Input(id="close_price_input", placeholder="Input options closing price...(i.e. 0.2)", type="text",
                                          style={'background-color': 'rgb(30, 34, 45)',
                                                'color': 'white'},
                                          ),
                                html.Div(style={'height': '1.5rem'}),
                                dbc.Label("Closing Notes:"),
                                dbc.Textarea(value='',
                                             style={'height': '7rem',
                                                    'background-color': 'rgb(30, 34, 45)',
                                                    'color': 'white'},
                                             maxlength=150,
                                             id='close_trade_text_area',
                                             placeholder="i.e. This trade went well/wrong because..."),
                                dbc.FormText(
                                    "Max 150 characters.",
                                    color="secondary",
                                    className="mb-3",
                                ),
                                html.Div(id='close_trade_success')
                            ],
                                style={'padding': '0.5rem'}),
                            dbc.Row([
                                dbc.Col(
                                    dbc.Button('SUBMIT', color='primary', id='close_trade_submit'),
                                    width='auto'),
                                dbc.Col(id='close_trade_btn_area',
                                        width='auto')
                            ]),
                        ],
                    ),
                ],
            )
        ],
        size='lg',
        id='close_trade_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
    )


def edit_user_modal():
    return dbc.Modal(
        [
            dbc.Row(
                [
                        dbc.Card(
                            [
                                html.H2('USER BIO EDIT:'),
                                dbc.Row([
                                    dbc.Textarea(value='',
                                                 style={'height': '7rem',
                                                        'background-color': 'rgb(30, 34, 45)',
                                                        'color': 'white'},
                                                 maxlength=150,
                                                 id='bio_text_area',
                                                 placeholder="i.e. I am a Foxy dude that likes premium for breakfast..."),
                                    dbc.FormText(
                                        "Max 150 characters.",
                                        color="secondary",
                                    ),
                                    html.Div(id='user_update_success', className="mb-3")
                                         ],
                                        style={'padding': '0.5rem'}),
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Button('SUBMIT', color='primary', id='edituser_submit'),
                                    width='auto'),
                                    dbc.Col(id='close_user_edit_btn_area',
                                    width='auto')
                                ]),
                            ],
                        ),
                ],
            )
        ],
        size='lg',
        id='edit_user_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
    )


def comment_modal():
    return dbc.Modal(
        [
            dbc.Row(
                [
                        dbc.Card(
                            [
                                html.H2('COMMENT TRADE:'),
                                dbc.Row([
                                    dbc.Textarea(value='',
                                                 style={'height': '7rem',
                                                        'background-color': 'rgb(30, 34, 45)',
                                                        'color': 'white'},
                                                 maxlength=150,
                                                 id='comment_area',
                                                 placeholder="i.e. I think this trade is going to the moon because..."),
                                    dbc.FormText(
                                        "INFO: To remove a comment please send a request to a moderator in discord.", color="secondary"
                                    ),
                                    dbc.FormText(
                                        "Max 150 characters.",
                                        color="secondary",
                                        className="mb-3",
                                    ),
                                    html.Div(id='comment_submmit_success')
                                         ],
                                        style={'padding': '0.5rem'}),
                                dbc.Row([
                                    dbc.Col(
                                        html.Div(dbc.Button('SUBMIT', color='primary', id='comment_submit'),
                                                 id='hide_comment_btn_id',
                                                 style={'display': ''}),
                                    width='auto'),
                                    dbc.Col(id='comment_submmit_btn_area',
                                    width='auto')
                                ]),
                            ],
                        ),
                ],
            )
        ],
        size='lg',
        id='comment_trade_modal',
        backdrop='static',
        is_open=False,
        keyboard=False,
    )
