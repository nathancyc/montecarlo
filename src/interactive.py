import numpy as np
import pandas as pd
from datetime import datetime
from data_fetcher import fetch_stock_data
from monte_carlo import run_simulation

def get_valid_date(prompt, default):
    while True:
        date_str = input(f"{prompt} [default: {default}]: ").strip() or default
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str

        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def reconfigure_all():
    config = {}
    
    stocks_input = input(
        "Enter stock tickers (comma separated) [default: AAPL, MSFT, GOOGL]: "
    ).strip()
    
    if stocks_input:
        config["stocks"] = [s.strip().upper() for s in stocks_input.split(",")]
    else:
        config["stocks"] = ["AAPL", "MSFT", "GOOGL"]

    config["start_date"] = get_valid_date("Enter start date (YYYY-MM-DD)", "2019-01-01")
    config["end_date"] = get_valid_date("Enter end date (YYYY-MM-DD)", "2024-01-01")
    
    num = input("Enter number of portfolios to simulate [default: 100000]: ").strip()
    try:
        config["num_portfolios"] = int(num) if num else 100000
    except ValueError:
        config["num_portfolios"] = 100000
        
    return config

def run_simulation_interactive():
    config = reconfigure_all()  # Initial full configuration

    while True:
        print("\nCurrent configuration:")
        print(f"  Stocks: {config['stocks']}")
        print(f"  Start Date: {config['start_date']}")
        print(f"  End Date: {config['end_date']}")
        print(f"  Portfolios: {config['num_portfolios']}")

        action = input(
            "\nChoose an option:\n"
            "  r: run simulation\n"
            "  c: reconfigure everything\n"
            "  s: change stocks only\n"
            "  d: change start date\n"
            "  e: change end date\n"
            "  n: change number of portfolios\n"
            "  m: return to main menu \n> "
        ).strip().lower()

        if action == 'c':
            config = reconfigure_all()
            continue
        elif action == 's':
            stocks_input = input("Enter new stock tickers (comma separated): ").strip()
            if stocks_input:
                config["stocks"] = [s.strip().upper() for s in stocks_input.split(",")]
            continue
        elif action == 'd':
            config["start_date"] = get_valid_date("Enter new start date (YYYY-MM-DD)", config["start_date"])
            continue
        elif action == 'e':
            config["end_date"] = get_valid_date("Enter new end date (YYYY-MM-DD)", config["end_date"])
            continue
        elif action == 'n':
            num = input("Enter new number of portfolios to simulate: ").strip()
            try:
                config["num_portfolios"] = int(num)
            except ValueError:
                print("Invalid number; keeping previous value.")
            continue
        elif action == 'm':
            break
        elif action != 'r':
            print("Invalid option. Try again.")
            continue

        print("\nFetching data and running simulation... Please wait.")
        try:
            data = fetch_stock_data(config["stocks"], config["start_date"], config["end_date"])
        except ValueError as err:
            print(err)
            print("Invalid ticker(s).")
            fix_choice = input("Enter 's' to reconfigure stocks or 'c' for full reconfiguration: ").strip().lower()
            if fix_choice == 's':
                stocks_input = input("Enter valid stock tickers (comma separated): ").strip()
                if stocks_input:
                    config["stocks"] = [s.strip().upper() for s in stocks_input.split(",")]
            elif fix_choice == 'c':
                config = reconfigure_all()
            continue

        returns = data.pct_change().dropna()
        mean_returns = returns.mean() * 252  # Annualized returns (252 trading day )
        cov_matrix = returns.cov() * 252     # Annualized covariance matrix

        results, weights_record = run_simulation(mean_returns, cov_matrix, config["num_portfolios"], config["stocks"])

        best_idx = np.argmax(results[2, :])
        print("\n----- Best Portfolio (Highest Sharpe Ratio) -----")
        print(f"Annualized Return: {results[0, best_idx]:.2%}")
        print(f"Volatility: {results[1, best_idx]:.2%}")
        print(f"Sharpe Ratio: {results[2, best_idx]:.2f}")
        for s, w in zip(config["stocks"], weights_record[best_idx]):
            print(f"  {s}: {w:.2%}")

        min_idx = np.argmin(results[1, :])
        print("\n----- Minimum Volatility Portfolio -----")
        print(f"Annualized Return: {results[0, min_idx]:.2%}")
        print(f"Volatility: {results[1, min_idx]:.2%}")
        print(f"Sharpe Ratio: {results[2, min_idx]:.2f}")
        for s, w in zip(config["stocks"], weights_record[min_idx]):
            print(f"  {s}: {w:.2%}")

        print("\n")
            
        show_plot = input("Enter 'x' to view the efficient frontier plot, or any key to skip: ").strip().lower()
        if show_plot == 'x':
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10, 6))
            plt.scatter(results[1, :], results[0, :], c=results[2, :], cmap='viridis', alpha=0.5)
            plt.xlabel('Volatility (Risk)')
            plt.ylabel('Expected Return')
            plt.colorbar(label='Sharpe Ratio')
            plt.title('Efficient Frontier - Real Market Data')
            plt.show(block=False)
            input("Press Enter to close the plot...")
            plt.close()

        post = input(
            "\nChoose an option:\n"
            "  c: reconfigure everything\n"
            "  s: change stocks only\n"
            "  d: change start date\n"
            "  e: change end date\n"
            "  n: change number of portfolios\n"
            "  m: return to main menu \n> "
        ).strip().lower()

        if post == 'c':
            config = reconfigure_all()

        elif post == 's':
            stocks_input = input("Enter new stock tickers (comma separated): ").strip()
            
            if stocks_input:
                config["stocks"] = [s.strip().upper() for s in stocks_input.split(",")]
    
        elif post == 'd':
            config["start_date"] = get_valid_date("Enter new start date (YYYY-MM-DD)", config["start_date"])

        elif post == 'e':
            config["end_date"] = get_valid_date("Enter new end date (YYYY-MM-DD)", config["end_date"])

        elif post == 'n':
            num = input("Enter new number of portfolios to simulate: ").strip()
            
            try:
                config["num_portfolios"] = int(num)
            except ValueError:
                print("Invalid number; keeping previous value.")

        elif post == 'm':
            break

        else:
            print("Invalid input; returning to main menu.")
            break