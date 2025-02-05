import plotly.graph_objects as go

def create_value_graph(home_value, mortgage_balance, equity_loan_balance):
    """Create a stacked bar chart showing home value breakdown."""
    fig = go.Figure(data=[
        go.Bar(name='Home Equity', 
               y=['Home'], 
               x=[home_value - mortgage_balance - equity_loan_balance], 
               marker_color='#2ecc71'),
        go.Bar(name='Mortgage Balance', 
               y=['Home'], 
               x=[mortgage_balance], 
               marker_color='#e74c3c'),
        go.Bar(name='Home Equity Loan', 
               y=['Home'], 
               x=[equity_loan_balance], 
               marker_color='#f39c12')
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
