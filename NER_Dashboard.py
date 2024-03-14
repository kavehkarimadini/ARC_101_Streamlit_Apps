import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Cache the dataframe so it's only loaded once
# @st.cache_data
#-------------------define functions----------------------------------------------------
def load_data():
    penguin_file = st.file_uploader("Select Your Local CSV (default provided)")
    if penguin_file is None:
        st.stop()
    # Create a new column 'Name_Count' to store the counts
    df = pd.read_csv(penguin_file)
    columns_name = df.columns.tolist()
    # # print(columns_name)
    # df_counts = df[columns_name[0]].value_counts().reset_index()
    # # Merge using inner join on the 'text' column
    # result = df_counts.merge(df, how='left', on="text").drop_duplicates()
    # Assuming df is your DataFrame and col1, col2 are the columns you want to count values from
    result = df.groupby(columns_name).size().reset_index()
    # print(type(result))
    res_cols = result.columns.tolist()
    print("res_cols: ",res_cols[-1],type(res_cols[-1]))
    final = result.rename(columns={res_cols[-1]:"Frequency"})
    print(final.columns.tolist())
    return final

def plotly_func(df,label,x_col,y_col):
    # freq = freq.Country.value_counts().reset_index().rename(columns={"index": "x"})

    # read in 3d volcano surface data
    # df_v = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/volcano.csv")

    # Initialize figure with subplots
    fig = make_subplots(
        rows=2, cols=2,
        column_widths=[0.6, 0.4],
        row_heights=[0.4, 0.6],
        specs=[[{"type": "bar", "rowspan": 2}, {"type": "bar"}],
            [            None                    , {"type": "surface"}]])

    # Add scattergeo globe map of volcano locations
    fig.add_trace(
        go.bar(df, x=x_col, y=y_col,
             hover_data=['count'], color='count',
             labels={x_col:'Named Entities',y_col:"frequency"}, height=400),
        row=1, col=1
    )

    # # Add locations bar chart
    # fig.add_trace(
    #     go.Bar(x=freq["x"][0:10],y=freq["Country"][0:10], marker=dict(color="crimson"), showlegend=False),
    #     row=1, col=2
    # )

    # # Add 3d surface of volcano
    # fig.add_trace(
    #     go.Surface(z=df_v.values.tolist(), showscale=False),
    #     row=2, col=2
    # )

    # # Update geo subplot properties
    # fig.update_geos(
    #     projection_type="orthographic",
    #     landcolor="white",
    #     oceancolor="MidnightBlue",
    #     showocean=True,
    #     lakecolor="LightBlue"
    # )

    # Rotate x-axis labels
    fig.update_xaxes(tickangle=45)

    # Set theme, margin, and annotation in layout
    fig.update_layout(
        template="plotly_dark",
        margin=dict(r=10, t=25, b=40, l=60),
        annotations=[
            dict(
                text="Source: NOAA",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0,
                y=0)
        ]
    )
    return fig
# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("Use container width", value=False, key="use_container_width")
df = load_data()
columns = df.columns
sort_col = st.selectbox(
 "What column do you want to sort descending?",
 columns,index=None,placeholder="choose a column to filter"
)
if sort_col is None:
    st.stop()
df = df.sort_values(by=[sort_col],ascending=False)
target_col = st.selectbox(
 "What column do you want to filter?",
 columns,index=None,placeholder="choose a column to filter"
)
if target_col is None:
    st.stop()
labels = df[target_col].unique().tolist()
label = st.selectbox(
 "What do you want the x variable to be?",
 labels,index=None,placeholder="choose a label"
)
def filter_labels(F_df,label):
    return F_df[F_df[target_col]==label]
if label in labels:
    filtered_df = filter_labels(df,label)
    edited_df = st.data_editor(filtered_df, num_rows="dynamic",use_container_width=st.session_state.use_container_width)
else:
    edited_df = st.data_editor(df, num_rows="dynamic",use_container_width=st.session_state.use_container_width)

# st.plotly_chart()

# favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
# st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
# Display the dataframe and allow the user to stretch the dataframe
# across the full width of the container, based on the checkbox value
# st.dataframe(df, use_container_width=st.session_state.use_container_width)
