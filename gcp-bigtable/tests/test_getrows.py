#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest
from typing import List
from getrows import get_rowkeys
from getrows import get_table_instance
from getrows import scan_rows_range


class TestGetrows(object):
    @pytest.fixture(scope="class")
    def rowkey(self):
        return ["1:213:7654321:ou:0:pre:betradar:1595906157"]
    
    
    @pytest.fixture(scope="class")
    def rowkeys(self):
        rowkeys = [
            "1:213:7654321:ou:0:pre:betradar:1595906157",
            "1:213:7654321:ou:0:pre:bet188:1595904940",
            "1:213:7654321:ou:0:pre:bet188:1595903291",
            "1:213:7654321:ou:0:pre:betradar:1595880201"
        ]
        return rowkeys


    @pytest.fixture(scope="class")
    def start_rowkey_single_vendor(self):
        return "1:213:7654321:ou:0:pre:betradar:0"
    
    
    @pytest.fixture(scope="class")
    def stop_rowkey_single_vendor(self):
        return "1:213:7654321:ou:0:pre:betradar:z"


    @pytest.fixture(scope="class")
    def table_instance(self, projectid, instanceid, tablename):
        table = get_table_instance(projectid, instanceid, tablename)
        return table


    def test_get_single_rowkey(self, table_instance, rowkey: List[str]):
        assert len(rowkey) == 1
        result_models = get_rowkeys(table_instance, rowkey, sep = ":")
        assert len(result_models) == 1


    def test_get_multiple_rowkeys(self, table_instance, rowkeys: List[str]):
        assert len(rowkeys) > 1
        result_models = get_rowkeys(table_instance, rowkeys, sep = ":")
        assert len(result_models) > 1
    
    def test_row_scan_single_vendor(
        self,
        table_instance,
        start_rowkey_single_vendor,
        stop_rowkey_single_vendor
    ):
        result_models = scan_rows_range(
                                        table_instance,
                                        start_rowkey_single_vendor,
                                        stop_rowkey_single_vendor,
                                        sep = ":")
        assert len(result_models) > 1