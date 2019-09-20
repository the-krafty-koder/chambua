from django.shortcuts import redirect
import dash, pickle, pandas as pd,dash_table
import dash_html_components as html
from django_plotly_dash import DjangoDash
from dash.dependencies import Input,Output

results="Not worked"
subjects = ["Mathematics","English","Kiswahili","Physics","Chemistry","Biology","Geography","History","Business","CRE","French"]
submit_app = DjangoDash("submission_table")
submit_app.layout = html.Div(children = [
    dash_table.DataTable(
        id="table_example",
        columns=(
            [{'name' : 'Number', 'id':'Number'}] + [{'name' : 'Adm No', 'id':'Adm No', 'type':'numeric'},
                                                    {'name' : 'Student Name', 'id':'Student Name', 'type':'text'}] +
            [{'name': sub, 'id': sub, 'type':'numeric'} for sub in subjects]
        ),
        data=[dict(Model=i, **{subj: 0 for subj in subjects}) for i in range(1, 30)],
        style_data={'whitespace':'normal'},
        style_table={
            'maxHeight':'600px',
            'overflowY': 'scroll',
        },
        style_cell={
                'whiteSpace': 'normal'
        },
        style_cell_conditional=[
                        {'if': {'column_id': 'Student Name'},
                         'width': '150px'},
                        {'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'},],
        style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
        editable= True,
    ),
    html.Button(id='submit-button', n_clicks=0,  children= "Done"),
    html.Div(id = "output", children= "Proceed to Submit form below"),
])
timer = 0

@submit_app.callback(
    Output('output', 'children'),
    [Input('submit-button', 'n_clicks'),
     Input('table_example', 'data'),
     Input('table_example', 'columns')])
def save_data(click, rows, column):
    if click > 0:

        exam_results = pd.DataFrame(rows, columns=[c['name'] for c in column])

        global results
        results = exam_results

        global timer
        timer = timer + 1
        return "Data submitted"

def sucess():
    global timer
    if timer>0:
        return results




