import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FunnelVision",
    page_icon="🎯",
    layout="wide"
)

DB_NAME = "funnelvision.db"

STAGES = [
    "Awareness",
    "Interest",
    "Consideration",
    "Intent",
    "Purchase",
    "Loyalty"
]

# =========================================================
# QUESTIONS
# =========================================================

QUESTIONS = [
    (
        "q1",
        "How did you first discover online shopping platforms like ours?",
        [
            ("Through social media advertisements", "Awareness", 3),
            ("Recommended by friends or family", "Interest", 3),
            ("Found via search engine results", "Consideration", 3),
            ("Visited directly from a bookmark or typed the URL", "Intent", 3),
            ("Received an email or newsletter", "Loyalty", 3),
            ("I am not aware of any such platforms yet", "Awareness", 1)
        ]
    ),
    (
        "q2",
        "How frequently do you browse e-commerce websites?",
        [
            ("This is my very first time", "Awareness", 3),
            ("Rarely, only when I see an ad", "Awareness", 2),
            ("A few times a month", "Interest", 3),
            ("Several times a week", "Consideration", 3),
            ("Almost every day", "Intent", 3),
            ("Multiple times daily - it is part of my routine", "Loyalty", 3)
        ]
    ),
    (
        "q3",
        "When you find a product that catches your eye, what is your typical next step?",
        [
            ("Just take a mental note and move on", "Interest", 3),
            ("Save it to a wishlist for later", "Consideration", 3),
            ("Compare it with similar products on other sites", "Consideration", 3),
            ("Read customer reviews and check ratings thoroughly", "Intent", 3),
            ("Add it to my cart right away", "Intent", 3),
            ("I rarely find products that catch my eye online", "Awareness", 3)
        ]
    ),
    (
        "q4",
        "How much do customer reviews and ratings influence your purchase decisions?",
        [
            ("Not at all - I rely on product descriptions alone", "Awareness", 3),
            ("Slightly - I glance at them but do not depend on them", "Interest", 3),
            ("Moderately - they are one factor among many", "Consideration", 3),
            ("Significantly - I read several reviews before deciding", "Intent", 3),
            ("They are the single most important factor for me", "Purchase", 3)
        ]
    ),
    (
        "q5",
        "What would most likely convince you to add an item to your cart right now?",
        [
            ("An eye-catching product image or video", "Awareness", 3),
            ("A detailed feature list and clear specifications", "Interest", 3),
            ("A price that is noticeably lower than competitors", "Consideration", 3),
            ("Free shipping or a limited-time discount code", "Intent", 3),
            ("A strong personal recommendation from someone I trust", "Loyalty", 3)
        ]
    ),
    (
        "q6",
        "How many online purchases have you made in the past 6 months?",
        [
            ("None at all", "Awareness", 3),
            ("1 to 2 purchases", "Purchase", 3),
            ("3 to 5 purchases", "Loyalty", 2),
            ("6 to 10 purchases", "Loyalty", 3),
            ("More than 10 purchases", "Loyalty", 3)
        ]
    ),
    (
        "q7",
        "How would you describe the pricing of products you typically shop for online?",
        [
            ("Too expensive - I rarely buy at full price", "Awareness", 3),
            ("Slightly high but I might buy during sales", "Interest", 3),
            ("Reasonable for the quality offered", "Consideration", 3),
            ("Good value - I feel confident making purchases", "Intent", 3),
            ("Excellent value - I consistently find great deals", "Loyalty", 3)
        ]
    ),
    (
        "q8",
        "Which factor would most encourage you to return to an online store?",
        [
            ("A wider and more interesting product selection", "Interest", 3),
            ("Better prices or a price-match guarantee", "Consideration", 3),
            ("Faster and more reliable delivery options", "Intent", 3),
            ("Loyalty rewards, points, or cashback programs", "Loyalty", 3),
            ("Personalized product recommendations tailored to me", "Loyalty", 3)
        ]
    ),
    (
        "q9",
        "How likely are you to recommend our platform to a friend or colleague?",
        [
            ("Very unlikely", "Awareness", 3),
            ("Unlikely", "Interest", 3),
            ("Neutral - it would depend on the overall experience", "Consideration", 3),
            ("Likely", "Purchase", 3),
            ("Very likely - I already have recommended it", "Loyalty", 3)
        ]
    ),
    (
        "q10",
        "Which statement best describes your current shopping mindset?",
        [
            ("Just browsing casually to see what is out there", "Awareness", 3),
            ("Looking for something specific but still exploring options", "Interest", 3),
            ("Actively comparing multiple products before deciding", "Consideration", 3),
            ("Ready to buy as soon as I find the right deal", "Intent", 3),
            ("I have made up my mind and am about to complete a purchase", "Purchase", 3),
            ("I am a satisfied repeat customer looking for my next purchase", "Loyalty", 3)
        ]
    )
]

# =========================================================
# PRODUCTS
# =========================================================

PRODUCTS = [
    ("Wireless Noise-Cancelling Headphones", "Electronics", 199.99, 4.7, 2340, ["trending", "bestseller"]),
    ("Smart Fitness Watch Pro", "Wearables", 149.99, 4.5, 1876, ["new", "trending"]),
    ("Premium Leather Backpack", "Accessories", 89.99, 4.8, 956, ["bestseller"]),
    ("Portable Bluetooth Speaker", "Electronics", 59.99, 4.3, 3210, ["trending", "value"]),
    ("Organic Cotton T-Shirt Pack", "Clothing", 39.99, 4.6, 4521, ["value", "bestseller"]),
    ("Stainless Steel Water Bottle", "Lifestyle", 24.99, 4.4, 5670, ["value"]),
    ("4K Ultra HD Webcam", "Electronics", 129.99, 4.2, 890, ["new"]),
    ("Ergonomic Office Chair", "Furniture", 349.99, 4.9, 1234, ["bestseller", "premium"]),
    ("Scented Candle Collection Set", "Home", 34.99, 4.7, 2100, ["trending"]),
    ("Wireless Charging Pad", "Electronics", 29.99, 4.1, 4300, ["value", "trending"]),
    ("Running Shoes Ultra Light", "Footwear", 119.99, 4.6, 1670, ["new", "bestseller"]),
    ("Smart Home Hub Controller", "Smart Home", 79.99, 4.3, 980, ["new"])
]

# =========================================================
# STAGE CONTENT
# =========================================================

STAGE_CONTENT = {
    "Awareness": (
        "You are at the beginning of your shopping journey.",
        [
            "Browse trending categories",
            "Check out new arrivals",
            "Follow product highlights"
        ],
        ["trending", "new"],
        "Welcome Explorer - Get 10% off your first order with code WELCOME10"
    ),
    "Interest": (
        "You have shown interest in certain products.",
        [
            "Read product guides and comparisons",
            "Watch product demo videos",
            "Sign up for product alerts"
        ],
        ["bestseller", "trending"],
        "Curious Shopper - Free shipping on your first purchase this month"
    ),
    "Consideration": (
        "You are actively comparing options.",
        [
            "Use side-by-side comparisons",
            "Read verified buyer reviews",
            "Check the price-match policy"
        ],
        ["bestseller", "value"],
        "Smart Buyer - Price match guarantee plus an extra 5% off"
    ),
    "Intent": (
        "You are almost ready to buy.",
        [
            "Add items to cart",
            "Apply available coupons",
            "Choose express shipping"
        ],
        ["trending", "value", "bestseller"],
        "Ready to Buy - Extra 15% off everything in your cart"
    ),
    "Purchase": (
        "You have made a purchase decision.",
        [
            "Complete checkout securely",
            "Track your order",
            "Leave a review for reward points"
        ],
        ["bestseller", "premium"],
        "New Customer - Earn double reward points on your first completed order"
    ),
    "Loyalty": (
        "You are a valued repeat customer.",
        [
            "Access VIP pricing",
            "Get early access to sales",
            "Refer friends for rewards"
        ],
        ["premium", "bestseller", "new"],
        "Loyal Member - Exclusive VIP pricing + free express shipping"
    )
}

# =========================================================
# DATABASE
# =========================================================

def setup_db():

    with sqlite3.connect(DB_NAME) as con:

        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS surveys(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                responses TEXT NOT NULL,
                stage TEXT NOT NULL,
                scores TEXT NOT NULL,
                hidden INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)

        # Add hidden column if an older database already exists
        columns = [
            row[1]
            for row in cur.execute(
                "PRAGMA table_info(surveys)"
            ).fetchall()
        ]

        if "hidden" not in columns:
            cur.execute(
                "ALTER TABLE surveys ADD COLUMN hidden INTEGER DEFAULT 0"
            )

        cur.execute("SELECT COUNT(*) FROM users")

        if cur.fetchone()[0] == 0:

            now = datetime.now()

            sample_users = [
                ("admin", "admin123", "admin", now - timedelta(days=30))
            ]

            for username, password, role, created in sample_users:

                cur.execute(
                    """
                    INSERT INTO users(
                        username,
                        password,
                        role,
                        created_at
                    )
                    VALUES(?,?,?,?)
                    """,
                    (
                        username,
                        password,
                        role,
                        created.isoformat()
                    )
                )

        con.commit()


def get_user(username, password):

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT id, username, password, role, created_at
            FROM users
            WHERE lower(username)=lower(?) AND password=?
            """,
            (username, password)
        ).fetchone()


def register_user(username, password):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            """
            INSERT INTO users(
                username,
                password,
                role,
                created_at
            )
            VALUES(?,?,?,?)
            """,
            (
                username,
                password,
                "user",
                datetime.now().isoformat()
            )
        )

        return con.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]


def get_surveys(user_id):

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT id,timestamp,responses,stage,scores,hidden
            FROM surveys
            WHERE user_id=? AND hidden=0
            ORDER BY id
            """,
            (user_id,)
        ).fetchall()


def save_survey(user_id, responses, stage, scores):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            """
            INSERT INTO surveys(
                user_id,
                timestamp,
                responses,
                stage,
                scores,
                hidden
            )
            VALUES(?,?,?,?,?,0)
            """,
            (
                user_id,
                datetime.now().isoformat(),
                str(responses),
                stage,
                str(scores)
            )
        )


def delete_user_account(user_id):

    with sqlite3.connect(DB_NAME) as con:

        # Delete all surveys belonging to this user
        con.execute(
            "DELETE FROM surveys WHERE user_id=?",
            (user_id,)
        )

        # Delete the user
        con.execute(
            "DELETE FROM users WHERE id=?",
            (user_id,)
        )

        con.commit()


def get_all_surveys():

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT
                s.id,
                u.username,
                s.timestamp,
                s.stage,
                s.responses,
                s.scores,
                s.hidden
            FROM surveys s
            JOIN users u
                ON s.user_id=u.id
            ORDER BY s.id DESC
            """
        ).fetchall()


def hide_survey(survey_id):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            "UPDATE surveys SET hidden=1 WHERE id=?",
            (survey_id,)
        )

        con.commit()


def unhide_survey(survey_id):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            "UPDATE surveys SET hidden=0 WHERE id=?",
            (survey_id,)
        )

        con.commit()


def delete_survey(survey_id):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            "DELETE FROM surveys WHERE id=?",
            (survey_id,)
        )

        con.commit()


# =========================================================
# SCORING
# =========================================================

def calculate(responses):

    scores = {
        stage: 0
        for stage in STAGES
    }

    for qid, question, options in QUESTIONS:

        idx = responses.get(qid)

        if idx is not None and 0 <= idx < len(options):

            _, stage, base_score = options[idx]

            multiplier = {
                1: 1.00,
                2: 1.25,
                3: 1.50
            }.get(
                base_score,
                1.00
            )

            scores[stage] += base_score * multiplier

    predicted = max(
        STAGES,
        key=lambda stage: scores[stage]
    )

    total_score = sum(scores.values())

    match_strength = (
        (scores[predicted] / total_score) * 100
        if total_score > 0
        else 0
    )

    return predicted, scores, match_strength


# =========================================================
# PRODUCT RECOMMENDATIONS
# =========================================================

def products_for_stage(stage):

    tags = STAGE_CONTENT[stage][2]

    matched = [
        product
        for product in PRODUCTS
        if any(
            tag in tags
            for tag in product[5]
        )
    ]

    others = [
        product
        for product in PRODUCTS
        if product not in matched
    ]

    return (matched + others)[:4]


# =========================================================
# SESSION STATE
# =========================================================

def init_state():

    defaults = {
        "page": "login",
        "user": None,
        "responses": {},
        "step": 0,
        "last_result": None
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


def logout():

    st.session_state.clear()

    init_state()

    st.rerun()


# =========================================================
# CSS
# =========================================================

def load_css():

    st.markdown(
        """
        <style>

        .main-title {
            font-size: 42px;
            font-weight: 800;
            color: #7c3aed;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #6b7280;
            margin-bottom: 25px;
        }

        .card {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(124,58,237,0.25);
            border-radius: 18px;
            padding: 25px;
            margin-bottom: 20px;
        }

        .hero {
            background: linear-gradient(
                135deg,
                rgba(124,58,237,0.20),
                rgba(99,102,241,0.10)
            );
            border: 1px solid rgba(124,58,237,0.35);
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
        }

        .stage {
            font-size: 34px;
            font-weight: 800;
            color: #8b5cf6;
            margin: 8px 0;
        }

        .metric {
            display: inline-block;
            padding: 10px 18px;
            border-radius: 12px;
            background: rgba(124,58,237,0.15);
            color: #8b5cf6;
            font-size: 20px;
            font-weight: 700;
            margin: 10px 0;
        }

        .tip {
            background: rgba(59,130,246,0.08);
            border-radius: 16px;
            padding: 20px;
            min-height: 180px;
        }

        .offer {
            background: rgba(16,185,129,0.08);
            border-radius: 16px;
            padding: 20px;
            min-height: 180px;
        }

        .product {
            border: 1px solid rgba(124,58,237,0.20);
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .badge {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            background: rgba(124,58,237,0.15);
            color: #8b5cf6;
            font-size: 12px;
            font-weight: 700;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

def header(title, subtitle=None):

    st.markdown(
        f'<div class="main-title">{title}</div>',
        unsafe_allow_html=True
    )

    if subtitle:

        st.markdown(
            f'<div class="subtitle">{subtitle}</div>',
            unsafe_allow_html=True
        )


# =========================================================
# LOGIN
# =========================================================

def login_page():

    header(
        "FunnelVision",
        "Smart E-Commerce Funnel Predictor"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("Welcome back")

    with st.form("login_form"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Sign In",
            use_container_width=True
        )

    if submitted:

        row = get_user(
            username.strip(),
            password
        )

        if row:

            st.session_state.user = {
                "id": row[0],
                "username": row[1],
  
