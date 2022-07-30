# (c) 2022 Jonathan Alles


from dash import Dash, html, Input, State, Output, dcc, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import uuid
import time

####### GLOBALS ######

USERNAME = "Jonathan"
PASSWORD = "Hund"

##### APP

app = Dash(external_stylesheets = [dbc.themes.FLATLY, dbc.icons.BOOTSTRAP], title = "Login Demo App")

# Login Page

login_div = html.Div([
    dbc.InputGroup(
        [dbc.InputGroupText('Username', style = {'width':'100px'}), dbc.Input(id='input_user', placeholder = "")]
    , style = {'width':'300px'}),
    dbc.InputGroup(
        [dbc.InputGroupText('Password', style = {'width':'100px'}), dbc.Input(id='input_pw', placeholder = "", type = 'password')]
    , style = {'width':'300px'}),
    dbc.Button("Login", id='login-button',outline = True, style = {'width':'300px'}, color = 'primary')
    ], 
    className='position-absolute top-50 start-50 translate-middle pb-5', 
    id='login-div')

# Dash Page

dashboard_div = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Button("Tool 1", color="dark", className="me-1")),
                        dbc.Col(dbc.Button("Tool 2", color="dark", className="me-1")),
                        dbc.Col(dbc.Button("Tool 3", color="dark", className="me-1"))
                    ],
                    className = 'g-0'
                )
            ],
            fluid = True
        )
    ),
    html.H2("Welcome to the App", className = "me-1")
])

base_div = html.Div([
    dcc.Store(id='loc'),
    html.Div([login_div],id='page_content')
])

app.layout = dbc.Container(
    base_div,
id='container',
fluid = True)

# Define validation layout
app.validation_layout = html.Div([
    login_div,
    dashboard_div,
    base_div
])



# Callback for page navigation
@app.callback(
    Output('page_content','children'),
    Input('input_user','valid'),
    Input('input_pw','valid'),
    State('loc','data')
)
def get_layout_location(input_user_valid, input_pw_valid, loc_data):
    # For app start loc is None, show login
    if input_user_valid and input_pw_valid:
        time.sleep(1)
        return dashboard_div
    else:
        return no_update

@app.callback(
#    Output('page-content','children'),
    Output('input_user','valid'),
    Output('input_user','invalid'),
    Output('input_pw','valid'),
    Output('input_pw','invalid'),
    Output('loc','data'),
    Input('login-button', 'n_clicks'),
    State('input_user', 'value'),
    State('input_pw', 'value')
)
def update_page(login_n_clicks, username, pw):
    
    if login_n_clicks is None:
        return no_update
    else:
        # check username if correct
        if username == USERNAME:
            if pw == PASSWORD:
                # If login successful create session-uuid
                uuid_str = str(uuid.uuid4())
                return True, False, True, False, {'loc':'dashboard'}
            else:
                return True, False, False, True, {'loc':'None'}
        else:
            return False, True, False, False, {'loc':'None'}

if __name__ == '__main__':
     app.run_server(debug=True)