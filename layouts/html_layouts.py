from temp import *
from layouts.modals import logout_conf_modal
from collections import Counter
from flask import session

from dataframe import data_frame
import dash_bootstrap_components as dbc
from dash import html, dash_table
import dash_trich_components as dtc


def header_content():
    version = 'v1.0.0'
    return [
        dbc.Col(
            [
                dbc.Row([
                    html.A('FoxyFi', id='logo', className='no_margin logo', href='/',
                           style={'text-decoration': 'none', 'color': '#ff8000'}),
                    html.P(version, id='version', className='font_12px padding_left_1rem')
                ])
            ],
            xs=12, sm=12, md=12, lg=5, xl=5,
            id='logo_section',
            className='logo_section'
        ),
        dbc.Col(
            logon_header_buttons(),
            xs=12, sm=12, md=12, lg=7, xl=7,
            align='end',
            id='login_signup_section',
            className='login_signup_section'
        )
    ]


def logon_header_buttons():
    return [
        dbc.Button('SIGN UP', id='signup_btn', color='primary', className='me-1 rounded-pill'),
        dbc.Button('LOGIN', id='login_btn', color='secondary', className='me-1 rounded-pill')
    ]


def logout_header_buttons():
    return [
        dbc.Button('LOGOUT', id='logout_btn', color='danger', className='me-1 rounded-pill', href='/logout'),
        logout_conf_modal()
    ]


def nav_bar():
    return dtc.SideBar(
        [
            dtc.SideBarItem(id='navitem_1', label="Home", icon="fas fa-home fa-2x"),
            dtc.SideBarItem(id='navitem_2', label="Learning Centre", icon="fa fa-lightbulb fa-2x"),
            dtc.SideBarItem(id='navitem_3', label="Ticker Analysis", icon="fab fa-searchengin fa-2x"),
            dtc.SideBarItem(id='navitem_4', label="FAQ", icon="fas fa-question-circle fa-2x"),
            dtc.SideBarItem(id='navitem_5', label="FoxyFi Stats", icon="fa fa-chart-line fa-2x"),
            dtc.SideBarItem(id='navitem_6', label="Youtube", icon="fa fa-youtube fa-2x"),
            # dtc.SideBarItem(id='navitem_7', label="Patreon/Discord", icon="fa fa-users fa-2x"),
            dtc.SideBarItem(id='navitem_8', label="Contact", icon="fa fa-address-card fa-2x"),
            # dtc.SideBarItem(id='navitem_9', label="Buy me a Coffee", icon="fa fa-coffee fa-2x"),
        ],
        bg_color='#1e222d',
    )


def main_site_stats(number_of_users):
    return [
        html.P('FoxyFi Stats:', className='bold padding_top_1rem'),
        html.Div(f'CURRENT USERS: {number_of_users}',
                 id='total_users',
                 className='padding_bottom_1rem'
                 )
    ]


def user_container_not_logged():
    return [
        html.P('Welcome to FoxyFi!'),
        html.P('Please Login or Register for full access!'),
        # html.P('💎🦊 Become one of the first 50 users and obtain free access to all Patreon Perks!🦊 💎',
        #            style={'color': 'rgb(255, 128, 0)',
        #                   'font-weight': 'bold',
        #                   'text-decoration': 'underline'})
    ]


def user_profile(user_data):
    ranking_text = score_return(user_data['score'])

    username = user_data['username']
    badges = user_data['badges']
    score = f"{user_data['score']:,}"
    ranking = ranking_text
    followers = user_data['followers']
    following = user_data['following']
    wins = user_data['wins']
    losses = user_data['losses']
    # bio = user_data['bio']
    if (wins + losses) != 0:
        win_rate = round((wins / (wins + losses)) * 100, 2)
    else:
        win_rate = 0
    pnl_ytd = f"{user_data['premium_ytd']:,}"
    pnl_overall = f"{user_data['premium_overall']:,}"
    number_trades = user_data['number_of_trades']
    avg_trade_lenght = user_data['avg_trade_length']

    user_and_badges = str(username) + ' ' + badges
    user_link = '/user=' + str(username)
    edit_user_link = '/edituser=' + str(username)

    user_and_badges = str(username) + ' ' + badges
    user_link = '/user=' + str(username)

    if user_data['access_type'] == 'foxy':
        user = dbc.Badge(user_and_badges, className='ms-1', color='light', href=user_link,
                         style={'text-decoration': 'none', 'width': 'auto'})
    else:
        user = html.H6(html.A(user_and_badges, href=user_link, style={'text-decoration': 'none'}), className='bold')

    return [
        dbc.Row([user], className='padding_left_1rem padding_top_1rem'),
        html.Br(),
        dbc.Row(html.P(f'SCORE: {score}'), className='padding_left_1rem'),
        dbc.Row(html.P(f'YOUR RANK: {ranking}'), className='padding_left_1rem'),
        html.Br(),
        dbc.Row(html.P(f'{followers} FOLLOWERS | {following} FOLLOWING'), className='padding_left_1rem'),
        html.Br(),
        dbc.Row(html.P('YOUR STATS:'), className='bold padding_left_1rem'),
        dbc.Row(html.P(f'Wins: {wins}'), className='padding_left_1rem'),
        dbc.Row(html.P(f'Losses: {losses}'), className='padding_left_1rem'),
        dbc.Row(html.P(f'Win %: {win_rate}%'), className='padding_left_1rem'),
        html.Br(),
        dbc.Row(html.P(f'Net PNL YTD: {pnl_ytd}$'), className='padding_left_1rem'),
        dbc.Row(html.P(f'Net PNL: {pnl_overall}$'), className='padding_left_1rem'),
        html.Br(),
        dbc.Row(html.P(f'# of Trades: {number_trades}'), className='padding_left_1rem'),
        dbc.Row(html.P(f'Avg. Trade Lenght: {avg_trade_lenght} days'), className='padding_left_1rem'),
        html.Br(),
        dbc.Button('ADD TRADE', id='add_trade_btn', color='primary', className='me-1 btn-block rounded-pill',
                   href='/add-trade-1'),
        dbc.Button('EDIT PROFILE', id='edit_profile_btn', href=edit_user_link, color='primary', className='me-1 btn-block rounded-pill'),
    ]


def home_page(dataframe):
    df = dataframe.head(40)
    trending = [word for word, count in Counter(list(df['SYMBOL'])).most_common(5)]
    return [
        html.Div(trending_trades(trending),
                 id='trending_trades',
                 className='padding_top_1rem'),
        html.Div(main_accordion(news_economic_cal_widget(), market_view_widget(),
                                True),
                 id='main_page_content',
                 className='padding_top_1rem')
    ]


def home_page_user(dataframe):
    df = dataframe.head(40)
    trending = [word for word, count in Counter(list(df['SYMBOL'])).most_common(5)]
    return [
        html.Div(trending_trades(trending),
                 id='trending_trades',
                 className='padding_top_1rem'),
        html.Div(main_accordion(news_economic_cal_widget(), market_view_widget(),
                                False),
                 id='main_page_content',
                 className='padding_top_1rem')
    ]


def trending_badges(ticker_list):
    trending = []
    for ticker in ticker_list:
        ticker_link = '/ticker=' + ticker
        trending.append(html.H5(dbc.Badge('🚀' + ticker + '$', className='ms-1', color='light', href=ticker_link,
                                          style={'text-decoration': 'none'})))
    return trending


def trending_trades(ticker_list):
    return [
        dbc.Row(
            [
                dbc.Col('Trending:', className='flex_grid font_16px', xs=2, sm=2, md=2, lg=2, xl=2),
                dbc.Col(trending_badges(ticker_list), className='flex_grid', xs=12, sm=12, md=12, lg=10, xl=10),
            ],
        ),
    ]


def main_accordion(content_1, content_2, my_tab):
    return dbc.Accordion(
        [
            dbc.AccordionItem(
                dbc.Card(
                    [
                        content_1
                    ],
                    color='#131722',
                    class_name='accordion_border'
                ),
                title='MARKET NEWS / ECONOMIC CALENDAR',
                item_id='item_1',
                className='trades_on_record',
                style={'background': '#131722'}
            ),
            dbc.AccordionItem(
                dbc.Card(
                    [
                        content_2
                    ],
                    color='#131722',
                    class_name='accordion_border'
                ),
                title='MARKET OVERVIEW',
                item_id='item_2',
                className='trades_on_record',
                style={'background': '#131722'}
            ),
            dbc.AccordionItem(
                dbc.Card(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    tab_id='all_trades_tab',
                                    label="TODAY's TRADES",
                                    active_tab_style={'font-weight': 'bold'},
                                    disabled=False
                                ),
                                dbc.Tab(
                                    tab_id='my_trades_tab',
                                    label="MY TRADES",
                                    active_tab_style={'font-weight': 'bold'},
                                    disabled=my_tab
                                ),
                            ],
                            id='home_page_tabs',
                            active_tab='all_trades_tab'
                        ),
                        html.Br(),
                        html.Div(id='main_tab_content', className='main_content')
                    ],
                    color='#131722',
                    class_name='accordion_border'
                ),
                title='LATEST TRADES',
                item_id='item_3',
                className='trades_on_record',
                style={'background': '#131722'}
            ),
        ],
        active_item='item_1'
    )


def container(title_text, content_text):
    container = html.Div(
        dbc.Container(
            [
                html.H4(title_text, className="display-4", style={'font-weight': 'bold'}),
                html.P(content_text, className="lead"),
                html.Br(),
                html.Hr(className="my-2"),
                html.P(
                    dbc.Button("HOME", color="secondary", href='/'), className="lead"
                ),
            ],
            id='container',
            fluid=True,
            className="py-3",
            style={'padding': '0rem'}
        ),
        className="p-3 rounded-3",
    )
    return [container]


def learning_page():
    return dbc.Card(
        [
            html.H4("Learning Centre", className="display-4"),
            dbc.Select(
                id="learning_select",
                placeholder="Please select an option...",
                options=[
                    {"label": 'What is a "Covered Call"?', "value": 'L1'},
                    {"label": 'What is a "Cash Secured Put"?', "value": 'L2'},
                    {"label": 'What is an "Straddle"?', "value": 'L3'},
                    {"label": 'What is a "Strangle"?', "value": 'L4'},
                    {"label": 'What is an "Iron Condor"?', "value": 'L5'},
                    {"label": 'What is an "Iron Butterfly (Iron Fly)"?', "value": 'L6'},
                    {"label": 'What is a "Poor Man Covered Call"?', "value": 'L7'},
                    {"label": 'What is a "Jade Lizard"?', "value": 'L8'},
                ],
                style={'color': 'white',
                       'background-color': '#222'},
            ),
            html.Br(),
            html.Div(id='learning_page_content')
        ],
        color='rgb(30, 34, 45)'
    ),


def faq_page():
    return dbc.Card(
        [
            html.H4("FoxyFi FAQ", className="display-4"),
            dbc.Select(
                id="FAQ_select",
                placeholder="Please select an option...",
                options=[
                    {"label": "Can i upload trades i have done in the past to my profile?", "value": 'Q1'},
                    {"label": "Can i delete my trades?", "value": 'Q2'},
                    {"label": "What if i submitted a wrong trade or a typo? Can i edit my trade?", "value": 'Q3'},
                    {"label": "How does the points and ranking system work in FoxyFi?", "value": 'Q4'},
                    {"label": "But Foxy...what prevents users from cheating to get more points?", "value": 'Q5'},
                    # {"label": "Is FoxyFi FREE??", "value": 'Q6'},
                    # {"label": "What do i get as a Patreon?", "value": 'Q7'},
                ],
                style={'color': 'white',
                       'background-color': '#222'},
            ),
            html.Br(),
            html.Div(id='FAQ_page_content')
        ],
        color='rgb(30, 34, 45)'
    ),


def youtube_page():
    return dbc.Card(
        [
            html.Div([
                        dbc.Row(dbc.Col(html.A(html.Img(src='https://www.pngkey.com/png/full/254-2543943_youtube-subscribe-your-youtube-channel.png',
                                                 style={'max-width': '30%',
                                                        'height': 'auto'}),
                                               href='https://www.youtube.com/c/foxyfi'),
                                        ),
                                style={'display': 'flex', 'text-align': '-webkit-center'}),
                        dbc.Row([
                            dbc.Col(dtc.Card(
                                link='https://www.youtube.com/watch?v=HsxSHM5PcHk&t=1s',
                                image='https://i.ytimg.com/vi/fO9z_QgaPs8/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDGl3-S-smMrbmEsrWvJeD9aW_t2A',
                                title='Stock Market Analysis using Python',
                                # description='Description text for the first video',
                                # badges=['PYTHON', 'FINANCE', 'FOXYFI'],
                                dark=True,
                                style={'margin-top': '1rem', 'margin-bottom': '1rem'}
                            ), xs=12, sm=12, md=12, lg=12, xl=4),
                            dbc.Col(dtc.Card(
                                link='https://www.youtube.com/watch?v=FAVKJaKW1RY&t=1s',
                                image='https://i.ytimg.com/vi/FAVKJaKW1RY/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLCgFHPEd2C7pAqmZEdK3ZLdu3qhPw',
                                title='How to easily find Support and Resistance Levels - Stock Market Analysis using Python',
                                # description='Description text for the second video',
                                # badges=['PYTHON', 'FINANCE', 'FOXYFI'],
                                dark=True,
                                style={'margin-top': '1rem', 'margin-bottom': '1rem'}
                            ), xs=12, sm=12, md=12, lg=12, xl=4),
                            dbc.Col(dtc.Card(
                                link='https://www.youtube.com/watch?v=HsxSHM5PcHk&t=1s',
                                image='https://i.ytimg.com/vi/HsxSHM5PcHk/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLCBsZhLEXWoj6LFlW2sjwbiaSXA8w',
                                title='Algo Trading Your Favorite Stocks using SMA Crossover Backtesting in Python',
                                # description='Description text for the third video',
                                # badges=['PYTHON', 'FINANCE', 'FOXYFI'],
                                dark=True,
                                style={'margin-top': '1rem', 'margin-bottom': '1rem'}
                            ), xs=12, sm=12, md=12, lg=12, xl=4),
                        ], style={'display': 'flex', 'text-align': '-webkit-center'}),
            ])
        ],
        color='rgb(30, 34, 45)'
    ),


def patreon_page():
    return dbc.Card(
        [
            html.Div(
                dbc.Container(
                    [
                        html.H4("Support FoxyFi through PATREON!", className="display-4"),
                        html.P(
                            "By subscribing the FoxyFi Tier in Patreon you get access to many perks such as (1) "
                            "USERNAME flare on the website, (2) access to the DISCORD FoxyFi community, (3) your "
                            "username shoutout on every bit of upcomming video content created by Foxy, (4) the "
                            "ability to make requests/suggestions for future features and upgrades to this website, "
                            "etc!",
                            className="lead",
                        ),
                        html.Br(),
                        html.Span('Follow this ', style={'font-size': '130%'}),
                        html.A("LINK", href='https://www.patreon.com/silviogobet', style={'font-size': '130%',
                                                                                          'margin-bottom': '2rem',
                                                                                          'color': 'rgb(255, 128, 0)'}),
                        html.Span(' to know more! ', style={'font-size': '130%'}),
                        html.Br(),
                        dbc.Row(dbc.Col([
                            html.A(
                                html.Img(
                                    src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Patreon_logo.svg/2048px-Patreon_logo.svg.png',
                                    style={'max-width': '20%',
                                           'height': 'auto',
                                           'margin-right': '1rem'}),
                                href='https://www.patreon.com/silviogobet'),
                        ],
                        width=12),
                        style={'display': 'flex', 'text-align': '-webkit-center', 'margin': '1rem'}),
                        html.Br(),
                        html.Hr(className="my-2"),
                        html.P(
                            dbc.Button("HOME", color="secondary", href='/'), className="lead"
                        ),
                    ],
                    fluid=True,
                    className="py-3",
                    style={'padding': '0rem'}
                ),
                className="p-3 rounded-3",
            )
        ],
        color='rgb(30, 34, 45)'
    ),


def contact_page():
    return dbc.Card(
        [
            html.Div(
                dbc.Container(
                    [
                        html.H4("Contact FoxyFi!", className="display-4"),
                        html.P(
                            "To get in touch with me please go ahead and message me on any of the social media "
                            "channels bellow by clicking on their respective image links!",
                            className="lead",
                        ),
                        html.Br(),
                        dbc.Row(dbc.Col([
                            html.A(
                                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/480px-LinkedIn_logo_initials.png',
                                            style={'max-width': '15%',
                                                   'height': 'auto',
                                                   'margin-right': '1rem'}),
                            href='https://www.linkedin.com/in/silviogobet/'),
                            html.A(
                                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/480px-Instagram_icon.png',
                                            style={'max-width': '15%',
                                                   'height': 'auto',
                                                   'margin-left': '1rem'}),
                            href='https://www.instagram.com/silviogobet/?hl=en')
                        ],
                            width=12),
                        style={'display': 'flex', 'text-align': '-webkit-center'}),
                        html.Br(),
                        html.Hr(className="my-2"),
                        html.P(
                            dbc.Button("HOME", color="secondary", href='/'), className="lead"
                        ),
                    ],
                    fluid=True,
                    className="py-3",
                    style={'padding': '0rem'}
                ),
                className="p-3 rounded-3",
            )
        ],
        color='rgb(30, 34, 45)'
    ),


def news_economic_cal_widget():
    return dbc.Row([
        dbc.Row([
        dbc.Col(dbc.Input(id="ticker_search", placeholder="🔍 Search for ticker...", type="text",
                          style={'margin-bottom': '1rem',
                                 'color': 'white',
                                 'font-size': '1rem',
                                 'background-color': '#222',
                                 'margin-left': '0.5rem'}), xs=9, sm=9, md=9, lg=3, xl=3),
        dbc.Col(id='ticker_search_btn_col',
                xs=1, sm=1, md=1, lg=1, xl=1, style={'padding': '0'}),
        ]),
        dbc.Row([
            dbc.Col(html.Iframe(
            srcDoc='''<!-- TradingView Widget BEGIN -->
                <div class="tradingview-widget-container">
                  <div class="tradingview-widget-container__widget"></div>
                  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/key-events/" rel="noopener" target="_blank"><span class="blue-text">Daily news roundup</span></a> by TradingView</div>
                  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
                  {
                  "feedMode": "all_symbols",
                  "colorTheme": "dark",
                  "isTransparent": false,
                  "displayMode": "regular",
                  "width": "100%",
                  "height": 500,
                  "locale": "en"
                }
                  </script>
                </div>
                <!-- TradingView Widget END -->''',
            style={"height": 517, 'width': '100%', 'display': 'table'},
        ),
            xs=12, sm=12, md=12, lg=7, xl=7),
        dbc.Col(html.Iframe(
            srcDoc='''<!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/markets/currencies/economic-calendar/" rel="noopener" target="_blank"><span class="blue-text">Economic Calendar</span></a> by TradingView</div>
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
              {
              "width": "100%",
              "height": 500,
              "colorTheme": "dark",
              "isTransparent": false,
              "locale": "en",
              "importanceFilter": "0,1",
              "currencyFilter": "USD,EUR,GBP"
            }
              </script>
            </div>
            <!-- TradingView Widget END -->''',
            style={"height": 517, 'width': '100%', 'display': 'table'},
        ),
            xs=12, sm=12, md=12, lg=5, xl=5, )],
        justify='center',
    )
    ])


def market_view_widget():
    return dbc.Row([
        dbc.Col(html.Iframe(
            srcDoc='''<!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/markets/stocks-usa/" rel="noopener" target="_blank"><span class="blue-text">Stock Market Today</span></a> by TradingView</div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-hotlists.js" async>
      {
      "colorTheme": "dark",
      "dateRange": "3M",
      "exchange": "US",
      "showChart": true,
      "locale": "en",
      "largeChartUrl": "",
      "isTransparent": false,
      "showSymbolLogo": true,
      "showFloatingTooltip": true,
      "width": "100%",
      "height": "600",
      "plotLineColorGrowing": "rgba(41, 98, 255, 1)",
      "plotLineColorFalling": "rgba(41, 98, 255, 1)",
      "gridLineColor": "rgba(240, 243, 250, 0)",
      "scaleFontColor": "rgba(120, 123, 134, 1)",
      "belowLineFillColorGrowing": "rgba(41, 98, 255, 0.12)",
      "belowLineFillColorFalling": "rgba(41, 98, 255, 0.12)",
      "belowLineFillColorGrowingBottom": "rgba(41, 98, 255, 0)",
      "belowLineFillColorFallingBottom": "rgba(41, 98, 255, 0)",
      "symbolActiveColor": "rgba(41, 98, 255, 0.12)"
    }
      </script>
    </div>
    <!-- TradingView Widget END -->''',
            style={"height": 617, 'width': '100%', 'display': 'table'},
        ),
            xs=12, sm=12, md=12, lg=4, xl=4, ),
        dbc.Col(html.Iframe(
            srcDoc='''<!-- TradingView Widget BEGIN -->
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
              <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/markets/" rel="noopener" target="_blank"><span class="blue-text">Financial Markets</span></a> by TradingView</div>
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
              {
              "width": "100%",
              "height": 600,
              "symbolsGroups": [
                {
                  "name": "Indices",
                  "originalName": "Indices",
                  "symbols": [
                    {
                      "name": "FOREXCOM:SPXUSD",
                      "displayName": "S&P 500"
                    },
                    {
                      "name": "FOREXCOM:NSXUSD",
                      "displayName": "US 100"
                    },
                    {
                      "name": "FOREXCOM:DJI",
                      "displayName": "Dow 30"
                    },
                    {
                      "name": "INDEX:NKY",
                      "displayName": "Nikkei 225"
                    },
                    {
                      "name": "INDEX:DEU40",
                      "displayName": "DAX Index"
                    },
                    {
                      "name": "FOREXCOM:UKXGBP",
                      "displayName": "UK 100"
                    }
                  ]
                },
                {
                  "name": "Futures",
                  "originalName": "Futures",
                  "symbols": [
                    {
                      "name": "CME_MINI:ES1!",
                      "displayName": "S&P 500"
                    },
                    {
                      "name": "CME:6E1!",
                      "displayName": "Euro"
                    },
                    {
                      "name": "COMEX:GC1!",
                      "displayName": "Gold"
                    },
                    {
                      "name": "NYMEX:CL1!",
                      "displayName": "Crude Oil"
                    },
                    {
                      "name": "NYMEX:NG1!",
                      "displayName": "Natural Gas"
                    },
                    {
                      "name": "CBOT:ZC1!",
                      "displayName": "Corn"
                    }
                  ]
                },
                {
                  "name": "Bonds",
                  "originalName": "Bonds",
                  "symbols": [
                    {
                      "name": "CME:GE1!",
                      "displayName": "Eurodollar"
                    },
                    {
                      "name": "CBOT:ZB1!",
                      "displayName": "T-Bond"
                    },
                    {
                      "name": "CBOT:UB1!",
                      "displayName": "Ultra T-Bond"
                    },
                    {
                      "name": "EUREX:FGBL1!",
                      "displayName": "Euro Bund"
                    },
                    {
                      "name": "EUREX:FBTP1!",
                      "displayName": "Euro BTP"
                    },
                    {
                      "name": "EUREX:FGBM1!",
                      "displayName": "Euro BOBL"
                    }
                  ]
                },
                {
                  "name": "Forex",
                  "originalName": "Forex",
                  "symbols": [
                    {
                      "name": "FX:EURUSD"
                    },
                    {
                      "name": "FX:GBPUSD"
                    },
                    {
                      "name": "FX:USDJPY"
                    },
                    {
                      "name": "FX:USDCHF"
                    },
                    {
                      "name": "FX:AUDUSD"
                    },
                    {
                      "name": "FX:USDCAD"
                    }
                  ]
                }
              ],
              "showSymbolLogo": true,
              "colorTheme": "dark",
              "isTransparent": false,
              "locale": "en"
            }
              </script>
            </div>
            <!-- TradingView Widget END -->''',
            style={"height": 617, 'width': '100%', 'display': 'table'},
        ), xs=12, sm=12, md=12, lg=8, xl=8),
    ],
        justify='center',
    )


def ticker_view(ticker, all_trades):
    df = all_trades.loc[all_trades['SYMBOL'] == str(ticker).upper()]
    df = df.head(40)
    if ticker not in ['spy', 'Spy', 'SPY', 'qqq', 'Qqq', 'QQQ']:
        ticker_news = ticker
    else:
        ticker_news = ''
    return html.Div(
        [
            dbc.Card(
                [
                    dbc.Col(dbc.Label("Lookup your favorite ticker:"), width=12, style={'padding': '0'}),
                    dbc.Row([
                        dbc.Col(dbc.Input(id="ticker_search", placeholder="🔍 Search for ticker...", type="text",
                                          style={'margin-bottom': '1rem',
                                                 'color': 'white',
                                                 'font-size': '1rem',
                                                 'background-color': '#222'}), xs=9, sm=9, md=9, lg=3, xl=3),
                        dbc.Col(id='ticker_search_btn_col',
                                xs=2, sm=2, md=2, lg=2, xl=2, style={'padding': '0'}),
                        dbc.Col(html.A(dbc.NavLink(' BACK', className='fas fa-arrow-left',
                                                   href='/',
                                                   style={'color': 'white'}), style={'text-align': 'right'}))
                    ]),
                ],
                color='#131722',
                style={'border': '2px solid #252d43'}
            ),
            dbc.Card(
                [
                    dbc.Col(html.Iframe(
                        srcDoc='''<!-- TradingView Widget BEGIN -->
                            <div class="tradingview-widget-container">
                            <div class="tradingview-widget-container__widget"></div>
                            <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Price Today</span></a> by TradingView</div>
                            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
                            {
                            "symbol": "''' + ticker + '''",
                            "width": "100%",
                            "locale": "en",
                            "colorTheme": "dark",
                            "isTransparent": false
                            }
                            </script>
                            </div>
                            <!-- TradingView Widget END -->''',
                        style={"height": 225, 'width': '100%', 'display': 'table'},
                    ),
                        xs=12, sm=12, md=12, lg=12, xl=12,
                        style={'padding-left': '0', 'padding-right': '0'}),
                    dbc.Col(html.Iframe(
                        srcDoc='''<!-- TradingView Widget BEGIN -->
                            <div class="tradingview-widget-container">
                              <div id="tradingview_7715e"></div>
                              <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
                              <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                              <script type="text/javascript">
                              new TradingView.widget(
                              {
                              "width": "100%",
                              "height": 770,
                              "symbol": "''' + ticker + '''",
                              "interval": "D",
                              "timezone": "Etc/UTC",
                              "theme": "dark",
                              "style": "1",
                              "locale": "en",
                              "toolbar_bg": "#f1f3f6",
                              "enable_publishing": false,
                              "withdateranges": true,
                              "allow_symbol_change": true,
                              "details": true,
                              "studies": [
                                "MACD@tv-basicstudies",
                                "StochasticRSI@tv-basicstudies"
                              ],
                              "container_id": "tradingview_7715e"
                            }
                              );
                              </script>
                            </div>
                            <!-- TradingView Widget END -->''',
                        style={"height": 787, 'width': '100%', 'display': 'table'},
                    ),
                        xs=12, sm=12, md=12, lg=12, xl=12,
                        style={'padding-left': '0', 'padding-right': '0'})
                ],
                color='#131722',
                style={'border': '2px solid #252d43'}
            ),
            dbc.Card(
                [
                    dbc.Col(html.Iframe(
                        srcDoc='''<!-- TradingView Widget BEGIN -->
                            <div class="tradingview-widget-container">
                            <div class="tradingview-widget-container__widget"></div>
                            <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AMD/history-timeline/" rel="noopener" target="_blank"><span class="blue-text">AMD History</span></a> by TradingView</div>
                            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
                            {
                            "feedMode": "symbol",
                            "symbol": "''' + ticker_news + '''",
                            "colorTheme": "dark",
                            "isTransparent": false,
                            "displayMode": "regular",
                            "width": "100%",
                            "height": 800,
                            "locale": "en"
                            }
                            </script>
                            </div>
                            <!-- TradingView Widget END -->''',
                        style={"height": 817, 'width': '100%', 'display': 'table'},
                    ),
                        xs=12, sm=12, md=12, lg=12, xl=12,
                        style={'padding-left': '0', 'padding-right': '0'})
                ],
                color='#131722',
                style={'border': '2px solid #252d43'}
            ),
            dbc.Card(
                [
                    dbc.Col(dbc.Label(f"RECENT {str(ticker).upper()} TRADES:", style={'font-size': '160%'}),
                            width=12),
                    dbc.Col(data_frame(df), width=12)
                ],
                color='#1e222d', className='df_div')
        ]
    )


def trade_view_row(header, style_header, data_point, style_datapoint):
    row =dbc.Row(
        [
            dbc.Col(header, style=style_header, xs=5, sm=4, md=4, lg=3, xl=3),
            dbc.Col(data_point, style=style_datapoint, xs=7, sm=6, md=6, lg=9, xl=9),
        ],
    )
    return row


def trade_view(trade_id, dataframe):
    try:
        df = dataframe.loc[dataframe.index == trade_id]
        data = df.iloc[0]
        df_all_symbol_trades = dataframe.loc[dataframe['SYMBOL'] == data['SYMBOL']]
        df_all_symbol_trades = df_all_symbol_trades.head(40)
        try:
            comments = pd.DataFrame(df.iloc[0]['USER COMMENTS'], columns=df.iloc[0]['USER COMMENTS'].keys()).T
        except:
            comments = pd.DataFrame()

        user_link = '/user=' + str(data['USERNAME'])
        symbol_link = '/ticker=' + str(data['SYMBOL'])
        trade_id_close_link = '/close-trade=' + str(trade_id)
        trade_id_comment_link = '/comment=' + str(trade_id)
        if data['PnL'] > 0:
            pnl_value = html.P(f"{data['PnL']:,}", id='price_closed_view', style={'color': '#7EFE76'})
        elif data['PnL'] < 0:
            pnl_value = html.P(f"{data['PnL']:,}", id='price_closed_view', style={'color': '#FE7676'})
        else:
            pnl_value = html.P(f"{data['PnL']:,}", id='price_closed_view')

        comment_btn = ''
        btn = ''
        if 'username' in session:
            comment_btn = dbc.Button('COMMENT', id='comment_btn', href=trade_id_comment_link, color='primary', className='me-1 btn-block')
            if data['USERNAME'] == session['username'] and data['CLOSE'] == 0:
                btn = dbc.Button('CLOSE TRADE', id='close_trade_btn', href=trade_id_close_link, color='danger', className='me-1 btn-block')

        style_label = {'font-weight': 'bold', 'color': '#9598a1'}
        style_row = {'display': 'flex', 'padding-bottom': '10px'}

        try:
            if 'N/A' in data['C.B.']:
                cost_basis = data['C.B.']
            else:
                cost_basis = f"{data['C.B.']:,}"
        except Exception as e:
            print(e)
            cost_basis = f"{data['C.B.']:,}"

        options_view = html.Div([dbc.Card(
            [
                dbc.Row([
                dbc.Col(html.A(dbc.NavLink(' BACK', className='fas fa-arrow-left',
                                           href='/',
                                           style={'color': 'white'}), style={'text-align': 'right'})),
                dbc.Col(html.Iframe(
                    srcDoc='''<!-- TradingView Widget BEGIN -->
                                        <div class="tradingview-widget-container">
                                        <div class="tradingview-widget-container__widget"></div>
                                        <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Price Today</span></a> by TradingView</div>
                                        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
                                        {
                                        "symbol": "''' + data['SYMBOL'] + '''",
                                        "width": "100%",
                                        "locale": "en",
                                        "colorTheme": "dark",
                                        "isTransparent": false
                                        }
                                        </script>
                                        </div>
                                        <!-- TradingView Widget END -->''',
                    style={'width': '100%', 'display': 'table'},
                    className='trade_view_widget',
                ),
                    xs=12, sm=12, md=12, lg=12, xl=12,
                    style={'padding-left': '0', 'padding-right': '0'}
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(html.A(data['USERNAME'],
                                                href=user_link,
                                                style={'text-decoration': 'none',
                                                       'font-size': '150%',
                                                       'color': '#d1d4dc'})),
                                width=12),
                    ],
                ),
                dbc.Col(
                    [
                        html.Br(),
                        trade_view_row(html.P('TRADE TYPE:', style=style_label),
                                       {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'},
                                       html.P(data['TRADE'], id='trade_type_view'),
                                       {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'}),
                        trade_view_row(html.P('SYMBOL:', style=style_label),
                                       {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'},
                                       html.A(data['SYMBOL'], href=symbol_link, id='symbol_view',
                                              style={'text-decoration': 'none', 'color': '#d1d4dc'}),
                                       {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'}),
                        html.Br(),
                        trade_view_row(html.P('QTY:', style=style_label), style_row,
                                       html.P(f"{data['QTY']:,}", id='qty_view'), style_row),
                        trade_view_row(html.P('STRIKES:', style=style_label), style_row,
                                       html.P(data['STRIKES'], id='strikes_view'), style_row),
                        trade_view_row(html.P('EXPIRATION:', style=style_label), style_row,
                                       html.P(data['EXPIRATION'], id='expiry_date_view'), style_row),
                        html.Br(),
                        trade_view_row(html.P('PRICE OPEN:', style=style_label), style_row,
                                       html.P(f"{float(data['OPEN']):,}", id='price_view'), style_row),
                        trade_view_row(html.P('PRICE CLOSED:', style=style_label), style_row,
                                       html.P(f"{float(data['CLOSE']):,}", id='price_closed_view'), style_row),
                        trade_view_row(html.P('COST BASIS:', style=style_label), style_row,
                                       html.P(cost_basis, id='cost_basis_view'), style_row),
                        trade_view_row(html.P('PnL:', style=style_label), style_row,
                                       html.P(pnl_value, id='pnl_view'), style_row),
                        html.Br(),
                        trade_view_row(html.P('DATE OPENED:', style=style_label), style_row,
                                       html.P(data['INPUT DATE'], id='date_open_view'), style_row),
                        trade_view_row(html.P('DATE CLOSED:', style=style_label), style_row,
                                       html.P(data['CLOSE DATE'], id='date_closed_view'), style_row),
                        html.Br(),
                        trade_view_row(html.P('TRADE LENGTH:', style=style_label), style_row,
                                       html.P(str(data['TRADE LENGTH']) + ' days', id='trade_length_view'), style_row),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(html.P('NOTES:', style=style_label), style=style_row),
                                        dbc.Row(html.P(data['NOTES'], id='comment_view'),
                                                style={'display': 'flex', 'padding-bottom': '10px', 'color': '#d1d4dc',
                                                       'font-weight': 'normal'}),
                                        html.Br(),
                                        dbc.Row(html.P('CLOSE COMMENT:', style=style_label), style=style_row),
                                        dbc.Row(html.P(data['CLOSE COMMENT'], id='closing_comment_view'),
                                                style={'display': 'flex', 'padding-bottom': '10px', 'color': '#d1d4dc',
                                                       'font-weight': 'normal'})
                                    ],
                                    width=12
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            dbc.Col(
                                dbc.FormText(f'TRADE ID: {str(trade_id)}', color="secondary"),
                                width=12
                            ),
                        className='mb-1'),
                    ],
                width=12),
                ]),
                comment_btn,
                btn,
            ],
        color='#1e222d',
        style={'font-size': '100%'}),
            ]
        )
        stock_view = html.Div([dbc.Card(
            [
                dbc.Row([
                    dbc.Col(html.A(dbc.NavLink(' BACK', className='fas fa-arrow-left',
                                               href='/',
                                               style={'color': 'white'}), style={'text-align': 'right'})),
                    dbc.Col(html.Iframe(
                        srcDoc='''<!-- TradingView Widget BEGIN -->
                                    <div class="tradingview-widget-container">
                                    <div class="tradingview-widget-container__widget"></div>
                                    <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Price Today</span></a> by TradingView</div>
                                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
                                    {
                                    "symbol": "''' + data['SYMBOL'] + '''",
                                    "width": "100%",
                                    "locale": "en",
                                    "colorTheme": "dark",
                                    "isTransparent": false
                                    }
                                    </script>
                                    </div>
                                    <!-- TradingView Widget END -->''',
                        style={'width': '100%', 'display': 'table'},
                        className='trade_view_widget',
                    ),
                        xs=12, sm=12, md=12, lg=12, xl=12,
                        style={'padding-left': '0', 'padding-right': '0'}
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(html.A(data['USERNAME'],
                                                    href=user_link,
                                                    style={'text-decoration': 'none',
                                                           'font-size': '150%',
                                                           'color': '#d1d4dc'})),
                                    width=12),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Br(),
                            trade_view_row(html.P('TRADE TYPE:', style=style_label),
                                           {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'},
                                           html.P(data['TRADE'], id='trade_type_view'),
                                           {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'}),
                            trade_view_row(html.P('SYMBOL:', style=style_label),
                                           {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'},
                                           html.A(data['SYMBOL'], href=symbol_link, id='symbol_view',
                                                  style={'text-decoration': 'none', 'color': '#d1d4dc'}),
                                           {'display': 'flex', 'padding-bottom': '10px', 'font-size': '110%'}),
                            html.Br(),
                            trade_view_row(html.P('QTY:', style=style_label),
                                           style_row,
                                           html.P(data['QTY'], id='qty_view'),
                                           style_row),
                            html.Br(),
                            trade_view_row(html.P('PRICE OPEN:', style=style_label), style_row,
                                           html.P(f"{float(data['OPEN']):,}", id='price_view'), style_row),
                            trade_view_row(html.P('PRICE CLOSED:', style=style_label), style_row,
                                           html.P(f"{float(data['CLOSE']):,}", id='price_closed_view'), style_row),
                            trade_view_row(html.P('COST BASIS:', style=style_label), style_row,
                                           html.P(cost_basis, id='cost_basis_view'), style_row),
                            trade_view_row(html.P('PnL:', style=style_label), style_row,
                                           html.P(pnl_value, id='pnl_view'), style_row),
                            html.Br(),
                            trade_view_row(html.P('DATE OPENED:', style=style_label), style_row,
                                           html.P(data['INPUT DATE'], id='date_open_view'), style_row),
                            trade_view_row(html.P('DATE CLOSED:', style=style_label), style_row,
                                           html.P(data['CLOSE DATE'], id='date_closed_view'), style_row),
                            html.Br(),
                            trade_view_row(html.P('TRADE LENGTH:', style=style_label), style_row,
                                           html.P(str(data['TRADE LENGTH']) + ' days', id='trade_length_view'), style_row),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Row(html.P('NOTES:', style=style_label), style=style_row),
                                            dbc.Row(html.P(data['NOTES'], id='comment_view'),
                                                    style={'display': 'flex', 'padding-bottom': '10px', 'color': '#d1d4dc',
                                                           'font-weight': 'normal'}),
                                            html.Br(),
                                            dbc.Row(html.P('CLOSE COMMENT', style=style_label), style=style_row),
                                            dbc.Row(html.P(data['CLOSE COMMENT'], id='closing_comment_view'),
                                                    style={'display': 'flex', 'padding-bottom': '10px', 'color': '#d1d4dc',
                                                           'font-weight': 'normal'})
                                        ],
                                        width=12
                                    )
                                ]
                            ),
                            html.Br(),
                            dbc.Row(
                                dbc.Col(
                                    dbc.FormText(f'TRADE ID: {str(trade_id)}', color="secondary"),
                                    width=12
                                ),
                            className='mb-1'),
                        ],
                    width=12),
                ], style={'display': 'flex'}),
                comment_btn,
                btn,
            ],
            color='#1e222d',
            style={'font-size': '100%'}),
            ]
        )
        other_symbol_trades = dbc.Card(
            [
                dbc.Col(dbc.Label(f"OTHER RECENT {str(data['SYMBOL']).upper()} TRADES:", style={'font-size': '160%'}), width=12),
                dbc.Col(data_frame(df_all_symbol_trades), width=12)
            ],
            color='#1e222d', className='df_div')
        if not comments.empty:
            list_of_cards = dbc.Card(comment_cards_list(comments), color='#1e222d')
        else:
            list_of_cards = []

        stock_trades = ['LONG POSITION', 'SHORT POSITION']
        if data['TRADE'] in stock_trades:
            if not list_of_cards:
                return [stock_view, other_symbol_trades]
            else:
                return [stock_view, list_of_cards, other_symbol_trades]
        else:
            if not list_of_cards:
                return [options_view, other_symbol_trades]
            else:
                return [options_view, list_of_cards, other_symbol_trades]
        return None  # add jumbotron in case of error (instead of none)
    except Exception as e:
        return html.Div(
                dbc.Container(
                    [
                        html.H1("Whoops! Something went wrong!", className="display-3"),
                        html.P(
                            "You are attempting to visit a page that does not exist in FoxyFi!",
                            className="lead",
                        ),
                        html.Hr(className="my-2"),
                        html.P(
                            dbc.Button("Go Home", color="secondary", href='/'), className="lead"
                        ),
                    ],
                    fluid=True,
                    className="py-3",
                ),
                className="p-3 bg-warning rounded-3",
            )

def comment_cards_list(comments_df):
    comments_list = comments_df.values.tolist()
    comment_cards = [html.H5('COMMENTS:',style={'color': 'rgb(149, 152, 161)', 'font-weight': 'bold'})]
    for i in comments_list:
        user_link = '/user=' + str(i[2])
        card = dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(html.A(i[2], href=user_link,
                                       style={'font-size': '110%', 'color': 'rgb(149, 152, 161)'}), width=6),
                        dbc.Col(i[1], width=6, style={'text-align': 'right', 'font-size': '110%', 'color': 'rgb(149, 152, 161)'}),
                    ]
                ),
                html.Br(),
                dbc.Row(
                    dbc.Col(i[0], width=12)
                )
            ],
            color='#282d38',
            style={'margin': '0.5rem'}
        )
        comment_cards.append(card)
    return comment_cards


def score_return(score):
    if score < 1000:
        ranking = 'BABY FOX'
    elif score < 5000:
        ranking = 'SILVER FOX'
    elif score < 10000:
        ranking = 'GOLDEN FOX'
    elif score < 15000:
        ranking = 'DIAMOND FOX'
    elif score < 25000:
        ranking = 'TITAN FOX'
    elif score >= 25000:
        ranking = 'SENSEI FOX'
    else:
        ranking = 'NEWBIE'
    return ranking


def user_view(data, all_trades):
    try:
        user_link = '/user=' + str(data['username'])
        user_edit_link = '/edituser=' + str(data['username'])
        btn = ''

        if data['access_type'] == 'foxy':
            username = '💎 ' + str(data['username']) + ' 💎'
            user = dbc.Badge(username, className='ms-1', color='light', href=user_link,
                             style={'text-decoration': 'none',
                                    'width': 'auto',
                                    'font-size': '160%'})
        else:
            user = html.A(data['username'], href=user_link, style={'text-decoration': 'none',
                                                                   'font-size': '160%'})

        if (data['wins'] + data['losses']) != 0:
            win_rate = str(round((data['wins'] / (data['wins'] + data['losses'])) * 100, 2)) + '%'
        else:
            win_rate = '0%'
        if 'username' in session:
            follow = '/follow='+str(data['username'])
            unfollow = '/unfollow='+str(data['username'])
            if data['username'] == session['username']:
                btn = dbc.Button('EDIT PROFILE', id='edit_profile_btn', href=user_edit_link, color='danger', className='me-1 btn-block')
            elif data['username'] != session['username'] and str(session['username']) not in data['followers_list']:
                btn = dbc.Button('FOLLOW', id='follow_btn', href=follow, color='success', className='me-1 btn-block')
            else:
                btn = dbc.Button('UNFOLLOW', href=unfollow, color='danger', className='me-1 btn-block')

        if len(data['followers_list']) > 0:
            display_followers_tooltip = {'display': ''}
        else:
            display_followers_tooltip = {'display': 'none'}
        if len(data['following_list']) > 0:
            display_following_tooltip = {'display': ''}
        else:
            display_following_tooltip = {'display': 'none'}

        ranking = score_return(data['score'])

        df = all_trades.loc[all_trades['USERNAME'] == str(data['username'])]

        user_view = html.Div([dbc.Card(
            [
                dbc.Row([
                dbc.Col(html.A(dbc.NavLink(' BACK', className='fas fa-arrow-left',
                                           href='/',
                                           style={'color': 'white'}), style={'text-align': 'right'})),
                ]),
                dbc.Row([
                    dbc.Col(html.Div(user), width=12),
                    dbc.Col(
                        [
                            html.Br(),
                            dbc.Row(html.P('BADGES:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P('SCORE:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P('RANKING:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P('FOLLOWERS:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P('FOLLOWING:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P('WINS:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P('LOSSES:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P('WIN %:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P('NET PREMIUM YTD:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P('NET PREMIUM:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P('# OF TRADES:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P('AVG. TRADE LENGTH:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                        ],
                        xs=6, sm=5, md=5, lg=4, xl=3,
                        style={'font-weight': 'bold', 'color': '#9598a1'}),
                    dbc.Col(
                        [
                            html.Br(),
                            dbc.Row(html.P(data['badges'], id='badges_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.A(f"{data['score']:,}", id='score_view',
                                           style={'text-decoration': 'none'}),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.A(ranking, id='ranking_view',
                                           style={'text-decoration': 'none'}),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row([html.P(data['followers'], id='followers_view', style={'cursor': 'pointer'}),
                                    dbc.Tooltip(data['followers_list'],
                                                target="followers_view",
                                                placement='right',
                                                style=display_followers_tooltip)],
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row([html.P(data['following'], id='following_view', style={'cursor': 'pointer'}),
                                    dbc.Tooltip(data['following_list'],
                                                target="following_view",
                                                placement='right',
                                                style=display_following_tooltip)],
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P(data['wins'], id='wins_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P(data['losses'], id='losses_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P(win_rate, id='win_rate_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P(f"{data['premium_ytd']:,}", id='premium_ytd_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P(f"{data['premium_overall']:,}", id='premium_overall_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            html.Br(),
                            dbc.Row(html.P(f"{data['number_of_trades']:,}", id='number_of_trades_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P([data['avg_trade_length'], ' days'], id='avg_trade_length_view'),
                                    style={'display': 'flex', 'padding-bottom': '10px'}),
                        ],
                        width='auto'),
                    dbc.Col(
                        [
                            dbc.Row(html.P('BIO:'), style={'display': 'flex', 'padding-bottom': '10px'}),
                            dbc.Row(html.P(data['bio'], id='bio_view', style={'font-weight': 'normal', 'color': 'white'}),
                                    style={'display': 'flex', 'padding-bottom': '10px'}, className='bio_row')
                        ],
                    width=12)
                ]),
                html.Br(),
                dbc.Row(btn),
            ],
        color='#1e222d',
        style={'font-size': '100%',
               'padding': '3rem'}),
        dbc.Card(
            [
                dbc.Col(dbc.Label(f"RECENT TRADES:", style={'font-size': '160%'}), width=12),
                dbc.Col(data_frame(df), width=12)
            ],
            color='#1e222d', className='df_div')]
        )
        return user_view
    except Exception as e:
        return html.Div(
            dbc.Container(
                [
                    html.H1("Whoops! Something went wrong!", className="display-3"),
                    html.P(
                        "You are attempting to visit a page that does not exist in FoxyFi!",
                        className="lead",
                    ),
                    html.Hr(className="my-2"),
                    html.P(
                        dbc.Button("Go Home", color="secondary", href='/'), className="lead"
                    ),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-warning rounded-3",
        )

def stats_view(users, pnl_stats):
    num_users = users['number_of_users']
    num_trades = f"{users['total_num_trades']:,}"
    num_patreons = users['patreons']
    pnl_profit = f"{pnl_stats['total_profit']:,}"
    pnl_lost = f"{pnl_stats['total_loss']:,}"
    overall_pnl = pnl_stats['total_pnl']
    if overall_pnl < 0:
        color = '#FE7676'
    elif overall_pnl > 0:
        color = '#7EFE76'
    else:
        color = 'white'
    overall_pnl = f"{pnl_stats['total_pnl']:,}"

    stats_view = dbc.Card(
        [
            dbc.Row([
            dbc.Col(html.A(dbc.NavLink(' BACK', className='fas fa-arrow-left',
                                       href='/',
                                       style={'color': 'white'}), style={'text-align': 'right'})),
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        html.H2('FOXYFI STATS:'),
                        html.Br(),
                        dbc.Row(html.P(['TOTAL NUMBER OF USERS: ', html.Span(f'{num_users}', style={'color': 'white', 'font-size': '120%'})]),
                                style={'padding-bottom': '10px', 'color': '#d1d4dc'}),
                        dbc.Row(html.P(['TOTAL NUMBER OF ACTIVE PATREONS: ', html.Span(f'{num_patreons}', style={'color': '#7EFE76', 'font-size': '120%'}), ' 🦊']),
                                style={'padding-bottom': '10px', 'color': '#d1d4dc'}),
                        dbc.Row(html.P(['TOTAL NUMBER OF TRADES: ', html.Span(f'{num_trades}', style={'color': 'white', 'font-size': '120%'})]),
                                style={'padding-bottom': '10px', 'color': '#d1d4dc'}),
                        html.Br(),
                        dbc.Row(html.P(['TOTAL OVERALL PnL PROFIT: ', html.Span(f'$ {pnl_profit}', style={'color': '#7EFE76', 'font-size': '120%'})]),
                                style={'padding-bottom': '10px', 'color': '#d1d4dc'}),
                        dbc.Row(html.P(['TOTAL OVERALL PnL LOST: ', html.Span(f'$ {pnl_lost}', style={'color': '#FE7676', 'font-size': '120%'})]),
                                style={'padding-bottom': '10px', 'color': '#d1d4dc'}),
                        dbc.Row(html.P(['TOTAL OVERALL NET PnL: ', html.Span(f'$ {overall_pnl}', style={'color': color, 'font-size': '120%'})]),
                                style={'padding-bottom': '10px', 'color': '#d1d4dc'}),
                    ],
                    xs=12, sm=12, md=12, lg=12, xl=12,
                    style={'font-weight': 'bold', 'color': '#9598a1'}),
            ]),
        ],
    color='#1e222d',
    style={'font-size': '100%',
           'padding': '3rem'})
    return stats_view
