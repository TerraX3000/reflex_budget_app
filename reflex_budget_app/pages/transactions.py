import reflex as rx
from ..models import Transaction
from ..templates import template
from sqlmodel import select
from typing import List
from reflex_ag_grid import ag_grid
import pandas as pd


def card() -> rx.Component:
    return (
        rx.card(
            rx.data_list.root(
                rx.data_list.item(
                    rx.data_list.label("Status"),
                    rx.data_list.value(
                        rx.badge(
                            "Authorized",
                            variant="soft",
                            radius="full",
                        )
                    ),
                    align="center",
                ),
                rx.data_list.item(
                    rx.data_list.label("ID"),
                    rx.data_list.value(rx.code("U-474747")),
                ),
                rx.data_list.item(
                    rx.data_list.label("Name"),
                    rx.data_list.value("Developer Success"),
                    align="center",
                ),
                rx.data_list.item(
                    rx.data_list.label("Email"),
                    rx.data_list.value(
                        rx.link(
                            "success@reflex.dev",
                            href="mailto:success@reflex.dev",
                        ),
                    ),
                ),
                rx.data_list.item(
                    rx.data_list.label("Company"),
                    rx.data_list.value(
                        rx.link(
                            "Reflex",
                            href="https://reflex.dev",
                        ),
                    ),
                ),
            ),
        ),
    )


class FormState(rx.State):
    form_data: dict = {}
    entries: List["Transaction"] = []

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        form_data["amount"] = float(form_data["amount"])
        self.form_data = form_data
        with rx.session() as session:
            db_entry = Transaction(**form_data)
            print(db_entry)
            session.add(db_entry)
            session.commit()
            self.list_entries()
            yield

    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(select(Transaction)).all()
            self.entries = entries


def transaction_form() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(
                    name="date",
                    type="date",
                ),
                rx.input(
                    placeholder="Description",
                    name="description",
                ),
                rx.input(
                    placeholder="Amount",
                    type="number",
                    name="amount",
                ),
                rx.select(
                    ["Food", "Transportation", "Housing"],
                    name="category",
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(),
        rx.heading("Results"),
        rx.text(FormState.form_data.to_string()),
    )


df = pd.read_csv("assets/wind_dataset.csv")

column_defs = [
    ag_grid.column_def(field="direction"),
    ag_grid.column_def(field="strength"),
    ag_grid.column_def(field="frequency"),
]


def ag_grid_simple():
    return ag_grid(
        id="ag_grid_basic_1",
        row_data=df.to_dict("records"),
        column_defs=column_defs,
        width="100%",
    )


transactions_columns = [
    ag_grid.column_def(field="date"),
    ag_grid.column_def(field="description"),
    ag_grid.column_def(field="amount"),
    ag_grid.column_def(field="category"),
]


def ag_grid_transactions():
    return ag_grid(
        id="ag_grid_transactions",
        row_data=FormState.entries,
        column_defs=transactions_columns,
        width="100%",
    )


@template(route="/transactions", title="Transactions", on_load=FormState.list_entries)
def transactions_page():
    return rx.vstack(
        card(),
        transaction_form(),
        ag_grid_simple(),
        ag_grid_transactions(),
    )


# @template(route="/transactions", title="Transactions")
# def transactions_page():
#     transactions = Transaction.query().all()
#     return rx.fragment(
#         rx.heading("Transactions"),
#         rx.table(
#             rx.table_header(
#                 rx.tr(
#                     rx.th("Date"),
#                     rx.th("Description"),
#                     rx.th("Amount"),
#                     rx.th("Category"),
#                 )
#             ),
#             rx.table_body(
#                 [
#                     rx.tr(
#                         rx.td(transaction.date),
#                         rx.td(transaction.description),
#                         rx.td(f"${transaction.amount:.2f}"),
#                         rx.td(transaction.category),
#                     )
#                     for transaction in transactions
#                 ]
#             ),
#         ),
#     )
