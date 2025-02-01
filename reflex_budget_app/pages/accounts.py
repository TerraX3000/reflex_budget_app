import reflex as rx
from ..models import Account
from ..templates import template
from reflex_budget_app.components.form_field import form_field, form_field_2
from sqlmodel import select, func
from typing import List


def add_account_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Account", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Account",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the account's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        form_field(
                            "Name",
                            "Account Name",
                            "text",
                            "name",
                            "user",
                        ),
                        # Email
                        form_field(
                            "Date Field", "Date Field", "text", "date_field", "calendar"
                        ),
                        # Phone
                        form_field(
                            "Description Field",
                            "Description Field",
                            "text",
                            "description_field",
                            "cog",
                        ),
                        # Address
                        form_field(
                            "Amount Field",
                            "Amount Field",
                            "text",
                            "amount_field",
                            "cog",
                        ),
                        # Payments
                        form_field(
                            "Payment ($)",
                            "Customer Payment",
                            "number",
                            "payments",
                            "dollar-sign",
                        ),
                        rx.checkbox(
                            "Reverse Negative Values",
                            name="is_reverse_negative_values",
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Submit Customer"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=AccountTableState.add_account_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def update_account_dialog(account: Account):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                rx.text("Edit", size="3"),
                color_scheme="blue",
                size="2",
                variant="solid",
                on_click=lambda: AccountTableState.get_account(account),
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="green",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Customer",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edit the customer's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        # form_field(
                        #     "Name",
                        #     "Name",
                        #     "text",
                        #     "name",
                        #     "user",
                        #     account.name,
                        # ),
                        form_field_2(
                            # label="Name",
                            placeholder="Name",
                            type="text",
                            name="name",
                            icon="landmark",
                            default_value=account.name,
                        ),
                        # Email
                        form_field(
                            "Date Field",
                            "Date Field",
                            "text",
                            "date_field",
                            "calendar",
                            account.date_field,
                        ),
                        # Phone
                        form_field(
                            "Description Field",
                            "Description Field",
                            "text",
                            "description_field",
                            "phone",
                            account.description_field,
                        ),
                        # Address
                        form_field(
                            "Amount Field",
                            "Amount Field",
                            "text",
                            "amount_field",
                            "home",
                            account.amount_field,
                        ),
                        rx.checkbox(
                            "Reverse Negative Values",
                            name="is_reverse_negative_values",
                            default_value=account.is_reverse_negative_values,
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Update Account"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=AccountTableState.update_account_to_db,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            style={"max_width": 450},
            box_shadow="lg",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def _header_cell(text: str, icon: str = None):
    is_icon = icon is not None
    icon = icon or "dot"
    return rx.table.column_header_cell(
        rx.hstack(
            rx.cond(
                is_icon,
                rx.icon(icon, size=18),
            ),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )


class AccountTableState(rx.State):
    accounts: list[Account] = []
    current_account: Account = Account()

    total_items: int
    offset: int = 0
    limit: int = 100

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1 + (1 if self.offset % self.limit else 0)

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return self.total_items // self.limit + (
            1 if self.total_items % self.limit else 0
        )

    @rx.event
    def prev_page(self):
        self.offset = max(self.offset - self.limit, 0)
        self.load_entries()

    @rx.event
    def next_page(self):
        if self.offset + self.limit < self.total_items:
            self.offset += self.limit
        self.load_entries()

    def _get_total_items(self, session):
        """Return the total number of items in the Customer table."""
        self.total_items = session.exec(select(func.count(Account.id))).one()

    @rx.event
    def load_entries(self) -> list[Account]:
        """Get all accounts from the database."""
        with rx.session() as session:
            query = select(Account)

            # Apply pagination
            query = query.offset(self.offset).limit(self.limit)

            self.accounts = session.exec(query).all()
            self._get_total_items(session)

    def update_account_to_db(self, form_data: dict):
        is_reverse_negative_values = form_data.get("is_reverse_negative_values")
        if is_reverse_negative_values == "on":
            form_data["is_reverse_negative_values"] = True
        else:
            form_data["is_reverse_negative_values"] = False

        # self.current_account.update(form_data)
        with rx.session() as session:
            account = session.exec(
                select(Account).where(Account.id == self.current_account.id)
            ).first()
            for field in Account.get_fields():
                if field != "id":
                    setattr(account, field, form_data[field])
            session.add(account)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Account {form_data['name']} has been modified.",
            position="bottom-right",
        )

    def get_account(self, account: Account):
        self.current_account = account

    def delete_account(self, id: int):
        """Delete an account from the database."""
        with rx.session() as session:
            account = session.exec(select(Account).where(Account.id == id)).first()
            session.delete(account)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"User {account.name} has been deleted.", position="bottom-right"
        )


def show_account(account: Account):
    """Show an account in a table row."""
    return rx.table.row(
        rx.table.cell(account.name),
        rx.table.cell(account.date_field),
        rx.table.cell(account.description_field),
        rx.table.cell(account.amount_field),
        rx.table.cell(account.is_reverse_negative_values),
        rx.table.cell(
            rx.hstack(
                update_account_dialog(account),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: AccountTableState.delete_account(
                        getattr(account, "id")
                    ),
                    size="2",
                    variant="solid",
                    color_scheme="red",
                ),
            )
        ),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def main_table():
    return rx.vstack(
        rx.hstack(
            rx.button(
                "Prev",
                on_click=AccountTableState.prev_page,
            ),
            rx.text(
                f"Page {AccountTableState.page_number} / {AccountTableState.total_pages}"
            ),
            rx.button(
                "Next",
                on_click=AccountTableState.next_page,
            ),
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Name", "user"),
                    _header_cell("Date Field", "calendar"),
                    _header_cell("Description Field", "cog"),
                    _header_cell("Amount Field"),
                    _header_cell("Is Reverse Negative Values", "cog"),
                    _header_cell("Actions", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(AccountTableState.accounts, show_account)),
            on_mount=AccountTableState.load_entries,
            width="100%",
            variant="surface",
            size="3",
        ),
        width="100%",
    )


@template(route="/accounts", title="Accounts")
def accounts_page():
    return rx.vstack(
        rx.box(
            main_table(),
            width="100%",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )
