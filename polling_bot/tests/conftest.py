import glob
import os

import pytest
#
# from vip_admin.main_config import DbConfig, HERE
# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import Session
# from vip_admin.database.base import Base
#
#
# @pytest.fixture(scope='session')
# def engine():
#     return create_engine(DbConfig.database_url)
#
#
# @pytest.yield_fixture(scope='session')
# def tables(engine):
#     Base.metadata.create_all(engine)
#     yield
#     # Base.metadata.drop_all(engine)
#     # database = glob.glob(HERE + '/*.db').pop()
#     # os.remove(database)
#
#
# @pytest.yield_fixture
# def dbsession(engine, tables):
#     """Returns an sqlalchemy session, and after the test tears down everything properly."""
#     session = Session(bind=engine)
#
#     yield session
#     session.rollback()
