import pandas as pd
# import string
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Cache the dataframe so it's only loaded once
# @st.cache_data
#-------------------define functions----------------------------------------------------
def load_data_ner():
    penguin_file = st.file_uploader("Select Your Local NER CSV file")
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

def load_data_senti():
    penguin_file = st.file_uploader("Select Your Local sentiment CSV file")
    if penguin_file is None:
        st.stop()
    # Create a new column 'Name_Count' to store the counts
    senti_df = pd.read_csv(penguin_file)
    # col_names = senti_df.columns.tolist()
    # senti_df[col_names[0]] = senti_df[col_names[0]].map(lambda x: x[:3].strip().replace(".","") if x[0].isdigit() else x)
    # print(senti_df[col_names[0]])
    return senti_df

def filter_labels(F_df,label):
    return F_df[F_df[target_col]==label]

def plotly_bar_NER_func(df,labels,label,x_col,y_col,color_col):
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

def plotly_bar_senti_func(formated_sent_df,col_names):
    # questions = formated_sent_df[col_names[0]].map(lambda x: x[:3].strip().replace(".","") if x[0].isdigit() else x)
    questions = formated_sent_df.index.tolist()
    print(questions)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=questions,
        hoverinfo = "all",
        y=formated_sent_df[col_names[1]].tolist(),
        name=col_names[1],
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=questions,
        hoverinfo = "all",
        y=formated_sent_df[col_names[2]].tolist(),
        name=col_names[2],
        marker_color='MediumPurple'
    ))
    fig.add_trace(go.Bar(
        x=questions,
        hoverinfo = "all",
        y=formated_sent_df[col_names[3]].tolist(),
        name=col_names[3],
        marker_color='DarkSlateGrey'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)#,template="plotly_dark")
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
df = load_data_ner()
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
plt_fig = plotly_bar_NER_func(df,labels,label,columns[-3],columns[-1],columns[-2])
sunburst_fig = plotly_sunburst_func(df,labels,label,columns[0],columns[1],columns[2])
tab1, tab2 = st.tabs(["Bar Chart NER", "Sun Burst Chart NER"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(plt_fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(sunburst_fig, theme="streamlit", use_container_width=True)
# st.plotly_chart(plt_fig)
# st.plotly_chart(sunburst_fig)

senti_df = load_data_senti()
senti_df_col_names = senti_df.columns.tolist()
if ('sentidf_key' not in st.session_state):# or st.session_state.sentidf_key > 0:
    st.session_state.sentidf_key = 1
# st.session_state.sentidf_key += 1
if st.button("Reset bellow dataframe", type="primary"):
    st.session_state.sentidf_key += 1
    print(f"Session state updated. New key: {st.session_state.sentidf_key}")
senti_edited_data = st.data_editor(senti_df.reset_index(), num_rows="dynamic",key=f'df_{st.session_state.sentidf_key}',use_container_width=st.session_state.use_container_width)
senti_bar_plt = plotly_bar_senti_func(senti_edited_data,senti_df_col_names)
st.plotly_chart(senti_bar_plt)
# st.button("Reset", type="primary")
# if st.button("Reset", type="primary"):
#     st.session_state.sentidf_key += 1
#     print(f"Session state updated. New key: {st.session_state.sentidf_key}")
    # senti_edited_data = st.data_editor(senti_df.reset_index(), num_rows="dynamic",key=f'sentidf_{st.session_state.sentidf_key}',use_container_width=st.session_state.use_container_width)
    # senti_edited_data = senti_edited_data = st.data_editor(senti_df.reset_index(), num_rows="dynamic",key=f'editor_{st.session_state.my_editor_key}',use_container_width=st.session_state.use_container_width)
    # senti_edited_data = st.data_editor(senti_df.reset_index(), num_rows="dynamic",use_container_width=st.session_state.use_container_width)
