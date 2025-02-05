def calculate_equity_assessment(approx_home_value, mortgage_balance, home_equity_loan_balance):
    """Calculate equity assessment values."""
    estimated_home_value = approx_home_value
    source = "ZILLOW"
    stated_debt = mortgage_balance + home_equity_loan_balance
    estimated_home_equity = estimated_home_value - stated_debt
    return {
        'estimated_home_value': estimated_home_value,
        'source': source,
        'stated_debt': stated_debt,
        'estimated_home_equity': estimated_home_equity
    }

def calculate_cheifs_investment(estimated_home_value, estimated_home_equity):
    """Calculate CHEIFS investment values."""
    max_50_cheifs_equity_share = 0.5
    current_home_to_value_ratio = estimated_home_equity / estimated_home_value
    a_less_b = max_50_cheifs_equity_share - current_home_to_value_ratio
    cheifs_investment_in_home = a_less_b * estimated_home_value
    proceeds_to_homeowner = cheifs_investment_in_home
    return {
        'max_50_cheifs_equity_share': max_50_cheifs_equity_share,
        'current_home_to_value_ratio': current_home_to_value_ratio,
        'a_less_b': a_less_b,
        'cheifs_investment_in_home': cheifs_investment_in_home,
        'proceeds_to_homeowner': proceeds_to_homeowner
    }

def calculate_funds_usage(cheifs_investment_in_home):
    """Calculate funds usage values."""
    fixed_coverage_amount = 225000
    leverage = fixed_coverage_amount / cheifs_investment_in_home if cheifs_investment_in_home != 0 else 0
    return {
        'premium_amount': cheifs_investment_in_home,
        'approx_coverage_amount': fixed_coverage_amount,
        'leverage': leverage
    }
