"""Модель базы данных."""
from datetime import datetime
from typing import Any
import os

from sqlalchemy import Column, Integer, String, create_engine, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_HOST = os.environ.get('DB_HOST', '0.0.0.0')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PORT = os.environ.get('DB_USER', '5432')

engine = create_engine(f'postgresql://{DB_NAME}@{DB_HOST}:{DB_PORT}/{DB_USER}')
Base: Any = declarative_base()
Session = sessionmaker(bind=engine)


class Drivers(Base):
    """Модель таблицы Drivers."""

    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор водителя")
    name = Column(String(100), nullable=False, comment="Имя водителя")
    car = Column(String(100), nullable=False, comment="Описание машины водителя")

    def __init__(self, name: str, car: str) -> None:
        """Конструктор."""
        self.name = name
        self.car = car

    def __repr__(self) -> str:
        """Магический метод для таблицы."""
        return f"Имя водителя {self.name} , Описание машины {self.car}"


class Clients(Base):
    """Модель таблицы Clients."""

    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Идентификатор клиента")
    name = Column(String(100), nullable=False, comment="Имя клиента")
    is_vip = Column(Boolean, nullable=False, comment="Vip клиент true/false")

    def __init__(self, name: str, is_vip: bool) -> None:
        """Конструктор."""
        self.name = name
        self.is_vip = is_vip

    def __repr__(self) -> str:
        """Магический метод для таблицы."""
        return f"<Имя клиента {self.name}> + '' + <Vip клиент {self.is_vip}>"


class Orders(Base):
    """Модель таблицы Orders."""

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address_from = Column(String, nullable=False)
    address_to = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    date_created = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    def __init__(self, address_from: str, address_to: str,
                 client_id: int, driver_id: int,
                 date_created: datetime, status: str) -> None:
        """Конструктор."""
        self.address_from = address_from
        self.address_to = address_to
        self.client_id = client_id
        self.driver_id = driver_id
        self.date_created = date_created
        self.status = status


Base.metadata.create_all(engine)
