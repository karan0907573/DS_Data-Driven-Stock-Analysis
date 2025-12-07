# Pages module for stock analysis dashboard
from . import volatility
from . import cumulative_return
from . import monthly_gainers_losers
from . import stock_correlation
from . import stock_return

__all__ = [
    "volatility",
    "cumulative_return",
    "monthly_gainers_losers",
    "stock_correlation",
    "stock_return",
]
