import streamlit as st
import sqlite3
from datetime import datetime
import ast


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FunnelVision",
    page_icon="🎯",
    layout="wide"
)


# =========================================================
# CONSTANTS
# =========================================================

DB_NAME = "funnelvision.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

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
    (
        "Wireless Noise-Cancelling Headphones",
        "Electronics",
        199.99,
        4.7,
        2340,
        ["trending", "bestseller"]
    ),

    (
        "Smart Fitness Watch Pro",
        "Wearables",
        149.99,
        4.5,
        1876,
        ["new", "trending"]
    ),

    (
        "Premium Leather Backpack",
        "Accessories",
        89.99,
        4.8,
        956,
        ["bestseller"]
    ),

    (
        "Portable Bluetooth Speaker",
        "Electronics",
        59.99,
        4.3,
        3210,
        ["trending", "value"]
    ),

    (
        "Organic Cotton T-Shirt Pack",
        "Clothing",
        39.99,
        4.6,
        4521,
        ["value", "bestseller"]
    ),

    (
        "Stainless Steel Water Bottle",
        "Lifestyle",
        24.99,
        4.4,
        5670,
        ["value"]
    ),

    (
        "4K Ultra HD Webcam",
        "Electronics",
        129.99,
        4.2,
        890,
        ["new"]
    ),

    (
        "Ergonomic Office Chair",
        "Furniture",
        349.99,
        4.9,
        1234,
        ["bestseller", "premium"]
    ),

    (
        "Scented Candle Collection Set",
        "Home",
        34.99,
        4.7,
        2100,
        ["trending"]
    ),

    (
        "Wireless Charging Pad",
        "Electronics",
        29.99,
        4.1,
        4300,
        ["value", "trending"]
    ),

    (
        "Running Shoes Ultra Light",
        "Footwear",
        119.99,
        4.6,
        1670,
        ["new", "bestseller"]
    ),

    (
        "Smart Home Hub Controller",
        "Smart Home",
        79.99,
        4.3,
        980,
        ["new"]
    )
]


# =========================================================
# STAGE CONTENT
# =========================================================

STAGE_CONTENT = {

    "Awareness": {
        "description":
            "You are at the beginning of your shopping journey.",

        "tips": [
            "Browse trending categories",
            "Check out new arrivals",
            "Explore product highlights"
        ],

        "tags": [
            "trending",
            "new"
        ],

        "offer":
            "Welcome Explorer - Get 10% off your first order with code WELCOME10"
    },

    "Interest": {
        "description":
            "You have shown interest in certain products.",

        "tips": [
            "Read product guides and comparisons",
            "Watch product demonstration videos",
            "Sign up for product alerts"
        ],

        "tags": [
            "bestseller",
            "trending"
        ],

        "offer":
            "Curious Shopper - Free shipping on your first purchase this month"
    },

    "Consideration": {
        "description":
            "You are actively comparing different options.",

        "tips": [
            "Use side-by-side comparisons",
            "Read verified buyer reviews",
            "Check the price-match policy"
        ],

        "tags": [
            "bestseller",
            "value"
        ],

        "offer":
            "Smart Buyer - Price match guarantee plus an extra 5% off"
    },

    "Intent": {
        "description":
            "You are getting close to making a purchase.",

        "tips": [
            "Add suitable items to your cart",
            "Check available coupons",
            "Choose the delivery option that suits you"
        ],

        "tags": [
            "trending",
            "value",
            "bestseller"
        ],

        "offer":
            "Ready to Buy - Extra 15% off everything in your cart"
    },

    "Purchase": {
        "description":
            "You have reached the purchase stage.",

        "tips": [
            "Complete checkout securely",
            "Track your order",
            "Leave a review after your purchase"
        ],

        "tags": [
            "bestseller",
            "premium"
        ],

        "offer":
            "New Customer - Earn double reward points on your first completed order"
    },

    "Loyalty": {
        "description":
            "You are a repeat shopper and an engaged customer.",

        "tips": [
            "Explore loyalty rewards",
            "Check early access offers",
            "Look for member benefits"
        ],

        "tags": [
            "premium",
            "bestseller",
            "new"
        ],

        "offer":
            "Loyal Member - Exclusive VIP pricing and free express shipping"
    }
}


# =========================================================
# DATABASE SETUP
# =========================================================

def setup_db():

    with sqlite3.connect(DB_NAME) as con:

        cur = con.cursor()

        cur.execute(
            "PRAGMA foreign_keys = ON"
        )

        # -------------------------------------------------
        # CONTROL TABLE
        # -------------------------------------------------

        cur.execute("""
            CREATE TABLE IF NOT EXISTS app_settings(
                setting_name TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL
            )
        """)

        # -------------------------------------------------
        # CHECK FOR CLEAN DATABASE VERSION
        # -------------------------------------------------

        cur.execute("""
            SELECT setting_value
            FROM app_settings
            WHERE setting_name = 'clean_database_v2'
        """)

        clean_database = cur.fetchone()

        # -------------------------------------------------
        # COMPLETE DATABASE REBUILD
        # -------------------------------------------------

        if clean_database is None:

            # Completely remove old surveys table.
            # This removes old hidden columns as well.
            cur.execute("""
                DROP TABLE IF EXISTS surveys
            """)

            # Completely remove old users table.
            # This removes old hidden-user structure as well.
            cur.execute("""
                DROP TABLE IF EXISTS users
            """)

            # -------------------------------------------------
            # NEW USERS TABLE
            # -------------------------------------------------

            cur.execute("""
                CREATE TABLE users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)

            # -------------------------------------------------
            # NEW SURVEYS TABLE
            # -------------------------------------------------

            cur.execute("""
                CREATE TABLE surveys(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    responses TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    scores TEXT NOT NULL,
                    FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
                )
            """)

            # -------------------------------------------------
            # FRESH ADMIN
            # -------------------------------------------------

            cur.execute("""
                INSERT INTO users(
                    username,
                    password,
                    role,
                    created_at
                )
                VALUES(?,?,?,?)
            """, (
                ADMIN_USERNAME,
                ADMIN_PASSWORD,
                "admin",
                datetime.now().isoformat()
            ))

            # -------------------------------------------------
            # MARK DATABASE AS CLEAN
            # -------------------------------------------------

            cur.execute("""
                INSERT INTO app_settings(
                    setting_name,
                    setting_value
                )
                VALUES(?,?)
            """, (
                "clean_database_v2",
                "completed"
            ))

        else:

            # -------------------------------------------------
            # NORMAL STARTUP
            # -------------------------------------------------

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
                    FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
                )
            """)

            # Make sure admin exists
            cur.execute("""
                SELECT id
                FROM users
                WHERE username = ?
                AND role = 'admin'
            """, (
                ADMIN_USERNAME,
            ))

            admin_exists = cur.fetchone()

            if admin_exists is None:

                cur.execute("""
                    INSERT INTO users(
                        username,
                        password,
                        role,
                        created_at
                    )
                    VALUES(?,?,?,?)
                """, (
                    ADMIN_USERNAME,
                    ADMIN_PASSWORD,
                    "admin",
                    datetime.now().isoformat()
                ))

        con.commit()


# =========================================================
# USER AUTHENTICATION
# =========================================================

def get_user(username, password):

    with sqlite3.connect(DB_NAME) as con:

        row = con.execute("""
            SELECT
                id,
                username,
                password,
                role,
                created_at
            FROM users
            WHERE lower(username) = lower(?)
            AND password = ?
        """, (
            username,
            password
        )).fetchone()

        return row


# =========================================================
# REGISTER USER
# =========================================================

def register_user(username, password):

    with sqlite3.connect(DB_NAME) as con:

        cur = con.cursor()

        cur.execute("""
            INSERT INTO users(
                username,
                password,
                role,
                created_at
            )
            VALUES(?,?,?,?)
        """, (
            username,
            password,
            "user",
            datetime.now().isoformat()
        ))

        user_id = cur.lastrowid

        con.commit()

        return user_id


# =========================================================
# DELETE USER
# =========================================================

def delete_user(user_id):

    with sqlite3.connect(DB_NAME) as con:

        cur = con.cursor()

        cur.execute(
            "PRAGMA foreign_keys = ON"
        )

        # Delete surveys first
        cur.execute("""
            DELETE FROM surveys
            WHERE user_id = ?
        """, (
            user_id,
        ))

        # Then delete user
        cur.execute("""
            DELETE FROM users
            WHERE id = ?
            AND role = 'user'
        """, (
            user_id,
        ))

        con.commit()


# =========================================================
# SAVE SURVEY
# =========================================================

def save_survey(
    user_id,
    responses,
    stage,
    scores
):

    with sqlite3.connect(DB_NAME) as con:

        con.execute("""
            INSERT INTO surveys(
                user_id,
                timestamp,
                responses,
                stage,
                scores
            )
            VALUES(?,?,?,?,?)
        """, (
            user_id,
            datetime.now().isoformat(),
            str(responses),
            stage,
            str(scores)
        ))

        con.commit()


# =========================================================
# GET USER SURVEYS
# =========================================================

def get_user_surveys(user_id):

    with sqlite3.connect(DB_NAME) as con:

        return con.execute("""
            SELECT
                id,
                timestamp,
                responses,
                stage,
                scores
            FROM surveys
            WHERE user_id = ?
            ORDER BY id ASC
        """, (
            user_id,
        )).fetchall()


# =========================================================
# GET ALL SURVEYS
# =========================================================

def get_all_surveys():

    with sqlite3.connect(DB_NAME) as con:

        return con.execute("""
            SELECT
                s.id,
                s.user_id,
                u.username,
                s.timestamp,
                s.stage,
                s.responses,
                s.scores
            FROM surveys s
            INNER JOIN users u
                ON s.user_id = u.id
            ORDER BY s.id DESC
        """).fetchall()


# =========================================================
# DELETE SURVEY
# =========================================================

def delete_survey(survey_id):

    with sqlite3.connect(DB_NAME) as con:

        con.execute("""
            DELETE FROM surveys
            WHERE id = ?
        """, (
            survey_id,
        ))

        con.commit()


# =========================================================
# GET LATEST STAGE
# =========================================================

def get_latest_stage(user_id):

    with sqlite3.connect(DB_NAME) as con:

        row = con.execute("""
            SELECT stage
            FROM surveys
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, (
            user_id,
        )).fetchone()

        if row:

            return row[0]

        return "Not completed"


# =========================================================
# GET ALL REGISTERED USERS
# =========================================================

def get_all_users():

    with sqlite3.connect(DB_NAME) as con:

        users = con.execute("""
            SELECT
                id,
                username,
                created_at
            FROM users
            WHERE role = 'user'
            ORDER BY id ASC
        """).fetchall()

        result = []

        for user in users:

            user_id = user[0]

            stage = get_latest_stage(
                user_id
            )

            result.append({
                "id": user[0],
                "username": user[1],
                "created_at": user[2],
                "stage": stage
            })

        return result


# =========================================================
# SCORING SYSTEM
# =========================================================

def calculate_scores(responses):

    scores = {
        stage: 0.0
        for stage in STAGES
    }

    for qid, question, options in QUESTIONS:

        selected = responses.get(qid)

        if selected is None:
            continue

        if selected < 0:
            continue

        if selected >= len(options):
            continue

        option_text, stage, base_score = options[selected]

        # Slight weighting based on answer strength
        weighting = {
            1: 1.00,
            2: 1.15,
            3: 1.30
        }.get(
            base_score,
            1.00
        )

        scores[stage] += (
            base_score * weighting
        )

    total_score = sum(
        scores.values()
    )

    if total_score == 0:

        predicted_stage = "Awareness"
        match_strength = 0

    else:

        predicted_stage = max(
            scores,
            key=scores.get
        )

        match_strength = (
            scores[predicted_stage]
            / total_score
        ) * 100

    return (
        predicted_stage,
        scores,
        match_strength
    )


# =========================================================
# PRODUCT RECOMMENDATION
# =========================================================

def get_recommended_products(stage):

    tags = STAGE_CONTENT[stage]["tags"]

    matching = []

    other_products = []

    for product in PRODUCTS:

        product_tags = product[5]

        if any(
            tag in product_tags
            for tag in tags
        ):

            matching.append(product)

        else:

            other_products.append(product)

    return (
        matching + other_products
    )[:4]


# =========================================================
# SESSION STATE
# =========================================================

def initialize_session():

    defaults = {
        "page": "login",
        "user": None,
        "responses": {},
        "question_number": 0,
        "last_result": None,
        "delete_user_id": None,
        "delete_survey_id": None
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =========================================================
# LOGOUT
# =========================================================

def logout():

    st.session_state.clear()

    initialize_session()

    st.rerun()


# =========================================================
# CUSTOM CSS
# =========================================================

def load_css():

    st.markdown("""
        <style>

        .main-title {
            font-size: 44px;
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
            padding: 25px;
            border-radius: 18px;
            border: 1px solid rgba(124, 58, 237, 0.25);
            margin-bottom: 20px;
        }

        .hero {
            padding: 30px;
            border-radius: 20px;
            border: 1px solid rgba(124, 58, 237, 0.30);
            margin: 20px 0;
        }

        .stage {
            font-size: 36px;
            font-weight: 800;
            color: #8b5cf6;
        }

        .metric-box {
            padding: 12px 18px;
            border-radius: 12px;
            background: rgba(124, 58, 237, 0.12);
            color: #8b5cf6;
            font-size: 20px;
            font-weight: 700;
            display: inline-block;
            margin: 10px 0;
        }

        .product-card {
            padding: 20px;
            border-radius: 16px;
            border: 1px solid rgba(124, 58, 237, 0.20);
            margin-bottom: 15px;
            min-height: 230px;
        }

        .badge {
            padding: 5px 10px;
            border-radius: 20px;
            background: rgba(124, 58, 237, 0.12);
            color: #7c3aed;
            font-size: 12px;
            font-weight: 700;
        }

        .table-header {
            font-weight: 700;
            color: #7c3aed;
        }

        </style>
    """, unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

def show_header(
    title,
    subtitle=None
):

    st.markdown(
        f"""
        <div class="main-title">
            {title}
        </div>
        """,
        unsafe_allow_html=True
    )

    if subtitle:

        st.markdown(
            f"""
            <div class="subtitle">
                {subtitle}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    show_header(
        "FunnelVision",
        "Smart E-Commerce Funnel Predictor"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "Welcome Back"
    )

    with st.form(
        "login_form"
    ):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login = st.form_submit_button(
            "Sign In",
            use_container_width=True
        )

    if login:

        username = username.strip()

        user = get_user(
            username,
            password
        )

        if user:

            st.session_state.user = {
                "id": user[0],
                "username": user[1],
                "role": user[3],
                "created_at": user[4]
            }

            if user[3] == "admin":

                st.session_state.page = "admin"

            else:

                st.session_state.page = "dashboard"

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "Create New Account",
        use_container_width=True
    ):

        st.session_state.page = "register"

        st.rerun()


# =========================================================
# REGISTER PAGE
# =========================================================

def register_page():

    show_header(
        "Create Account",
        "Create your FunnelVision account"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    with st.form(
        "register_form"
    ):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        create_account = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

    if create_account:

        username = username.strip()

        if len(username) < 3:

            st.error(
                "Username must contain at least 3 characters."
            )

        elif len(password) < 4:

            st.error(
                "Password must contain at least 4 characters."
            )

        elif password != confirm_password:

            st.error(
                "Passwords do not match."
            )

        elif username.lower() == "admin":

            st.error(
                "This username is reserved."
            )

        else:

            try:

                user_id = register_user(
                    username,
                    password
                )

                st.session_state.user = {
                    "id": user_id,
                    "username": username,
                    "role": "user",
                    "created_at": datetime.now().isoformat()
                }

                st.session_state.responses = {}

                st.session_state.question_number = 0

                st.session_state.page = "survey"

                st.rerun()

            except sqlite3.IntegrityError:

                st.error(
                    "That username already exists."
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "Back to Login"
    ):

        st.session_state.page = "login"

        st.rerun()


# =========================================================
# USER DASHBOARD
# =========================================================

def dashboard_page():

    user = st.session_state.user

    show_header(
        "FunnelVision",
        f"Welcome, {user['username']}"
    )

    if st.button(
        "Sign Out"
    ):

        logout()

    surveys = get_user_surveys(
        user["id"]
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "Your Shopping Profile"
    )

    if surveys:

        latest_stage = surveys[-1][3]

        st.markdown(
            f"""
            <div class="stage">
                {latest_stage}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            STAGE_CONTENT[
                latest_stage
            ]["description"]
        )

        st.write(
            f"Surveys completed: **{len(surveys)}**"
        )

    else:

        st.info(
            "You have not completed a survey yet."
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if st.button(
        "Retake Survey"
        if surveys
        else "Start Survey",
        type="primary",
        use_container_width=True
    ):

        st.session_state.responses = {}

        st.session_state.question_number = 0

        st.session_state.page = "survey"

        st.rerun()

    # -----------------------------------------------------
    # ACCOUNT DELETE
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Account Settings"
    )

    st.warning(
        "Deleting your account permanently removes "
        "your account and all of its survey records."
    )

    if st.session_state.get(
        "confirm_account_delete",
        False
    ) is False:

        if st.button(
            "Delete My Account"
        ):

            st.session_state.confirm_account_delete = True

            st.rerun()

    else:

        st.error(
            "Are you sure you want to permanently delete your account?"
        )

        yes_col, no_col = st.columns(2)

        with yes_col:

            if st.button(
                "Yes, Delete My Account",
                type="primary",
                use_container_width=True
            ):

                delete_user(
                    user["id"]
                )

                st.session_state.clear()

                initialize_session()

                st.rerun()

        with no_col:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.confirm_account_delete = False

                st.rerun()


# =========================================================
# SURVEY PAGE
# =========================================================

def survey_page():

    current = st.session_state.question_number

    qid, question, options = QUESTIONS[current]

    total_questions = len(
        QUESTIONS
    )

    progress = (
        current + 1
    ) / total_questions

    show_header(
        "FunnelVision Survey",
        f"Question {current + 1} of {total_questions}"
    )

    st.progress(
        progress
    )

    st.caption(
        f"{int(progress * 100)}% complete"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader(
        question
    )

    option_texts = [
        option[0]
        for option in options
    ]

    previous_answer = (
        st.session_state.responses.get(
            qid
        )
    )

    selected = st.radio(
        "Choose one:",
        options=range(
            len(option_texts)
        ),
        format_func=lambda x:
            option_texts[x],
        index=(
            previous_answer
            if previous_answer is not None
            else None
        ),
        key=f"question_{current}"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    left, middle, right = st.columns(3)

    with left:

        if st.button(
            "← Previous",
            disabled=(current == 0),
            use_container_width=True
        ):

            if selected is not None:

                st.session_state.responses[qid] = selected

            st.session_state.question_number -= 1

            st.rerun()

    with middle:

        if st.button(
            "Exit Survey",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()

    with right:

        button_text = (
            "Submit Survey"
            if current == total_questions - 1
            else "Next →"
        )

        if st.button(
            button_text,
            type="primary",
            use_container_width=True
        ):

            if selected is None:

                st.warning(
                    "Please select an option before continuing."
                )

            else:

                st.session_state.responses[qid] = selected

                if current < total_questions - 1:

                    st.session_state.question_number += 1

                    st.rerun()

                else:

                    (
                        predicted_stage,
                        scores,
                        match_strength
                    ) = calculate_scores(
                        st.session_state.responses
                    )

                    save_survey(
                        st.session_state.user["id"],
                        st.session_state.responses,
                        predicted_stage,
                        scores
                    )

                    st.session_state.last_result = {
                        "stage": predicted_stage,
                        "scores": scores,
                        "match_strength": match_strength
                    }

                    st.session_state.page = "results"

                    st.rerun()


# =========================================================
# RESULTS PAGE
# =========================================================

def results_page():

    result = st.session_state.last_result

    stage = result["stage"]

    scores = result["scores"]

    match_strength = result["match_strength"]

    content = STAGE_CONTENT[stage]

    show_header(
        "Your FunnelVision Result",
        "Your current shopping stage"
    )

    st.markdown(
        '<div class="hero">',
        unsafe_allow_html=True
    )

    st.caption(
        "PREDICTED STAGE"
    )

    st.markdown(
        f"""
        <div class="stage">
            {stage}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="metric-box">
            Match Strength: {match_strength:.0f}%
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        content["description"]
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # TIPS
    # -----------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader(
            "💡 Personalized Tips"
        )

        for tip in content["tips"]:

            st.write(
                f"✓ {tip}"
            )

    with right:

        st.subheader(
            "🎁 Special Offer"
        )

        st.info(
            content["offer"]
        )

    # -----------------------------------------------------
    # SCORE BREAKDOWN
    # -----------------------------------------------------

    st.subheader(
        "Stage Score Breakdown"
    )

    for funnel_stage in STAGES:

        score = scores.get(
            funnel_stage,
            0
        )

        st.write(
            f"**{funnel_stage}:** {score:.2f}"
        )

        st.progress(
            min(
                int(
                    (
                        score
                        / max(
                            max(scores.values()),
                            1
                        )
                    ) * 100
                ),
                100
            )
        )

    # -----------------------------------------------------
    # PRODUCTS
    # -----------------------------------------------------

    st.subheader(
        "🛍 Recommended Products"
    )

    products = get_recommended_products(
        stage
    )

    columns = st.columns(2)

    for index, product in enumerate(products):

        (
            name,
            category,
            price,
            rating,
            reviews,
            tags
        ) = product

        with columns[index % 2]:

            st.markdown(
                '<div class="product-card">',
                unsafe_allow_html=True
            )

            if index == 0:

                badge = "BEST MATCH"

            elif "bestseller" in tags:

                badge = "BESTSELLER"

            elif "trending" in tags:

                badge = "TRENDING"

            elif "value" in tags:

                badge = "BEST VALUE"

            else:

                badge = "RECOMMENDED"

            st.markdown(
                f"""
                <span class="badge">
                    {badge}
                </span>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"### {name}"
            )

            st.caption(
                category
            )

            st.write(
                f"⭐ {rating} • "
                f"{reviews:,} reviews"
            )

            st.markdown(
                f"### ${price:.2f}"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    left, right = st.columns(2)

    with left:

        if st.button(
            "← Back to Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "dashboard"

            st.rerun()

    with right:

        if st.button(
            "Retake Survey",
            type="primary",
            use_container_width=True
        ):

            st.session_state.responses = {}

            st.session_state.question_number = 0

            st.session_state.page = "survey"

            st.rerun()


# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_page():

    show_header(
        "Admin Dashboard",
        "Manage registered users and survey records"
    )

    if st.button(
        "Sign Out"
    ):

        logout()

    # =====================================================
    # USERS
    # =====================================================

    st.subheader(
        "👥 Users"
    )

    users = get_all_users()

    st.write(
        f"Currently registered users: **{len(users)}**"
    )

    if not users:

        st.info(
            "No users are currently registered."
        )

    else:

        # -------------------------------------------------
        # TABLE HEADER
        # -------------------------------------------------

        h1, h2, h3, h4, h5 = st.columns(
            [0.7, 2.0, 2.5, 2.0, 1.3]
        )

        h1.markdown(
            "**ID**"
        )

        h2.markdown(
            "**Username**"
        )

        h3.markdown(
            "**Created**"
        )

        h4.markdown(
            "**Predicted Stage**"
        )

        h5.markdown(
            "**Action**"
        )

        st.divider()

        # -------------------------------------------------
        # USER ROWS
        # -------------------------------------------------

        for user in users:

            user_id = user["id"]

            username = user["username"]

            created_at = user["created_at"]

            predicted_stage = user["stage"]

            c1, c2, c3, c4, c5 = st.columns(
                [0.7, 2.0, 2.5, 2.0, 1.3]
            )

            c1.write(
                user_id
            )

            c2.write(
                username
            )

            c3.write(
                created_at
                .replace(
                    "T",
                    " "
                )[:19]
            )

            c4.write(
                predicted_stage
            )

            if c5.button(
                "🗑️ Delete",
                key=f"user_delete_{user_id}",
                use_container_width=True
            ):

                st.session_state.delete_user_id = user_id

                st.rerun()

            # ---------------------------------------------
            # CONFIRM USER DELETION
            # ---------------------------------------------

            if (
                st.session_state.delete_user_id
                == user_id
            ):

                st.warning(
                    f"Delete '{username}' permanently? "
                    "All surveys belonging to this user "
                    "will also be deleted."
                )

                confirm, cancel = st.columns(2)

                with confirm:

                    if st.button(
                        "Yes, Delete User",
                        key=f"confirm_user_{user_id}",
                        type="primary",
                        use_container_width=True
                    ):

                        delete_user(
                            user_id
                        )

                        st.session_state.delete_user_id = None

                        st.rerun()

                with cancel:

                    if st.button(
                        "Cancel",
                        key=f"cancel_user_{user_id}",
                        use_container_width=True
                    ):

                        st.session_state.delete_user_id = None

                        st.rerun()

            st.divider()

    # =====================================================
    # SURVEY MANAGEMENT
    # =====================================================

    st.subheader(
        "📋 Survey Management"
    )

    all_surveys = get_all_surveys()

    st.write(
        f"Total surveys: **{len(all_surveys)}**"
    )

    if not all_surveys:

        st.info(
            "No surveys have been completed."
        )

    else:

        # -------------------------------------------------
        # SURVEY TABLE HEADER
        # -------------------------------------------------

        s1, s2, s3, s4, s5 = st.columns(
            [0.7, 2.0, 2.5, 2.0, 1.3]
        )

        s1.markdown(
            "**ID**"
        )

        s2.markdown(
            "**Username**"
        )

        s3.markdown(
            "**Date**"
        )

        s4.markdown(
            "**Predicted Stage**"
        )

        s5.markdown(
            "**Action**"
        )

        st.divider()

        # -------------------------------------------------
        # SURVEY ROWS
        # -------------------------------------------------

        for survey in all_surveys:

            survey_id = survey[0]

            user_id = survey[1]

            username = survey[2]

            timestamp = survey[3]

            stage = survey[4]

            c1, c2, c3, c4, c5 = st.columns(
                [0.7, 2.0, 2.5, 2.0, 1.3]
            )

            c1.write(
                survey_id
            )

            c2.write(
                username
            )

            c3.write(
                timestamp
                .replace(
                    "T",
                    " "
                )[:19]
            )

            c4.write(
                stage
            )

            if c5.button(
                "🗑️ Delete",
                key=f"survey_delete_{survey_id}",
                use_container_width=True
            ):

                st.session_state.delete_survey_id = survey_id

                st.rerun()

            # ---------------------------------------------
            # CONFIRM SURVEY DELETION
            # ---------------------------------------------

            if (
                st.session_state.delete_survey_id
                == survey_id
            ):

                st.warning(
                    f"Delete Survey #{survey_id} permanently?"
                )

                confirm, cancel = st.columns(2)

                with confirm:

                    if st.button(
                        "Yes, Delete Survey",
                        key=f"confirm_survey_{survey_id}",
                        type="primary",
                        use_container_width=True
                    ):

                        delete_survey(
                            survey_id
                        )

                        st.session_state.delete_survey_id = None

                        st.rerun()

                with cancel:

                    if st.button(
                        "Cancel",
                        key=f"cancel_survey_{survey_id}",
                        use_container_width=True
                    ):

                        st.session_state.delete_survey_id = None

                        st.rerun()

            st.divider()


# =========================================================
# APPLICATION START
# =========================================================

load_css()

setup_db()

initialize_session()


# =========================================================
# PAGE ROUTING
# =========================================================

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
