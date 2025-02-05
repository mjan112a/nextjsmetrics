import plotly.graph_objects as go

def create_value_graph(home_value, mortgage_balance, equity_loan_balance):
    """Create a pie chart showing home value breakdown."""
    equity = home_value - mortgage_balance - equity_loan_balance
    
    # Calculate percentages for labels
    total = home_value
    equity_pct = (equity / total) * 100
    mortgage_pct = (mortgage_balance / total) * 100
    loan_pct = (equity_loan_balance / total) * 100
    
    fig = go.Figure(data=[
        go.Pie(
            labels=['Home Equity', 'Mortgage Balance', 'Home Equity Loan'],
            values=[equity, mortgage_balance, equity_loan_balance],
            text=[f'{equity_pct:.1f}%', f'{mortgage_pct:.1f}%', f'{loan_pct:.1f}%'],
            textinfo='label+text',
            hole=0.3,
            marker=dict(
                colors=['#2ecc71', '#e74c3c', '#f39c12']
            )
        )
    ])
    
    fig.update_layout(
        title='Home Value Breakdown',
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        annotations=[
            dict(
                text=f'${home_value:,.0f}',
                x=0.5, y=0.5,
                font=dict(size=14),
                showarrow=False
            )
        ]
    )
    return fig

def create_equity_ratio_graph(home_value, total_debt):
    """Create a gauge chart showing equity ratio."""
    equity_ratio = (home_value - total_debt) / home_value if home_value != 0 else 0
    
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
