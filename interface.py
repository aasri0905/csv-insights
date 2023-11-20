import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

from agent import query_agent, create_agent  

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """
    print(response_dict)
    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
st.markdown(
    """
    <style>
    body {
        color: black;
        background-color: #f4f4f4;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("👨‍💻 Chat with your CSV")

st.write("Please upload your CSV file below.")

data = st.file_uploader("Upload a CSV")

query = st.text_area("Insert your query")

if st.button("Submit Query", type="primary"):
    # Create an agent from the CSV file.
    agent, df = create_agent(data)
    columns = df.columns.tolist()

    selected_row = st.selectbox("Select a row", columns)
    selected_column = st.selectbox("Select a column", columns)

    visualization_type = st.radio("Select visualization type", ('Scatter Plot', 'Line Graph', 'Bar Chart', 'Pie Chart'))

    if selected_row and selected_column and visualization_type:
        if visualization_type == 'Scatter Plot':
            st.write(f"### Scatter Plot between {selected_row} and {selected_column}")
            if df[selected_row].dtype in ['int', 'float'] and df[selected_column].dtype in ['int', 'float']:
                plt.figure(figsize=(8, 6))
                plt.scatter(df[selected_column], df[selected_row], alpha=0.5)
                plt.xlabel(selected_column)
                plt.ylabel(selected_row)
                plt.title(f"{selected_column} vs {selected_row} Scatter Plot")
                st.pyplot(plt)
            else:
                st.write("Please select columns with numerical data for plotting.")

        elif visualization_type == 'Line Graph':
            st.write(f"### Line Graph for {selected_column}")
            if df[selected_column].dtype in ['int', 'float']:
                plt.figure(figsize=(8, 6))
                plt.plot(df[selected_column])
                plt.xlabel("Index")
                plt.ylabel(selected_column)
                plt.title(f"Line Graph for {selected_column}")
                st.pyplot(plt)
            else:
                st.write("Please select a column with numerical data for plotting.")

        elif visualization_type == 'Bar Chart':
            st.write(f"### Bar Chart for {selected_column}")
            if df[selected_column].dtype in ['int', 'float']:
                plt.figure(figsize=(8, 6))
                df[selected_column].plot(kind='bar')
                plt.xlabel("Index")
                plt.ylabel(selected_column)
                plt.title(f"Bar Chart for {selected_column}")
                st.pyplot(plt)
            else:
                st.write("Please select a column with numerical data for plotting.")

        elif visualization_type == 'Pie Chart':
            st.write(f"### Pie Chart for {selected_column}")
            if df[selected_column].dtype in ['int', 'float']:
                plt.figure(figsize=(8, 6))
                df[selected_column].plot(kind='pie')
                plt.title(f"Pie Chart for {selected_column}")
                st.pyplot(plt)
            else:
                st.write("Please select a column with numerical data for plotting.")

    # Query the agent.
    response = query_agent(agent=agent, query=query)

    # Decode the response.
    decoded_response = decode_response(response)

    # Write the response to the Streamlit app.
    write_response(decoded_response)
