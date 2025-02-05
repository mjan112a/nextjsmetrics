from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import io

def generate_pdf_report(data):
    """Generate a PDF report with the provided data."""
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
    
    # Equity Assessment Section
    story.append(Paragraph("EQUITY ASSESSMENT", styles["Heading2"]))
    story.extend([
        Paragraph(f"ESTIMATED HOME VALUE: ${data['equity']['estimated_home_value']:,.2f}", styles["Normal"]),
        Paragraph(f"SOURCE: {data['equity']['source']}", styles["Normal"]),
        Paragraph(f"STATED DEBT: ${data['equity']['stated_debt']:,.2f}", styles["Normal"]),
        Paragraph(f"ESTIMATED HOME EQUITY: ${data['equity']['estimated_home_equity']:,.2f}", styles["Normal"]),
        Spacer(1, 20)
    ])
    
    # CHEIFS Investment Section
    story.append(Paragraph("CHEIFS INVESTMENT", styles["Heading2"]))
    story.extend([
        Paragraph(f"MAX 50% CHEIFS EQUITY SHARE: {data['investment']['max_50_cheifs_equity_share']}", styles["Normal"]),
        Paragraph(f"CURRENT HOME TO VALUE RATIO: {data['investment']['current_home_to_value_ratio']:.4f}", styles["Normal"]),
        Paragraph(f"A LESS B (CHEIFS EQUITY SHARE): {data['investment']['a_less_b']:.4f}", styles["Normal"]),
        Paragraph(f"CHEIFS INVESTMENT IN HOME: ${data['investment']['cheifs_investment_in_home']:,.2f}", styles["Normal"]),
        Paragraph(f"PROCEEDS TO HOMEOWNER: ${data['investment']['proceeds_to_homeowner']:,.2f}", styles["Normal"]),
        Spacer(1, 20)
    ])
    
    # Funds Usage Section
    story.append(Paragraph("DESIRED USE OF FUNDS", styles["Heading2"]))
    story.extend([
        Paragraph(f"PREMIUM AMOUNT: ${data['funds']['premium_amount']:,.2f}", styles["Normal"]),
        Paragraph(f"APPROX COVERAGE AMOUNT: ${data['funds']['approx_coverage_amount']:,}", styles["Normal"]),
        Paragraph(f"LEVERAGE: {data['funds']['leverage']:.2f}", styles["Normal"]),
        Spacer(1, 20)
    ])
    
    story.append(Paragraph("*ALL FIGURES ARE PRELIMINARY AND FOR INFORMATIONAL PURPOSES", styles["Italic"]))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
