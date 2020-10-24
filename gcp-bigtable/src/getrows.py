#!/usr/bin/env python


import argparse
import models
import time
from google.cloud import bigtable
from google.cloud import happybase
from pydantic import BaseModel
from typing import List


def get_table_instance(project_id: str, instance_id: str, table_name: str) -> happybase.table.Table:
    """Create a table instance according to the given ``project_id``, ``instance_id``, and ``table_name``.

    This function create a table instance for reading/writing data.

    Args:
        project_id (str): The project ID on GCP.
        instance_id (str): The Bigtable instance ID on GCP.
        table_name (str): The target table name in Bigtable on GCP.

    Returns:
        happybase.Table: A table instance.
    """
    start = time.time()
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    connection = happybase.Connection(instance=instance)
    table = connection.table(table_name)
    end = time.time()
    print("Elapsed time for getting table instance: {}s".format(end - start))
    return table


def _get_row_json(rowkey: str, sep: str) -> dict:
    """Generate a dictionary from the given ``row_obj``.

    Args:
        rowkey (str): A given row key.
        sep (str): The delimiter used in the given ``rowkey``.

    Returns:
        dict: [description]
    """
    keys = ["sid", "lid", "mid", "mkt", "seq", "per", "vendor", "ts"]
    row_dict = dict(zip(keys, rowkey.split(sep)))
    row_dict["info"] = {}
    row_dict["odds"] = {}
    return row_dict


def _get_target_column_list(market: str) -> list:
    """Generate a column list according to the ``market``.
    
    Each market has its own column list. This function generates the corresponding list 
    of column qualifiers in terms of the given ``market``.

    Args:
        market (str): The given market such as `1x2`, `ah`, `ou` etc.

    Returns:
        list: A list of column qualifiers.
    """
    odds_1x2_cols = ["h", "a", "d"]
    odds_ah_cols = ["k", "h", "a"]
    odds_ou_cols = ["k", "ovr", "und"]
    target_cols = []
    if market.startswith("1x2"):
        target_cols = odds_1x2_cols
    elif market.startswith("ah"):
        target_cols = odds_ah_cols
    else:
        target_cols = odds_ou_cols
    return target_cols


def _get_single_row(table_instance, rowkey: str, sep: str = "#") -> models.ModelOddBasicInfo:
    """Get a single row matching the given ``rowkey``.

    This function tries to get a single row from the given ``table_instance`` 
    according to the ``rowkey``.

    Args:
        table_instance ([type]): A given table instance.
        rowkey (str): A given row key.
        sep (str, optional): The delimiter used in the given ``rowkey``. Defaults to "#".

    Returns:
        models.ModelOddBasicInfo: The data model corresponding to the query result.
    """
    info_list: list = ["s", "per", "et"]
    key = rowkey.encode('utf-8')
    row = table_instance.row(key)
    row_json = _get_row_json(rowkey, sep)
    row_model = models.ModelOddBasicInfo(**row_json)
    for col in info_list:
        col_name = ":".join(["info", col])
        row_json["info"][col] = row[col_name.encode("utf-8")]
    row_info_model = models.OddInfoModel(**row_json["info"])

    target_cols = _get_target_column_list(row_json["mkt"])
    for col in target_cols:
        col_name = ":".join(["odds", col])
        row_json["odds"][col] = row[col_name.encode("utf-8")]
    
    odd_model = None
    if row_json["mkt"].startswith("1x2"):
        odd_model = models.ColumnModel1x2(**row_json["odds"])
    elif row_json["mkt"].startswith("ah"):
        odd_model = models.ColumnModelAH(**row_json["odds"])
    else:
        odd_model = models.ColumnModelOU(**row_json["odds"])

    row_model.info = row_info_model
    row_model.odds = odd_model
    return row_model


def get_rowkeys(table_name: str, rowkeys: List[str]):
    """Query table with respect to given ``table_name`` and ``rowkeys``.

    Given at least one element in `rowkeys`, this function queries the 
    target table in Bigtable to retrieve the corresponding columns.

    Args:
        table_name (str): The table name to query.
        rowkeys (List[str]): A list of rowkeys to query.
    """
    pass


def scan_rows_range(start: str, end: str):
    """

    Given start row key and end row key, this function queries the 
    target table

    Args:
        start (str): [description]
        end (str): [description]
    """
    pass


def main(project_id: str, instance_id: str, table_name: str, rowkey: str, start_rowkey: str, end_rowkey: str) -> None:
    """The main function of ``getrows`` program.

    This main function takes 6 parameters 

    Args:
        project_id (str): [description]
        instance_id (str): [description]
        table_name (str): [description]
        rowkey (str): [description]
        start_rowkey (str): [description]
        end_rowkey (str): [description]
    """
    table = get_table_instance(project_id, instance_id, table_name)
    if rowkey:
        start = time.process_time()
        model = _get_single_row(table, rowkey, sep = ":")
        end = time.process_time()
        print("Elapsed time for getting single row: {}s".format(end - start))
        print(model.dict())
    else:
        pass


if __name__ == "__main__":
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
        '--table',
        type=str,
        help='Table to write odd data.',
        default='odds')
    parser.add_argument(
        '--rowkey',
        type=str,
        help="A given row key with \"#\" as seperator. Once specified, \
            \'--start-rowkey\' and \'--end-rowkey\' will have no effect.",
        default=""
    )
    parser.add_argument(
        "--start_rowkey",
        type=str,
        help="The start row key for range search based on row key. Once \
            specified, \'--rowkey\' must not be given.",
        default=""
    )
    parser.add_argument(
        "--end_rowkey",
        type=str,
        help="The end row key for range search based on row key. This \
            parameter must be used against \'--start-rowkey\'.",
        default=""
    )

    args = parser.parse_args()
    main(args.project_id, args.instance_id, args.table,
         args.rowkey, args.start_rowkey, args.end_rowkey)
