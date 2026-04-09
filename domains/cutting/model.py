from sqlalchemy import Column, Integer, String
from database import Base


class CuttingScheme(Base):
    __tablename__ = "cutting_schemes"

    id = Column(Integer, primary_key=True)
    pipe_name = Column(String)
    pipes_in = Column(Integer)
    post = Column(Integer)


class CuttingSchemeOutput(Base):
    __tablename__ = "cutting_scheme_outputs"

    id = Column(Integer, primary_key=True)
    scheme_id = Column(Integer)
    detail_article = Column(Integer)
    quantity = Column(Integer)