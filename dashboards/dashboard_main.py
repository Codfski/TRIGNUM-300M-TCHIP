# Starter for interactive dashboard
import dash
from dash import dcc, html

from trignum_core.subtractive_filter import SubtractiveFilter

app = dash.Dash(__name__)
sf = SubtractiveFilter()

app.layout = html.Div([
    html.H1("TRIGNUM-300M Hallucination Dashboard"),
    dcc.Textarea(id="input_text", placeholder="Paste LLM output here", style={"width": "100%", "height": 200}),
    html.Button("Run Subtractive Filter", id="run_button"),
    html.Div(id="output_results")
])

@app.callback(
    dash.dependencies.Output("output_results", "children"),
    [dash.dependencies.Input("run_button", "n_clicks")],
    [dash.dependencies.State("input_text", "value")]
)
def run_filter(n_clicks, value):
    if not value:
        return "No input text provided."
    result = sf.apply(value)
    return html.Pre(str(result))

if __name__ == "__main__":
    app.run_server(debug=True)
