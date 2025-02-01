import reflex as rx
from ..models import Budget
from ..templates import template
from sqlmodel import select
from ..components.form_field import form_field, form_field_2
from typing import Dict


class BudgetTableState(rx.State):
    entries = []
    current_resource: Budget = Budget()
    columns = [
        {
            "title": "Category",
            "icon": "user",
            "data": "category",
        },
        {
            "title": "Time Period",
            "icon": "user",
            "data": "time_period",
        },
        {
            "title": "Amount",
            "icon": "user",
            "data": "amount",
        },
    ]

    @rx.event
    def load_entries(self) -> list[Budget]:
        """Get all entries from the database."""
        with rx.session() as session:
            query = select(Budget)
            self.entries = session.exec(query).all()

    def update_resource_to_db(self, form_data: dict):
        with rx.session() as session:
            resource = session.exec(
                select(Budget).where(Budget.id == self.current_resource.id)
            ).first()
            for field in Budget.get_fields():
                if field != "id":
                    setattr(resource, field, form_data[field])
            session.add(resource)
            session.commit()
        self.load_entries()
        return rx.toast.info(
            f"Resource has been modified.",
            position="bottom-right",
        )

    def get_resource(self, resource: Budget):
        self.current_resource = resource

    def delete_resource(self, id: int):
        """Delete a resource from the database."""
        with rx.session() as session:
            resource = session.exec(select(Budget).where(Budget.id == id)).first()
            session.delete(resource)
            session.commit()
        self.load_entries()
        return rx.toast.info(f"Resource has been deleted.", position="bottom-right")


def update_resource_dialog(resource: Budget):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                rx.text("Edit", size="3"),
                color_scheme="blue",
                size="2",
                variant="solid",
                on_click=lambda: BudgetTableState.get_resource(resource),
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
                        #     resource.name,
                        # ),
                        form_field_2(
                            # label="Name",
                            placeholder="Name",
                            type="text",
                            name="name",
                            icon="landmark",
                            default_value=resource.name,
                        ),
                        # Email
                        form_field(
                            "Date Field",
                            "Date Field",
                            "text",
                            "date_field",
                            "calendar",
                            resource.date_field,
                        ),
                        # Phone
                        form_field(
                            "Description Field",
                            "Description Field",
                            "text",
                            "description_field",
                            "phone",
                            resource.description_field,
                        ),
                        # Address
                        form_field(
                            "Amount Field",
                            "Amount Field",
                            "text",
                            "amount_field",
                            "home",
                            resource.amount_field,
                        ),
                        rx.checkbox(
                            "Reverse Negative Values",
                            name="is_reverse_negative_values",
                            default_value=resource.is_reverse_negative_values,
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
                                rx.button("Update Resource"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=BudgetTableState.update_account_to_db,
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


def _header_cell(column: Dict[str, str]):
    title = column["title"]
    icon = column.get("icon")
    is_icon = icon is not None
    icon = icon or "dot"
    return rx.table.column_header_cell(
        rx.hstack(
            rx.cond(
                is_icon,
                rx.icon(icon, size=18),
            ),
            rx.text(title),
            align="center",
            spacing="2",
        ),
    )


def show_table_row(resource: Budget):
    """Show a table row."""
    return rx.table.row(
        rx.table.cell(resource.name),
        rx.table.cell(resource.date_field),
        rx.table.cell(resource.description_field),
        rx.table.cell(resource.amount_field),
        rx.table.cell(resource.is_reverse_negative_values),
        rx.table.cell(
            rx.hstack(
                update_resource_dialog(resource),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: BudgetTableState.delete_resource(
                        getattr(resource, "id")
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


def main_table(TableState):
    return rx.vstack(
        rx.hstack(
            rx.button(
                "Prev",
                on_click=TableState.prev_page,
            ),
            rx.text(f"Page {TableState.page_number} / {TableState.total_pages}"),
            rx.button(
                "Next",
                on_click=TableState.next_page,
            ),
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(rx.foreach(TableState.columns, _header_cell)),
            ),
            rx.table.body(rx.foreach(TableState.entries, show_table_row)),
            on_mount=TableState.load_entries,
            width="100%",
            variant="surface",
            size="3",
        ),
        width="100%",
    )


@template(route="/budget", title="Budget")
def budget_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Budget", size="5"),
        rx.text("This is the budget page.", size="3"),
    )
