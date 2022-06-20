from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date


# TRADE TYPE
def stage_1_buttons():
    return [
        html.Div(id='stage1_submit_btn'),
        dbc.Button("Close", id="close_new_trade_1", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# SYMBOL
def stage_2_buttons():
    return [
        html.Div(id='stage2_submit_btn'),
        dbc.Button("Close", id="close_new_trade_2", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# QTY
def stage_3_buttons():
    return [
        html.Div(id='stage3_submit_btn'),
        dbc.Button("Close", id="close_new_trade_3", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# STRIKES
def stage_4_buttons():
    return [
        dbc.Button("Next", id="addtrade_next_4", href='/add-trade-5', className='me-1 btn-block', n_clicks=0,
                   style={'margin': '0.5rem'}),
        dbc.Button("Close", id="close_new_trade_4", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# EXPIRATION
def stage_5_buttons():
    return [
        html.Div(id='stage5_submit_btn'),
        dbc.Button("Close", id="close_new_trade_5", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# FILL PRICE
def stage_6_buttons():
    return [
        html.Div(id='stage6_submit_btn'),
        dbc.Button("Close", id="close_new_trade_6", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# COMMENT
def stage_7_buttons():
    return [
        html.Div(id='stage7_submit_btn'),
        dbc.Button("Close", id="close_new_trade_7", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# GO BACK NAV LINK
def add_trade_back(pathname, title):
    path_links = {'/add-trade-1': '/',
                  '/add-trade-2': '/add-trade-1',
                  '/add-trade-3': '/add-trade-2',
                  '/add-trade-4': '/add-trade-3',
                  '/add-trade-5': '/add-trade-4',
                  '/add-trade-6': '/add-trade-5',
                  '/add-trade-7': '/add-trade-6',
                  '/add-trade-stocks': '/add-trade-4'}
    path_refresh = False
    if pathname == '/add-trade-2':
        path_refresh = True
    href_link = '/'
    for path, link in path_links.items():
        if path == pathname:
            href_link = link
    return [html.P(title),
            html.A(dbc.NavLink(className='fas fa-arrow-left',
                               href=href_link,
                               external_link=path_refresh,
                               style={'color': 'white'}))
            ]


# EXCEPTIONAL stage stocks
def stage_stocks_buttons():
    return [
        html.Div(id='stagestocks_submit_btn'),
        dbc.Button("Close", id="close_new_trade_stocks", color='danger', className='me-1 btn-block', n_clicks=0,
                   href='/', style={'margin': '0.5rem'}, external_link=True),
    ]


# TRADE PREVIEW SECTION
def trade_preview(pathname, session):
    output_label =[]
    output = []
    paths_labels = {
        '/add-trade-1': ['TRADE TYPE:', None, None, None, None, None, None, None],
        '/add-trade-2': ['TRADE TYPE:', 'SYMBOL:', None, None, None, None, None, None],
        '/add-trade-3': ['TRADE TYPE:', 'SYMBOL:', 'QTY:', None, None, None, None, None],
        '/add-trade-4': ['TRADE TYPE:', 'SYMBOL:', 'QTY:', 'STRIKES / STOCK PRICE:', None, None, None, None],
        '/add-trade-5': ['TRADE TYPE:', 'SYMBOL:', 'QTY:', 'STRIKES:', None, 'EXPIRATION:', None, None],
        '/add-trade-6': ['TRADE TYPE:', 'SYMBOL:', 'QTY:', 'STRIKES:', None, 'EXPIRATION:', 'PRICE:', None,],
        '/add-trade-7': ['TRADE TYPE:', 'SYMBOL:', 'QTY:', 'STRIKES:', None, 'EXPIRATION:', 'PRICE:', 'COMMENT:'],
        '/add-trade-stocks': ['TRADE TYPE:', 'SYMBOL:', 'QTY:', 'STOCK PRICE:', None, None, None, 'COMMENT:'],
    }
    for path, content in paths_labels.items():
        if pathname == path:
            output_label = content
    paths = {
        '/add-trade-1': [None, None, None, None, None, None, None],
        '/add-trade-2': [session['trade_type'], None, None, None, None, None, None],
        '/add-trade-3': [session['trade_type'], session['symbol'], None, None, None, None, None],
        '/add-trade-4': [session['trade_type'], session['symbol'], session['qty'], None, None, None, None],
        '/add-trade-5': [session['trade_type'], session['symbol'], session['qty'], None, session['strikes'], None,
                         None],
        '/add-trade-6': [session['trade_type'], session['symbol'], session['qty'], None, session['strikes'],
                         session['expiration'], None],
        '/add-trade-7': [session['trade_type'], session['symbol'], session['qty'], None, session['strikes'],
                         session['expiration'], session['price']],
        '/add-trade-stocks': [session['trade_type'], session['symbol'], session['qty'], session['stock_price'], None, None,
                              None],
    }
    for path, content in paths.items():
        if pathname == path:
            output = content
    return [
        html.H4('PREVIEW', id='preview_title', style={'font-weight': 'bold'}),
        dbc.Row(
            [
                dbc.Col(
                    [
                    dbc.Row(output_label[0], id='trade_type_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[1], id='symbol_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[2], id='qty_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[3], id='stock_price_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[4], id='strikes_profile_1_label', style={'display': 'none', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[4], id='strikes_profile_2_label', style={'display': 'none', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[4], id='strikes_profile_3_label', style={'display': 'none', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[4], id='strikes_profile_4_label', style={'display': 'none', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[5], id='expiry_date_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[6], id='price_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'}),
                    dbc.Row(output_label[7], id='comment_profile_label', style={'display': 'flex', 'font-weight': 'bold', 'color': 'white'})
                    ],
                width=3),
                dbc.Col(
                    [
                        dbc.Row(output[0], id='trade_type_profile', style={'display': 'flex'}),
                        dbc.Row(output[1], id='symbol_profile', style={'display': 'flex'}),
                        dbc.Row(output[2], id='qty_profile', style={'display': 'flex'}),
                        dbc.Row(output[3], id='stock_price_profile', style={'display': 'flex'}),
                        dbc.Row(output[4], id='strikes_profile_1', style={'display': 'none'}),
                        dbc.Row(output[4], id='strikes_profile_2', style={'display': 'none'}),
                        dbc.Row(output[4], id='strikes_profile_3', style={'display': 'none'}),
                        dbc.Row(output[4], id='strikes_profile_4', style={'display': 'none'}),
                        dbc.Row(output[5], id='expiry_date_profile', style={'display': 'flex'}),
                        dbc.Row(output[6], id='price_profile', style={'display': 'flex'}),
                        dbc.Row(id='comment_profile', style={'display': 'flex'})
                    ],
                    width=9),
            ],
            style={'display': 'flex',
                   'padding': '1rem'}
        )
    ]


# TRADE TYPE SELECTOR INPUT
def trade_type():
    trade_types = ['LONG POSITION', 'SHORT POSITION',
                   'CASH SECURED PUT', 'COVERED CALL',
                   'PUT CREDIT SPREAD', 'CALL CREDIT SPREAD',
                   'PUT DEBIT SPREAD', 'CALL DEBIT SPREAD',
                   'LONG NAKED CALL', 'LONG NAKED PUT',
                   'SHORT NAKED CALL', 'SHORT NAKED PUT',
                   'LONG STRANGLE', 'SHORT STRANGLE',
                   'LONG STRADDLE', 'SHORT STRADDLE',
                   'SYNTHETIC LONG', 'SYNTHETIC SHORT',
                   'IRON CONDOR', 'IRON BUTTERFLY',
                   'PMCC', 'JADE LIZARD']
    return [
        dbc.ModalBody(
            [
                html.Div([
                    html.P('Pick a trade type below to continue to the next step.',
                           style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
                    dbc.Select(
                        options=[
                            {'label': i} for i in trade_types
                        ],
                        style={'color': 'white',
                               'background-color': '#222'},
                        id='trade_type',
                    ),
                ])
            ]
        ),
    ]


# TRADE SYMBOL INPUT
def add_trade_symbol():
    return [
        html.P('Pick a company symbol/ticker.',
               style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
        dbc.Input(placeholder="i.e. AMD, NVDA, SPY",
                  id='trade_symbol',
                  type="text",
                  style={'color': 'white',
                         'background-color': '#222',
                         'margin-left': '1rem',
                         'margin-right': '1rem',
                         'width': 'min-intrinsic'}
                  ),
    ]


# TRADE QTY INPUT
def add_trade_qty():
    return [
        html.P('Choose quantity.',
               style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
        dbc.Input(placeholder="i.e. 1, 10, 100",
                  id='trade_qty',
                  type="number",
                  style={'color': 'white',
                         'background-color': '#222',
                         'margin-left': '1rem',
                         'margin-right': '1rem',
                         'width': 'min-intrinsic'}
                  ),
    ]


# TRADE STOCK PRICE INPUT
def add_stock_price(session):
    trade_types = {'LONG POSITION': 'STOCK PRICE',
                   'SHORT POSITION': 'STOCK PRICE'}
    placeholder = []
    for trade_type, profile in trade_types.items():
        if session['trade_type'] == profile:
            placeholder = profile
    return [
        html.P('Stock price.',
               style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
        dbc.Input(placeholder=placeholder,
                  id='trade_stock_price',
                  type="number",
                  style={'color': 'white',
                         'background-color': '#222',
                         'margin-left': '1rem',
                         'margin-right': '1rem',
                         'width': 'min-intrinsic'}
                  ),
    ]


def option_identification(strike, placeholder):
    if 'LONG' in str(placeholder) and 'CALL' in str(placeholder):
        strikes = '+' + str(strike) + 'C'
    elif 'LONG' in str(placeholder) and 'PUT' in str(placeholder):
        strikes = '+' + str(strike) + 'P'
    elif 'SHORT' in str(placeholder) and 'CALL' in str(placeholder):
        strikes = '-' + str(strike) + 'C'
    elif 'SHORT' in str(placeholder) and 'PUT' in str(placeholder):
        strikes = '-' + str(strike) + 'P'
    else:
        strikes = str(placeholder)
    return str(strikes)


# TRADE STRIKES INPUT
def add_trade_strikes(session):
    trade_types = {'CASH SECURED PUT': [1, 'SHORT PUT STRIKE'],
                   'COVERED CALL': [1, 'SHORT CALL STRIKE'],
                   'PUT CREDIT SPREAD': [2, 'LONG PUT STRIKE', 'SHORT PUT STRIKE'],
                   'CALL CREDIT SPREAD': [2, 'SHORT CALL STRIKE', 'LONG CALL STRIKE'],
                   'PUT DEBIT SPREAD': [2, 'SHORT PUT STRIKE', 'LONG PUT STRIKE'],
                   'CALL DEBIT SPREAD': [2, 'LONG CALL STRIKE', 'SHORT CALL STRIKE'],
                   'LONG NAKED CALL': [1, 'LONG CALL STRIKE'],
                   'LONG NAKED PUT': [1, 'LONG PUT STRIKE'],
                   'SHORT NAKED CALL': [1, 'SHORT CALL STRIKE'],
                   'SHORT NAKED PUT': [1, 'SHORT PUT STRIKE'],
                   'LONG STRANGLE': [2, 'LONG PUT STRIKE', 'LONG CALL STRIKE'],
                   'SHORT STRANGLE': [2, 'SHORT PUT STRIKE', 'SHORT CALL STRIKE'],
                   'LONG STRADDLE': [2, 'LONG PUT STRIKE', 'LONG CALL STRIKE'],
                   'SHORT STRADDLE': [2, 'SHORT PUT STRIKE', 'SHORT CALL STRIKE'],
                   'PMCC': [2, 'LONG CALL STRIKE', 'SHORT CALL STRIKE'],
                   'SYNTHETIC LONG': [2, 'LONG CALL STRIKE', 'SHORT PUT STRIKE'],
                   'SYNTHETIC SHORT': [2, 'LONG PUT STRIKE', 'SHORT CALL STRIKE'],
                   'IRON CONDOR': [4,
                                   'LONG PUT STRIKE', 'SHORT PUT STRIKE',
                                   'SHORT CALL STRIKE', 'LONG CALL STRIKE'],
                   'IRON BUTTERFLY': [4,
                                      'LONG PUT STRIKE', 'SHORT PUT STRIKE',
                                      'SHORT CALL STRIKE', 'LONG CALL STRIKE'],
                   'JADE LIZARD': [3, 'SHORT PUT STRIKE', 'SHORT CALL STRIKE', 'LONG CALL STRIKE']}
    trade_legs = 0
    placeholders = []
    for trade_type, profile in trade_types.items():
        if session['trade_type'] == trade_type:
            trade_legs = profile[0]
            placeholders = profile[1:]
    if trade_legs == 1:
        return [
            html.P('Strike(s) levels.',
                   style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
            dbc.Input(placeholder=placeholders[0],
                      id='trade_strike_1',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
        ]
    elif trade_legs == 2:
        return [
            html.P('Strike(s) levels.',
                   style={'padding-left': '1rem',
                          'padding-bottom': '1rem'}),
            dbc.Input(placeholder=placeholders[0],
                      id='trade_strike_2_1',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
            dbc.Input(placeholder=placeholders[1],
                      id='trade_strike_2_2',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-top': '1rem',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
        ]
    elif trade_legs == 3:
        return [
            html.P('Strike(s) levels.',
                   style={'padding-left': '1rem',
                          'padding-bottom': '1rem'}),
            dbc.Input(placeholder=placeholders[0],
                      id='trade_strike_3_1',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
            dbc.Input(placeholder=placeholders[1],
                      id='trade_strike_3_2',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-top': '1rem',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
            dbc.Input(placeholder=placeholders[2],
                      id='trade_strike_3_3',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-top': '1rem',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
        ]
    elif trade_legs == 4:
        return [
            html.P('Strike(s) levels.',
                   style={'padding-left': '1rem',
                          'padding-bottom': '1rem'}),
            dbc.Input(placeholder=placeholders[0],
                      id='trade_strike_4_1',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
            dbc.Input(placeholder=placeholders[1],
                      id='trade_strike_4_2',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-top': '1rem',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
            dbc.Input(placeholder=placeholders[2],
                      id='trade_strike_4_3',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-top': '1rem',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
            dbc.Input(placeholder=placeholders[3],
                      id='trade_strike_4_4',
                      type="number",
                      required=True,
                      style={'color': 'white',
                             'background-color': '#222',
                             'margin-top': '1rem',
                             'margin-left': '1rem',
                             'margin-right': '1rem',
                             'width': 'min-intrinsic'}
                      ),
        ]


# TRADE EXPIRY SELECTOR
def add_trade_expiry():
    today = date.today()
    return [
        html.P('Choose the expiry date.',
               style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
        dcc.DatePickerSingle(
            id='trade_expiration',
            min_date_allowed=today,
            initial_visible_month=today,
            date=None,
            display_format='DD-MM-YYYY',
            placeholder='Select a date',
            style={'padding-left': '1rem'}
        ),
    ]


# TRADE PRICE INPUT
def add_trade_price():
    return [
        html.P('Price executed.',
               style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
        dbc.Input(placeholder="i.e. 0.5, 2.5, 5", id='trade_price',
                  type="number",
                  style={'color': 'white',
                         'background-color': '#222',
                         'margin-left': '1rem',
                         'margin-right': '1rem',
                         'width': 'min-intrinsic'}
                  ),
    ]


# TRADE COMMENT INPUT
def add_trade_comment():
    return [
        html.P('Comment your trade.',
               style={'padding-left': '1rem', 'padding-bottom': '1rem'}),
        dbc.Textarea(placeholder="i.e. 'I am bullish on...'", id='trade_comment', maxlength=150,
                     style={'color': 'white',
                            'background-color': '#222',
                            'margin-left': '1rem',
                            'margin-right': '1rem',
                            'width': 'min-intrinsic'}
                      ),
        dbc.FormText(
            "Max 150 characters.",
            color="secondary",
            className="mb-3",
            style={'margin-left': '1rem'}
        ),
    ]
