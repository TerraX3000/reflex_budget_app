import reflex as rx


def form_field(
    label: str,
    placeholder: str,
    type: str,
    name: str,
    icon: str,
    default_value: str = "",
) -> rx.Component:
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.icon(icon, size=16, stroke_width=1.5),
                rx.form.label(label),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type, default_value=default_value
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )


def form_field_2(
    label: str = "",
    placeholder: str = "",
    type: str = "text",
    name: str = "",
    icon: str = "",
    default_value: str = "",
) -> rx.Component:
    is_icon = icon is not None
    icon = icon or "dot"
    return rx.form.field(
        rx.flex(
            rx.hstack(
                rx.cond(
                    is_icon,
                    rx.icon(icon, size=16, stroke_width=1.5),
                ),
                rx.cond(
                    label,
                    rx.form.label(label),
                ),
                align="center",
                spacing="2",
            ),
            rx.form.control(
                rx.input(
                    placeholder=placeholder, type=type, default_value=default_value
                ),
                as_child=True,
            ),
            direction="column",
            spacing="1",
        ),
        name=name,
        width="100%",
    )
