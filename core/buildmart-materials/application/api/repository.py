MATERIALS = [
    {
        "id": "m1", "name": "OPC 53 Grade Cement", "category": "cement",
        "unit": "50 kg bag", "price": 380, "brand": "UltraTech",
        "description": "High-strength Ordinary Portland Cement for structural work",
        "inStock": True, "deliveryAvailable": True, "minOrder": 10,
        "rating": 4.7, "supplier": "M&P Supplies",
    },
    {
        "id": "m2", "name": "PPC Cement", "category": "cement",
        "unit": "50 kg bag", "price": 350, "brand": "Ambuja",
        "description": "Portland Pozzolana Cement for general construction",
        "inStock": True, "deliveryAvailable": True, "minOrder": 10,
        "rating": 4.5, "supplier": "Cement Hub India",
    },
    {
        "id": "m3", "name": "TMT Steel Bars 12mm", "category": "steel",
        "unit": "per ton", "price": 62000, "brand": "TATA Tiscon",
        "description": "Fe 500D grade TMT bars for RCC construction",
        "inStock": True, "deliveryAvailable": True, "minOrder": 1,
        "rating": 4.8, "supplier": "Steel World",
    },
    {
        "id": "m4", "name": "Red Clay Bricks", "category": "bricks",
        "unit": "per 1000 pcs", "price": 6500, "brand": "Local",
        "description": "Standard size 9x4x3 inch red clay bricks",
        "inStock": True, "deliveryAvailable": True, "minOrder": 1000,
        "rating": 4.3, "supplier": "Brick Depot",
    },
    {
        "id": "m5", "name": "Vitrified Floor Tiles 2x2 ft", "category": "tiles",
        "unit": "per box (4 pcs)", "price": 850, "brand": "Kajaria",
        "description": "Premium vitrified tiles, glossy finish",
        "inStock": True, "deliveryAvailable": True, "minOrder": 5,
        "rating": 4.6, "supplier": "Tile Gallery",
    },
    {
        "id": "m6", "name": "Exterior Emulsion Paint", "category": "paint",
        "unit": "20 litre bucket", "price": 3200, "brand": "Asian Paints",
        "description": "Weather-proof exterior emulsion, 10-year warranty",
        "inStock": True, "deliveryAvailable": True, "minOrder": 1,
        "rating": 4.7, "supplier": "Paint Mart",
    },
]

_COLUMN_DEFS = [
    {"field": "name", "headerName": "Material"},
    {"field": "category", "headerName": "Category"},
    {"field": "price", "headerName": "Price"},
    {"field": "unit", "headerName": "Unit"},
    {"field": "brand", "headerName": "Brand"},
    {"field": "supplier", "headerName": "Supplier"},
]
