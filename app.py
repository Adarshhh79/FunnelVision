import streamlit as st
import sqlite3
from datetime import datetime
import json


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FunnelVision",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# CONSTANTS
# ============================================================

DB_NAME = "funnelvision.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# New version forces ONE fresh database reset.
# It will not reset the database again after completion.
DATABASE_VERSION = "fresh_start_v3"

STAGES = [
    "Awareness",
    "Interest",
    "Consideration",
    "Intent",
    "Purchase",
    "Loyalty"
]


# ============================================================
# QUESTIONS
# ============================================================

QUESTIONS = [
    {
        "question": "How do you usually discover new products?",
        "options": [
            "I rarely notice new products",
            "Social media or advertisements",
            "Recommendations and reviews",
            "I actively search for products",
            "I already know what I want"
        ]
    },
    {
        "question": "How often do you browse products online?",
        "options": [
            "Almost never",
            "Occasionally",
            "A few times a week",
            "Almost every day",
            "Very frequently"
        ]
    },
    {
        "question": "What do you usually do when a product catches your attention?",
        "options": [
            "Ignore it",
            "Look at it briefly",
            "Read more about it",
            "Compare it with alternatives",
            "Consider buying it"
        ]
    },
    {
        "question": "How much do customer reviews influence your decision?",
        "options": [
            "Not at all",
            "A little",
            "Moderately",
            "A lot",
            "They are very important"
        ]
    },
    {
        "question": "What usually convinces you to add a product to your cart?",
        "options": [
            "I rarely add products to cart",
            "Interesting features",
            "Good reviews",
            "Good value for money",
            "I am already planning to buy it"
        ]
    },
    {
        "question": "How many online purchases have you made in the past 6 months?",
        "options": [
            "None",
            "1–2",
            "3–5",
            "6–10",
            "More than 10"
        ]
    },
    {
        "question": "How do you usually react to the price of a product?",
        "options": [
            "Price immediately stops me",
            "I usually wait for discounts",
            "I compare prices",
            "I pay if the value is good",
            "Price is rarely a concern"
        ]
    },
    {
        "question": "How important is a return or replacement policy to you?",
        "options": [
            "Not important",
            "Slightly important",
            "Moderately important",
            "Very important",
            "Essential before buying"
        ]
    },
    {
        "question": "How likely are you to recommend a product you like?",
        "options": [
            "Very unlikely",
            "Unlikely",
            "Maybe",
            "Likely",
            "Very likely"
        ]
    },
    {
        "question": "Which statement best describes your current shopping mindset?",
        "options": [
            "Just browsing",
            "Looking for ideas",
            "Researching options",
            "Planning to buy",
            "Ready to purchase"
        ]
    }
]


# ============================================================
# PRODUCTS
# ============================================================

PRODUCTS = [
    "Wireless Noise-Cancelling Headphones",
    "Smart Fitness Watch Pro",
    "Premium Leather Backpack",
    "Portable Bluetooth Speaker",
    "Organic Cotton T-Shirt Pack",
    "Stainless Steel Water Bottle",
    "4K Ultra HD Webcam",
    "Ergonomic Office Chair",
    "Scented Candle Collection Set",
    "Wireless Charging Pad",
    "Running Shoes Ultra Light",
    "Smart Home Hub Controller"
]


# ============================================================
# STAGE CONTENT
# ============================================================

STAGE_CONTENT = {

    "Awareness": {
        "description":
            "You are discovering products and becoming aware of available options.",

        "tips": [
            "Explore different product categories.",
            "Look at product features and basic information.",
            "Save products that catch your attention."
        ],

        "tags": [
            "Exploring",
            "Discovering",
            "Browsing"
        ],

        "offer":
            "Explore products and discover what matches your needs."
    },

    "Interest": {
        "description":
            "You have started showing interest in products and want to know more.",

        "tips": [
            "Read product descriptions carefully.",
            "Check customer reviews.",
            "Compare important features."
        ],

        "tags": [
            "Interested",
            "Researching",
            "Exploring"
        ],

        "offer":
            "Compare products and find the features that matter most to you."
    },

    "Consideration": {
        "description":
            "You are seriously comparing products before making a decision.",

        "tips": [
            "Compare prices between alternatives.",
            "Check specifications and reviews.",
            "Consider warranty and return policies."
        ],

        "tags": [
            "Comparing",
            "Evaluating",
            "Researching"
        ],

        "offer":
            "Compare your shortlisted options before making your decision."
    },

    "Intent": {
        "description":
            "You are showing strong interest and may be preparing to purchase.",

        "tips": [
            "Check the final price.",
            "Review delivery and return information.",
            "Make sure the product meets your requirements."
        ],

        "tags": [
            "Ready",
            "Decision Making",
            "High Interest"
        ],

        "offer":
            "Review your final options and prepare for your purchase."
    },

    "Purchase": {
        "description":
            "You are at the stage where you are highly prepared to purchase.",

        "tips": [
            "Check the final order details.",
            "Confirm product availability.",
            "Review payment and delivery information."
        ],

        "tags": [
            "Purchase Ready",
            "High Intent",
            "Decision"
        ],

        "offer":
            "You appear ready to complete your purchase decision."
    },

    "Loyalty": {
        "description":
            "You show strong purchasing activity and potential for repeat engagement.",

        "tips": [
            "Look for products that complement previous purchases.",
            "Keep track of useful offers.",
            "Share useful products with people you know."
        ],

        "tags": [
            "Returning",
            "Engaged",
            "Loyal"
        ],

        "offer":
            "Discover products and offers that complement your interests."
    }
}


# ============================================================
# CSS
# ============================================================

def load_css():

    st.markdown(
        """
        <style>

        .main-title {
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }

        .stage-card {
            padding: 25px;
            border-radius: 15px;
            background: linear-gradient(
                135deg,
                #f5f7ff,
                #ffffff
            );
            border: 1px solid #e1e5f2;
            margin-bottom: 20px;
        }

        .stage-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .metric-card {
            padding: 20px;
            border-radius: 15px;
            background: #f7f8fc;
            border: 1px solid #e2e5ef;
            text-align: center;
        }

        .login-box {
            max-width: 500px;
            margin: auto;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    con = sqlite3.connect(DB_NAME)

    con.execute("PRAGMA foreign_keys = ON")

    return con


# ============================================================
# DATABASE SETUP
# ============================================================

def setup_db():

    with get_connection() as con:

        cur = con.cursor()

        # Settings table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS app_settings(
                setting_name TEXT PRIMARY KEY,
                setting_value TEXT NOT NULL
            )
            """
        )

        # Check whether this fresh version has already been completed.
        cur.execute(
            """
            SELECT setting_value
            FROM app_settings
            WHERE setting_name = ?
            """,
            (DATABASE_VERSION,)
        )

        version_exists = cur.fetchone()

        # ----------------------------------------------------
        # FIRST RUN OF THIS VERSION
        # ----------------------------------------------------

        if version_exists is None:

            # Completely remove old tables.
            # This removes the old hidden-column structure too.

            cur.execute("DROP TABLE IF EXISTS surveys")
            cur.execute("DROP TABLE IF EXISTS users")

            # ------------------------------------------------
            # CLEAN USERS TABLE
            # ------------------------------------------------

            cur.execute(
                """
                CREATE TABLE users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            # ------------------------------------------------
            # CLEAN SURVEYS TABLE
            # ------------------------------------------------

            cur.execute(
                """
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
                """
            )

            # ------------------------------------------------
            # CREATE FRESH ADMIN
            # ------------------------------------------------

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
                    ADMIN_USERNAME,
                    ADMIN_PASSWORD,
                    "admin",
                    datetime.now().isoformat()
                )
            )

            # Mark reset as completed.
            cur.execute(
                """
                INSERT INTO app_settings(
                    setting_name,
                    setting_value
                )
                VALUES(?,?)
                """,
                (
                    DATABASE_VERSION,
                    "completed"
                )
            )

            con.commit()

        else:

            # ------------------------------------------------
            # NORMAL STARTUP
            # ------------------------------------------------

            # Make sure the tables exist.
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            cur.execute(
                """
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
                """
            )

            # Make sure admin exists.
            cur.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (ADMIN_USERNAME,)
            )

            admin_exists = cur.fetchone()

            if admin_exists is None:

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
                        ADMIN_USERNAME,
                        ADMIN_PASSWORD,
                        "admin",
                        datetime.now().isoformat()
                    )
                )

            con.commit()


# ============================================================
# USER FUNCTIONS
# ============================================================

def register_user(username, password):

    username = username.strip()

    if not username or not password:
        return False, "Username and password are required."

    if username.lower() == ADMIN_USERNAME.lower():
        return False, "This username is reserved."

    try:

        with get_connection() as con:

            con.execute(
                """
                INSERT INTO users(
                    username,
                    password,
                    role,
                    created_at
                )
                VALUES(?,?,?,?,)
                """.replace("?,?,?,?,", "?,?,?,"),
                (
                    username,
                    password,
                    "user",
                    datetime.now().isoformat()
                )
            )

            con.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "Username already exists."


def authenticate(username, password):

    with get_connection() as con:

        cur = con.cursor()

        cur.execute(
            """
            SELECT id, username, role
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (
                username,
                password
            )
        )

        return cur.fetchone()


def get_user_by_id(user_id):

    with get_connection() as con:

        cur = con.cursor()

        cur.execute(
            """
            SELECT id, username, role, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        )

        return cur.fetchone()


def delete_user(user_id):

    with get_connection() as con:

        cur = con.cursor()

        # Delete surveys first.
        cur.execute(
            """
            DELETE FROM surveys
            WHERE user_id = ?
            """,
            (user_id,)
        )

        # Then delete the user.
        cur.execute(
            """
            DELETE FROM users
            WHERE id = ?
            AND role = 'user'
            """,
            (user_id,)
        )

        con.commit()


# ============================================================
# SURVEY FUNCTIONS
# ============================================================

def save_survey(
    user_id,
    responses,
    stage,
    scores
):

    with get_connection() as con:

        con.execute(
            """
            INSERT INTO surveys(
                user_id,
                timestamp,
                responses,
                stage,
                scores
            )
            VALUES(?,?,?,?,?)
            """,
            (
                user_id,
                datetime.now().isoformat(),
                json.dumps(responses),
                stage,
                json.dumps(scores)
            )
        )

        con.commit()


def get_user_surveys(user_id):

    with get_connection() as con:

        cur = con.cursor()

        cur.execute(
            """
            SELECT
                id,
                timestamp,
                responses,
                stage,
                scores
            FROM surveys
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

        return cur.fetchall()


def get_latest_stage(user_id):

    with get_connection() as con:

        cur = con.cursor()

        cur.execute(
            """
            SELECT stage
            FROM surveys
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        result = cur.fetchone()

        if result:
            return result[0]

        return "Not completed"


def delete_survey(survey_id):

    with get_connection() as con:

        con.execute(
            """
            DELETE FROM surveys
            WHERE id = ?
            """,
            (survey_id,)
        )

        con.commit()


# ============================================================
# ADMIN DATA
# ============================================================

def get_all_users():

    with get_connection() as con:

        cur = con.cursor()

        cur.execute(
            """
            SELECT
                u.id,
                u.username,
                u.created_at,

                COALESCE(
                    (
                        SELECT s.stage
                        FROM surveys s
                        WHERE s.user_id = u.id
                        ORDER BY s.id DESC
                        LIMIT 1
                    ),
                    'Not completed'
                ) AS predicted_stage

            FROM users u

            WHERE u.role = 'user'

            ORDER BY u.id ASC
            """
        )

        return cur.fetchall()


def get_all_surveys():

    with get_connection() as con:

        cur = con.cursor()

        cur.execute(
            """
            SELECT
                s.id,
                u.username,
                s.timestamp,
                s.stage

            FROM surveys s

            INNER JOIN users u
                ON s.user_id = u.id

            ORDER BY s.id DESC
            """
        )

        return cur.fetchall()


# ============================================================
# SCORING
# ============================================================

def calculate_scores(responses):

    scores = {
        "Awareness": 0,
        "Interest": 0,
        "Consideration": 0,
        "Intent": 0,
        "Purchase": 0,
        "Loyalty": 0
    }

    # Each answer contributes progressively.
    for index, answer in enumerate(responses):

        answer_index = QUESTIONS[index]["options"].index(answer)

        value = answer_index + 1

        # Base score
        scores["Awareness"] += max(0, 6 - value)

        scores["Interest"] += value * 1.00

        scores["Consideration"] += value * 1.15

        scores["Intent"] += value * 1.30

        scores["Purchase"] += value * 1.30

        scores["Loyalty"] += value * 1.15

    return scores


def predict_stage(scores):

    # Determine highest scoring stage.
    highest_stage = max(
        scores,
        key=scores.get
    )

    return highest_stage


def calculate_match_strength(scores, stage):

    total = sum(scores.values())

    if total <= 0:
        return 0

    stage_score = scores.get(stage, 0)

    strength = (
        stage_score / total
    ) * 100

    return round(
        min(strength * 3, 100),
        1
    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

def get_recommendations(stage):

    if stage == "Awareness":

        return PRODUCTS[:4]

    if stage == "Interest":

        return PRODUCTS[2:7]

    if stage == "Consideration":

        return PRODUCTS[4:9]

    if stage == "Intent":

        return PRODUCTS[6:11]

    if stage == "Purchase":

        return PRODUCTS[7:12]

    if stage == "Loyalty":

        return PRODUCTS[3:9]

    return PRODUCTS[:4]


# ============================================================
# SESSION INITIALIZATION
# ============================================================

def initialize_session():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "username" not in st.session_state:
        st.session_state.username = None

    if "role" not in st.session_state:
        st.session_state.role = None

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if "survey_responses" not in st.session_state:
        st.session_state.survey_responses = []

    if "survey_scores" not in st.session_state:
        st.session_state.survey_scores = {}

    if "survey_stage" not in st.session_state:
        st.session_state.survey_stage = None


# ============================================================
# LOGOUT
# ============================================================

def logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.page = "Home"

    st.rerun()


# ============================================================
# HEADER
# ============================================================

def show_header():

    st.markdown(
        '<div class="main-title">🎯 FunnelVision</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Understand your customer journey'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# HOME PAGE
# ============================================================

def home_page():

    show_header()

    st.markdown(
        """
        ### Welcome to FunnelVision

        FunnelVision analyzes your shopping behaviour and
        estimates which stage of the customer journey best
        describes your current behaviour.
        """
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            """
            ### 🔎 Discover

            Understand how you discover products
            and what catches your attention.
            """
        )

    with col2:

        st.info(
            """
            ### 📊 Analyze

            Answer a short set of questions
            about your shopping behaviour.
            """
        )

    with col3:

        st.info(
            """
            ### 🎯 Understand

            See your predicted customer journey
            stage and recommendations.
            """
        )

    st.write("")

    if not st.session_state.logged_in:

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Login",
                use_container_width=True
            ):

                st.session_state.page = "Login"
                st.rerun()

        with col2:

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                st.session_state.page = "Register"
                st.rerun()

    else:

        if st.button(
            "Go to Dashboard",
            use_container_width=True
        ):

            st.session_state.page = "Dashboard"
            st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )

    st.title("🔐 Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = authenticate(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.username = user[1]
            st.session_state.role = user[2]

            if user[2] == "admin":
                st.session_state.page = "Admin"
            else:
                st.session_state.page = "Dashboard"

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    if st.button(
        "Create a new account"
    ):

        st.session_state.page = "Register"
        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# REGISTER PAGE
# ============================================================

def register_page():

    st.title("📝 Create Account")

    username = st.text_input(
        "Choose a username"
    )

    password = st.text_input(
        "Choose a password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm password",
        type="password"
    )

    if st.button(
        "Create Account",
        use_container_width=True
    ):

        if password != confirm_password:

            st.error(
                "Passwords do not match."
            )

            return

        success, message = register_user(
            username,
            password
        )

        if success:

            st.success(message)

            st.info(
                "You can now login using your new account."
            )

        else:

            st.error(message)

    if st.button(
        "Back to Login"
    ):

        st.session_state.page = "Login"
        st.rerun()


# ============================================================
# SURVEY PAGE
# ============================================================

def survey_page():

    st.title("📋 FunnelVision Survey")

    st.write(
        "Answer each question based on your usual shopping behaviour."
    )

    responses = []

    for index, question_data in enumerate(QUESTIONS):

        st.subheader(
            f"{index + 1}. {question_data['question']}"
        )

        answer = st.radio(
            "Select one:",
            question_data["options"],
            key=f"question_{index}",
            index=None
        )

        responses.append(answer)

        st.divider()

    if st.button(
        "Submit Survey",
        use_container_width=True
    ):

        if any(
            answer is None
            for answer in responses
        ):

            st.warning(
                "Please answer all questions before submitting."
            )

            return

        scores = calculate_scores(
            responses
        )

        stage = predict_stage(
            scores
        )

        st.session_state.survey_responses = responses
        st.session_state.survey_scores = scores
        st.session_state.survey_stage = stage

        save_survey(
            st.session_state.user_id,
            responses,
            stage,
            scores
        )

        st.session_state.page = "Results"

        st.rerun()


# ============================================================
# RESULTS PAGE
# ============================================================

def results_page():

    stage = st.session_state.survey_stage

    scores = st.session_state.survey_scores

    if not stage:

        st.warning(
            "No survey result is available."
        )

        return

    content = STAGE_CONTENT[stage]

    match_strength = calculate_match_strength(
        scores,
        stage
    )

    st.title("🎯 Your FunnelVision Result")

    st.markdown(
        f"""
        <div class="stage-card">

        <div class="stage-title">
        {stage}
        </div>

        <p>
        {content["description"]}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Predicted Stage",
            stage
        )

    with col2:

        st.metric(
            "Match Strength",
            f"{match_strength}%"
        )

    st.subheader("📌 Key Points")

    for tip in content["tips"]:

        st.write(
            f"• {tip}"
        )

    st.subheader("🏷️ Behaviour Tags")

    for tag in content["tags"]:

        st.write(
            f"**{tag}**"
        )

    st.info(
        content["offer"]
    )

    st.subheader("🛍️ Recommended Products")

    recommendations = get_recommendations(
        stage
    )

    for product in recommendations:

        st.write(
            f"• {product}"
        )

    st.subheader("📊 Stage Scores")

    score_data = {
        "Stage": list(scores.keys()),
        "Score": list(scores.values())
    }

    st.dataframe(
        score_data,
        use_container_width=True,
        hide_index=True
    )

    st.write("")

    if st.button(
        "Take Survey Again",
        use_container_width=True
    ):

        st.session_state.page = "Survey"
        st.rerun()


# ============================================================
# USER DASHBOARD
# ============================================================

def dashboard_page():

    user = get_user_by_id(
        st.session_state.user_id
    )

    if not user:

        logout()
        return

    st.title(
        f"👋 Welcome, {user[1]}"
    )

    latest_stage = get_latest_stage(
        st.session_state.user_id
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Username",
            user[1]
        )

    with col2:

        st.metric(
            "Current Stage",
            latest_stage
        )

    with col3:

        surveys = get_user_surveys(
            st.session_state.user_id
        )

        st.metric(
            "Surveys Completed",
            len(surveys)
        )

    st.write("")

    if st.button(
        "📋 Take FunnelVision Survey",
        use_container_width=True
    ):

        st.session_state.page = "Survey"
        st.rerun()

    st.subheader("📊 My Survey History")

    if surveys:

        history = []

        for survey in surveys:

            history.append(
                {
                    "Survey ID": survey[0],
                    "Date": survey[1],
                    "Predicted Stage": survey[3]
                }
            )

        st.dataframe(
            history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "You have not completed a survey yet."
        )

    st.divider()

    st.subheader("⚠️ Account")

    st.warning(
        "Deleting your account permanently removes your account "
        "and all associated survey records."
    )

    if st.button(
        "Delete My Account",
        type="secondary"
    ):

        st.session_state.confirm_account_delete = True

    if st.session_state.get(
        "confirm_account_delete",
        False
    ):

        st.error(
            "Are you sure you want to permanently delete your account?"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Yes, Delete Account",
                type="primary"
            ):

                delete_user(
                    st.session_state.user_id
                )

                st.session_state.logged_in = False
                st.session_state.user_id = None
                st.session_state.username = None
                st.session_state.role = None
                st.session_state.page = "Home"
                st.session_state.confirm_account_delete = False

                st.rerun()

        with col2:

            if st.button(
                "Cancel"
            ):

                st.session_state.confirm_account_delete = False
                st.rerun()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_page():

    st.title("🛠️ Admin Dashboard")

    st.caption(
        "Manage registered users and completed surveys."
    )

    # ========================================================
    # USERS TABLE
    # ========================================================

    st.header("👥 Users")

    users = get_all_users()

    if users:

        user_table = []

        for user in users:

            user_table.append(
                {
                    "ID": user[0],
                    "Username": user[1],
                    "Created": user[2],
                    "Predicted Stage": user[3]
                }
            )

        # REAL TABULAR DISPLAY
        st.dataframe(
            user_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn(
                    "ID",
                    width="small"
                ),
                "Username": st.column_config.TextColumn(
                    "Username",
                    width="medium"
                ),
                "Created": st.column_config.TextColumn(
                    "Created",
                    width="large"
                ),
                "Predicted Stage": st.column_config.TextColumn(
                    "Predicted Stage",
                    width="medium"
                )
            }
        )

        st.subheader("Delete User")

        delete_user_options = {
            f"{user[1]} (ID: {user[0]})": user[0]
            for user in users
        }

        selected_user = st.selectbox(
            "Select a user to delete",
            list(delete_user_options.keys()),
            key="delete_user_select"
        )

        if st.button(
            "🗑️ Delete Selected User",
            type="secondary",
            use_container_width=True
        ):

            user_id = delete_user_options[
                selected_user
            ]

            st.session_state.delete_user_id = user_id
            st.session_state.confirm_admin_user_delete = True

        if st.session_state.get(
            "confirm_admin_user_delete",
            False
        ):

            st.warning(
                "This will permanently delete the selected user "
                "and all of their surveys."
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Confirm User Deletion",
                    type="primary",
                    key="confirm_user_delete"
                ):

                    delete_user(
                        st.session_state.delete_user_id
                    )

                    st.session_state.confirm_admin_user_delete = False
                    st.session_state.delete_user_id = None

                    st.success(
                        "User permanently deleted."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Cancel",
                    key="cancel_user_delete"
                ):

                    st.session_state.confirm_admin_user_delete = False
                    st.session_state.delete_user_id = None

                    st.rerun()

    else:

        st.info(
            "No registered users found."
        )

    # ========================================================
    # SURVEY MANAGEMENT
    # ========================================================

    st.divider()

    st.header("📋 Survey Management")

    surveys = get_all_surveys()

    if surveys:

        survey_table = []

        for survey in surveys:

            survey_table.append(
                {
                    "Survey ID": survey[0],
                    "Username": survey[1],
                    "Date": survey[2],
                    "Predicted Stage": survey[3]
                }
            )

        # REAL TABULAR DISPLAY
        st.dataframe(
            survey_table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Survey ID": st.column_config.NumberColumn(
                    "Survey ID",
                    width="small"
                ),
                "Username": st.column_config.TextColumn(
                    "Username",
                    width="medium"
                ),
                "Date": st.column_config.TextColumn(
                    "Date",
                    width="large"
                ),
                "Predicted Stage": st.column_config.TextColumn(
                    "Predicted Stage",
                    width="medium"
                )
            }
        )

        st.subheader("Delete Survey")

        delete_survey_options = {
            f"Survey #{survey[0]} — {survey[1]} — {survey[3]}":
                survey[0]
            for survey in surveys
        }

        selected_survey = st.selectbox(
            "Select a survey to delete",
            list(delete_survey_options.keys()),
            key="delete_survey_select"
        )

        if st.button(
            "🗑️ Delete Selected Survey",
            type="secondary",
            use_container_width=True
        ):

            survey_id = delete_survey_options[
                selected_survey
            ]

            st.session_state.delete_survey_id = survey_id
            st.session_state.confirm_admin_survey_delete = True

        if st.session_state.get(
            "confirm_admin_survey_delete",
            False
        ):

            st.warning(
                "This survey will be permanently deleted."
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Confirm Survey Deletion",
                    type="primary",
                    key="confirm_survey_delete"
                ):

                    delete_survey(
                        st.session_state.delete_survey_id
                    )

                    st.session_state.confirm_admin_survey_delete = False
                    st.session_state.delete_survey_id = None

                    st.success(
                        "Survey permanently deleted."
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "Cancel",
                    key="cancel_survey_delete"
                ):

                    st.session_state.confirm_admin_survey_delete = False
                    st.session_state.delete_survey_id = None

                    st.rerun()

    else:

        st.info(
            "No surveys have been completed yet."
        )

    # ========================================================
    # ADMIN INFORMATION
    # ========================================================

    st.divider()

    st.subheader("ℹ️ Database Information")

    total_users = len(
        get_all_users()
    )

    total_surveys = len(
        get_all_surveys()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Registered Users",
            total_users
        )

    with col2:

        st.metric(
            "Completed Surveys",
            total_surveys
        )


# ============================================================
# SIDEBAR
# ============================================================

def sidebar():

    with st.sidebar:

        st.title("🎯 FunnelVision")

        st.divider()

        if st.session_state.logged_in:

            st.write(
                f"**Logged in as:** "
                f"{st.session_state.username}"
            )

            st.divider()

            if st.session_state.role == "admin":

                if st.button(
                    "🛠️ Admin Dashboard",
                    use_container_width=True
                ):

                    st.session_state.page = "Admin"
                    st.rerun()

            else:

                if st.button(
                    "🏠 Home",
                    use_container_width=True
                ):

                    st.session_state.page = "Home"
                    st.rerun()

                if st.button(
                    "📊 Dashboard",
                    use_container_width=True
                ):

                    st.session_state.page = "Dashboard"
                    st.rerun()

                if st.button(
                    "📋 Take Survey",
                    use_container_width=True
                ):

                    st.session_state.page = "Survey"
                    st.rerun()

            st.divider()

            if st.button(
                "🚪 Logout",
                use_container_width=True
            ):

                logout()

        else:

            if st.button(
                "🏠 Home",
                use_container_width=True
            ):

                st.session_state.page = "Home"
                st.rerun()

            if st.button(
                "🔐 Login",
                use_container_width=True
            ):

                st.session_state.page = "Login"
                st.rerun()

            if st.button(
                "📝 Register",
                use_container_width=True
            ):

                st.session_state.page = "Register"
                st.rerun()


# ============================================================
# MAIN APPLICATION
# ============================================================

load_css()

setup_db()

initialize_session()

sidebar()


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "Home":

    home_page()

elif st.session_state.page == "Login":

    login_page()

elif st.session_state.page == "Register":

    register_page()

elif st.session_state.page == "Survey":

    if st.session_state.logged_in:

        survey_page()

    else:

        st.session_state.page = "Login"
        st.rerun()

elif st.session_state.page == "Results":

    if st.session_state.logged_in:

        results_page()

    else:

        st.session_state.page = "Login"
        st.rerun()

elif st.session_state.page == "Dashboard":

    if (
        st.session_state.logged_in
        and st.session_state.role == "user"
    ):

        dashboard_page()

    else:

        st.session_state.page = "Login"
        st.rerun()

elif st.session_state.page == "Admin":

    if (
        st.session_state.logged_in
        and st.session_state.role == "admin"
    ):

        admin_page()

    else:

        st.session_state.page = "Login"
        st.rerun()

else:

    home_page()
