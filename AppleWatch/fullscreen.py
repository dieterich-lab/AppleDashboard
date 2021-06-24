"""
modal_plt_1 = dbc.Modal([
            dbc.ModalHeader(dbc.Row(close_button_plt_1)),
        dbc.ModalBody(
    dbc.FormGroup([html.Div[ ],id = "plt_modal_container_1")])),],
            id = "modal_plt_1"
            is_open = False, style = {"Width":"100vh","max-width": "none", "max-height": "none", "minheight": "90vh" }
    )



@app.callback(
    [Output("plt_container_1","children"),
     Output("plt_modal_container1","children"),
     Output("plt_modal_medium_container_1","children")],
    [Input("modal_plt_1","is_open"),
     Input("modal_medium_plt_1","is_open")]
)
def plt_container_2(modal_plt_1,modal_medium_plt_2):
    plt = dcc.Graph
"""
#https://community.plotly.com/t/dash-graph-display-on-full-screen/11118/5