import streamlit as st
from datetime import datetime
from utils import (
    calculate_equity_assessment,
    calculate_cheifs_investment,
    calculate_funds_usage
)
from graphs import create_value_graph, create_equity_ratio_graph
from pdf_generator import generate_pdf_report

def render_input_form():
    """Render the input form using tabs for better organization."""
    st.sidebar.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <h1 style='color: #1f77b4;'>Panorama FA</h1>
            <h3>PRELIMINARY CHEIFS REPORT FACT FINDER</h3>
        </div>
    """, unsafe_allow_html=True)

    # Create tabs for different input sections
    client_tab, property_tab, financial_tab = st.sidebar.tabs([
        "👥 Client", "🏠 Property", "💰 Financial"
    ])

    with client_tab:
        client_name = st.text_input("CLIENT NAME(S)", "JIM AND MARY SMITH")
        age = st.text_input("AGE(S)", "65/60")

    with property_tab:
        property_address = st.text_input("PROPERTY ADDRESS", "123 MAIN STREET ANYTOWN, USA 45612")
        property_type = st.selectbox("PROPERTY TYPE", 
                                   ["SINGLE FAMILY RESIDENCE", "CONDOMINIUM", "PUD"])

    with financial_tab:
        st.markdown("### Property Value")
        approx_home_value = st.slider("ESTIMATED HOME VALUE", 
            min_value=100000, 
            max_value=2000000, 
            value=595000,
            step=5000,
            format="$%d")

        st.markdown("### Current Loans")
        mortgage_balance = st.slider("MORTGAGE BALANCE",
            min_value=0,
            max_value=int(approx_home_value * 0.95),
            value=83000,
            step=1000,
            format="$%d")

        home_equity_loan_balance = st.slider("HOME EQUITY LOAN BALANCE",
            min_value=0,
            max_value=int((approx_home_value - mortgage_balance) * 0.9),
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
    """Render the visualization graphs."""
    # Create two columns for the visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Display the value breakdown graph
        value_fig = create_value_graph(home_value, mortgage_balance, equity_loan_balance)
        st.plotly_chart(value_fig, use_container_width=True)
    
    with col2:
        # Display the equity ratio gauge
        equity_fig = create_equity_ratio_graph(home_value, mortgage_balance + equity_loan_balance)
        st.plotly_chart(equity_fig, use_container_width=True)

def render_funds_selection():
    """Render the funds selection."""
    st.subheader("DESIRED USE OF FUNDS:")
    return st.selectbox(" ", [
        "I WANT MORE INCOME",
        "I WANT TO BUY LTC COVERAGE",
        "A COMBINATION OF BOTH"
    ], index=1)

def render_main_report(equity_data, investment_data, funds_data):
    """Render the main report section with improved visual layout."""
    # Create two columns for header and export button
    header_col, export_col = st.columns([0.85, 0.15])

    with header_col:
        st.markdown("""
            <h1 style='color: #1f77b4; margin-bottom: 0;'>PRELIMINARY CHEIFS REPORT</h1>
        """, unsafe_allow_html=True)
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

    # Equity Assessment Section
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;'>
            <h3 style='color: #2c3e50; margin-top: 0;'>🏠 EQUITY ASSESSMENT</h3>
            <table style='width: 100%;'>
                <tr>
                    <td style='padding: 8px 0;'>ESTIMATED HOME VALUE:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>SOURCE:</td>
                    <td style='text-align: right;'><strong>{}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>STATED DEBT:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>ESTIMATED HOME EQUITY:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
            </table>
        </div>
    """.format(
        equity_data['estimated_home_value'],
        equity_data['source'],
        equity_data['stated_debt'],
        equity_data['estimated_home_equity']
    ), unsafe_allow_html=True)

    # CHEIFS Investment Section
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;'>
            <h3 style='color: #2c3e50; margin-top: 0;'>💰 CHEIFS INVESTMENT</h3>
            <table style='width: 100%;'>
                <tr>
                    <td style='padding: 8px 0;'>MAX 50% CHEIFS EQUITY SHARE:</td>
                    <td style='text-align: right;'><strong>{:.1%}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>DEBT TO HOME VALUE RATIO:</td>
                    <td style='text-align: right;'><strong>{:.1%}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>CHEIFS EQUITY SHARE:</td>
                    <td style='text-align: right;'><strong>{:.1%}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>CHEIFS INVESTMENT IN HOME:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>PROCEEDS TO HOMEOWNER:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
            </table>
        </div>
    """.format(
        investment_data['max_50_cheifs_equity_share'],
        investment_data['debt_to_home_value_ratio'],
        investment_data['cheifs_equity_share'],
        investment_data['cheifs_investment_in_home'],
        investment_data['proceeds_to_homeowner']
    ), unsafe_allow_html=True)

    # Funds Usage Section
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 10px 0;'>
            <h3 style='color: #2c3e50; margin-top: 0;'>📊 DESIRED USE OF FUNDS</h3>
            <table style='width: 100%;'>
                <tr>
                    <td style='padding: 8px 0;'>PREMIUM AMOUNT:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>APPROX COVERAGE AMOUNT:</td>
                    <td style='text-align: right;'><strong>${:,.2f}</strong></td>
                </tr>
                <tr>
                    <td style='padding: 8px 0;'>LEVERAGE:</td>
                    <td style='text-align: right;'><strong>{:.2%}</strong></td>
                </tr>
            </table>
        </div>
    """.format(
        funds_data['premium_amount'],
        funds_data['approx_coverage_amount'],
        funds_data['leverage']
    ), unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; color: #666; font-style: italic; margin-top: 20px;'>
            *ALL FIGURES ARE PRELIMINARY AND FOR INFORMATIONAL PURPOSES
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function."""
    # Set page config for better mobile display
    st.set_page_config(
        page_title="CHEIFS Calculator",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Add custom CSS for mobile responsiveness
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        .stTabs [data-baseweb="tab"] {
            padding-right: 4px;
            padding-left: 4px;
        }
        @media (max-width: 640px) {
            .main .block-container {
                padding-top: 1rem;
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Get user inputs using the new tabbed interface
    inputs = render_input_form()
    
    # Calculate values
    equity_data = calculate_equity_assessment(
        inputs['approx_home_value'],
        inputs['mortgage_balance'],
        inputs['home_equity_loan_balance']
    )
    
    investment_data = calculate_cheifs_investment(
        equity_data['estimated_home_value'],
        equity_data['stated_debt'],
        equity_data['estimated_home_equity']
    )
    
    funds_data = calculate_funds_usage(investment_data['proceeds_to_homeowner'])
    
    # Create tabs for main content
    overview_tab, details_tab = st.tabs(["Overview", "Detailed Report"])
    
    with overview_tab:
        # Render visualizations in the main content area
        render_visualizations(
            inputs['approx_home_value'],
            inputs['mortgage_balance'],
            inputs['home_equity_loan_balance']
        )
        
        # Get funds selection
        use_of_funds = render_funds_selection()
    
    with details_tab:
        # Render detailed report
        render_main_report(equity_data, investment_data, funds_data)

if __name__ == "__main__":
    main()
