import streamlit as st
import pandas as pd

st.title("Stock Adjustment Tool")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

target_sum = st.number_input("Enter Target Total", value=0.0)

if uploaded_file and target_sum > 0:
    df = pd.read_excel(uploaded_file)

    df = df[[
        "Item Name",
        "Inventory Asset Value",
        "Usage Unit",
        "SKU",
        "Category Name"
    ]]

    fixed = df[df["Inventory Asset Value"] <= 1].copy()
    adjustable = df[df["Inventory Asset Value"] > 1].copy()

    fixed_total = fixed["Inventory Asset Value"].sum()
    adjustable_total = adjustable["Inventory Asset Value"].sum()

    remaining = target_sum - fixed_total

    if adjustable_total == 0:
        st.error("No values greater than 1 to adjust.")
    elif remaining < 0:
        st.error("Target sum is too small.")
    else:
        adjustable["Adjusted Value"] = adjustable["Inventory Asset Value"] * (remaining / adjustable_total)
        fixed["Adjusted Value"] = fixed["Inventory Asset Value"]

        final_df = pd.concat([fixed, adjustable])
        final_df["Difference"] = final_df["Adjusted Value"] - final_df["Inventory Asset Value"]

        st.success("Processing complete!")

        st.download_button(
            label="Download Adjusted Excel",
            data=final_df.to_excel(index=False, engine='openpyxl'),
            file_name="adjusted_output.xlsx"
        )