import numpy as np
import pandas as pd
from interactive import run_simulation_interactive

def main():
    print("Monte Carlo Portfolio Optimization")
    while True:
        choice = input("\nEnter 'r' to run a simulation or 'q' to quit: ").strip().lower()
        if choice == 'r':
            run_simulation_interactive()
        elif choice == 'q':
            print("Exiting. Thank you!")
            break
        else:
            print("Invalid input. Please enter 'r' to run or 'q' to quit.")

if __name__ == '__main__':
    main()
