import reflex as rx
from ..models import Account
from ..templates import template
from sqlmodel import select, func
from typing import List
from reflex_ag_grid import ag_grid


class FormState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        print(form_data)
        is_reverse_negative_values = form_data.get("is_reverse_negative_values")
        if is_reverse_negative_values == "on":
            form_data["is_reverse_negative_values"] = True
        else:
            form_data["is_reverse_negative_values"] = False
        self.form_data = form_data
        with rx.session() as session:
            db_entry = Account(**form_data)
            print(db_entry)
            session.add(db_entry)
            session.commit()
            AGGridDatabaseState.update_data()
            yield


def account_form() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.input(
                    name="name",
                    placeholder="Name",
                ),
                rx.input(
                    placeholder="Date Field",
                    name="date_field",
                    type="date_field",
                ),
                rx.input(
                    placeholder="Description Field",
                    name="description_field",
                ),
                rx.input(
                    placeholder="Amount Field",
                    name="amount_field",
                ),
                rx.checkbox(
                    "Reverse Negative Values",
                    name="is_reverse_negative_values",
                    default_value=False,
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


class AGGridDatabaseState(rx.State):
    accounts: List[Account] = []
    columns: List = [
        ag_grid.column_def(field="name", checkbox_selection=True),
        ag_grid.column_def(field="date_field"),
        ag_grid.column_def(field="amount_field"),
        ag_grid.column_def(field="description_field"),
        ag_grid.column_def(
            field="is_reverse_negative_values",
            editable=True,
            cell_editor=ag_grid.editors.checkbox,
        ),
        ag_grid.column_def(field="options"),
    ]

    @rx.var(cache=True)
    def data(self) -> list[dict]:
        with rx.session() as session:
            results = session.exec(select(Account)).all()
            # self.accounts = [result.dict() for result in results]
            self.accounts = [{**result.dict(), "options": "⋮"} for result in results]
        return self.accounts

    def update_data(self):
        with rx.session() as session:
            results = session.exec(select(Account)).all()
            self.accounts = [result.dict() for result in results]

    @rx.event
    def cell_value_changed(self, row, col_field, new_value):
        account_name = self.accounts[row]["name"]
        self.accounts[row][col_field] = new_value
        with rx.session() as session:
            account = Account(**self.accounts[row])
            session.merge(account)
            session.commit()
        yield rx.toast(f"{account_name} updated successfully", position="top-center")

    @rx.event
    def on_row_selected(self, event):
        print(event)


def ag_grid_accounts():
    return ag_grid(
        id="ag_grid_accounts",
        row_data=AGGridDatabaseState.data,
        column_defs=AGGridDatabaseState.columns,
        width="100%",
        on_cell_value_changed=AGGridDatabaseState.cell_value_changed,
        row_selection="single",
        on_row_selected=AGGridDatabaseState.on_row_selected,
    )
