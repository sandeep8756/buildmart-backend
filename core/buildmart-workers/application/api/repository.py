WORKERS = [
    {
        "id": "w1", "name": "Ramesh Kumar", "category": "carpenter",
        "experience": 15, "hourlyRate": 400, "dailyRate": 1200,
        "rating": 4.8, "reviews": 124, "location": "Mumbai, Maharashtra",
        "phone": "+91 98765 43210", "available": True,
        "skills": ["Furniture", "Doors & Windows", "Modular Kitchen"],
        "verified": True,
    },
    {
        "id": "w2", "name": "Suresh Patel", "category": "plumber",
        "experience": 12, "hourlyRate": 350, "dailyRate": 1000,
        "rating": 4.7, "reviews": 98, "location": "Ahmedabad, Gujarat",
        "phone": "+91 98765 43211", "available": True,
        "skills": ["Pipe Fitting", "Bathroom Fitting", "Water Tank"],
        "verified": True,
    },
    {
        "id": "w3", "name": "Lakshmi Devi", "category": "maid",
        "experience": 5, "hourlyRate": 200, "dailyRate": 800,
        "rating": 4.9, "reviews": 203, "location": "Bangalore, Karnataka",
        "phone": "+91 98765 43215", "available": True,
        "skills": ["House Cleaning", "Cooking", "Laundry"],
        "verified": True,
    },
    {
        "id": "w4", "name": "Anil Sharma", "category": "electrician",
        "experience": 10, "hourlyRate": 400, "dailyRate": 1200,
        "rating": 4.6, "reviews": 87, "location": "Delhi NCR",
        "phone": "+91 98765 43212", "available": True,
        "skills": ["House Wiring", "MCB Panel", "Solar Installation"],
        "verified": True,
    },
]

_COLUMN_DEFS = [
    {"field": "name", "headerName": "Name"},
    {"field": "category", "headerName": "Category"},
    {"field": "hourlyRate", "headerName": "Hourly Rate"},
    {"field": "dailyRate", "headerName": "Daily Rate"},
    {"field": "location", "headerName": "Location"},
    {"field": "rating", "headerName": "Rating"},
]
