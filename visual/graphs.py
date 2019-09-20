import dash_core_components as dcc
from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django.shortcuts import redirect
from plotly import tools
import numpy as np, pandas as pd
from processing.apply import *
from submission.models import *
import dash.dependencies

external_stylesheets = ['templates/dash.css']


def set_dataframe(institution, Class, Stream, Exam, teach):
    global stream, school, standard, ex
    school = Institution.objects.find(institution)
    standard = school.find(Class)
    stream = standard.find(Stream)
    ex = stream.find(Exam).exam_name
    ord = stream.find_ordinal(Exam)
    dataframe = Institution.objects.find(institution).find(Class).find(Stream).find(Exam).results

    global previous_exams_mean

    try:
        previous_exams = {exx.exam_name: processing(exx.results, teach).clean() for exx in
                          Institution.objects.find(institution).find(Class).find(Stream).exam[:ord]}
    except IndexError:
        previous_exams = None

    if previous_exams != None:
        previous_exams_mean = {ex_name.exam_name: processing(ex_name.results, teach).result().mean()["Total"] for
                               ex_name in Institution.objects.find(institution).find(Class).find(Stream).exam[:ord]}
    else:
        previous_exams_mean = None
    processing(dataframe, teach).clean()

    global data
    data = processing(dataframe, teach)


#set_dataframe("Premier High School","Form Three","Terror","Term Two Mocky3",Teacher.objects.all()[0])

class graph():

    def get_dropdown(self):
        dropdown = DjangoDash("dropdown", external_stylesheets=external_stylesheets)
        dropdown.layout = html.Div(children=[
            dcc.Dropdown(
                id='mydropdown',
                options=[
                    {'label': col, 'value': col} for col in [obj.exam_name for obj in stream.exam]
                ],
                value=ex,
            ),
            html.Div(id="selection")
        ])

        @dropdown.callback(Output('selection', 'children'), [Input('mydropdown', 'value')])
        def drop(sent_value):
            set_dataframe(school, standard, stream, sent_value)
            return redirect('/see')

        return dropdown

    def get_donut(self):
        donut = DjangoDash("donut", external_stylesheets=external_stylesheets)
        donut.layout = html.Div(children=[
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        {
                            "values": [data.number_of_subject_grades(subj)["A"] for subj in data.subjects],
                            "labels": [i for i in data.subjects],
                            "name": "Number of As",
                            "hoverinfo": "label+percent+name",
                            "hole": .4,
                            "type": "pie",
                            "showlegend": True
                        },
                    ],
                    layout={

                        "title": "Grade Distribution for exam Jesma",
                        "annotations": [
                            {
                                "font": {
                                    "size": 15
                                },
                                "showarrow": False,
                                "text": "A's",
                                "x": 0.50,
                                "y": 0.5
                            },
                        ],
                    }
                )
            ),
            dcc.Graph(
                figure=go.Figure(
                    data=[
                        {
                            "values": [data.number_of_subject_grades(subj)["B"] for subj in data.subjects],
                            "labels": [i for i in data.subjects],
                            "name": "Number of As",
                            "hoverinfo": "label+percent+name",
                            "hole": .4,
                            "type": "pie",
                            "showlegend": True
                        },
                    ],
                    layout={

                        "title": "Grade Distribution for exam Jesma",
                        "annotations": [
                            {
                                "font": {
                                    "size": 15
                                },
                                "showarrow": False,
                                "text": "B's",
                                "x": 0.50,
                                "y": 0.5
                            },
                        ],
                    }
                )
            )
        ])

        def disp():
            pass

        return donut
    """
    def get_lineplot(self):
        if previous_exams_mean != None:
            trace1 = go.Scatter(
                x=list(previous_exams_mean.keys()),
                y=list(previous_exams_mean.values()),
                name="Perfomance Over Time",
                mode="lines+markers",
                showlegend=False
            )
            trace2 = go.Scatter(
                x=["Maths", "English", "Kiswahili", "Geography", "History", "French", "Business"],
                y=[60, 78, 30, 49, 57, 80, 44],
                name="Class Average",
                mode="lines+markers",
                showlegend=False
            )

            fig = tools.make_subplots(rows=3, cols=1, shared_xaxes=False, shared_yaxes=True, vertical_spacing=0.3)
            fig['layout'].update(
                height=570,
                width=640,
                title='Stacked subplots',
                yaxis=dict(showline=False, tickmode="auto", nticks=4),
                xaxis=dict(showline=True),
                yaxis1=dict(showline=False, tickmode="auto", nticks=2),
                xaxis1=dict(showline=True),
                yaxis2=dict(showline=False, tickmode="auto", nticks=4),
                xaxis2=dict(showline=True),
                legend=dict(x=0, y=1)
            )

            fig.append_trace(trace1, 1, 1)
            fig.append_trace(trace2, 2, 1)
            fig.append_trace(trace1, 3, 1)
            fig.append_trace(trace2, 3, 1)

            lineplot1 = DjangoDash("lineplot1", external_stylesheets=external_stylesheets)

            lineplot1.layout = html.Div(children=[

                dcc.Graph(figure=fig, id="Subplot Graph")

            ]

            )
        else:
            lineplot1 = DjangoDash("lineplot1", external_stylesheets=external_stylesheets)

            lineplot1.layout = html.Div(children=[

                html.P(children=[
                    html.Div(children="No Exams Done Before", style={"fontSize": "20"})
                ])

            ]

            )

        return lineplot1
    """
    def get_scatter(self):

        trace4 = go.Scatter(
            x=data.science().where(data.science()[1] == "A").dropna()[2].values.tolist(),
            y=data.science().where(data.science()[1] == "A").dropna()[0].values.tolist(),
            name="Grade A in Sciences",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.science().where(data.science()[1] == "A").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='green',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace5 = go.Scatter(
            x=data.science().where(data.science()[1] == "B").dropna()[2].values.tolist(),
            y=data.science().where(data.science()[1] == "B").dropna()[0].values.tolist(),
            name="Grade B in Sciences",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.science().where(data.science()[1] == "B").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='blue',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace6 = go.Scatter(
            x=data.science().where(data.science()[1] == "C").dropna()[2].values.tolist(),
            y=data.science().where(data.science()[1] == "C").dropna()[0].values.tolist(),
            name="Grade C in Sciences",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.science().where(data.science()[1] == "C").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='violet',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace7 = go.Scatter(
            x=data.science().where(data.science()[1] == "D").dropna()[2].values.tolist(),
            y=data.science().where(data.science()[1] == "D").dropna()[0].values.tolist(),
            name="Grade D in Sciences",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.science().where(data.science()[1] == "D").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='grey',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace8 = go.Scatter(
            x=data.science().where(data.science()[1] == "E").dropna()[2].values.tolist(),
            y=data.science().where(data.science()[1] == "E").dropna()[0].values.tolist(),
            name="Grade E in Sciences",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.science().where(data.science()[1] == "E").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='#FF0000',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )

        scatter_fig = tools.make_subplots(rows=1, cols=1, shared_yaxes=True, shared_xaxes=True)
        scatter_fig['layout'].update(
            title="Perfomance in Sciences Vs Overall Grade",
            legend=dict(x=0, y=1),
            width=500,
            xaxis=dict(
                title="Overall Grades",
                tickmode="auto",
                autorange=True,
                nticks=45,
                zeroline=False,
                showline=False,
            ),
            yaxis=dict(
                title="Perfomance in Sciences [Maths,Physics,Chemistry]",
                autorange=True,
                zeroline=False,
                showline=False,
            )
        )
        scatter_fig.append_trace(trace4, 1, 1)
        scatter_fig.append_trace(trace5, 1, 1)
        scatter_fig.append_trace(trace6, 1, 1)
        scatter_fig.append_trace(trace7, 1, 1)
        scatter_fig.append_trace(trace8, 1, 1)

        scatter = DjangoDash("scatter", external_stylesheets=external_stylesheets)
        scatter.layout = html.Div(
            dcc.Graph(figure=scatter_fig, id="scattter_subplot")
        )

        return scatter

    def get_scatter_arts(self):

        trace4 = go.Scatter(
            x=data.arts().where(data.arts()[1] == "A").dropna()[2].values.tolist(),
            y=data.arts().where(data.arts()[1] == "A").dropna()[0].values.tolist(),
            name="Grade A in Arts",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.arts().where(data.arts()[1] == "A").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='green',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace5 = go.Scatter(
            x=data.arts().where(data.arts()[1] == "B").dropna()[2].values.tolist(),
            y=data.arts().where(data.arts()[1] == "B").dropna()[0].values.tolist(),
            name="Grade B in Arts",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.arts().where(data.arts()[1] == "B").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='blue',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace6 = go.Scatter(
            x=data.arts().where(data.arts()[1] == "C").dropna()[2].values.tolist(),
            y=data.arts().where(data.arts()[1] == "C").dropna()[0].values.tolist(),
            name="Grade C in Arts",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.arts().where(data.arts()[1] == "C").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='violet',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace7 = go.Scatter(
            x=data.arts().where(data.arts()[1] == "D").dropna()[2].values.tolist(),
            y=data.arts().where(data.arts()[1] == "D").dropna()[0].values.tolist(),
            name="Grade D in Arts",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.arts().where(data.arts()[1] == "D").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='grey',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace8 = go.Scatter(
            x=data.arts().where(data.arts()[1] == "E").dropna()[2].values.tolist(),
            y=data.arts().where(data.arts()[1] == "E").dropna()[0].values.tolist(),
            name="Grade E in Arts",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.arts().where(data.arts()[1] == "E").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='#FF0000',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )

        scatter_fig = tools.make_subplots(rows=1, cols=1, shared_yaxes=True, shared_xaxes=True)
        scatter_fig['layout'].update(
            title="Perfomance in Arts Vs Overall Grade",
            legend=dict(x=0, y=1),
            width=500,
            xaxis=dict(
                title="Overall Grades",
                tickmode="auto",
                autorange=True,
                nticks=45,
                zeroline=False,
                showline=False,
            ),
            yaxis=dict(
                title="Perfomance in Arts and Humanities",
                autorange=True,
                zeroline=False,
                showline=False,
            )
        )
        scatter_fig.append_trace(trace4, 1, 1)
        scatter_fig.append_trace(trace5, 1, 1)
        scatter_fig.append_trace(trace6, 1, 1)
        scatter_fig.append_trace(trace7, 1, 1)
        scatter_fig.append_trace(trace8, 1, 1)

        scatter = DjangoDash("scatter_arts", external_stylesheets=external_stylesheets)
        scatter.layout = html.Div(
            dcc.Graph(figure=scatter_fig, id="scattter_subplot")
        )

        return scatter

    def get_scatter_math(self):

        trace4 = go.Scatter(
            x=data.math().where(data.math()[1] == "A").dropna()[2].values.tolist(),
            y=data.math().where(data.math()[1] == "A").dropna()[0].values.tolist(),
            name="Grade A in Maths",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.math().where(data.math()[1] == "A").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='green',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace5 = go.Scatter(
            x=data.math().where(data.math()[1] == "B").dropna()[2].values.tolist(),
            y=data.math().where(data.math()[1] == "B").dropna()[0].values.tolist(),
            name="Grade B in Maths",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in data.math().where(data.math()[1] == "B").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='blue',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace6 = go.Scatter(
            x=data.math().where(data.math()[1] == "C").dropna()[2].values.tolist(),
            y=data.math().where(data.math()[1] == "C").dropna()[0].values.tolist(),
            name="Grade C in Maths",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in data.math().where(data.math()[1] == "C").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='violet',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace7 = go.Scatter(
            x=data.math().where(data.math()[1] == "D").dropna()[2].values.tolist(),
            y=data.math().where(data.math()[1] == "D").dropna()[0].values.tolist(),
            name="Grade D in Maths",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.math().where(data.math()[1] == "D").dropna()[0].index.tolist()],
            marker=dict(
                symbol="circle-dot",
                size=16,
                color='grey',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )
        trace8 = go.Scatter(
            x=data.math().where(data.math()[1] == "E").dropna()[2].values.tolist(),
            y=data.math().where(data.math()[1] == "E").dropna()[0].values.tolist(),
            name="Grade E in Maths",
            mode="markers",
            hovertext=[data.result().loc[b]["Student Name"] for b in
                       data.math().where(data.math()[1] == "E").dropna()[0].index.tolist()],

            marker=dict(
                symbol="circle-dot",
                size=16,
                color='#FF0000',
                opacity=0.7,
                line={'width': 0.5, 'color': 'white'}
            )
        )

        scatter_fig = tools.make_subplots(rows=1, cols=1, shared_yaxes=True, shared_xaxes=True)
        scatter_fig['layout'].update(
            title="Perfomance in Maths Vs Overall Grade",
            legend=dict(x=0, y=1),
            width=500,
            xaxis=dict(
                title="Overall Grades",
                tickmode="auto",
                autorange=True,
                nticks=45,
                zeroline=False,
                showline=False,
            ),
            yaxis=dict(
                title="Perfomance in Maths",
                autorange=True,
                zeroline=False,
                showline=False,
            )
        )
        scatter_fig.append_trace(trace4, 1, 1)
        scatter_fig.append_trace(trace5, 1, 1)
        scatter_fig.append_trace(trace6, 1, 1)
        scatter_fig.append_trace(trace7, 1, 1)
        scatter_fig.append_trace(trace8, 1, 1)

        scatter = DjangoDash("scatter_math", external_stylesheets=external_stylesheets)
        scatter.layout = html.Div(
            dcc.Graph(figure=scatter_fig, id="scattter_subplot")
        )

        return scatter

    def generate_within(dataframe, row):
        trace1 = go.Scatter(
            x=dataframe.iloc[row][:-1].index.values.tolist(),
            y=dataframe.iloc[row][:-1].values.tolist(),
            name="Perfomance",
            mode="lines+markers",
            showlegend=False
        )
        trace2 = go.Scatter(
            x=dataframe.iloc[row][:-1].index.values.tolist(),
            y=[dataframe[col].mean() for col in dataframe.columns[:-1]],
            name="Class Average",
            mode="lines+markers",
            showlegend=False
        )

        within = tools.make_subplots(rows=1, cols=1, shared_xaxes=True, shared_yaxes=True)
        within['layout'].update(
            title='Stacked subplots',
            yaxis=dict(showline=False, tickmode="auto", nticks=4),
            xaxis=dict(showline=True),
            yaxis1=dict(showline=False, tickmode="auto", nticks=2),
            xaxis1=dict(showline=True),
            yaxis2=dict(showline=False, tickmode="auto", nticks=4),
            xaxis2=dict(showline=True),
            legend=dict(x=0, y=1)
        )
        within.append_trace(trace1, 1, 1)
        within.append_trace(trace2, 1, 1)

        return within

    def get_interactive(self):
        contrib = data.individual_subject_contribution
        dataframe = data.rankings()
        rank = data.number_rankings_per_subject()
        interactive = DjangoDash("interactive", external_stylesheets=external_stylesheets)
        interactive.layout = html.Div(children=[
            dash_table.DataTable(
                id="interactive_table",
                columns=[
                    {'name': i, 'id': i} for i in dataframe.columns],
                data=dataframe.to_dict("rows"),
                sorting=True,
                sorting_type="multi",
                row_selectable="single",
                selected_rows=[],
                pagination_mode="fe",
                pagination_settings={
                    "displayed_pages": 4,
                    "current_page": 0,
                    "page_size": 10,
                },
                navigation="page"
            ),
            html.Div(id="output_histograms")
        ])

        @interactive.callback(
            Output('output_histograms', "children"),
            [Input('interactive_table', "derived_virtual_data"),
             Input('interactive_table', "derived_virtual_selected_rows")])
        def update(rows, derived_virtual_selected_rows):
            if derived_virtual_selected_rows is None:
                row_number = []
            else:
                row_number = derived_virtual_selected_rows[0]
            if rows is None:
                derived = dataframe
            else:
                derived = pd.DataFrame(rows)

            return html.Div(children=[
                dcc.Graph(
                    figure=go.Figure(
                        data=[
                            {
                                "name": "Perfomance",
                                "x": derived.iloc[row_number][3:14].index.values.tolist(),
                                "y": derived.iloc[row_number][3:14].values.tolist(),
                                "type": "bar",
                                "marker": {"color": "#0074D9"},
                            },
                            {
                                "name": "Class Average",
                                "x": derived.iloc[row_number][3:14].index.values.tolist(),
                                "y": [i for i in derived[derived.columns[3:14]].mean()],
                                "type": "bar",
                                "marker": {"color": "#7FDBFF"}
                            }

                        ],
                        layout={

                            "xaxis": {"automargin": True},
                            "yaxis": {"automargin": True},
                            "height": 270,
                            "margin": {"t": 7, "l": 7, "r": 7},
                            "showlegend": True

                        },
                    )
                ),
                html.Div(children="Position Rankings Per Subject", style={"fontSize": "20"}),
                html.Div(
                    children=[

                        html.Div(
                            children=[
                                html.P(children=[
                                    html.Div(children=[
                                        html.Div(children=round(rank.iloc[row_number][col]),
                                                 style={"fontSize": "20", "color": "#0074D9",
                                                        "display": "inline-block"}),
                                        html.Div(children="%d%%" % contrib(row_number)[col],
                                                 style={"color": "#7FDBFF", "width": "20%", "display": "inline-block",
                                                        "fontSize": "13"}),
                                        html.Div(children=col, style={"fontSize": "20"})])],
                                    style={
                                        "width": "20%",
                                        "fontSize": "20",
                                        "display": "inline-block",
                                        "textAlign": "center"

                                    }
                                ) for col in rank.iloc[row_number][2:14].index.tolist()]
                        )
                    ]),
            ])

        return interactive

    def get_subj_interactive(self):

        subj_dataframe = pd.DataFrame(data.subject_rankings().sort_values().tolist(), columns=["Rank"],
                                      index=data.subject_rankings().sort_values().index)
        subj_dataframe["Subject"] = data.subject_rankings().sort_values().index
        subj_dataframe["Mean"] = [data.result()[i].mean() for i in subj_dataframe.index]
        subj_dataframe["ClassTeacher"] = stream.classteacher
        cols = ["Rank", "Subject", "Mean", "ClassTeacher"]

        subj_interactive = DjangoDash("subj_interactive", external_stylesheets=external_stylesheets)
        subj_interactive.layout = html.Div(children=[
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in cols],
                data=subj_dataframe.to_dict("rows"),
                id="interactive",
                sorting=True,
                sorting_type="multi",
                row_selectable="single",
                selected_rows=[],
                pagination_mode="fe",
                pagination_settings={
                    "displayed_pages": 2,
                    "current_page": 0,
                    "page_size": 6
                },
                navigation="page"
            ),
            html.Div(id="output_subj_data")
        ])

        @subj_interactive.callback(
            Output("output_subj_data", "children"),
            [Input("interactive", "derived_virtual_data"),
             Input("interactive", "derived_virtual_selected_rows")]
        )
        def generate(rows, derived_virtual_selected_rows):
            if derived_virtual_selected_rows is None:
                row_number = []
            else:
                row_number = derived_virtual_selected_rows
            if rows is None:
                derived = subj_dataframe
            else:
                derived = pd.DataFrame(rows)

            disp = html.Div(
                children=[

                    html.Div(
                        children=[
                            html.P(children=[
                                html.Div(children=
                                         data.number_of_subject_grades("%s" % derived.iloc[row_number[0]]["Subject"])[
                                             "A"]),
                                html.Div(children="Number of A's", style={"fontSize": "20"})])],
                        style={
                            "width": "20%",
                            "fontSize": "50",
                            "display": "inline-block",
                            "textAlign": "center"

                        }
                    ),

                    html.Div(
                        children=[
                            html.P(children=[
                                html.Div(children=round(derived["Mean"][row_number[0]], 2)),
                                html.Div(children="Average", style={"fontSize": "20"})])],
                        style={
                            "width": "20%",
                            "fontSize": "50",
                            "display": "inline-block",
                            "textAlign": "center"

                        }
                    ),

                    html.Div(
                        children=[
                            html.P(children=[
                                html.Div(
                                    children=round(data.pass_percentage("%s" % derived.iloc[row_number[0]]["Subject"]),
                                                   2)),
                                html.Div(children="Pass Percentage", style={"fontSize": "20"})])],
                        style={
                            "width": "20%",
                            "fontSize": "50",
                            "display": "inline-block",
                            "textAlign": "center"

                        }
                    ),

                    html.Div(
                        children=[
                            html.P(children=[
                                html.Div(children=data.std("%s" % derived.iloc[row_number[0]]["Subject"])),
                                html.Div(children="Standard Deviation", style={"fontSize": "20"})])],
                        style={
                            "width": "20%",
                            "fontSize": "50",
                            "display": "inline-block",
                            "textAlign": "center"

                        }
                    ),
                    html.Div(
                        children=[
                            html.P(children=[
                                html.Div(children=data.top_student("%s" % derived.iloc[row_number[0]]["Subject"])),
                                html.Div(children="Top Student", style={"fontSize": "20"})])],
                        style={
                            "width": "20%",
                            "height": "25%",
                            "fontSize": "30",
                            "display": "inline-block",
                            "textAlign": "center"

                        }
                    )

                ]
            )

            return disp

        return subj_interactive

    def get_teacher_ranking(self):

        teacher = DjangoDash("teacher", external_stylesheets=external_stylesheets)
        teacher.layout = html.Div(children=[
            dash_table.DataTable(
                columns=[{"name": "Teachers", "id": "Teachers"},{"name":"Subject","id":"Subject"},{"name":"Weighted Average","id":0}],
                data=data.weighted().to_dict("rows"),
                id="interactive",
                sorting=True,
                pagination_mode="fe",
                pagination_settings={
                    "displayed_pages": 2,
                    "current_page": 0,
                    "page_size": 6
                },
                navigation="page"
            ),
            html.Div(id="output_subj_data")
        ])

        return teacher

    def corry(self):
        return {"Chem": data.corr_chem(), "Eng": data.corr_eng()}

    def improve(self):
        perf = data.result().mean()[2:13].sort_values(ascending=False)
        return {"low1": perf.index[-1], "low2": perf.index[-2], "high1": perf.index[0], "high2": perf.index[1],
                "high3": perf.index[2]}

    def number(self):
        return {"A": data.number_of_grades()["A"], "B": data.number_of_grades()["B"], "C": data.number_of_grades()["C"],
                "D": data.number_of_grades()["D"], "E": data.number_of_grades()["E"]}

    def str_wk(self):
        return {"weight1": data.weighted().iloc[0].name, "weight2": data.weighted().iloc[1].name,
                "weight3": data.weighted().iloc[-1].name,"weight4": data.weighted().iloc[-2].name}

    def details(self):
        return {"top": data.rankings().iloc[0]["Student Name"], "Mean": data.result().mean()["Total"],
                "Last": data.rankings().iloc[-1]["Student Name"]}
