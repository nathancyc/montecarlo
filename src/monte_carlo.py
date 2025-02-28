import numpy as np

def run_simulation(mean_returns, cov_matrix, num_portfolios, stocks):
    """
    Runs Monte Carlo simulations to compute portfolio performance metrics.
    
    Parameters:
        mean_returns (Series): Annualized mean returns of stocks.
        cov_matrix (DataFrame): Annualized covariance matrix.
        num_portfolios (int): Number of random portfolios to generate.
        stocks (list): List of stock tickers.
    
    Returns:
        tuple: (results, weights_record)
        - results: A numpy array with rows for return, volatility, and Sharpe ratio.
        - weights_record: A list of arrays containing portfolio weights.
    """
    results = np.zeros((3, num_portfolios))
    weights_record = []
    
    np.random.seed(42)

    for i in range(num_portfolios):
        # Generate random weights and normalize them
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
        weights_record.append(weights)
        
        # Calculate portfolio return, volatility, and Sharpe ratio
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility
        
        results[0, i] = portfolio_return
        results[1, i] = portfolio_volatility
        results[2, i] = sharpe_ratio

    return results, weights_record
