import streamlit as st
import pandas as pd

# Function to calculate monthly payment
def calculate_payment(price, down, term, rate):
    loan_amount = price - down
    monthly_rate = rate / 100 / 12

    if monthly_rate > 0:
        payment = (monthly_rate * loan_amount) / (1 - (1 + monthly_rate) ** -term)
    else:
        payment = loan_amount / term

    return round(payment, 2), loan_amount, monthly_rate

# Streamlit UI
st.title("Auto Loan Estimator with Amortization")

price = st.number_input("Vehicle Price ($)", value=25000)
down = st.number_input("Down Payment ($)", value=5000)
term = st.number_input("Loan Term (Months)", value=60)
rate = st.number_input("Interest Rate (APR %)", value=6.5)

if st.button("Calculate"):
    payment, loan_amount, monthly_rate = calculate_payment(price, down, term, rate)
    st.write(f"**Monthly Payment:** ${payment}")
    st.write(f"**Loan Amount:** ${loan_amount}")
    
    # Amortization schedule
    schedule = []
    balance = loan_amount

    for month in range(1, term + 1):
        interest = balance * monthly_rate
        principal = payment - interest
        balance -= principal

        schedule.append({
            "Month": month,
            "Payment": round(payment, 2),
            "Principal": round(principal, 2),
            "Interest": round(interest, 2),
            "Balance": round(balance, 2)
        })

        if balance <= 0:
            break

    df = pd.DataFrame(schedule)
    st.dataframe(df)

    # CSV export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "amortization_schedule.csv", "text/csv")
