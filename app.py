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

# Password required to open Hidden Users
# CHANGE THIS PASSWORD IF YOU WANT
HIDDEN_USERS_PASSWORD = "FunnelHidden@123"

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
# DATABASE SETUP
# =========================================================

def setup_db():

    with sqlite3.connect(DB_NAME) as con:

        cur = con.cursor()

        # USERS TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                hidden INTEGER DEFAULT 0
            )
        """)

        # SURVEYS TABLE
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

        # -------------------------------------------------
        # DATABASE MIGRATION
        # -------------------------------------------------

        user_columns = [
            row[1]
            for row in cur.execute(
                "PRAGMA table_info(users)"
            ).fetchall()
        ]

        if "hidden" not in user_columns:

            cur.execute(
                "ALTER TABLE users ADD COLUMN hidden INTEGER DEFAULT 0"
            )

        survey_columns = [
            row[1]
            for row in cur.execute(
                "PRAGMA table_info(surveys)"
            ).fetchall()
        ]

        if "hidden" not in survey_columns:

            cur.execute(
                "ALTER TABLE surveys ADD COLUMN hidden INTEGER DEFAULT 0"
            )

        # -------------------------------------------------
        # CREATE ADMIN ONLY IF DATABASE HAS NO USERS
        # -------------------------------------------------

        cur.execute(
            "SELECT COUNT(*) FROM users"
        )

        user_count = cur.fetchone()[0]

        if user_count == 0:

            now = datetime.now()

            cur.execute(
                """
                INSERT INTO users(
                    username,
                    password,
                    role,
                    created_at,
                    hidden
                )
                VALUES(?,?,?,?,0)
                """,
                (
                    "admin",
                    "admin123",
                    "admin",
                    (now - timedelta(days=30)).isoformat()
                )
            )

        con.commit()


# =========================================================
# USER FUNCTIONS
# =========================================================

def get_user(username, password):

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT
                id,
                username,
                password,
                role,
                created_at,
                hidden
            FROM users
            WHERE lower(username)=lower(?)
            AND password=?
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
                created_at,
                hidden
            )
            VALUES(?,?,?,?,0)
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


def get_visible_users():

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT
                id,
                username,
                created_at
            FROM users
            WHERE role='user'
            AND hidden=0
            ORDER BY id
            """
        ).fetchall()


def get_hidden_users():

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT
                id,
                username,
                created_at
            FROM users
            WHERE role='user'
            AND hidden=1
            ORDER BY id
            """
        ).fetchall()


def hide_user(user_id):

    with sqlite3.connect(DB_NAME) as con:

        # Hide the user
        con.execute(
            """
            UPDATE users
            SET hidden=1
            WHERE id=?
            AND role='user'
            """,
            (user_id,)
        )

        # Also hide all of this user's surveys
        con.execute(
            """
            UPDATE surveys
            SET hidden=1
            WHERE user_id=?
            """,
            (user_id,)
        )

        con.commit()


def unhide_user(user_id):

    with sqlite3.connect(DB_NAME) as con:

        # Unhide user
        con.execute(
            """
            UPDATE users
            SET hidden=0
            WHERE id=?
            AND role='user'
            """,
            (user_id,)
        )

        # Unhide this user's surveys
        con.execute(
            """
            UPDATE surveys
            SET hidden=0
            WHERE user_id=?
            """,
            (user_id,)
        )

        con.commit()


def delete_user_account(user_id):

    with sqlite3.connect(DB_NAME) as con:

        # First delete all surveys
        con.execute(
            """
            DELETE FROM surveys
            WHERE user_id=?
            """,
            (user_id,)
        )

        # Then delete the user
        con.execute(
            """
            DELETE FROM users
            WHERE id=?
            AND role='user'
            """,
            (user_id,)
        )

        con.commit()


# =========================================================
# SURVEY FUNCTIONS
# =========================================================

def get_surveys(user_id):

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT
                id,
                timestamp,
                responses,
                stage,
                scores,
                hidden
            FROM surveys
            WHERE user_id=?
            AND hidden=0
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

        con.commit()


def get_all_surveys():

    with sqlite3.connect(DB_NAME) as con:

        return con.execute(
            """
            SELECT
                s.id,
                u.username,
                u.hidden,
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
            """
            UPDATE surveys
            SET hidden=1
            WHERE id=?
            """,
            (survey_id,)
        )

        con.commit()


def unhide_survey(survey_id):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            """
            UPDATE surveys
            SET hidden=0
            WHERE id=?
            """,
            (survey_id,)
        )

        con.commit()


def delete_survey(survey_id):

    with sqlite3.connect(DB_NAME) as con:

        con.execute(
            """
            DELETE FROM surveys
            WHERE id=?
            """,
            (survey_id,)
        )

        con.commit()


# =========================================================
# GET LATEST PREDICTED STAGE FOR USER
# =========================================================

def get_latest_stage(user_id):

    with sqlite3.connect(DB_NAME) as con:

        row = con.execute(
            """
            SELECT stage
            FROM surveys
            WHERE user_id=?
            AND hidden=0
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        ).fetchone()

        if row:

            return row[0]

        return "Not completed"


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

            scores[stage] += (
                base_score * multiplier
            )

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
        "last_result": None,
        "confirm_delete": False,
        "hidden_users_unlocked": False
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

            # Prevent hidden users from logging in
            if row[5] == 1 and row[3] == "user":

                st.error(
                    "This account is currently hidden."
                )

            else:

                st.session_state.user = {
                    "id": row[0],
                    "username": row[1],
                    "role": row[3],
                    "created_at": row[4]
                }

                if row[3] == "admin":

                    st.session_state.page = "admin"

                else:

                    st.session_state.page = "dashboard"

                st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    if st.button(
        "Create an account",
        use_container_width=True
    ):

        st.session_state.page = "register"

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# REGISTER
# =========================================================

def register_page():

    header(
        "Create Account",
        "Join FunnelVision and discover your shopping profile"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    with st.form("register_form"):

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button(
            "Create Account & Start Survey",
            use_container_width=True
        )

    if submitted:

        if len(username.strip()) < 3:

            st.error(
                "Username must be at least 3 characters."
            )

        elif len(password) < 4:

            st.error(
                "Password must be at least 4 characters."
            )

        elif password != confirm:

            st.error(
                "Passwords do not match."
            )

        else:

            try:

                uid = register_user(
                    username.strip(),
                    password
                )

                st.session_state.user = {
                    "id": uid,
                    "username": username.strip(),
                    "role": "user",
                    "created_at": datetime.now().isoformat()
                }

                st.session_state.responses = {}

                st.session_state.step = 0

                st.session_state.page = "survey"

                st.rerun()

            except sqlite3.IntegrityError:

                st.error(
                    "Username already exists."
                )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("Back to Sign In"):

        st.session_state.page = "login"

        st.rerun()


# =========================================================
# DELETE ACCOUNT
# =========================================================

def delete_account_section():

    st.markdown("---")

    st.subheader("⚠️ Account Settings")

    st.warning(
        "Deleting your account will permanently delete "
        "your account and all surveys associated with it."
    )

    if "confirm_delete" not in st.session_state:

        st.session_state.confirm_delete = False

    if not st.session_state.confirm_delete:

        if st.button(
            "Delete My Account",
            type="secondary"
        ):

            st.session_state.confirm_delete = True

            st.rerun()

    else:

        st.error(
            "Are you sure? This action cannot be undone."
        )

        a, b = st.columns(2)

        with a:

            if st.button(
                "Yes, Permanently Delete",
                type="primary",
                use_container_width=True
            ):

                user_id = st.session_state.user["id"]

                delete_user_account(user_id)

                st.session_state.clear()

                init_state()

                st.rerun()

        with b:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.confirm_delete = False

                st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

def dashboard_page():

    user = st.session_state.user

    header(
        "FunnelVision",
        f"Welcome, {user['username']}"
    )

    if st.button("Sign Out"):

        logout()

    surveys = get_surveys(user["id"])

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "Your Shopping Funnel Profile"
    )

    st.write(
        f"{len(surveys)} survey(s) completed"
    )

    button_text = (
        "Retake Survey"
        if surveys
        else "Begin Survey"
    )

    if st.button(
        button_text,
        type="primary"
    ):

        st.session_state.responses = {}

        st.session_state.step = 0

        st.session_state.page = "survey"

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    if surveys:

        stage = surveys[-1][3]

        content = STAGE_CONTENT[stage]

        st.markdown(
            '<div class="hero">',
            unsafe_allow_html=True
        )

        st.markdown(
            f"### Latest Stage: "
            f"<span class='stage'>{stage}</span>",
            unsafe_allow_html=True
        )

        st.write(content[0])

        st.markdown(
            "**Recommended products:**"
        )

        for product in products_for_stage(stage):

            st.write(
                f"• {product[0]} | "
                f"${product[2]:.2f} | "
                f"⭐ {product[3]}"
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    delete_account_section()


# =========================================================
# SURVEY
# =========================================================

def survey_page():

    step = st.session_state.step

    qid, question, options = QUESTIONS[step]

    progress = (
        (step + 1) /
        len(QUESTIONS)
    )

    header(
        "Survey",
        f"Question {step + 1} of {len(QUESTIONS)}"
    )

    st.progress(progress)

    st.caption(
        f"{int(progress * 100)}% complete"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### {question}"
    )

    labels = [
        option[0]
        for option in options
    ]

    previous = st.session_state.responses.get(qid)

    selected = st.radio(
        "Choose one:",
        range(len(labels)),
        format_func=lambda i: labels[i],
        index=(
            previous
            if previous is not None
            else None
        ),
        key=f"answer_{step}"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    a, b, c = st.columns(3)

    with a:

        if st.button(
            "Previous",
            disabled=(step == 0),
            use_container_width=True
        ):

            st.session_state.responses[qid] = selected

            st.session_state.step -= 1

            st.rerun()

    with b:

        if st.button(
            "Exit",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()

    with c:

        label = (
            "Submit Survey"
            if step == len(QUESTIONS) - 1
            else "Next"
        )

        if st.button(
            label,
            type="primary",
            use_container_width=True
        ):

            if selected is None:

                st.warning(
                    "Please select an option."
                )

            else:

                st.session_state.responses[qid] = selected

                if step < len(QUESTIONS) - 1:

                    st.session_state.step += 1

                    st.rerun()

                else:

                    stage, scores, strength = calculate(
                        st.session_state.responses
                    )

                    save_survey(
                        st.session_state.user["id"],
                        st.session_state.responses,
                        stage,
                        scores
                    )

                    st.session_state.last_result = (
                        stage,
                        scores,
                        strength
                    )

                    st.session_state.page = "results"

                    st.rerun()


# =========================================================
# RESULTS
# =========================================================

def results_page():

    stage, scores, match_strength = (
        st.session_state.last_result
    )

    content = STAGE_CONTENT[stage]

    header(
        "Your Shopping Profile",
        "Your strongest funnel stage is ready"
    )

    st.markdown(
        '<div class="hero">',
        unsafe_allow_html=True
    )

    st.caption(
        "🏆 STRONGEST FUNNEL STAGE"
    )

    st.markdown(
        f'<div class="stage">{stage}</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"**Your score:** "
        f"{scores[stage]:.1f}"
    )

    st.markdown(
        f'<div class="metric">'
        f'Match Strength: {match_strength:.0f}%'
        f'</div>',
        unsafe_allow_html=True
    )

    st.write(content[0])

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="tip">',
            unsafe_allow_html=True
        )

        st.subheader(
            "💡 Personalized Tips"
        )

        for tip in content[1]:

            st.write(
                "✓ " + tip
            )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with right:

        st.markdown(
            '<div class="offer">',
            unsafe_allow_html=True
        )

        st.subheader(
            "🎁 Special Offer"
        )

        st.markdown(
            f"**{content[3]}**"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    st.subheader(
        "🛍 Picked For You"
    )

    st.caption(
        "Products selected using your strongest shopping stage"
    )

    columns = st.columns(2)

    for i, product in enumerate(
        products_for_stage(stage)
    ):

        name, category, price, rating, reviews, tags = product

        if i == 0:

            badge = "BEST MATCH"

        elif "trending" in tags:

            badge = "TRENDING"

        elif "value" in tags:

            badge = "BEST VALUE"

        elif rating >= 4.7:

            badge = "TOP RATED"

        else:

            badge = "RECOMMENDED"

        with columns[i % 2]:

            st.markdown(
                '<div class="product">',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<span class="badge">{badge}</span>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"### 🛍️ {name}"
            )

            st.caption(
                category.upper()
            )

            st.write(
                f"⭐ {rating:.1f} • "
                f"{reviews:,} reviews"
            )

            st.markdown(
                f"**${price:.2f}**"
            )

            why = {
                "Awareness":
                    "A great discovery pick for your browsing style.",
                "Interest":
                    "Matches your current product-exploration mindset.",
                "Consideration":
                    "Useful for comparing quality, value and reviews.",
                "Intent":
                    "A strong match for someone close to buying.",
                "Purchase":
                    "A solid choice for your purchase-ready profile.",
                "Loyalty":
                    "A great pick for repeat shoppers looking for value."
            }.get(
                stage,
                "Selected based on your shopping profile."
            )

            st.caption(
                "Why this matches you: " + why
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    a, b = st.columns(2)

    with a:

        if st.button(
            "← Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()

    with b:

        if st.button(
            "Retake Survey",
            type="primary",
            use_container_width=True
        ):

            st.session_state.responses = {}

            st.session_state.step = 0

            st.session_state.page = "survey"

            st.rerun()


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_page():

    header(
        "Admin Dashboard",
        "Manage users and survey records"
    )

    if st.button("Sign Out"):

        logout()

    # =====================================================
    # USERS
    # =====================================================

    st.subheader("👥 Users")

    visible_users = get_visible_users()

    hidden_users = get_hidden_users()

    st.write(
        f"Total visible registered users: "
        f"**{len(visible_users)}**"
    )

    # -----------------------------------------------------
    # VISIBLE USERS TABLE
    # -----------------------------------------------------

    if visible_users:

        user_rows = []

        for user in visible_users:

            user_id = user[0]

            username = user[1]

            created = user[2].replace(
                "T",
                " "
            )[:19]

            predicted_stage = get_latest_stage(
                user_id
            )

            user_rows.append(
                {
                    "User ID": user_id,
                    "Username": username,
                    "Predicted Stage": predicted_stage,
                    "Created": created
                }
            )

        st.dataframe(
            user_rows,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # USER MANAGEMENT BUTTONS
        # -------------------------------------------------

        st.markdown("### Manage Users")

        for user in visible_users:

            user_id = user[0]

            username = user[1]

            with st.container(border=True):

                left, middle, right = st.columns(
                    [3, 2, 2]
                )

                with left:

                    st.markdown(
                        f"**{username}**"
                    )

                    st.caption(
                        f"User ID: {user_id}"
                    )

                with middle:

                    st.write(
                        "Predicted Stage:"
                    )

                    st.write(
                        f"**{get_latest_stage(user_id)}**"
                    )

                with right:

                    hide_key = (
                        f"hide_user_{user_id}"
                    )

                    delete_key = (
                        f"delete_user_{user_id}"
                    )

                    if st.button(
                        "👁️ Hide User",
                        key=hide_key,
                        use_container_width=True
                    ):

                        hide_user(user_id)

                        st.success(
                            f"{username} has been hidden."
                        )

                        st.rerun()

                    if st.button(
                        "🗑️ Delete User",
                        key=delete_key,
                        use_container_width=True
                    ):

                        delete_user_account(
                            user_id
                        )

                        st.success(
                            f"{username} has been deleted."
                        )

                        st.rerun()

    else:

        st.info(
            "No visible users found."
        )

    # =====================================================
    # HIDDEN USERS
    # =====================================================

    st.markdown("---")

    st.subheader("🔒 Hidden Users")

    st.write(
        "Hidden users are protected and are not displayed "
        "in the normal Users table."
    )

    # -----------------------------------------------------
    # PASSWORD PROTECTION
    # -----------------------------------------------------

    if not st.session_state.hidden_users_unlocked:

        with st.form("hidden_users_password_form"):

            hidden_password = st.text_input(
                "Enter Hidden Users Password",
                type="password"
            )

            unlock = st.form_submit_button(
                "🔓 Open Hidden Users",
                use_container_width=True
            )

        if unlock:

            if hidden_password == HIDDEN_USERS_PASSWORD:

                st.session_state.hidden_users_unlocked = True

                st.success(
                    "Hidden Users unlocked."
                )

                st.rerun()

            else:

                st.error(
                    "Incorrect password."
                )

    # -----------------------------------------------------
    # UNLOCKED HIDDEN USERS
    # -----------------------------------------------------

    else:

        st.success(
            f"{len(hidden_users)} hidden user(s) found."
        )

        if st.button(
            "🔒 Lock Hidden Users",
            use_container_width=True
        ):

            st.session_state.hidden_users_unlocked = False

            st.rerun()

        if hidden_users:

            for user in hidden_users:

                user_id = user[0]

                username = user[1]

                created = user[2].replace(
                    "T",
                    " "
                )[:19]

                with st.container(border=True):

                    left, middle, right = st.columns(
                        [3, 2, 2]
                    )

                    with left:

                        st.markdown(
                            f"**{username}**"
                        )

                        st.caption(
                            f"User ID: {user_id}"
                        )

                        st.caption(
                            f"Created: {created}"
                        )

                    with middle:

                        st.write(
                            "Predicted Stage:"
                        )

                        st.write(
                            f"**{get_latest_stage(user_id)}**"
                        )

                    with right:

                        unhide_key = (
                            f"unhide_user_{user_id}"
                        )

                        delete_hidden_key = (
                            f"delete_hidden_user_{user_id}"
                        )

                        if st.button(
                            "👁️ Unhide User",
                            key=unhide_key,
                            use_container_width=True
                        ):

                            unhide_user(
                                user_id
                            )

                            st.success(
                                f"{username} has been unhidden."
                            )

                            st.rerun()

                        if st.button(
                            "🗑️ Delete User",
                            key=delete_hidden_key,
                            use_container_width=True
                        ):

                            delete_user_account(
                                user_id
                            )

                            st.success(
                                f"{username} has been permanently deleted."
                            )

                            st.rerun()

        else:

            st.info(
                "There are no hidden users."
            )

    # =====================================================
    # SURVEY MANAGEMENT
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Survey Management")

    all_surveys = get_all_surveys()

    # Visible survey:
    # survey[2] = user hidden status
    # survey[7] = survey hidden status

    visible_surveys = [
        survey
        for survey in all_surveys
        if survey[2] == 0
        and survey[7] == 0
    ]

    hidden_surveys = [
        survey
        for survey in all_surveys
        if survey[2] == 0
        and survey[7] == 1
    ]

    counts = {
        stage: 0
        for stage in STAGES
    }

    for survey in visible_surveys:

        if survey[4] in counts:

            counts[survey[4]] += 1

    top_stage = (
        max(
            STAGES,
            key=lambda stage: counts[stage]
        )
        if visible_surveys
        else "—"
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Visible Surveys",
        len(visible_surveys)
    )

    b.metric(
        "Hidden Surveys",
        len(hidden_surveys)
    )

    c.metric(
        "Total Surveys",
        len(all_surveys)
    )

    d.metric(
        "Most Recorded Stage",
        top_stage
    )

    # -----------------------------------------------------
    # FILTER
    # -----------------------------------------------------

    chosen = st.selectbox(
        "Filter visible surveys by stage",
        ["All Stages"] + STAGES
    )

    filtered_surveys = visible_surveys

    if chosen != "All Stages":

        filtered_surveys = [
            survey
            for survey in visible_surveys
            if survey[4] == chosen
        ]

    # -----------------------------------------------------
    # VISIBLE SURVEYS
    # -----------------------------------------------------

    st.markdown("### Visible Surveys")

    if not filtered_surveys:

        st.info(
            "There are no visible surveys."
        )

    else:

        for survey in filtered_surveys:

            survey_id = survey[0]

            username = survey[1]

            timestamp = survey[3]

            stage = survey[4]

            with st.container(border=True):

                left, middle, right = st.columns(
                    [3, 3, 2]
                )

                with left:

                    st.markdown(
                        f"**Survey #{survey_id}**"
                    )

                    st.write(
                        f"User: **{username}**"
                    )

                with middle:

                    st.write(
                        f"Date: "
                        f"{timestamp.replace('T', ' ')[:19]}"
                    )

                    st.write(
                        f"Stage: **{stage}**"
                    )

                with right:

                    if st.button(
                        "👁️ Hide",
                        key=f"hide_survey_{survey_id}",
                        use_container_width=True
                    ):

                        hide_survey(
                            survey_id
                        )

                        st.rerun()

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_survey_{survey_id}",
                        use_container_width=True
                    ):

                        delete_survey(
                            survey_id
                        )

                        st.rerun()

    # -----------------------------------------------------
    # HIDDEN SURVEYS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 👁️ Hidden Surveys"
    )

    if not hidden_surveys:

        st.info(
            "There are no hidden surveys."
        )

    else:

        for survey in hidden_surveys:

            survey_id = survey[0]

            username = survey[1]

            timestamp = survey[3]

            stage = survey[4]

            with st.container(border=True):

                left, middle, right = st.columns(
                    [3, 3, 2]
                )

                with left:

                    st.markdown(
                        f"**Survey #{survey_id}**"
                    )

                    st.write(
                        f"User: **{username}**"
                    )

                with middle:

                    st.write(
                        f"Date: "
                        f"{timestamp.replace('T', ' ')[:19]}"
                    )

                    st.write(
                        f"Stage: **{stage}**"
                    )

                with right:

                    if st.button(
                        "👁️ Unhide",
                        key=f"unhide_survey_{survey_id}",
                        use_container_width=True
                    ):

                        unhide_survey(
                            survey_id
                        )

                        st.rerun()

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_hidden_survey_{survey_id}",
                        use_container_width=True
                    ):

                        delete_survey(
                            survey_id
                        )

                        st.rerun()


# =========================================================
# START APPLICATION
# =========================================================

load_css()

setup_db()

init_state()

if st.session_state.user is None:

    if st.session_state.page == "register":

        register_page()

    else:

        login_page()

else:

    if st.session_state.user["role"] == "admin":

        admin_page()

    elif st.session_state.page == "dashboard":

        dashboard_page()

    elif st.session_state.page == "survey":

        survey_page()

    elif st.session_state.page == "results":

        results_page()

    else:

        dashboard_page()
