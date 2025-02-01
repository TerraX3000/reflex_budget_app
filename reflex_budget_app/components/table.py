import reflex as rx


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
