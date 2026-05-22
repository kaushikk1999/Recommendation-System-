"""
Product Catalog
Contains the complete product database for the recommendation system.
"""

PRODUCTS = [
    # ==================== PHONES ====================
    {
        "id": "phone-001",
        "name": "Pixel Nova X1",
        "category": "Phones",
        "price": 449,
        "rating": 4.7,
        "description": "Flagship-level camera with clean Android experience and 5 years of updates.",
        "specs": {"display": "6.3\" OLED", "storage": "128GB", "camera": "50MP AI", "battery": "4500mAh"},
        "tags": ["photography", "android", "clean os", "updates", "ai camera"],
        "emoji": "📱",
        "best_for": "Photography enthusiasts and pure Android lovers"
    },
    {
        "id": "phone-002",
        "name": "Galaxy Budget Pro",
        "category": "Phones",
        "price": 299,
        "rating": 4.3,
        "description": "Best-in-class budget phone with AMOLED display and solid performance.",
        "specs": {"display": "6.5\" AMOLED", "storage": "64GB", "camera": "48MP", "battery": "5000mAh"},
        "tags": ["budget", "value", "amoled", "long battery"],
        "emoji": "📲",
        "best_for": "Budget-conscious users who want quality"
    },
    {
        "id": "phone-003",
        "name": "iPhone Lite 15",
        "category": "Phones",
        "price": 599,
        "rating": 4.8,
        "description": "Premium iOS experience with A17 chip and excellent ecosystem integration.",
        "specs": {"display": "6.1\" Super Retina", "storage": "128GB", "camera": "48MP", "battery": "3500mAh"},
        "tags": ["ios", "premium", "ecosystem", "apple", "secure"],
        "emoji": "🍎",
        "best_for": "Apple ecosystem users and privacy-focused"
    },
    
    # ==================== LAPTOPS ====================
    {
        "id": "laptop-001",
        "name": "AeroBook Student 14",
        "category": "Laptops",
        "price": 499,
        "rating": 4.4,
        "description": "Ultra-lightweight laptop perfect for students with all-day battery life.",
        "specs": {"display": "14\" FHD IPS", "ram": "8GB", "storage": "256GB SSD", "weight": "1.3kg"},
        "tags": ["student", "lightweight", "portable", "budget", "long battery"],
        "emoji": "💻",
        "best_for": "Students and everyday productivity"
    },
    {
        "id": "laptop-002",
        "name": "CreatorBook Pro 16",
        "category": "Laptops",
        "price": 1299,
        "rating": 4.9,
        "description": "Professional workstation for content creators with stunning 4K display.",
        "specs": {"display": "16\" 4K OLED", "ram": "32GB", "storage": "1TB SSD", "gpu": "RTX 4060"},
        "tags": ["creator", "professional", "4k", "video editing", "design"],
        "emoji": "🎨",
        "best_for": "Content creators and video editors"
    },
    {
        "id": "laptop-003",
        "name": "GameStorm Titan 15",
        "category": "Laptops",
        "price": 999,
        "rating": 4.6,
        "description": "High-performance gaming laptop with RGB keyboard and 144Hz display.",
        "specs": {"display": "15.6\" 144Hz", "ram": "16GB", "storage": "512GB SSD", "gpu": "RTX 4050"},
        "tags": ["gaming", "performance", "rgb", "high fps", "esports"],
        "emoji": "🎮",
        "best_for": "Gamers and performance enthusiasts"
    },
    {
        "id": "laptop-004",
        "name": "UltraSlim Business X1",
        "category": "Laptops",
        "price": 899,
        "rating": 4.5,
        "description": "Enterprise-grade laptop with fingerprint reader and military-grade durability.",
        "specs": {"display": "14\" 2K IPS", "ram": "16GB", "storage": "512GB SSD", "weight": "1.2kg"},
        "tags": ["business", "enterprise", "secure", "durable", "professional"],
        "emoji": "💼",
        "best_for": "Business professionals and executives"
    },
    
    # ==================== HEADPHONES ====================
    {
        "id": "headphones-001",
        "name": "BassPods Max",
        "category": "Headphones",
        "price": 129,
        "rating": 4.5,
        "description": "Premium wireless headphones with 60-hour battery and deep bass.",
        "specs": {"type": "Over-ear", "battery": "60 hours", "anc": "Yes", "bluetooth": "5.3"},
        "tags": ["long battery", "bass", "wireless", "anc", "comfortable"],
        "emoji": "🎧",
        "best_for": "Music lovers who need long battery life"
    },
    {
        "id": "headphones-002",
        "name": "StudioPro Monitors",
        "category": "Headphones",
        "price": 249,
        "rating": 4.8,
        "description": "Studio-quality reference headphones for audio professionals.",
        "specs": {"type": "Over-ear", "frequency": "5Hz-40kHz", "impedance": "32Ω", "driver": "50mm"},
        "tags": ["studio", "professional", "flat response", "mixing", "accurate"],
        "emoji": "🎵",
        "best_for": "Audio professionals and audiophiles"
    },
    {
        "id": "headphones-003",
        "name": "SportBuds Elite",
        "category": "Headphones",
        "price": 89,
        "rating": 4.4,
        "description": "Sweat-resistant earbuds with secure fit for intense workouts.",
        "specs": {"type": "In-ear", "battery": "8 hours", "waterproof": "IPX7", "bluetooth": "5.2"},
        "tags": ["sports", "workout", "waterproof", "running", "gym"],
        "emoji": "🏃",
        "best_for": "Athletes and fitness enthusiasts"
    },
    
    # ==================== SMARTWATCHES ====================
    {
        "id": "watch-001",
        "name": "FitPulse Watch 3",
        "category": "Smartwatches",
        "price": 199,
        "rating": 4.6,
        "description": "Advanced fitness tracker with ECG, SpO2, and 7-day battery life.",
        "specs": {"display": "1.4\" AMOLED", "battery": "7 days", "sensors": "ECG, SpO2, HR", "gps": "Built-in"},
        "tags": ["fitness", "health", "ecg", "tracking", "sports"],
        "emoji": "⌚",
        "best_for": "Fitness tracking and health monitoring"
    },
    {
        "id": "watch-002",
        "name": "SmartLife Premium",
        "category": "Smartwatches",
        "price": 349,
        "rating": 4.7,
        "description": "Premium smartwatch with LTE, sapphire glass, and premium materials.",
        "specs": {"display": "1.5\" OLED", "battery": "2 days", "lte": "Yes", "material": "Titanium"},
        "tags": ["premium", "luxury", "lte", "style", "fashion"],
        "emoji": "✨",
        "best_for": "Style-conscious users who want premium features"
    },
    {
        "id": "watch-003",
        "name": "BudgetFit Band",
        "category": "Smartwatches",
        "price": 49,
        "rating": 4.2,
        "description": "Affordable fitness band with essential tracking and 14-day battery.",
        "specs": {"display": "0.96\" Color", "battery": "14 days", "sensors": "HR, Steps", "waterproof": "5ATM"},
        "tags": ["budget", "affordable", "basic", "long battery", "simple"],
        "emoji": "📊",
        "best_for": "Basic fitness tracking on a budget"
    },
    
    # ==================== TABLETS ====================
    {
        "id": "tablet-001",
        "name": "ProTab Studio 12",
        "category": "Tablets",
        "price": 799,
        "rating": 4.8,
        "description": "Professional tablet with stylus support and desktop-class performance.",
        "specs": {"display": "12.4\" 120Hz", "ram": "8GB", "storage": "256GB", "stylus": "Included"},
        "tags": ["professional", "stylus", "drawing", "creative", "productivity"],
        "emoji": "📝",
        "best_for": "Digital artists and creative professionals"
    },
    {
        "id": "tablet-002",
        "name": "MediaPad Entertainment",
        "category": "Tablets",
        "price": 299,
        "rating": 4.4,
        "description": "Perfect entertainment tablet with quad speakers and vibrant display.",
        "specs": {"display": "10.5\" 2K", "ram": "4GB", "storage": "64GB", "speakers": "Quad Dolby"},
        "tags": ["entertainment", "media", "movies", "streaming", "family"],
        "emoji": "🎬",
        "best_for": "Media consumption and entertainment"
    },
    {
        "id": "tablet-003",
        "name": "KidsTab Learn",
        "category": "Tablets",
        "price": 149,
        "rating": 4.3,
        "description": "Kid-friendly tablet with parental controls and educational apps.",
        "specs": {"display": "8\" HD", "ram": "3GB", "storage": "32GB", "case": "Rugged included"},
        "tags": ["kids", "education", "parental controls", "rugged", "learning"],
        "emoji": "🧒",
        "best_for": "Children's learning and entertainment"
    },
    
    # ==================== ACCESSORIES ====================
    {
        "id": "accessory-001",
        "name": "PowerBank Ultra 20K",
        "category": "Accessories",
        "price": 59,
        "rating": 4.5,
        "description": "High-capacity power bank with 65W fast charging and laptop support.",
        "specs": {"capacity": "20000mAh", "output": "65W PD", "ports": "USB-C x2, USB-A", "weight": "350g"},
        "tags": ["charging", "portable", "fast charge", "travel", "power"],
        "emoji": "🔋",
        "best_for": "Travelers and heavy device users"
    },
    {
        "id": "accessory-002",
        "name": "ErgoStand Pro",
        "category": "Accessories",
        "price": 79,
        "rating": 4.6,
        "description": "Adjustable laptop stand with cooling fans and ergonomic design.",
        "specs": {"material": "Aluminum", "adjustable": "6 angles", "cooling": "2 fans", "max_size": "17\""},
        "tags": ["ergonomic", "stand", "cooling", "productivity", "comfort"],
        "emoji": "🖥️",
        "best_for": "Remote workers and ergonomic setups"
    },
    {
        "id": "accessory-003",
        "name": "MagSafe Duo Charger",
        "category": "Accessories",
        "price": 99,
        "rating": 4.4,
        "description": "Dual wireless charger for phone and watch with premium design.",
        "specs": {"output": "15W + 5W", "compatibility": "Qi2, MagSafe", "design": "Foldable", "cable": "USB-C"},
        "tags": ["wireless charging", "magsafe", "convenient", "desk", "nightstand"],
        "emoji": "⚡",
        "best_for": "Apple users with multiple devices"
    },
]


def get_all_products() -> list[dict]:
    """Return all products in the catalog."""
    return PRODUCTS


def get_product_by_id(product_id: str) -> dict | None:
    """Find a product by its ID."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def get_products_by_category(category: str) -> list[dict]:
    """Filter products by category."""
    return [p for p in PRODUCTS if p["category"].lower() == category.lower()]


def get_all_categories() -> list[str]:
    """Get unique list of all categories."""
    return sorted(list(set(p["category"] for p in PRODUCTS)))


def get_price_range() -> tuple[float, float]:
    """Get min and max prices in the catalog."""
    prices = [p["price"] for p in PRODUCTS]
    return min(prices), max(prices)
