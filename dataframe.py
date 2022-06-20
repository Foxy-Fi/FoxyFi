import dash_bootstrap_components as dbc
from dash import html

def column(data, link, font_size, font_weight, white_space, align, font_color, text_decorator, border):
    return dbc.Col(
                html.A(data,
                       href=link,
                       style={
                           'font-size': font_size,
                           'font-weight': font_weight,
                           'margin-bottom': '0',
                           'overflow': 'visible',
                           'white-space': white_space,
                           'word-break': 'normal',
                           'text-align': align,
                           'color': font_color,
                           'text-decoration': text_decorator,
                       },
                       id='data_tbl_txt',
                       className = 'df_row'
                       ),
                style={
                    'border-bottom': border,
                    'width': '2rem',
                    'height': '2rem',
                    'display': 'grid',
                    'justify-content': 'center',
                    'align-content': 'center',
                    'flex-direction': 'column',
                    'padding-right': '0',
                },
            )


def data_frame(data):
    df = data
    try:
        len(df['USER COMMENTS'])
        df.loc[df['USER COMMENTS'].notnull(), 'USERNAME'] = '💬 ' + df['USERNAME']
    except Exception as e:
        print(e)

    df['TRADE_ID'] = df.index
    df = df[['TRADE_ID', 'USERNAME', 'TRADE', 'SYMBOL', 'QTY', 'STRIKES', 'EXPIRATION', 'OPEN', 'CLOSE', 'C.B.', 'PnL']]
    data_frame = []
    centering_index = [2, 3, 4, 5, 6, 7, 8, 9]
    list_of_cols = []
    index = 0
    columns = list(df.columns)
    for i in columns[1:]:
        align = 'left'
        if index in centering_index:
            align = 'center'
        list_of_cols.append(
            column(i, None, '', 'bold', 'nowrap', align, '#9598a1', None, '3px #252d43 solid'),
        )
        index += 1
    # list_of_cols.append(column('', None, '', 'bold', 'nowrap', align, '#d1d4dc', None, '3px #252d43 solid')) # adding 1 last column with no header for the view button
    data_frame.append(dbc.Row(list_of_cols))

    df_data_list = df.values.tolist()
    for i in df_data_list:
        list_of_cols = []
        index = 0
        trade_id_link = i[0]
        pnl = float(i[10])
        for n in i[1:]:
            align = 'left'
            if pnl == 0:
                font_color = '#d1d4dc'
            else:
                font_color = 'black'
            if index in centering_index:
                align = 'center'
            if index == 0:
                if '💬 ' in str(n):
                    n_link = str(n)[2:]
                else:
                    n_link = str(n)
                list_of_cols.append(
                    column(n, f'/user={n_link}', '', 'bold', 'nowrap', align, font_color, None, '3px #252d43 solid'),
                )
            elif index == 2:
                list_of_cols.append(
                    column(n, f'/ticker={n}', '', 'bold', 'wrap', align, font_color, None,
                           '3px #252d43 solid'),
                )
            elif index == 5:
                list_of_cols.append(
                    column(n, f'/tradeid={trade_id_link}', '', 'bold', 'nowrap', align, font_color, 'none', '3px #252d43 solid'),
                )
            else:
                list_of_cols.append(
                    column(n, f'/tradeid={trade_id_link}', '', 'bold', 'wrap', align, font_color, 'none', '3px #252d43 solid'),
                )
            index += 1

        bg_color = ''
        if pnl is not None:
            if pnl > 0:
                bg_color = '#7EFE76'
            elif pnl < 0:
                bg_color = '#FE7676'

        data_frame.append(dbc.Row(list_of_cols, id=trade_id_link, style={'background-color': bg_color, 'height': '1.95rem'}))
    return data_frame