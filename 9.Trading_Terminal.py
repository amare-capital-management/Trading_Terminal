import MetaTrader5 as mt5
import time
from datetime import datetime
from rich.console import Console, Group
from rich.table import Table
from rich.live import Live
from itertools import cycle, islice

console = Console()
flash_bidask_colors = cycle(["red", "magenta", "blue", "cyan"])

# ---------------- Helper Functions ----------------
def fetch_account_info():
    ai = mt5.account_info()
    if ai is None:
        return None
    margin_used = ai.margin
    balance = ai.balance
    equity = ai.equity
    margin_free = ai.margin_free
    margin_level = ai.margin_level
    currency = ai.currency
    risk_pct = (margin_used / balance * 100) if balance else 0
    positions = mt5.positions_get()
    daily_profit = sum(p.profit for p in positions) if positions else 0.0
    num_positions = len(positions) if positions else 0
    return {
        "Login": ai.login,
        "Currency": currency,
        "Balance": f"{balance:.2f}",
        "Equity": f"{equity:.2f}",
        "Margin Used": f"{margin_used:.2f}",
        "Free Margin": f"{margin_free:.2f}",
        "Margin Level": f"{margin_level:.2f}%",
        "Risk %": f"{risk_pct:.2f}%",
        "Open Trades": str(num_positions),
        "Daily P/L": f"{daily_profit:.2f}"
    }

def fetch_positions():
    positions = mt5.positions_get()
    if positions is None:
        return []
    data = []
    now = datetime.now()
    for p in positions:
        symbol_info = mt5.symbol_info(p.symbol)
        bid = getattr(symbol_info, "bid", 0.0)
        ask = getattr(symbol_info, "ask", 0.0)
        spread = ask - bid
        open_time = datetime.fromtimestamp(p.time)
        age_sec = (now - open_time).total_seconds()
        age = f"{int(age_sec//3600)}h {int((age_sec%3600)//60)}m"
        volume = p.volume
        data.append({
            "ticket": p.ticket,
            "symbol": p.symbol,
            "type": "BUY" if p.type == 0 else "SELL",
            "volume": volume,
            "open": p.price_open,
            "current": p.price_current,
            "bid": bid,
            "ask": ask,
            "spread": spread,
            "sl": p.sl,
            "tp": p.tp,
            "profit": p.profit,
            "age": age
        })
    return data

# ---------------- Build Tables ----------------
def build_account_table(account):
    table = Table(show_header=False, expand=False, box=None)
    if account:
        for k, v in account.items():
            if k in ["Margin Level", "Risk %"]:
                color = "green" if float(v.strip('%')) > 50 else "red"
            elif k == "Daily P/L":
                color = "green" if float(v) >= 0 else "red"
            else:
                color = "white"
            table.add_row(f"[cyan]{k}[/cyan]", f"[{color}]{v}[/{color}]")
    else:
        table.add_row("[red]No account info[/red]")
    return table

def build_positions_table(positions, start=0, page_size=10):
    table = Table(expand=True, show_header=True, header_style="cyan", box=None)
    cols = ["Ticket","Symbol","Type","Vol","Open","Current","Bid","Ask","Spread","SL","TP","P/L","Age"]
    for c in cols:
        justify = "right" if c in ["Vol","Open","Current","Bid","Ask","Spread","SL","TP","P/L"] else "left"
        table.add_column(c, justify=justify, no_wrap=True)

    if not positions:
        table.add_row(*["-" for _ in cols])
    else:
        flash_bid_color = next(flash_bidask_colors)
        flash_ask_color = next(flash_bidask_colors)
        for p in islice(positions, start, start + page_size):
            type_color = "green" if p["type"] == "BUY" else "red"
            pl_color = "green" if p["profit"] >= 0 else "red"
            sl_color = "yellow" if p["sl"] > 0 else "white"
            tp_color = "cyan" if p["tp"] > 0 else "white"
            bid_color = flash_bid_color
            ask_color = flash_ask_color
            table.add_row(
                str(p["ticket"]),
                p["symbol"],
                f"[{type_color}]{p['type']}[/{type_color}]",
                f"{p['volume']:.2f}",
                f"{p['open']:.5f}",
                f"{p['current']:.5f}",
                f"[{bid_color}]{p['bid']:.5f}[/{bid_color}]",
                f"[{ask_color}]{p['ask']:.5f}[/{ask_color}]",
                f"{p['spread']:.5f}",
                f"[{sl_color}]{p['sl']:.5f}[/{sl_color}]",
                f"[{tp_color}]{p['tp']:.5f}[/{tp_color}]",
                f"[{pl_color}]{p['profit']:.2f}[/{pl_color}]",
                p["age"]
            )
    return table

# ---------------- Main Loop with Auto Scrolling ----------------
def dashboard(page_size=10, scroll_speed=2.0):
    start_index = 0
    with Live(refresh_per_second=1, screen=False) as live:
        last_scroll = time.time()
        while True:
            account = fetch_account_info()
            positions = fetch_positions()

            # Auto scroll
            if len(positions) > page_size and time.time() - last_scroll > scroll_speed:
                start_index += 1
                if start_index > len(positions) - page_size:
                    start_index = 0
                last_scroll = time.time()

            account_table = build_account_table(account)
            positions_table = build_positions_table(positions, start=start_index, page_size=page_size)
            combined = Group(account_table, positions_table)
            live.update(combined)
            time.sleep(0.2)

# ---------------- Run ----------------
if __name__ == "__main__":
    if not mt5.initialize():
        console.print("[bold red]Failed to initialize MT5[/bold red]")
    else:
        dashboard()
        mt5.shutdown()