import pandas as pd
import pytest


@pytest.fixture
def lines() -> pd.DataFrame:
    """Five order lines from three orders: small enough to check every number by hand."""
    return pd.DataFrame({
        "order_id":      [1, 1, 2, 3, 3],
        "customer_name": ["Sharma Hardware", "Sharma Hardware", "Metro Mart", "Green Leaf Hotels", "Green Leaf Hotels"],
        "category":      ["Storage", "Kitchen", "Storage", "Kitchen", "Furniture"],
        "net_revenue":   [10000.0, 2500.0, 6000.0, 1500.0, 5000.0],
    })
