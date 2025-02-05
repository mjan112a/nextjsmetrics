import streamlit as st
from datetime import datetime
from utils import (
    calculate_equity_assessment,
    calculate_cheifs_investment,
    calculate_funds_usage
)
from graphs import create_value_graph, create_equity_ratio_graph
from pdf_generator import generate_pdf_report

def render_sidebar():
    """Render the sidebar input form."""
    st.sidebar.header("PRELIMINARY CHEIFS REPORT FACT FINDER")

    st.sidebar.subheader("PROPERTY INFORMATION:")
    client_name = st.sidebar.text_input("CLIENT NAME(S)", "JIM AND MARY SMITH")
    age = st.sidebar.text_input("AGE(S)", "65/60")
    property_address = st.sidebar.text_input("PROPERTY ADDRESS", "123 MAIN STREET ANYTOWN, USA 45612")
    property_type = st.sidebar.selectbox("PROPERTY TYPE (CIRCLE ONE)", 
                                       ["SINGLE FAMILY RESIDENCE", "CONDOMINIUM", "PUD"])

    # Convert number inputs to sliders with appropriate ranges
    approx_home_value = st.sidebar.slider("APPROX. HOME VALUE", 
        min_value=100000, 
        max_value=2000000, 
        value=550000,
        step=10000,
        format="$%d")

    mortgage_balance = st.sidebar.slider("MORTGAGE BALANCE",
        min_value=0,
        max_value=int(approx_home_value * 0.95),  # Max 95% of home value
        value=83000,
        step=1000,
        format="$%d")

    home_equity_loan_balance = st.sidebar.slider("HOME EQUITY LOAN BALANCE",
        min_value=0,
        max_value=int((approx_home_value - mortgage_balance) * 0.9),  # Max 90% of remaining equity
        value=10000,
        step=1000,
        format="$%d")

    return {
        'client_name': client_name,
        'age': age,
        'property_address': property_address,
        'property_type': property_type,
        'approx_home_value': approx_home_value,
        'mortgage_balance': mortgage_balance,
        'home_equity_loan_balance': home_equity_loan_balance
    }

def render_visualizations(home_value, mortgage_balance, equity_loan_balance):
    """Render the visualization graphs in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("VALUE VISUALIZATION")

    # Display the value breakdown graph
    value_fig = create_value_graph(home_value, mortgage_balance, equity_loan_balance)
    st.sidebar.plotly_chart(value_fig, use_container_width=True)

    # Display the equity ratio gauge
    equity_fig = create_equity_ratio_graph(home_value, mortgage_balance + equity_loan_balance)
    st.sidebar.plotly_chart(equity_fig, use_container_width=True)

def render_funds_selection():
    """Render the funds selection in the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("DESIRED USE OF FUNDS:")
    return st.sidebar.selectbox(" ", [
        "I WANT MORE INCOME",
        "I WANT TO BUY LTC COVERAGE",
        "A COMBINATION OF BOTH"
    ], index=1)

def render_main_report(equity_data, investment_data, funds_data):
    """Render the main report section."""
    # Create two columns for header and export button
    header_col, export_col = st.columns([0.85, 0.15])

    with header_col:
        st.header("PRELIMINARY CHEIFS REPORT")
    with export_col:
        if st.button("📄 Export PDF"):
            try:
                pdf_data = {
                    'equity': equity_data,
                    'investment': investment_data,
                    'funds': funds_data
                }
                pdf_buffer = generate_pdf_report(pdf_data)
                
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=f"cheifs_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

    st.subheader("*EQUITY ASSESSMENT")
    st.write(f"ESTIMATED HOME VALUE: {equity_data['estimated_home_value']}")
    st.write(f"SOURCE: {equity_data['source']}")
    st.write(f"STATED DEBT: {equity_data['stated_debt']}")
    st.write(f"ESTIMATED HOME EQUITY: {equity_data['estimated_home_equity']}")

    st.subheader("*CHEIFS INVESTMENT")
    st.write(f"MAX 50% CHEIFS EQUITY SHARE: {investment_data['max_50_cheifs_equity_share']}")
    st.write(f"CURRENT HOME TO VALUE RATIO: {investment_data['current_home_to_value_ratio']:.4f}")
    st.write(f"A LESS B (CHEIFS EQUITY SHARE): {investment_data['a_less_b']:.4f}")
    st.write(f"CHEIFS INVESTMENT IN HOME: {investment_data['cheifs_investment_in_home']:.2f}")
    st.write(f"PROCEEDS TO HOMEOWNER: {investment_data['proceeds_to_homeowner']:.2f}")

    st.subheader("DESIRED USE OF FUNDS:")
    st.write(f"PREMIUM AMOUNT: {funds_data['premium_amount']:.2f}")
    st.write(f"APPROX COVERAGE AMOUNT: {funds_data['approx_coverage_amount']}")
    st.write(f"LEVERAGE: {funds_data['leverage']:.2f}")

    st.write("*ALL FIGURES ARE PRELIMINARY AND FOR INFORMATIONAL PURPOSES")

def main():
    """Main application function."""
    # Get user inputs
    inputs = render_sidebar()
    
    # Calculate values
    equity_data = calculate_equity_assessment(
        inputs['approx_home_value'],
        inputs['mortgage_balance'],
        inputs['home_equity_loan_balance']
    )
    
    investment_data = calculate_cheifs_investment(
        equity_data['estimated_home_value'],
        equity_data['estimated_home_equity']
    )
    
    funds_data = calculate_funds_usage(investment_data['cheifs_investment_in_home'])
    
    # Render visualizations
    render_visualizations(
        inputs['approx_home_value'],
        inputs['mortgage_balance'],
        inputs['home_equity_loan_balance']
    )
    
    # Get funds selection
    use_of_funds = render_funds_selection()
    
    # Render main report
    render_main_report(equity_data, investment_data, funds_data)

if __name__ == "__main__":
    main()
