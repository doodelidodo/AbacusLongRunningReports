from xmlrpc.client import Boolean
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# SQLite-Datenbank erstellen
engine = create_engine('sqlite:///LongRuningReports.sqlite', echo=True)

# Basisdeklaration für ORM-Objekte erstellen
Base = declarative_base()


# ORM-Klasse für Tabelle definieren
class Table(Base):
    __tablename__ = 'LongRuningReports'

    TimeStamp = Column(DateTime, primary_key=True)
    User = Column(String)
    Report = Column(String)
    ReportPfad = Column(String)
    done = Column(Integer)
    Finds = Column(Integer)
    Rows = Column(Integer)
    Kriterien = Column(String)
    Run = Column(String)
    ReportTyp = Column(String)

# Tabelle erstellen
Base.metadata.create_all(engine)
