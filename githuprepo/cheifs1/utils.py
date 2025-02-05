def calculate_equity_assessment(home_value, mortgage_balance, home_equity_loan_balance):
    """Calculate equity assessment values based on Excel formulas."""
    estimated_home_value = home_value
    source = "ZILLOW"
    stated_debt = mortgage_balance + home_equity_loan_balance  # INTAKE!C10 + INTAKE!C11
    estimated_home_equity = estimated_home_value - stated_debt  # C4-C6
    return {
        'estimated_home_value': estimated_home_value,
        'source': source,
        'stated_debt': stated_debt,
        'estimated_home_equity': estimated_home_equity
    }

def calculate_cheifs_investment(estimated_home_value, stated_debt, estimated_home_equity):
    """Calculate CHEIFS investment values based on Excel formulas."""
    max_50_cheifs_equity_share = 0.5  # 0.5 constant
    debt_to_home_value_ratio = stated_debt / estimated_home_value  # C6/C4
    cheifs_equity_share = max_50_cheifs_equity_share - debt_to_home_value_ratio  # C10-C11
    cheifs_investment_in_home = 0.44 * cheifs_equity_share * estimated_home_value  # 0.44*C12
    proceeds_to_homeowner = cheifs_investment_in_home  # C13*C4
    return {
        'max_50_cheifs_equity_share': max_50_cheifs_equity_share,
        'debt_to_home_value_ratio': debt_to_home_value_ratio,
        'cheifs_equity_share': cheifs_equity_share,
        'cheifs_investment_in_home': cheifs_investment_in_home,
        'proceeds_to_homeowner': proceeds_to_homeowner
    }

def calculate_funds_usage(proceeds_to_homeowner):
    """Calculate funds usage values based on Excel formulas."""
    premium_amount = proceeds_to_homeowner  # C14
    approx_coverage_amount = 225000  # Fixed value
    leverage = approx_coverage_amount / premium_amount if premium_amount != 0 else 0  # C18/C17
    return {
        'premium_amount': premium_amount,
        'approx_coverage_amount': approx_coverage_amount,
        'leverage': leverage
    }
