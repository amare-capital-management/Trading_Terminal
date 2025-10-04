<img width="780" height="253" alt="ACM w color" src="https://github.com/user-attachments/assets/4c55a421-1885-4887-813f-6456d2404608" />

### The 9.Trading_Terminal.py script is a real-time trading dashboard for monitoring account and position data from the MetaTrader 5 (MT5) trading platform. Here's a detailed breakdown of its functionality:

*1. Imports and Setup:*

Uses the MetaTrader5 library to interact with the MT5 platform.
Utilizes the rich library for creating a visually appealing terminal-based dashboard.
Includes helper libraries like time, datetime, and itertools for time management and cycling colors.

*2. Account Information:*
   
fetch_account_info:
Retrieves account details such as balance, equity, margin, risk percentage, and daily profit/loss.
Calculates derived metrics like margin level and risk percentage.

*3. Position Information:*

fetch_positions:
Retrieves open positions from MT5, including details like:
Symbol, type (BUY/SELL), volume, open price, current price, bid/ask prices, spread, stop loss (SL), take profit (TP), profit, and position age.
Formats the data for display in the dashboard.

*4. Dashboard Tables:*

build_account_table:
Creates a table to display account information.
Highlights key metrics like margin level, risk percentage, and daily profit/loss with color coding.
build_positions_table:
Creates a table to display open positions.
Includes color-coded highlights for position type, profit/loss, stop loss, take profit, and bid/ask prices.
Supports pagination for scrolling through positions.

*5. Real-Time Dashboard:*
   
dashboard:
Continuously updates the dashboard with account and position data.
Implements auto-scrolling for positions if the number of positions exceeds the page size.
Refreshes the dashboard at a configurable interval (refresh_per_second=1).

*6. Main Execution:*
   
Initializes the MT5 connection.
Starts the real-time dashboard if the connection is successful.
Shuts down the MT5 connection when the script exits.

*Purpose:*

This script is a trading terminal designed to:

Provide real-time updates on account metrics and open positions.
Display data in a visually appealing and color-coded format.
Enable traders to monitor their trading activity efficiently.

### It is particularly useful for traders using the MetaTrader 5 platform who want a terminal-based solution for real-time monitoring.
