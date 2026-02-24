# Starter for interactive dashboard
import dash
from dash import Input, Output, State, dcc, html

from trignum_core.subtractive_filter import SubtractiveFilter

app = dash.Dash(__name__)
sf = SubtractiveFilter()

app.layout = html.Div(
    [
        html.H1("TRIGNUM-300M Hallucination Dashboard"),
        dcc.Textarea(
            id="input_text",
            placeholder="Paste LLM output here",
            style={"width": "100%", "height": 200},
        ),
        html.Button("Run Subtractive Filter", id="run_button"),
        html.Div(id="output_results"),
    ]
)


@app.callback(
    Output("output_results", "children"),
    Input("run_button", "n_clicks"),
    State("input_text", "value"),
)
def run_filter(n_clicks, value):
    if not value:
        return "No input text provided."
    result = sf.apply(value)
    return html.Pre(str(result))


if __name__ == "__main__":
    app.run(debug=True)
