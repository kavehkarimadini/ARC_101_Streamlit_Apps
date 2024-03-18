import pandas as pd
import streamlit as st
# import plotly.graph_objects as go
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
    # print("res_cols: ",res_cols[-1],type(res_cols[-1]))
    final = result.rename(columns={res_cols[-1]:"Frequency"})
    # print(final.columns.tolist())
    return final[final["Frequency"]>3]

def filter_labels(F_df,label):
    return F_df[F_df[target_col]==label]

def plotly_bar_func(df,labels,label,x_col,y_col,color_col):
    if label not in labels:
        # Create a bar chart
        fig = px.bar(df, x=x_col, y=y_col, color=df[color_col],
                    title='Frequency of Text Elements',
                    labels={'count':'Frequency', 'text':'Text Elements'},
                    template='plotly_dark')
    else:
        filtered_df = filter_labels(df,label)
        fig = px.bar(filtered_df, x=x_col, y=y_col, color=filtered_df[color_col],
            title='Frequency of Text Elements',
            labels={'count':'Frequency', 'text':'Text Elements'},
            template='plotly_dark')
        
    fig.update_layout(
        xaxis_title='Text Elements',
        yaxis_title='Frequency',
        legend_title='Labels',
        font=dict(family="Courier New, monospace", size=18, color="white")
    )
    return fig

def plotly_sunburst_func(df,labels,label,text_col,label_col,freq_col):
    if label not in labels:
        # Create a sunburst chart
        fig = px.sunburst(
                            df,
                            path=[label_col, text_col],
                            values=freq_col,
                        )
    else:
        filtered_df = filter_labels(df,label)
        # Create a sunburst chart
        fig = px.sunburst(
                            filtered_df,
                            path=[label_col, text_col],
                            values=freq_col,
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
if label in labels:
    filtered_df = filter_labels(df,label)
    edited_df = st.data_editor(filtered_df, num_rows="dynamic",use_container_width=st.session_state.use_container_width)
else:
    edited_df = st.data_editor(df, num_rows="dynamic",use_container_width=st.session_state.use_container_width)
plt_fig = plotly_bar_func(df,labels,label,columns[-3],columns[-1],columns[-2])
sunburst_fig = plotly_sunburst_func(df,labels,label,columns[0],columns[1],columns[2])
st.plotly_chart(plt_fig)
st.plotly_chart(sunburst_fig)
# favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
# st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
# Display the dataframe and allow the user to stretch the dataframe
# across the full width of the container, based on the checkbox value
# st.dataframe(df, use_container_width=st.session_state.use_container_width)
