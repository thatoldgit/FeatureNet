from sqlalchemy import create_engine, Column, ForeignKey, String, Integer, Date, Boolean
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base


db = create_engine("sqlite:///./relations_exported.db")
Base = declarative_base()

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key = True)
    name = Column(String)
    gender = Column (Integer)
    area = Column (Integer)
    external_id = Column(Integer)

    #left_cs = relationship("Collaboration",
    #                        back_populates="left")

    #right_cs = relationship("Collaboration",
    #                        back_populates="right")

    @property
    def collaborations(self):
        return list(self.left_cs) + list(self.right_cs)

    @property
    def collaborators(self):
        return (
                [c.right for c in self.left_cs]
                + [c.left for c in self.right_cs]
            )


    def __init__(self, name, gender, area, external_id = -1):
        self.name = name
        self.gender = gender
        self.area = area
        self.external_id = external_id


class Collaboration(Base):
    __tablename__ = "collaborations"

    id = Column(Integer, primary_key=True)

    left_id = Column(Integer, ForeignKey("artists.id"))
    right_id = Column(Integer, ForeignKey("artists.id"))

    left = relationship("Artist", backref=backref("left_cs"),
                    foreign_keys=[left_id])
    right = relationship("Artist", backref=backref("right_cs"),
                    foreign_keys=[right_id])

    date = Column(Date)
    external_artist_credit_id = Column(Integer)

    is_feature = Column(Boolean)

    def __init__(self, left_id, right_id, date=None, external_id=-1, is_feature = False):
        self.left_id = left_id
        self.right_id = right_id
        self.date = date
        self.external_artist_credit_id = external_id
        self.is_feature = is_feature
