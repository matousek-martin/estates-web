from flask_sqlalchemy import declarative_base

from app import db


Base = declarative_base()
Base.metadata.bind = db.engine


class Estates(Base):
    __tablename__ = 'silver_estates_web'
    __table_args__ = {'autoload': True}

    # Aliases for columns with white space in name for querying
    price = db.Column('Celková cena', db.String)
    area_m2 = db.Column('Užitná plocha', db.Integer)
    floor = db.Column('Podlaží', db.String)
    building_type = db.Column('Stavba', db.String)
    building_state = db.Column('Stav objektu', db.String)
    price_details = db.Column('Poznámka k ceně', db.String)
    efficiency = db.Column('Energetická náročnost budovy', db.String)
    ownership = db.Column('Vlastnictví', db.String)
    furnishing = db.Column('Vybavení', db.String)
    elevator = db.Column('Výtah', db.String)

    def __repr__(self):
        return '<Estate {}>'.format(self.estate_id)


class EstateImages(Base):
    __tablename__ = 'silver_estate_images'
    __table_args__ = {'autoload': True}

    def __repr__(self):
        return '<Image {}>'.format(self.image_id)
