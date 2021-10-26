import modules.load_data_from_database as ldd
from db import connect_db

# connection with database
rdb = connect_db()


def table(df, group):


    table_summary = df.round(2)
    if group == 'M': index = 'month'
    elif group == 'W': index = 'week'
    elif group == 'DOW': index = ['DOW','DOW_number']
    else: index = 'date'

    if group == 'DOW':
        table_summary = table_summary.pivot(index=index, columns='name', values='Value') \
            .reset_index().sort_values(by=['DOW_number']).drop(columns=['DOW_number'])
    else:
        table_summary = table_summary.pivot(index=index, columns='name', values='Value') \
            .reset_index()

    return table_summary
