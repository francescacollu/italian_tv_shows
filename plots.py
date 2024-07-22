from analysis import *
import plotly.express as px
import chart_studio.plotly as py
from credential_file import *
import chart_studio.tools as tls
import matplotlib.pyplot as plt
from pywaffle import Waffle

tls.set_credentials_file(username=username, api_key=api_key) # I set username and api_key in the hidden credential_file

colors_dictionary = {'Piazza Pulita':'#211C23', 'Otto e Mezzo':'#3269A4', 'Propaganda Live':'#EDA455', 'Di Martedi':'#B21810'}

df['Colors'] = df['Show'].map(colors_dictionary)

def set_layout(fig_input):
    fig_input.update_layout(template="plotly_white", font_color="black", 
                            title = dict(font=dict(size=20, color = "black", family = "sans-serif")),
                            title_xanchor = 'auto')
    fig_input.update_layout(plot_bgcolor="white", xaxis=dict(linecolor="black"), yaxis=dict(linecolor="black"))
    fig_input.update_xaxes(ticks="outside")
    fig_input.update_yaxes(ticks="outside")

def plot_total_list_genre(df):
    df = overall_plain_total_set(df)
    fig = plt.figure(
        FigureClass = Waffle,
        rows = 10,
        values = df.Count,
        labels = [f"{k} ({int(v / sum(df.values()) * 100)}%)" for k, v in df.items()]
        )
    fig.savefig("genre_total_list.png", bbox_inches="tight")

def plot_percentage_evolution_per_show(df):
    fig = px.line(df, x='Data', y='FemalePercentage', color='Show', color_discrete_map=colors_dictionary, facet_row="Show", markers=True, title="<b>Evolution of Female Guest Presence Over the Season</b>", facet_col_spacing=0.05)
    set_layout(fig)
    fig.for_each_annotation(lambda a: a.update(text=f'<b>{a.text.split("=")[1]}</b>', font=dict(color=colors_dictionary[a.text.split("=")[1]])))
    fig.update_yaxes(tickformat=".0%", title=None)
    fig.update_xaxes(title=None)
    fig.update_layout(showlegend=False)
    row_i = 4
    for show, color in colors_dictionary.items():
        show_data = df[df['Show'] == show]
        min_value = show_data['FemalePercentage'].min()
        max_value = show_data['FemalePercentage'].max()
        fig.add_hrect(
            y0=min_value, y1=max_value,
            fillcolor=color,
            opacity=0.2,
            layer="below",
            line_width=0,
            row=row_i,
            col=1
        )
        row_i=row_i-1
    fig.write_html('results/evolution.html')
    py.plot(fig, filename='evolution', auto_open = False)

def plot_total_percentage_per_show(df):
    data = each_show_total_set_of_guests(df)
    data['Percentage'] = data.groupby('Show')['Count'].apply(lambda x: 100 * x / float(x.sum()))
    fig = px.bar(data, y='Show', x="Count", color="GenderList", custom_data=['GenderList'], orientation='h', color_discrete_map={'F':'#fa4e56', 'M':'#692ac5', 'Unknown':'#a5a5a5'}, title="<b>Gender Split of Unique Guests by Show</b>", text=data['Percentage'].apply(lambda x: '{0:1.1f}%'.format(x)), labels={'GenderList':'Gender'})
    fig.update_traces(hovertemplate='<b>Show:</b> %{y}<br><b>Count:</b> %{x}<br><b>Gender:</b> %{customdata[0]}<extra></extra>')
    fig.update_yaxes(title=None)
    fig.update_xaxes(title=None)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    set_layout(fig)
    fig.write_html('results/total_percentage_per_show.html')
    py.plot(fig, filename='total_percentage_per_show', auto_open = False)

def lollipop_chart(df, values_col, categories_col, values_label, categories_label, color_string):
    fig = px.scatter(df, x=df[values_col], y=df[categories_col], labels={values_col:values_label, categories_col:categories_label})
    fig.update_traces(marker_size=12, marker_color=color_string)
    for i in range(0, len(df[values_col])):
        fig.add_shape(type="line", 
                      x0=0, y0=i, 
                      x1=df.loc[i, values_col], y1=i,
                      line=dict(color=color_string))
    return fig

def plot_mean_female_percentage_per_show(df):
    fig = lollipop_chart(df, 'MeanFemalePercentage', 'Show', "Women Presence Percentage", "", '#fa4e56')
    fig.update_traces(hovertemplate='<b>Women Presence Percentage:</b> %{x}<br><b>Show:</b> %{customdata[0]}<extra></extra>', customdata=df[['Show', 'MeanFemalePercentage']])
    set_layout(fig)
    fig.update_xaxes(tickformat=".1%", title=None)
    fig.update_layout(title="<b>Average Female Guest Presence Across Shows Throughout the Season</b>")
    fig.write_html('results/mean_percentage_per_show.html')
    py.plot(fig, filename='mean_percentage_per_show', auto_open = False)

def plot_guests_histogram():
    df = pd.read_csv("results/per_show_guests_frequence.csv")
    fig = px.histogram(df, x='Count', color='Show', color_discrete_map=colors_dictionary, histnorm='percent', title="<b>Guest Appearance Distribution Across TV Shows</b>")
    fig.update_traces(hovertemplate='<b>Invitations:</b> %{x}<br><b>InviteFrequencyPercentage:</b> %{y:.2f}%<extra></extra>')
    set_layout(fig)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    fig.write_html('results/guests_distribution.html')
    py.plot(fig, filename='guests_distribution', auto_open = False)



###
#plot_percentage_evolution_per_show(df)
#plot_total_percentage_per_show(df)
#plot_mean_female_percentage_per_show(each_show_mean)
plot_guests_histogram()
