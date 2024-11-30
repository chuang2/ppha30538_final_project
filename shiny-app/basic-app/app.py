from shiny import App, render, ui
import pandas as pd
import altair as alt


app_ui = ui.page_fluid(
    ui.panel_title("Hello Shiny!"),
    ui.input_slider("n", "N", 0, 100, 20),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @output
    @render.plot
    def main():
        return f"n*2 is {input.n() * 2}"


app = App(app_ui, server)
