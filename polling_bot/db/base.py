# In the name of God

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from polling_bot.config import Config

engine = create_engine(Config.database_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()
