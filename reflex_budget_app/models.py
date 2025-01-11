import reflex as rx
from sqlmodel import Field
from datetime import date


class Transaction(rx.Model, table=True):
    date: date
    description: str
    amount: float
    category: str
