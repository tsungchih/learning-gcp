#!/usr/bin/env python

import csv
import datetime
import typing
import argparse
from pydantic import BaseModel
from google.cloud import bigtable
from google.cloud import happybase


class CSVModel(BaseModel):
    """Represent one CSV row from odds message.

    Args:
        o (OrderedDict[str, str]): one row of odds message.
    """
    o: typing.OrderedDict[str, str]


def gen_rowkey(
        sport_id: int,
        league_id: int,
        match_id: int,
        market: str,
        seq: int,
        period: str,
        vendor: str,
        timestamp: int) -> str:
    """Generate a row key based on the following format with ``#`` as the seperator.
    
    <sport_id>#<league_id>#<match_id>#<market>#<seq>#<period>#<vendor>#<timestamp>,
    
    Args:
        sport_id (int): The sport ID.
        league_id (int): The league ID.
        match_id (int): The match ID.
        market (str): The abbriviated market name, e.g., `1x2`, `ah`, `ou`, `ah_1st`, `ou_1st`, etc.
        seq (int): The sequence of the odd pair if more than 1 odd pairs exist in a market.
        period (str): The abbriviated current period, e.g., 1st half (`1h`)/2nd half (`2h`) in soccer, 1st quarter/2nd quarter/... etc. in basketball.
        vendor (str): The vendor from which the odd messages originate.
        timestamp (int): The epoch timestamp of the creation time included in the original odd message.

    Returns:
        str: The row key corresponds to the given input prarmeters.
    """
    rowkey_list = [str(sport_id), str(league_id), str(match_id), market,
                   str(seq), period, vendor, str(timestamp)]
    return ":".join(rowkey_list)


def get_column_dict(model_instance) -> dict:
    """Generate the corresponding column dictionary.

    Args:
        model_instance (CSVModel): The corresponding CSVModel instance to one CSV row from odds message.

    Returns:
        dict: The column dictionary containing odds information corresponding to a CSV row.
    """
    cols = {
        "info": {
            "per": model_instance.o["game_state"],
            "s": model_instance.o["score"],
            "et": model_instance.o["game_time"]
        }
    }
    if model_instance.o["market"].startswith("ah"):
        cols["odds"] = {
            "k": model_instance.o["k"],
            "h": model_instance.o["h"],
            "a": model_instance.o["a"]
        }
    elif model_instance.o["market"].startswith("ou") or \
            model_instance.o["market"].startswith("a-ou") or \
            model_instance.o["market"].startswith("h-ou"):
        cols["odds"] = {
            "k": model_instance.o["k"],
            "ovr": model_instance.o["ov"],
            "und": model_instance.o["ud"]
        }
    else: # csv_model.o["market"] == "1x2"
        cols["odds"] = {
            "h": model_instance.o["h"],
            "a": model_instance.o["a"],
            "d": model_instance.o["d"]
        }
    return cols


def main(project_id: str, instance_id: str, src: str, table_name: str):
    """The main function of this program.
    
    At first, we connect to a Bigtable instance specified by ``project_id`` 
    and ``instance_id``. Then we read rows from the given CSV file and write 
    them into the table specified by ``table_name``.

    Args:
        project_id (str): The target project ID on GCP.
        instance_id (str): The target Bigtable instance ID on GCP.
        src (str): The source CSV file.
        table_name (str): The target table name in the specified Bigtable instance.
    """
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)

    table = connection.table(table_name)

    with open(src, 'r') as csv_file:
        rows = csv.DictReader(csv_file)
        column_name = ""
        for row in rows:
            csv_model = CSVModel(o=row)
            seq = csv_model.o["oddSeq"] if csv_model.o["oddSeq"] else "0"
            ts = int(datetime.datetime.fromisoformat(csv_model.o["created_ts"]).timestamp())
            rowkey = gen_rowkey(
                1,
                213,
                7654321,
                csv_model.o["market"],
                seq,
                "pre" if csv_model.o["game_state"] in ["prematch"] else csv_model.o["game_state"],
                csv_model.o["vendor"],
                ts
            )
            col_dict = get_column_dict(csv_model)
            for family, cols in col_dict.items():
                for k, v in cols.items():
                    column_name = "{fam}:{qualifier}".format(fam=family, qualifier=k)
                    table.put(
                        rowkey, {column_name.encode('utf-8'): v.encode('utf-8')}
                    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'project_id',
        type=str,
        help='Your Cloud Platform project ID.'
    )
    parser.add_argument(
        'instance_id',
        type=str,
        help='ID of the Cloud Bigtable instance to connect to.')
    parser.add_argument(
        'src',
        type=str,
        help='CSV-formated file as the data source.'
    )
    parser.add_argument(
        '--table',
        type=str,
        help='Table to write odd data.',
        default='odds')

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.src, args.table)
