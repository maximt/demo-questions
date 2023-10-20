import os
from abc import ABC
from functools import cache

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()


def get_database_url():
    return "postgresql://{}:{}@{}/{}".format(
        os.environ.get("POSTGRES_USER"),
        os.environ.get("POSTGRES_PASSWORD"),
        os.environ.get("POSTGRES_SERVER"),
        os.environ.get("POSTGRES_DB")
    )


class DBSession(ABC):

    @staticmethod
    @cache
    def engine():
        return create_engine(get_database_url())

    @staticmethod
    @cache
    def sessionLocal():
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=DBSession.engine()
        )

    @staticmethod
    @cache
    def Base():
        return declarative_base()

    @staticmethod
    @cache
    def create_all():
        DBSession.Base().metadata.create_all(bind=DBSession.engine())
