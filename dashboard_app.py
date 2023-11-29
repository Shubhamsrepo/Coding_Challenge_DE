import streamlit as st
import pandas as pd
import snowflake.connector

# Snowflake connection details
snowflake_account = st.secrets["account"]
snowflake_user = st.secrets["user"]
snowflake_password = st.secrets["password"]
snowflake_database = "DEMO_DB"
snowflake_schema = "PUBLIC"
snowflake_warehouse = "COMPUTE_WH"

# Snowflake connection
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    warehouse=snowflake_warehouse,
    database=snowflake_database,
    schema=snowflake_schema
)

# Function to retrieve data from Snowflake
def get_data():
    query = "SELECT * FROM BOOKS"
    return pd.read_sql(query, conn)

# Streamlit app
def main():
    st.title("Snowflake Data Dashboard")
    
    # Retrieve data from Snowflake
    data = get_data()

    # Display the raw data
    st.subheader("Raw Data")
    st.write(data)

    # Display some basic statistics
    st.subheader("Basic Statistics")
    st.write(data.describe())

    # Sorting and filtering options
    st.sidebar.subheader("Sorting and Filtering Options")

    # Sorting
    sorted_column = st.sidebar.selectbox("Sort by Column", data.columns)
    ascending = st.sidebar.checkbox("Ascending", True)
    data_sorted = data.sort_values(by=sorted_column, ascending=ascending)

    # Filtering
    selected_rating = st.sidebar.slider("Filter by Rating", min_value=1, max_value=5, value=(1, 5))
    data_filtered = data[(data['RATING'] >= selected_rating[0]) & (data['RATING'] <= selected_rating[1])]

    # Display sorted and filtered data
    st.subheader("Sorted and Filtered Data")
    st.write(data_sorted)
    st.write(f"Number of records after filtering: {len(data_filtered)}")

    # Additional visualizations can be added based on your specific requirements

if __name__ == "__main__":
    main()
