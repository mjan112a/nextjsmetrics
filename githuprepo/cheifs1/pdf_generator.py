from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime
import io

def generate_pdf_report(data):
    """Generate a professionally formatted PDF report with the provided data."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=50)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1f77b4'),
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2c3e50')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8,
        leading=16
    )
    
    # Header with Panorama FA branding
    story.append(Paragraph("Panorama FA", title_style))
    story.append(Paragraph("PRELIMINARY CHEIFS REPORT", heading_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Equity Assessment Section
    story.append(Paragraph("🏠 EQUITY ASSESSMENT", heading_style))
    story.extend([
        Paragraph(f"ESTIMATED HOME VALUE: ${data['equity']['estimated_home_value']:,.2f}", normal_style),
        Paragraph(f"SOURCE: {data['equity']['source']}", normal_style),
        Paragraph(f"STATED DEBT: ${data['equity']['stated_debt']:,.2f}", normal_style),
        Paragraph(f"ESTIMATED HOME EQUITY: ${data['equity']['estimated_home_equity']:,.2f}", normal_style),
        Spacer(1, 10)
    ])
    
    # CHEIFS Investment Section
    story.append(Paragraph("💰 CHEIFS INVESTMENT", heading_style))
    story.extend([
        Paragraph(f"MAX 50% CHEIFS EQUITY SHARE: {data['investment']['max_50_cheifs_equity_share']:.1%}", normal_style),
        Paragraph(f"DEBT TO HOME VALUE RATIO: {data['investment']['debt_to_home_value_ratio']:.1%}", normal_style),
        Paragraph(f"CHEIFS EQUITY SHARE: {data['investment']['cheifs_equity_share']:.1%}", normal_style),
        Paragraph(f"CHEIFS INVESTMENT IN HOME: ${data['investment']['cheifs_investment_in_home']:,.2f}", normal_style),
        Paragraph(f"PROCEEDS TO HOMEOWNER: ${data['investment']['proceeds_to_homeowner']:,.2f}", normal_style),
        Spacer(1, 10)
    ])
    
    # Funds Usage Section
    story.append(Paragraph("📊 DESIRED USE OF FUNDS", heading_style))
    story.extend([
        Paragraph(f"PREMIUM AMOUNT: ${data['funds']['premium_amount']:,.2f}", normal_style),
        Paragraph(f"APPROX COVERAGE AMOUNT: ${data['funds']['approx_coverage_amount']:,}", normal_style),
        Paragraph(f"LEVERAGE: {data['funds']['leverage']:.2%}", normal_style),
        Spacer(1, 20)
    ])
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Italic'],
        fontSize=10,
        textColor=colors.gray,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("*ALL FIGURES ARE PRELIMINARY AND FOR INFORMATIONAL PURPOSES", footer_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
