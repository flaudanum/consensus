import pandas as pd

from consensus.alternative import Alternative
from consensus.group import Group


def pd_payoff_table(payoff_result: list[list], group: Group):
    # List of records for building the table
    records = {}

    for row in payoff_result:
        alternative: Alternative = row[0]
        records[alternative.name] = row[1:]

    # Sets table columns' names
    column_names = sorted(group.members)
    column_names.append("payoff")

    # Creates a table
    df_out =  pd.DataFrame.from_dict(records, orient="index", columns=column_names)

    # Sorts the table by alternative name
    df_out.sort_index(inplace=True)

    # Then sorts the table by payoff values
    df_out.sort_values(by=["payoff"], ascending=False, inplace=True)
    return df_out

