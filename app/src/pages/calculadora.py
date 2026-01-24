import flet as ft
from pages import ferramentas,home

def criar_calculadora(page: ft.Page):

    operator = "+"
    operand1 = 0
    new_operand = True

    result = ft.Text(
        value="0",
        size=32,
        text_align=ft.TextAlign.RIGHT,
    )

    historico_coluna = ft.Column(
        spacing=5,
        scroll=ft.ScrollMode.AUTO,
    )

    historico_container = ft.Container(
        content=historico_coluna,
        bgcolor=ft.Colors.BLACK26,
        padding=10,
        border_radius=27,
        expand=True,
        width=page.width
    )

    def reset():
        nonlocal operator, operand1, new_operand
        operator = "+"
        operand1 = 0
        new_operand = True

    def format_number(num):
        return int(num) if num % 1 == 0 else num

    def calculate(op1, op2, op):
        try:
            if op == "+":
                return format_number(op1 + op2)
            if op == "-":
                return format_number(op1 - op2)
            if op == "*":
                return format_number(op1 * op2)
            if op == "/":
                return "Error" if op2 == 0 else format_number(op1 / op2)
        except:
            return "Error"

    def registrar_historico(expressao, resultado):
        historico_coluna.controls.append(
            ft.Text(
                f"{expressao} = {resultado}",
                size=12,
                color=ft.Colors.WHITE70,
            )
        )

    def on_button_click(e):
        nonlocal operator, operand1, new_operand

        data = e.control.content.value

        if result.value == "Error" or data == "AC":
            result.value = "0"
            historico_coluna.controls.clear()
            reset()

        elif data.isdigit() or data == ".":
            if result.value == "0" or new_operand:
                result.value = data
                new_operand = False
            else:
                result.value += data

        elif data in "+-*/":
            operand1 = float(result.value)
            operator = data
            new_operand = True

        elif data == "=":
            operand2 = float(result.value)
            resultado = calculate(operand1, operand2, operator)

            registrar_historico(
                f"{format_number(operand1)} {operator} {format_number(operand2)}",
                resultado,
            )

            result.value = str(resultado)
            reset()

        elif data == "%":
            result.value = str(float(result.value) / 100)
            reset()

        elif data == "+/-":
            if result.value.startswith("-"):
                result.value = result.value[1:]
            elif result.value != "0":
                result.value = "-" + result.value

        page.update()

    def button(text, bgcolor, color=ft.Colors.WHITE, expand=1):
        return ft.ElevatedButton(
            content=ft.Text(text),
            height=50,
            bgcolor=bgcolor,
            color=color,
            expand=expand,
            on_click=on_button_click,
        )

    calculadora = ft.Container(
        height=page.height*0.8,
        bgcolor=ft.Colors.TRANSPARENT,
        padding=15,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.END,
            expand=True,
            controls=[
                # HISTÓRICO (pequeno, rolável)
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.with_opacity(color=ft.Colors.BLACK,opacity = 0),
                    height=120,
                    content=historico_container,
                ),

                # VISOR
                ft.Container(
                    bgcolor=ft.Colors.TRANSPARENT,
                    content=result,
                    alignment=ft.Alignment.CENTER_RIGHT,
                    padding=10,
                ),

                # BOTÕES
                ft.Row(
                    controls=[
                        button("AC", ft.Colors.BLUE_GREY_100, ft.Colors.BLACK),
                        button("+/-", ft.Colors.BLUE_GREY_100, ft.Colors.BLACK),
                        button("%", ft.Colors.BLUE_GREY_100, ft.Colors.BLACK),
                        button("/", ft.Colors.ORANGE),
                    ],
                ),
                ft.Row(
                    controls=[
                        button("7", ft.Colors.WHITE24),
                        button("8", ft.Colors.WHITE24),
                        button("9", ft.Colors.WHITE24),
                        button("*", ft.Colors.ORANGE),
                    ],
                ),
                ft.Row(
                    controls=[
                        button("4", ft.Colors.WHITE24),
                        button("5", ft.Colors.WHITE24),
                        button("6", ft.Colors.WHITE24),
                        button("-", ft.Colors.ORANGE),
                    ],
                ),
                ft.Row(
                    controls=[
                        button("1", ft.Colors.WHITE24),
                        button("2", ft.Colors.WHITE24),
                        button("3", ft.Colors.WHITE24),
                        button("+", ft.Colors.ORANGE),
                    ],
                ),
                ft.Row(
                    controls=[
                        button("0", ft.Colors.WHITE24, expand=2),
                        button(".", ft.Colors.WHITE24),
                        button("=", ft.Colors.ORANGE),
                    ],
                ),
            ],
        ),
    )

    return calculadora

def calculadora(page: ft.Page):
    page.clean()
    page.add(ferramentas.header(page=page, titulo='Calculadora',icone=ft.Icons.CALCULATE_ROUNDED))
    page.add(ferramentas.container(page,controles=[criar_calculadora(page)]))
    page.update()