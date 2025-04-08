import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

st.title("Analyze, Slice, Dice the Data")
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("**Shape of dataset:**", df.shape)
    st.write(f"Rows originally: {df.shape[0]}")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    st.sidebar.title("Filter Options")
    filter_columns = st.sidebar.multiselect("Select columns to filter by", df.columns)

    filtered_df = df.copy()
    for col in filter_columns:
        unique_values = df[col].dropna().unique()
        selected_values = st.sidebar.multiselect(f"Filter {col}", unique_values)
        if selected_values:
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

    # st.subheader("Filtered Dataset")
    # st.write(f"Rows after filtering: {filtered_df.shape[0]}")
    # st.dataframe(filtered_df.head())

    if st.checkbox("Show Raw Data"):
        st.dataframe(df)
      
    with st.expander("Dataset Overview"):
        st.write("**Column names and types:**")
        st.dataframe(df.dtypes.astype(str))

        st.write("**Missing values:**")
        st.dataframe(df.isnull().sum())

        st.write("**Unique values per column:**")
        unique_vals = pd.DataFrame({col: [df[col].nunique()] for col in df.columns}).T
        unique_vals.columns = ['Unique Count']
        st.dataframe(unique_vals)

        st.text("Statistical information of the dataset")

    with st.expander("Summary Statistics"):
        st.dataframe(df.describe(include='all'))

    st.subheader("Plotting Section")

    x_col = st.selectbox("Select X-axis", df.columns)
    y_col = st.selectbox("Select Y-axis (if applicable)", ['None'] + list(df.columns))
    group_col = st.selectbox("Group by (optional)", ['None'] + list(df.columns))

    plot_type = st.selectbox("Select Plot Type", [
        'Scatter Plot', 'Box Plot', 'Bar Chart',
        'Line Plot', 'Histogram', 'Violin Plot'
    ])

    fig, ax = plt.subplots(figsize=(10, 6))

    try:
        if plot_type == "Scatter Plot":
            if y_col != 'None':
                sns.scatterplot(data=filtered_df, x=x_col, y=y_col,
                                hue=group_col if group_col != 'None' else None, ax=ax)

        # Box Plot
        elif plot_type == "Box Plot":
            if y_col != 'None':
                sns.boxplot(data=filtered_df, x=x_col, y=y_col,
                            hue=group_col if group_col != 'None' else None, ax=ax)

        # Violin Plot
        elif plot_type == "Violin Plot":
            if y_col != 'None':
                sns.violinplot(data=filtered_df, x=x_col, y=y_col,
                               hue=group_col if group_col != 'None' else None, ax=ax)

        # Histogram
        elif plot_type == "Histogram":
            sns.histplot(data=filtered_df, x=x_col,
                         hue=group_col if group_col != 'None' else None, kde=True, ax=ax)

        # Bar Chart
        elif plot_type == "Bar Chart":
            if group_col != 'None':
                count_df = filtered_df.groupby([x_col, group_col]).size().reset_index(name='count')
                sns.barplot(data=count_df, x=x_col, y='count', hue=group_col, ax=ax)
            else:
                count_df = filtered_df[x_col].value_counts().reset_index()
                count_df.columns = [x_col, 'count']
                sns.barplot(data=count_df, x=x_col, y='count', ax=ax)

        # Line Plot
        elif plot_type == "Line Plot":
            if y_col != 'None':
                sns.lineplot(data=filtered_df, x=x_col, y=y_col,
                             hue=group_col if group_col != 'None' else None, ax=ax)

        # Correlation Heatmap
        # elif plot_type == "Correlation Heatmap":
        #     corr = filtered_df.select_dtypes(include=np.number).corr()
        #     fig, ax = plt.subplots(figsize=(10, 6))
        #     sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Plotting failed: {e}")
    
    st.subheader("📊 Explore Grouped Combinations")

    group_cols = st.multiselect("Select column(s) to group by", df.columns)
    agg_func = st.selectbox("Choose aggregation function", ['mean', 'sum', 'count', 'min', 'max'])

    if group_cols:
        try:
            numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()

            # Exclude group_cols from aggregation list
            agg_cols = [col for col in numeric_cols if col not in group_cols]
            agg_df = filtered_df[group_cols + agg_cols]

            grouped_df = agg_df.groupby(group_cols).agg(agg_func).reset_index()

            st.write(f"**Aggregated using `{agg_func}` on numeric columns grouped by {group_cols}**")
            st.dataframe(grouped_df)

        except Exception as e:
            st.warning(f"Grouping error: {e}")

    # # 6. Grouped Summary View (Dicing Aggregation)
    # st.subheader("Explore Grouped Combinations")

    # group_cols = st.multiselect("Select column(s) to group by", df.columns)

    # # Let user choose aggregation function
    # agg_func = st.selectbox("Choose aggregation function", ['mean', 'sum', 'count', 'min', 'max'])

    # if group_cols:
    #     try:
    #         # Select only numeric columns for aggregation
    #         numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()
    #         agg_df = filtered_df[group_cols + numeric_cols]

    #         # Perform aggregation
    #         grouped_df = agg_df.groupby(group_cols).agg(agg_func).reset_index()

    #         st.write(f"**Aggregated using `{agg_func}` on numeric columns grouped by {group_cols}**")
    #         st.dataframe(grouped_df)

    #     except Exception as e:
    #         st.warning(f"Grouping error: {e}")


    # # 5. Grouped Slice-Dice View
    # st.subheader("📊 Explore Grouped Combinations")
    # group_cols = st.multiselect("Select columns for groupby analysis", df.columns)

    # if group_cols:
    #     try:
    #         # Identify numeric columns only
    #         numeric_cols = filtered_df.select_dtypes(include='number').columns.tolist()

    #         # Combine group columns with numeric columns only
    #         agg_df = filtered_df[group_cols + numeric_cols]

    #         # Group by and aggregate
    #         grouped_df = agg_df.groupby(group_cols).mean(numeric_only=True).reset_index()

    #         st.write("Grouped successfully by:", group_cols)
    #         st.dataframe(grouped_df)
    #     except Exception as e:
    #         st.warning(f"Grouping error: {e}")
