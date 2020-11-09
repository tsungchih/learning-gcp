#!/usr/bin/env python


import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--projectid", 
        action="store",
        help="The project ID on GCP.")
    parser.addoption(
        "--instanceid",
        action="store",
        help="The instance ID of Bigtable on GCP.")
    parser.addoption(
        "--tablename",
        action="store",
        help="The table name in Bigtable on GCP."
    )


@pytest.fixture(scope="class")
def projectid(request):
    return request.config.getoption("--projectid")


@pytest.fixture(scope="class")
def instanceid(request):
    return request.config.getoption("--instanceid")


@pytest.fixture(scope="class")
def tablename(request):
    return request.config.getoption("--tablename")
