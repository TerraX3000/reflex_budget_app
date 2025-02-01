import reflex as rx
from datetime import date
from enum import Enum as PyEnum
from typing import List, Optional
from sqlmodel import Field, Relationship
from sqlalchemy import Enum


# ✅ TimePeriod Enum
class TimePeriod(PyEnum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    SEMIANNUALLY = "Semiannually"
    ANNUALLY = "Annually"


# ✅ Category Model
class Category(rx.Model, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    description: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # Relationships
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Category.id"},
    )
    children: List["Category"] = Relationship(
        back_populates="parent",
        cascade_delete=True,
    )
    transactions: List["Transaction"] = Relationship(back_populates="category")
    splits: List["Split"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(
        back_populates="category",
        cascade_delete=True,
    )


# ✅ Budget Model
class Budget(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id", nullable=False)
    time_period: TimePeriod = Field(sa_column=Enum(TimePeriod))
    amount: float

    # Relationships
    category: "Category" = Relationship(back_populates="budgets")


# ✅ Account Model
class Account(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    date_field: str
    amount_field: str
    description_field: str
    is_reverse_negative_values: bool

    # Relationships
    transactions: List["Transaction"] = Relationship(
        back_populates="account",
        cascade_delete=True,
    )


# ✅ Transaction Model
class Transaction(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    date: str
    description: str
    category_id: int = Field(foreign_key="category.id", nullable=True)
    account_id: int = Field(foreign_key="account.id", nullable=False)
    gross_amount: float | None = None  # Total before splits
    amount: float  # Net amount (after splits)

    # Relationships
    category: "Category" = Relationship(back_populates="transactions")
    account: "Account" = Relationship(back_populates="transactions")
    splits: List["Split"] = Relationship(
        back_populates="transaction",
        cascade_delete=True,
    )


# ✅ Split Model
class Split(rx.Model, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transaction.id", nullable=False)
    category_id: int | None = Field(default=None, foreign_key="category.id")
    description: str | None = None
    amount: float

    # Relationships
    transaction: "Transaction" = Relationship(back_populates="splits")
    category: Optional["Category"] = Relationship()
