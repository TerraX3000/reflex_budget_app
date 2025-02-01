"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

# from . import styles
# from .pages import accounts_page
from .pages.accounts import accounts_page
from .pages.budget import budget_page

# Create the app.
app = rx.App(
    # style=styles.base_style,
    # stylesheets=styles.base_stylesheets,
    theme=rx.theme(
        appearance="dark", has_background=True, radius="large", accent_color="grass"
    ),
)

app.add_page(
    accounts_page,
    title="Customer Data App",
    description="A simple app to manage customer data.",
    route="/",
)
