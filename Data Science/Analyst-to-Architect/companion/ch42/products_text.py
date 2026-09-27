"""
Analyst to Architect · Chapter 42 helper
products_text.py: adds a short text description to each of the 24 catalogue products (from ../baskets/products.csv),
for the content-based filtering section. Descriptions are short and deliberately plain, written once by hand,
not generated -- this is metadata, not synthetic customer text.
"""
import pathlib
import pandas as pd

DESCRIPTIONS = {
    "P01": "Stackable 50 litre plastic storage crate for retail and home organisation, ventilated sides, food safe.",
    "P02": "Larger 80 litre stackable plastic storage crate, heavy duty base, food safe, ventilated sides.",
    "P03": "Snap-fit lid for the 50 litre storage crate, dust and pest resistant, stackable when closed.",
    "P04": "Snap-fit lid for the 80 litre storage crate, dust and pest resistant, stackable when closed.",
    "P05": "Small stackable storage bin with hinged lid, for shelves and small parts organisation.",
    "P06": "Large stackable storage bin with hinged lid, for bulk household or retail storage.",
    "P07": "2 litre airtight food storage container, microwave and freezer safe, BPA free plastic.",
    "P08": "5 litre airtight food storage container, microwave and freezer safe, BPA free plastic.",
    "P09": "Pack of replacement silicone seals for airtight food containers, keeps contents fresh longer.",
    "P10": "Rectangular serving tray with raised edge and carry handles, for hotels and restaurants.",
    "P11": "Heavy duty polyethylene chopping board, dishwasher safe, for commercial kitchens.",
    "P12": "5 litre insulated jug for hot or cold beverages, double wall, drip free pour spout.",
    "P13": "200 litre industrial crate for bulk storage and transport, forklift compatible base.",
    "P14": "Large collapsible pallet box for warehouse storage, folds flat when empty to save space.",
    "P15": "Wheeled trolley sized for moving industrial crates between the warehouse floor and loading bay.",
    "P16": "Set of heavy duty castor wheels for fitting under pallet boxes and crates for easy movement.",
    "P17": "60 litre plastic drum with screw lid, for bulk liquid or granular storage.",
    "P18": "Replacement tap fitting for 60 litre drums, food and chemical grade plastic.",
    "P19": "Stackable outdoor garden chair, UV resistant plastic, for hospitality and home gardens.",
    "P20": "Weather resistant plastic garden table, matches the garden chair range, seats four to six.",
    "P21": "Weatherproof cushion set for garden chairs, quick dry foam, machine washable cover.",
    "P22": "Compact folding stool, lightweight plastic, for outdoor events and extra seating.",
    "P23": "4 tier freestanding plastic shelf unit, for garage, warehouse, or kitchen storage.",
    "P24": "Stackable plastic shoe rack, 3 tier, for home or hospitality entrance areas.",
}


def load_products():
    products = pd.read_csv(pathlib.Path(__file__).resolve().parent.parent / "baskets" / "products.csv")
    products["description"] = products["product_id"].map(DESCRIPTIONS)
    return products
