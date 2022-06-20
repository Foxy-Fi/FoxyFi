from collections import OrderedDict
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html

styling_row = {'display': 'list-item', 'margin': '0rem 1.5rem 0rem 1.5rem'}
styling_row_FAQ = {'margin': '1rem 1.5rem 1rem 1.5rem'}

learning_content = {
        'L1': {
            'title': 'What is a "Covered Call"?',
            'text': [
                dbc.Row('A Covered Call is a common strategy that is used to enhance a long stock position. '
                        'The position limits the profit potential of a long stock position by selling a call option '
                        'against the shares. This adds no risk to the position and reduces the cost basis of the '
                        'shares over time.', className='learn_faq_row'),
                dbc.Row('This strategy has a BULLISH directional assumption on the underlying asset and works best '
                        'in HIGH IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('An example would be to BUY 100 SHARES of APPLE and sell 1 AT THE MONEY or 1 OUT OF THE MONEY '
                        'call for every 100 shares owned with a high delta (if you want a higher probability of '
                        'getting assigned and selling the shares or a lower delta if you want to keep the shares '
                        'as much as possible and continue selling calls as they expire. The higher the delta the more '
                        'premium you receive for selling the calls.', className='learn_faq_row'),
                dbc.Row('The maximum amount of profit is calculated as the difference between the pruchasing price of '
                        'the 100 stocks and the price at which the shares were assigned when the Call Option expires '
                        'IN THE MONEY + the Credit Received for the initial sale of the Call Option.',
                        className='learn_faq_row')
            ]
        },
        'L2': {
            'title': 'What is a "Cash Secured Put"?',
            'text': [
                dbc.Row('A Cash Secured Put is a common strategy that has the goal to (1) buy stock below the current '
                        'price or (2) to earn a reasonable return on the cash deposit without taking risk greater than '
                        'owning the underlying stock.', className='learn_faq_row'),
                dbc.Row('Investors who sell cash-secured puts generally are willing to buy the underlying shares of '
                        'stock. Rather than buy the shares at the current price, however, they hope the put will be '
                        'assigned and the shares will be purchased at a lower price.', className='learn_faq_row'),
                dbc.Row('The motivation behind selling Cash Secured Puts is usually to acquire the stock at a lower '
                        'price than its current price.', className='learn_faq_row'),
                dbc.Row('For example, if $XYZ stock was trading at $100 and an investor '
                        'shorted 1 $XYZ 98 put for $2 per share, the investor would need to buy the stock in the event '
                        'that the option is exercised. If the investor shorted a naked put option instead, the above '
                        'scenario would be seen as a negative outcome as the intention of the investor was to profit '
                        'from receiving the premium and not having to buy the shares.', className='learn_faq_row'),
                dbc.Row('The ideal outlook for this strategy is that the stock has a short-term retracement before '
                        'continuing a longer-term rally. Investors should have a neutral/slightly bullish short-term '
                        'view while having a bullish long-term view. Having a short-term bullish view is not ideal '
                        'for this strategy as the retracement may take longer than expected.', className='learn_faq_row'),
                dbc.Row('This strategy works best for investors looking to acquire the stock at a cheaper price than '
                        'the current market price. This strategy supports a “short-term bearish but long-term bullish” '
                        'outlook. By shorting a put and setting aside cash to buy the stock if the put is exercised, '
                        'investors can take advantage of short-term retracements in long-term trends of a stock. While '
                        'the strike price and time to expiration are dependent on the risk tolerance of the investor, '
                        'short-term options with strike prices close to the current price are more ideal for '
                        'this strategy.', className='learn_faq_row'),
            ]
        },
        'L3': {
            'title': 'What is an "Straddle"?',
            'text': [
                dbc.Row('A short straddle is a position that is a neutral strategy that profits from the passage of'
                        'time and any decreases in implied volatility. The short straddle is an '
                        'undefined risk option strategy.', className='learn_faq_row'),
                dbc.Row('This strategy has a NEUTRAL directional assumption on the underlying asset and works best '
                        'in HIGH IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('The strategy is built by SELLING an AT THE MONEY Call Option and SELLING an '
                        'AT THE MONEY Put Option', className='learn_faq_row'),
                dbc.Row('The maximum amount of profit is limited to the credit received when setting up this strategy, '
                        'and the breakevens stand on (1) the short call strike + the credit received on the '
                        'UPSIDE or (2) the short put strike + the credit received on the DOWNSIDE.',
                        className='learn_faq_row'),
                dbc.Row('This strategy is usually recommended to be closed when we reach 25% of our max profit. '
                        'This can increase your win rate over time, as you are taking risk off '
                        'the table and locking in profits. The closing is done by buying the straddle back for 75% of '
                        'the credit received at order entry.', className='learn_faq_row')
            ]
        },
        'L4': {
            'title': 'What is a "Strangle"?',
            'text': [
                dbc.Row('A short strangle is a position that is a neutral strategy that profits when the stock stays '
                        'between the short strikes as time passes, as well as any decreases in implied volatility. '
                        'The short strangle is an undefined risk option strategy.', className='learn_faq_row'),
                dbc.Row('This strategy has a NEUTRAL directional assumption on the underlying asset and works best '
                        'in HIGH IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('The strategy is built by SELLING an OUT OF THE MONEY Call Option and SELLING an '
                        'OUT OF THE MONEY Put Option.', className='learn_faq_row'),
                dbc.Row('The maximum amount of profit is limited to the credit received when setting up this strategy, '
                        'and the breakevens stand on (1) the short call strike + the credit received on the '
                        'UPSIDE or (2) the short put strike + the credit received on the DOWNSIDE.',
                        className='learn_faq_row'),
                dbc.Row('Much like a Straddle spread, this strategy is usually recommended to be closed when we reach '
                        '50% of our max profit. This can increase your win rate over time, as you are taking risk off '
                        'the table and locking in profits. The closing is done by buying the straddle back for 50% of '
                        'the credit received at order entry.', className='learn_faq_row')
            ]
        },
        'L5': {
            'title': 'What is an "Iron Condor"?',
            'text': [
                dbc.Row('An iron condor is a directionally neutral, defined risk strategy that profits from the '
                        'underlying trading in a range, through the expiration of the options contract. It’s made up '
                        'of a short vertical put spread and a short vertical call spread in a single transaction, in '
                        'the same expiration.', className='learn_faq_row'),
                dbc.Row('Simply put, an iron condor is a short strangle with long options that are purchased further '
                        'OUT OF THE MONEY (OTM) to define your risk. Just like with a strangle, this is a great way '
                        'to get exposure to stock without taking a directional position. It benefits from the passage '
                        'of time and any decreases in implied volatility (IV). It’s also a way of potentially playing '
                        'a non-movement and a volatility contraction going into earnings.', className='learn_faq_row'),
                dbc.Row('This strategy has a NEUTRAL directional assumption on the underlying asset and works best '
                        'in HIGH IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('An Iron Condor is a defined risk strategy that profits the most from a stock trading within a '
                        'specific range until the expiration of the options. It therefore benefits from the passing '
                        'of time (theta decay) and any decreases in implied volatility on the underlying asset.',
                        className='learn_faq_row'),
                dbc.Row('An example would be to SELL a bearish OUT OF THE MONEY Vertical Call Spread and SELL a '
                        'bullish OUT OF THE MONEY Vertical Put Spread.', className='learn_faq_row'),
                dbc.Row('The maximum amount of profit is limited to the credit received when setting up this strategy.',
                        className='learn_faq_row'),
                dbc.Row('Much like other standard premium generating option selling strategies, this strategy is '
                        'usually recommended to be closed when we reach 50% of our max profit. This can increase '
                        'your win rate over time, as you are taking risk off the table and locking in profits.',
                        className='learn_faq_row')
            ]
        },
        'L6': {
            'title': 'What is an "Iron Butterfly (Iron Fly)"?',
            'text': [
                dbc.Row('An Iron Fly is essentially an Iron Condor with call and put credit spreads that share the '
                        'same short strike. This creates a very neutral position that profits from the passage of '
                        'time and any decreases in implied volatility. An Iron Fly is synthetically the same as a '
                        'long butterfly spread using the same strikes.', className='learn_faq_row'),
                dbc.Row('This strategy has a NEUTRAL directional assumption on the underlying asset and works best '
                        'in HIGH IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('An example would be to BUY an OUT OF THE MONEY Put Option, SELL a STRADDLE, and BUY an '
                        'OUT OF THE MONEY Call Option', className='learn_faq_row'),
                dbc.Row('The maximum amount of profit is limited to the credit received when setting up this strategy, '
                        'and the breakevens stand on (1) the short call strike + the credit received on the '
                        'UPSIDE or (2) the short put strike + the credit received on the DOWNSIDE.',
                        className='learn_faq_row'),
                dbc.Row('Much like a Straddle spread, this strategy is usually recommended to be closed when we reach '
                        '25% of our max profit. This can increase your win rate over time, as you are taking risk off '
                        'the table and locking in profits.', className='learn_faq_row')
            ]
        },

        'L7': {
            'title': 'What is a "Poor Man Covered Call"?',
            'text': [
                dbc.Row('A "Poor Man’s Covered Call" is a Long Call Diagonal Debit Spread that is used to replicate'
                        'a Covered Call position. The strategy gets its name from the reduced risk and capital'
                        'requirement relative to a standard covered call.', className='learn_faq_row'),
                dbc.Row('This strategy has a BULLISH directional assumption on the underlying asset and works best '
                        'in LOW IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('An example would be to BUY an IN THE MONEY Call Option with a longer term expiration '
                        'and SELL an OUT OF THE MONEY Call option with a shorter term expiration.',
                        className='learn_faq_row'),
                dbc.Row('The maximum amount of profit is the width of the call strikes minus the debit paid to open '
                        'this strategy (cost of the long call Option minus credit received for the short call '
                        'option, and its breakeven stands at the long call option strike plus the premium cost of '
                        'opening this strategy.', className='learn_faq_row'),
                dbc.Row('In the best case scenario, a PMCC will be closed for a winner if the stock price increases '
                        'significantly in one expiration cycle. This is because the call options will trade close to '
                        'intrinsic value and the profit potential for the trade will diminish.', className='learn_faq_row')
            ]
        },
        'L8': {
            'title': 'What is a "Jade Lizard"?',
            'text': [
                dbc.Row('A Jade Lizard is a slightly bullish strategy that combines a short put and a short call '
                        'spread. The strategy is created to have no upside risk, which is done by collecting a total '
                        'credit greater than the width of the short call spread.', className='learn_faq_row'),
                dbc.Row('This strategy has a NEUTRAL directional assumption on the underlying asset and works best '
                        'in HIGH IMPLIED VOLATILITY environments.', className='learn_faq_row'),
                dbc.Row('The strategy is composed by SELLING an OUT OF THE MONEY Put Option '
                        'and SELLING an OUT OF THE MONEY vertical Call Spread (selling an OTM call and buying an '
                        'even further OTM call).', className='learn_faq_row'),
                dbc.Row('Max profit is realized when the stock price is between the short strikes at expiration.',
                        className='learn_faq_row'),
                dbc.Row('The trade is most often closed by purchasing the options back for a net debit that is less '
                        'than the credit collected when the trade was opened. The first profit target is usually 50% '
                        'of max profit, or half of the credit that was initially received at order entry.',
                        className='learn_faq_row')
            ]
        },
        None: {
            'title': '',
            'text': ''
        },
    }

faq_content = {
        'Q1': {
            'title': 'Can I upload trades I have done in the past to my profile?',
            'text': [dbc.Row('Absolutely. All Patreons have access to Discord. In Discord there is a channel called '
                             '"FoxyFi User Requests" specifically made for users to make special requests.',
                             className='learn_faq_row'),
                     dbc.Row('One of the requests you can make is ask for a mass history trade upload.',
                             className='learn_faq_row'),
                     dbc.Row('I will give you a Google Spreadsheet with the columns that are required for you to fill '
                             'in and send back to me and i will run a script to add them to the Database.',
                             className='learn_faq_row')]
        },
        'Q2': {
            'title': 'Can I delete my trades?',
            'text': [dbc.Row('There are RARE exceptions to this rule but the answer is "No you cannot."',
                             className='learn_faq_row'),
                     dbc.Row('FoxyFi is there as a free platform for users to have a bit of a fun '
                             'competition and learn to become more emotionally confident with their trades.',
                             className='learn_faq_row'),
                     dbc.Row('Part of this learning process is also to own up to your loosing trades.',
                             className='learn_faq_row'),
                     dbc.Row('There is nothing wrong with loosing and nobody should be judging loosing trades '
                             'on this platform. Most loosing trades come from emotional attachment to the trade '
                             'which make the trader close and realize the losses out of fear.',
                             className='learn_faq_row'),
                     dbc.Row('Now...you should not be married to your loosing trades so at times we need to cut '
                             'our losses and move to the next trade.',
                             className='learn_faq_row'),
                     dbc.Row('These are an important part of the learning process and thus you should own up to them '
                             'as much as you should own up to your winning trades.',
                             className='learn_faq_row'),
                     dbc.Row('Plus, if you were able to just delete trades...if you were to delete all losing trades '
                             'you would end up with completely wrong Win% and PnL stats which would be a shame not only'
                             ' to FoxiFy users but especially a shame since you would be lieing to yourself as well.',
                             className='learn_faq_row')]
        },
        'Q3': {
            'title': 'What if I submitted a wrong trade or a typo? Can I edit my trade?',
            'text': [dbc.Row("Unfortunately you can't edit the trades yourself.",
                             className='learn_faq_row'),
                     dbc.Row("If you are a Patreon you can make exception requests on Discord that will be looked "
                             "at for its merits one by one, but this should be an exception!",
                             className='learn_faq_row'),
                     dbc.Row("If you end up making requests too often they will end up being disregarded, and if you "
                             "are coming across as pushy or unfair to the rest of the community your user account "
                             "will end up being suspended/banned.",
                             className='learn_faq_row'),
                     dbc.Row('Having said this...if you really made a typo and if you are not a Patreon then you '
                             'can always close the trade for 0 (zero) PnL and write in your closing comments that this '
                             'trade was a type. Then you can open up a new one with the correct inputs! :)',
                             className='learn_faq_row')]
        },
        'Q4': {
            'title': 'How does the points and ranking system work in FoxyFi?',
            'text': [dbc.Row("The FoxyFi platform awards you points for every trade you submit and every trade you"
                             "close.",
                             className='learn_faq_row'),
                     dbc.Row("To award you for the fact that you cannot delete your losing trades you get 250 points "
                             "for every winning trade you close.",
                             className='learn_faq_row'),
                     dbc.Row("You also get 100 points for every new trade you open and submit to the platform.",
                             className='learn_faq_row'),
                     dbc.Row('These points translate into your ranking. Now...this should not be seen as a competition '
                             'but rather more as a fun way to reward your loyalty to FoxyFi and your "EXPERIENCE".',
                             className='learn_faq_row'),
                     dbc.Row('Which means the more trades you submit and the more successful you are as a trader '
                             'on FoxFi the higher your ranking will be.',
                             className='learn_faq_row'),
                     dbc.Row('Currently the rankings are -BABY FOX- if you are under 1000 points, -SILVER FOX- if you '
                             'are within 1000 and 5000 points, -GOLDEN FOX- if you are within 5000 and 10000 points, '
                             '-DIAMOND FOX- if you are within 10000 and 15000 points,  -TITAN FOX- if you are within '
                             '15000 and 25000 points, and finally -SENSEI FOX- if you are over 25000 points!',
                             className='learn_faq_row')]
        },
        'Q5': {
            'title': 'But Foxy...what prevents users from cheating to get more points?',
            'text': [dbc.Row("I have thought about that...and honestly the conclusion i have reached is it does "
                             "not really matter.",
                             className='learn_faq_row'),
                     dbc.Row("Since there is nothing to win from this ranking, if someone is there just to cheat on "
                             "his score that user will either get caught ny the community by submitting too many "
                             "strange winning trades in a short period of time (or weird strikes, close prices, etc) "
                             "or eventually the cheater will just get bored from doing so since it adds no value and "
                             "would be rather time consuming to keep doing so.",
                             className='learn_faq_row')]
        },

        # 'Q6': {
        #     'title': 'Is FoxyFi FREE??',
        #     'text': [dbc.Row("FoxyFi is a 100% FREE website with NO ADS whatsoever!",
        #                      className='learn_faq_row'),
        #              dbc.Row('The website is 100% supported by me "Foxy" and by the most amazing generous Patreons '
        #                      'that subscribe to the FoxyFi Tier for USD 10 helping maintain the costs of the database ,'
        #                      'website hosting, domain fees, etc.',
        #                      className='learn_faq_row'),
        #              dbc.Row('There are no limits on how many Patreons can subscribe to the USD 10 tier and the only '
        #                      'tier change will be in the future a slightly more rewarding tier that will have physical '
        #                      'rewards such as T-SHIRT, PINS, STICKERS, hoodies with the FoxyFi logo!',
        #                      className='learn_faq_row'),
        #              dbc.Row('But do not feel pressured to subscribe. If you cannot afford to become a Patreon you '
        #                      'can still use the website and its many functionalities 100% for FREE and participate in '
        #                      'the live streams or watch the content i will keep creating on YouTube whether on the '
        #                      'investment and my portfolio update front, or on how to learn to use Python and create '
        #                      'stuff like the FoxyFi website or produce technical analysis on stocks, etc.',
        #                      className='learn_faq_row')]
        # },
        # 'Q7': {
        #     'title': 'What do I get as a Patreon?',
        #     'text': [dbc.Row("To thank you for your absolutely awesome support you get the following perks and "
        #                      "rewards for becoming a Patreon:",
        #                      className='learn_faq_row'),
        #              dbc.Row('(1) Access to the Discord community that we FoxyFi is growing tightly where we share '
        #                      'our trades, investment ideas, have fun discussing markets and other stuff, get notified '
        #                      'on YouTube content release, and where you can ask Foxy how to learn to code and create '
        #                      'stuff like this website.',
        #                      className='learn_faq_row'),
        #              dbc.Row('(2) You are able to ask for your historical trades to be added to your user profile in '
        #                      'the FoxyFi database to be seen by all.',
        #                      className='learn_faq_row'),
        #              dbc.Row('(3) You can make suggestions and requests directly to Foxy for upcoming upgrades '
        #                      'to the FoxyFi website.',
        #                      className='learn_faq_row'),
        #              dbc.Row('(4) You get special flair for your USERNAME on the FoyFi platform! Your username becomes '
        #                      'a badge and you can request Foxy on Discord to add two emojis to your website username '
        #                      'flair!!',
        #                      className='learn_faq_row'),
        #              dbc.Row('(5) You get your name shouted out on every upcoming YouTube content video i will make '
        #                      'in the future and you get my eternal gratitude to help me support and continue hosting '
        #                      'this site and creating content like this!',
        #                      className='learn_faq_row')]
        # },
        None: {
            'title': 'What is FoxyFi?',
            'text': [html.Span('FoxyFi is a social media trading platform made by ', style={'font-size': '130%'}),
                            dbc.Badge("@foxy", color="info", className="me-1 text-decoration-none", href='/user=foxy',
                                      style={'font-size': '100%'}),
                            html.Span(", where you can ", style={'font-size': '130%',
                                                                 'margin-bottom': '2rem'}),
                            html.Span("register", style={'font-size': '130%',
                                                         'margin-bottom': '2rem',
                                                         'color': 'rgb(255, 128, 0)'}),
                            html.Span(" and:", style={'font-size': '130%', 'margin-bottom': '2rem'}),
                            dbc.Row("Share your trades and favorite trading ideas.", style=styling_row),
                            dbc.Row("Follow and be followed by other traders.", style=styling_row),
                            dbc.Row("Interact/comment yours and other people's trades.", style=styling_row),
                            dbc.Row("Interactively track/compare your PnL, Win% Rate, Cost Basis and other statistics "
                                    "from your trading profile.", style=styling_row),
                            dbc.Row("Easily obtain news, financials and technical analysis on your favorite stocks, "
                                    "ETF's, cryptos, etc.", style=styling_row),
                            dbc.Row("Earn points/ranking as you input your trades, record your wins and "
                                    "losses, and grow as a trader.", style=styling_row),
                            dbc.Row("Become part of the FoxyFi community and share your views, trades, "
                                    "and ideas on Discord!", style=styling_row),
                            html.Div(style={'margin-bottom': '1rem', 'text-align': 'justify'})]
        },
    }
