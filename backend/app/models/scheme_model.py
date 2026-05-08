from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String)
    category = Column(String)
    description = Column(Text)
    benefits = Column(Text)
    eligibility = Column(Text)

    keywords = Column(Text)
    eligibility_tags = Column(Text)
    documents_required = Column(Text)

    application_link = Column(String)
    state = Column(String)

    min_age = Column(Integer)
    max_age = Column(Integer)
    max_income = Column(Integer)

    type = Column(String)
    priority = Column(Integer)