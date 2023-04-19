import streamlit as st
import pandas as pd
import base64

# Define function to clean the dataset
def clean_data(data):
    # Select the important columns
    columns_to_keep = ['Response ID', 'How Disempowered/Empowered are you about your Abilities & Attributes? Abilities & Attributes', 'How Disempowered/Empowered are you about your Age? Age', 'How Disempowered/Empowered are you about your Class? Class', 'How Disempowered/Empowered are you about your Education? Education', 'How Disempowered/Empowered are you about your Ethnicity? Ethnicity', 'How Disempowered/Empowered are you about your Gender? Gender', 'How Disempowered/Empowered are you about your Language? Language', 'How Disempowered/Empowered are you about your Race? Race', 'How Disempowered/Empowered are you about your Religion? Religion', 'How Disempowered/Empowered are you about your Sexuality? Sexuality']
    data = data.loc[:, columns_to_keep]
    
    # Rename columns
    new_column_names = ['Response ID', 'Abilities & Attributes', 'Age', 'Class', 'Education', 'Ethnicity', 'Gender', 'Language', 'Race', 'Religion', 'Sexuality']
    data.columns = new_column_names
    
    # Convert columns to strings
    for col in new_column_names[1:]:
        data[col] = data[col].astype(str)
    
    # Replace the string "Empowered" or "Disempowered" with the attribute name
    for col in new_column_names[1:]:
        data[col] = data[col].str.split(" ").str[-1]
    
    return data


# Define function to find top and bottom 3 values
def find_top_bottom_3(data):
    # Create a new DataFrame to store the top and bottom 3 values
    top_bottom_df = pd.DataFrame(columns=['Response ID', 'Top 3', 'Bottom 3'])
    
    # Loop through each row and find the top and bottom 3 values
    for index, row in data.iterrows():
        # Convert numeric columns to float
        numeric_cols = row.iloc[1:].apply(pd.to_numeric, errors='coerce')
        # Get top and bottom 3 values from numeric columns
        top_3 = numeric_cols.nlargest(3).index.tolist()
        bottom_3 = numeric_cols.nsmallest(3).index.tolist()
        # Get Response ID and add top and bottom 3 values to DataFrame
        top_bottom_df.loc[index] = [row['Response ID'], ', '.join(top_3), ', '.join(bottom_3)]
    
    return top_bottom_df

# Define the Streamlit app
def main():
    # Add a title to the app
    st.title("Empowering Differences Survey Results")
    
    # Add a file uploader to the app
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])
    
    # If a file is uploaded
    if uploaded_file is not None:
        # Load the data from the file
        data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        
        # Clean the data
        cleaned_data = clean_data(data)
        
        # Find the top and bottom 3 values
        top_bottom_df = find_top_bottom_3(cleaned_data)
        
        # Display the top and bottom 3 values in a table
        st.write(top_bottom_df)
        
        # Add a download link for the table
        csv = top_bottom_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="top_bottom_results.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

        
if __name__ == '__main__':
    main()
