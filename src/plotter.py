import matplotlib.pyplot as plt

def plot_efficient_frontier(results):
    """
    Plots the efficient frontier using the simulation results.
    """
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', alpha=0.5)
    plt.xlabel('Volatility (Risk)')
    plt.ylabel('Expected Return')
    plt.colorbar(scatter, label='Sharpe Ratio')
    plt.title('Efficient Frontier - Real Market Data')
    plt.show()
