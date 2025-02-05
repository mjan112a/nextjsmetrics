import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_value_graph(home_value, mortgage_balance, equity_loan_balance):
    # Create a bar chart showing home value breakdown
    fig = go.Figure(data=[
        go.Bar(name='Home Equity', y=['Home'], x=[home_value - mortgage_balance - equity_loan_balance], marker_color='#2ecc71'),
        go.Bar(name='Mortgage Balance', y=['Home'], x=[mortgage_balance], marker_color='#e74c3c'),
        go.Bar(name='Home Equity Loan', y=['Home'], x=[equity_loan_balance], marker_color='#f39c12')
    ])
    
    fig.update_layout(
        barmode='stack',
        title='Home Value Breakdown',
        xaxis_title='Amount ($)',
        height=200,
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig

def create_equity_ratio_graph(home_value, total_debt):
    # Create a gauge chart showing equity ratio
    equity_ratio = (home_value - total_debt) / home_value
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = equity_ratio * 100,
        title = {'text': "Equity Ratio"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2ecc71"},
            'steps': [
                {'range': [0, 33], 'color': "#ffebee"},
                {'range': [33, 66], 'color': "#e8f5e9"},
                {'range': [66, 100], 'color': "#c8e6c9"}
            ]
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    return fig

# Function to create PDF
def export_to_pdf():
    import pdfkit
    from datetime import datetime
    
    # Hide the button when generating PDF
    st.session_state.generating_pdf = True
    st.experimental_rerun()

# --- Input Form ---
st.sidebar.header("PRELIMINARY CHEIFS REPORT FACT FINDER")

st.sidebar.subheader("PROPERTY INFORMATION:")
client_name = st.sidebar.text_input("CLIENT NAME(S)", "JIM AND MARY SMITH")
age = st.sidebar.text_input("AGE(S)", "65/60")
property_address = st.sidebar.text_input("PROPERTY ADDRESS", "123 MAIN STREET ANYTOWN, USA 45612")
property_type = st.sidebar.selectbox("PROPERTY TYPE (CIRCLE ONE)", ["SINGLE FAMILY RESIDENCE", "CONDOMINIUM", "PUD"])

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

# Add graphs to sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("VALUE VISUALIZATION")

# Display the value breakdown graph
value_fig = create_value_graph(approx_home_value, mortgage_balance, home_equity_loan_balance)
st.sidebar.plotly_chart(value_fig, use_container_width=True)

# Display the equity ratio gauge
equity_fig = create_equity_ratio_graph(approx_home_value, mortgage_balance + home_equity_loan_balance)
st.sidebar.plotly_chart(equity_fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.subheader("DESIRED USE OF FUNDS:")
use_of_funds = st.sidebar.selectbox(" ", ["I WANT MORE INCOME", "I WANT TO BUY LTC COVERAGE", "A COMBINATION OF BOTH"], index=1)

# --- Calculations ---

# EQUITY ASSESSMENT
estimated_home_value = approx_home_value  # Use approx_home_value from input
source = "ZILLOW"  # You can make this an input if needed
stated_debt = mortgage_balance + home_equity_loan_balance
estimated_home_equity = estimated_home_value - stated_debt

# CHEIFS INVESTMENT
max_50_cheifs_equity_share = 0.5
current_home_to_value_ratio = estimated_home_equity / estimated_home_value
a_less_b = max_50_cheifs_equity_share - current_home_to_value_ratio
cheifs_investment_in_home = a_less_b * estimated_home_value
proceeds_to_homeowner = cheifs_investment_in_home

# --- Output ---

# Create two columns for header and export button
header_col, export_col = st.columns([0.85, 0.15])

with header_col:
    st.header("PRELIMINARY CHEIFS REPORT")
with export_col:
    if st.button("📄 Export PDF"):
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from datetime import datetime
            import io
            
            # Create an in-memory PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Custom style for the title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30
            )
            
            # Add content
            story.append(Paragraph("PRELIMINARY CHEIFS REPORT", title_style))
            story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
            story.append(Spacer(1, 20))
            
            # Add sections
            story.append(Paragraph("EQUITY ASSESSMENT", styles["Heading2"]))
            story.extend([
                Paragraph(f"ESTIMATED HOME VALUE: ${estimated_home_value:,.2f}", styles["Normal"]),
                Paragraph(f"SOURCE: {source}", styles["Normal"]),
                Paragraph(f"STATED DEBT: ${stated_debt:,.2f}", styles["Normal"]),
                Paragraph(f"ESTIMATED HOME EQUITY: ${estimated_home_equity:,.2f}", styles["Normal"]),
                Spacer(1, 20)
            ])
            
            story.append(Paragraph("CHEIFS INVESTMENT", styles["Heading2"]))
            story.extend([
                Paragraph(f"MAX 50% CHEIFS EQUITY SHARE: {max_50_cheifs_equity_share}", styles["Normal"]),
                Paragraph(f"CURRENT HOME TO VALUE RATIO: {current_home_to_value_ratio:.4f}", styles["Normal"]),
                Paragraph(f"A LESS B (CHEIFS EQUITY SHARE): {a_less_b:.4f}", styles["Normal"]),
                Paragraph(f"CHEIFS INVESTMENT IN HOME: ${cheifs_investment_in_home:,.2f}", styles["Normal"]),
                Paragraph(f"PROCEEDS TO HOMEOWNER: ${proceeds_to_homeowner:,.2f}", styles["Normal"]),
                Spacer(1, 20)
            ])
            
            story.append(Paragraph("DESIRED USE OF FUNDS", styles["Heading2"]))
            story.extend([
                Paragraph(f"PREMIUM AMOUNT: ${cheifs_investment_in_home:,.2f}", styles["Normal"]),
                Paragraph(f"APPROX COVERAGE AMOUNT: $225,000", styles["Normal"]),
                Paragraph(f"LEVERAGE: {225000/proceeds_to_homeowner:.2f}", styles["Normal"]),
                Spacer(1, 20)
            ])
            
            story.append(Paragraph("*ALL FIGURES ARE PRELIMINARY AND FOR INFORMATIONAL PURPOSES", styles["Italic"]))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            # Provide download button
            st.download_button(
                label="Download PDF",
                data=buffer,
                file_name=f"cheifs_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Error generating PDF. Please ensure wkhtmltopdf is installed. Error: {str(e)}")

st.subheader("*EQUITY ASSESSMENT")
st.write(f"ESTIMATED HOME VALUE: {estimated_home_value}")
st.write(f"SOURCE: {source}")
st.write(f"STATED DEBT: {stated_debt}")
st.write(f"ESTIMATED HOME EQUITY: {estimated_home_equity}")

st.subheader("*CHEIFS INVESTMENT")
st.write(f"MAX 50% CHEIFS EQUITY SHARE: {max_50_cheifs_equity_share}")
st.write(f"CURRENT HOME TO VALUE RATIO: {current_home_to_value_ratio:.4f}")
st.write(f"A LESS B (CHEIFS EQUITY SHARE): {a_less_b:.4f}")
st.write(f"CHEIFS INVESTMENT IN HOME: {cheifs_investment_in_home:.2f}")
st.write(f"PROCEEDS TO HOMEOWNER: {proceeds_to_homeowner:.2f}")

st.subheader("DESIRED USE OF FUNDS:")
st.write(f"PREMIUM AMOUNT: {cheifs_investment_in_home:.2f}")
st.write(f"APPROX COVERAGE AMOUNT: {225000}") # fixed
st.write(f"LEVERAGE: {225000/proceeds_to_homeowner:.2f}") # fixed / proceeds_to_homeowner

st.write("*ALL FIGURES ARE PRELIMINARY AND FOR INFORMATIONAL PURPOSES")
