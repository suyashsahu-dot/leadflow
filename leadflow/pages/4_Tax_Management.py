import streamlit as st
import pandas as pd

st.title("Tax Management for Freelancers and Agency Owners")

if "expenses" not in st.session_state:
    st.session_state.expenses = []

st.subheader("Income")
total_income = st.number_input("Enter your total income (in USD):", min_value=0.0, value=0.0)

st.subheader("Expenses")
expense_categories = ["Software", "Marketing", "Office Supplies", "Travel", "Other"]

with st.form("expense_form"):
    st.write("Add an expense:")
    category = st.selectbox("Category", expense_categories)
    amount = st.number_input("Amount (in USD):", min_value=0.0, value=0.0)
    description = st.text_input("Description (optional):")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        st.session_state.expenses.append({
            "Category": category,
            "Amount": amount,
            "Description": description
        })
        st.success("Expense added!")

if st.session_state.expenses:
    st.subheader("All Expenses")
    expense_df = pd.DataFrame(st.session_state.expenses)
    st.dataframe(expense_df)

    total_expenses = expense_df["Amount"].sum()
    st.write(f"**Total Expenses:** ${total_expenses:.2f}")

if total_income > 0 or st.session_state.expenses:
    st.subheader("Tax Calculation")

    tax_rate = st.number_input("Enter your tax rate (in %):", min_value=0.0, max_value=100.0, value=20.0)

    taxable_income = total_income - total_expenses
    taxes_owed = taxable_income * (tax_rate / 100)

    st.write("### Tax Summary")
    st.write(f"**Total Income:** ${total_income:.2f}")
    st.write(f"**Total Expenses:** ${total_expenses:.2f}")
    st.write(f"**Taxable Income:** ${taxable_income:.2f}")
    st.write(f"**Taxes Owed ({tax_rate}%):** ${taxes_owed:.2f}")

    summary_data = {
        "Total Income": [total_income],
        "Total Expenses": [total_expenses],
        "Taxable Income": [taxable_income],
        "Taxes Owed": [taxes_owed]
    }
    summary_df = pd.DataFrame(summary_data)

    excel_file = "tax_summary.xlsx"
    summary_df.to_excel(excel_file, index=False)
    st.download_button(
        label="Download Tax Summary as Excel",
        data=open(excel_file, "rb").read(),
        file_name=excel_file,
        mime="application/vnd.ms-excel"
    )
else:
    st.info("Please enter your income and expenses to calculate taxes.")

if st.session_state.expenses:
    if st.button("Clear All Expenses"):
        st.session_state.expenses = []
        st.success("All expenses cleared!")