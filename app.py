STAGES = ["Awareness", "Interest", "Consideration", "Intent", "Purchase", "Loyalty"]

QUESTIONS = [
    ("q1", "How did you first discover online shopping platforms like ours?",
     [("Through social media advertisements","Awareness",3),("Recommended by friends or family","Interest",3),
      ("Found via search engine results","Consideration",3),("Visited directly from a bookmark or typed the URL","Intent",3),
      ("Received an email or newsletter","Loyalty",3),("I am not aware of any such platforms yet","Awareness",1)]),
    ("q2", "How frequently do you browse e-commerce websites?",
     [("This is my very first time","Awareness",3),("Rarely, only when I see an ad","Awareness",2),
      ("A few times a month","Interest",3),("Several times a week","Consideration",3),
      ("Almost every day","Intent",3),("Multiple times daily - it is part of my routine","Loyalty",3)]),
    ("q3", "When you find a product that catches your eye, what is your typical next step?",
     [("Just take a mental note and move on","Interest",3),("Save it to a wishlist for later","Consideration",3),
      ("Compare it with similar products on other sites","Consideration",3),
      ("Read customer reviews and check ratings thoroughly","Intent",3),("Add it to my cart right away","Intent",3),
      ("I rarely find products that catch my eye online","Awareness",3)]),
    ("q4", "How much do customer reviews and ratings influence your purchase decisions?",
     [("Not at all - I rely on product descriptions alone","Awareness",3),
      ("Slightly - I glance at them but do not depend on them","Interest",3),
      ("Moderately - they are one factor among many","Consideration",3),
      ("Significantly - I read several reviews before deciding","Intent",3),
      ("They are the single most important factor for me","Purchase",3)]),
    ("q5", "What would most likely convince you to add an item to your cart right now?",
     [("An eye-catching product image or video","Awareness",3),
      ("A detailed feature list and clear specifications","Interest",3),
      ("A price that is noticeably lower than competitors","Consideration",3),
      ("Free shipping or a limited-time discount code","Intent",3),
      ("A strong personal recommendation from someone I trust","Loyalty",3)]),
    ("q6", "How many online purchases have you made in the past 6 months?",
     [("None at all","Awareness",3),("1 to 2 purchases","Purchase",3),
      ("3 to 5 purchases","Loyalty",2),("6 to 10 purchases","Loyalty",3),
      ("More than 10 purchases","Loyalty",3)]),
    ("q7", "How would you describe the pricing of products you typically shop for online?",
     [("Too expensive - I rarely buy at full price","Awareness",3),
      ("Slightly high but I might buy during sales","Interest",3),
      ("Reasonable for the quality offered","Consideration",3),
      ("Good value - I feel confident making purchases","Intent",3),
      ("Excellent value - I consistently find great deals","Loyalty",3)]),
    ("q8", "Which factor would most encourage you to return to an online store?",
     [("A wider and more interesting product selection","Interest",3),
      ("Better prices or a price-match guarantee","Consideration",3),
      ("Faster and more reliable delivery options","Intent",3),
      ("Loyalty rewards, points, or cashback programs","Loyalty",3),
      ("Personalized product recommendations tailored to me","Loyalty",3)]),
    ("q9", "How likely are you to recommend our platform to a friend or colleague?",
     [("Very unlikely","Awareness",3),("Unlikely","Interest",3),
      ("Neutral - it would depend on the overall experience","Consideration",3),
      ("Likely","Purchase",3),("Very likely - I already have recommended it","Loyalty",3)]),
    ("q10", "Which statement best describes your current shopping mindset?",
     [("Just browsing casually to see what is out there","Awareness",3),
      ("Looking for something specific but still exploring options","Interest",3),
      ("Actively comparing multiple products before deciding","Consideration",3),
      ("Ready to buy as soon as I find the right deal","Intent",3),
      ("I have made up my mind and am about to complete a purchase","Purchase",3),
      ("I am a satisfied repeat customer looking for my next purchase","Loyalty",3)])
]

PRODUCTS = [
    ("Wireless Noise-Cancelling Headphones","Electronics",199.99,4.7,2340,["trending","bestseller"]),
    ("Smart Fitness Watch Pro","Wearables",149.99,4.5,1876,["new","trending"]),
    ("Premium Leather Backpack","Accessories",89.99,4.8,956,["bestseller"]),
    ("Portable Bluetooth Speaker","Electronics",59.99,4.3,3210,["trending","value"]),
    ("Organic Cotton T-Shirt Pack","Clothing",39.99,4.6,4521,["value","bestseller"]),
    ("Stainless Steel Water Bottle","Lifestyle",24.99,4.4,5670,["value"]),
    ("4K Ultra HD Webcam","Electronics",129.99,4.2,890,["new"]),
    ("Ergonomic Office Chair","Furniture",349.99,4.9,1234,["bestseller","premium"]),
    ("Scented Candle Collection Set","Home",34.99,4.7,2100,["trending"]),
    ("Wireless Charging Pad","Electronics",29.99,4.1,4300,["value","trending"]),
    ("Running Shoes Ultra Light","Footwear",119.99,4.6,1670,["new","bestseller"]),
    ("Smart Home Hub Controller","Smart Home",79.99,4.3,980,["new"])
]

STAGE_CONTENT = {
    "Awareness": ("You are at the beginning of your shopping journey.",
                  ["Browse trending categories","Check out new arrivals","Follow product highlights"],["trending","new"],
                  "Welcome Explorer - Get 10% off your first order with code WELCOME10"),
    "Interest": ("You have shown interest in certain products.",
                  ["Read product guides and comparisons","Watch product demo videos","Sign up for product alerts"],["bestseller","trending"],
                  "Curious Shopper - Free shipping on your first purchase this month"),
    "Consideration": ("You are actively comparing options.",
                       ["Use side-by-side comparisons","Read verified buyer reviews","Check the price-match policy"],["bestseller","value"],
                       "Smart Buyer - Price match guarantee plus an extra 5% off"),
    "Intent": ("You are almost ready to buy.",
               ["Add items to cart","Apply available coupons","Choose express shipping"],["trending","value","bestseller"],
               "Ready to Buy - Extra 15% off everything in your cart"),
    "Purchase": ("You have made a purchase decision.",
                 ["Complete checkout securely","Track your order","Leave a review for reward points"],["bestseller","premium"],
                 "New Customer - Earn double reward points on your first completed order"),
    "Loyalty": ("You are a valued repeat customer.",
                ["Access VIP pricing","Get early access to sales","Refer friends for rewards"],["premium","bestseller","new"],
                "Loyal Member - Exclusive VIP pricing + free express shipping")
}

def setup_db():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TEXT NOT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS surveys(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            responses TEXT NOT NULL,
            stage TEXT NOT NULL,
            scores TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id))""")
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            now = datetime.now()
            sample = [
                ("admin","admin123","admin",now-timedelta(days=30)),
                ("sarah_m","shop2024","user",now-timedelta(days=20)),
                ("james_k","deal99","user",now-timedelta(days=10)),
                ("emma_r","browse1","user",now-timedelta(days=3)),
                ("mike_t","buyer77","user",now-timedelta(days=7))
            ]
            for u,p,r,d in sample:
                cur.execute("INSERT INTO users(username,password,role,created_at) VALUES(?,?,?,?)",
                            (u,p,r,d.isoformat()))
            con.commit()

def get_user(username, password):
    with sqlite3.connect(DB_NAME) as con:
        return con.execute(
            "SELECT id,username,password,role,created_at FROM users "
            "WHERE lower(username)=lower(?) AND password=?",
            (username, password)).fetchone()

def register_user(username, password):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            "INSERT INTO users(username,password,role,created_at) VALUES(?,?,?,?)",
            (username, password, "user", datetime.now().isoformat()))
        return con.execute("SELECT last_insert_rowid()").fetchone()[0]

def get_surveys(user_id):
    with sqlite3.connect(DB_NAME) as con:
        return con.execute(
            "SELECT id,timestamp,responses,stage,scores FROM surveys WHERE user_id=? ORDER BY id",
            (user_id,)).fetchall()

def save_survey(user_id, responses, stage, scores):
    with sqlite3.connect(DB_NAME) as con:
        con.execute(
            "INSERT INTO surveys(user_id,timestamp,responses,stage,scores) VALUES(?,?,?,?,?)",
            (user_id, datetime.now().isoformat(), str(responses), stage, str(scores)))

def calculate(responses):
    scores = {s: 0 for s in STAGES}
    for qid, _, options in QUESTIONS:
        idx = responses.get(qid)
        if idx is not None and idx >= 0:
            _, stage, base_score = options[idx]
            multiplier = {1:1.00, 2:1.25, 3:1.50}.get(base_score, 1.00)
            scores[stage] += base_score * multiplier
    predicted = max(STAGES, key=lambda s: scores[s])
    total_score = sum(scores.values())
    match_strength = (scores[predicted] / total_score) * 100 if total_score else 0
    return predicted, scores, match_strength

def products_for_stage(stage):
    tags = STAGE_CONTENT[stage][2]
    matched = [p for p in PRODUCTS if any(t in tags for t in p[5])]
    others = [p for p in PRODUCTS if p not in matched]
    return (matched + others)[:4]

def init_state():
    defaults = {"page":"login","user":None,"responses":{},"step":0,
                "last_result":None,"register_mode":False}
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def logout():
    st.session_state.clear()
    init_state()
    st.rerun()

def header(title, subtitle=None):
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)

def login_page():
    header("FunnelVision","Smart E-Commerce Funnel Predictor")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Welcome back")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
    if submitted:
        row = get_user(username.strip(), password)
        if row:
            st.session_state.user = {"id":row[0],"username":row[1],"role":row[3],"created_at":row[4]}
            st.session_state.page = "admin" if row[3]=="admin" else "dashboard"
            st.rerun()
        else:
            st.error("Invalid username or password.")
    if st.button("Create an account", use_container_width=True):
        st.session_state.page="register"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Demo admin: admin / admin123")

def register_page():
    header("Create Account","Join FunnelVision and discover your shopping profile")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("register_form"):
        username=st.text_input("Username")
        password=st.text_input("Password",type="password")
        confirm=st.text_input("Confirm Password",type="password")
        submitted=st.form_submit_button("Create Account & Start Survey",use_container_width=True)
    if submitted:
        if len(username.strip())<3 or len(password)<4:
            st.error("Username must be 3+ characters and password 4+ characters.")
        elif password != confirm:
            st.error("Passwords do not match.")
        else:
            try:
                uid=register_user(username.strip(),password)
                st.session_state.user={"id":uid,"username":username.strip(),"role":"user",
                                        "created_at":datetime.now().isoformat()}
                st.session_state.responses={}
                st.session_state.step=0
                st.session_state.page="survey"
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Username already exists.")
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("Back to Sign In"):
        st.session_state.page="login"
        st.rerun()

def dashboard_page():
    user=st.session_state.user
    header("FunnelVision",f"Welcome, {user['username']}")
    if st.button("Sign Out"): logout()
    surveys=get_surveys(user["id"])
    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.subheader("Your Shopping Funnel Profile")
    st.write(f"{len(surveys)} survey(s) completed")
    if st.button("Retake Survey" if surveys else "Begin Survey",type="primary"):
        st.session_state.responses={}
        st.session_state.step=0
        st.session_state.page="survey"
        st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)
    if surveys:
        stage=surveys[-1][3]
        content=STAGE_CONTENT[stage]
        st.markdown('<div class="hero">',unsafe_allow_html=True)
        st.markdown(f"### Latest Stage: <span class='stage'>{stage}</span>",unsafe_allow_html=True)
        st.write(content[0])
        st.markdown("**Recommended products:**")
        for p in products_for_stage(stage):
            st.write(f"• {p[0]} | ${p[2]:.2f} | ⭐ {p[3]}")
        st.markdown('</div>',unsafe_allow_html=True)

def survey_page():
    step=st.session_state.step
    qid,question,options=QUESTIONS[step]
    progress=(step+1)/len(QUESTIONS)
    header("Survey",f"Question {step+1} of {len(QUESTIONS)}")
    st.progress(progress)
    st.caption(f"{int(progress*100)}% complete")
    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.markdown(f"### {question}")
    labels=[o[0] for o in options]
    previous=st.session_state.responses.get(qid)
    selected=st.radio("Choose one:",range(len(labels)),
                      format_func=lambda i:labels[i],
                      index=previous if previous is not None else None,
                      key=f"answer_{step}")
    st.markdown('</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a:
        if st.button("Previous",disabled=step==0,use_container_width=True):
            st.session_state.responses[qid]=selected
            st.session_state.step-=1
            st.rerun()
    with b:
        if st.button("Exit",use_container_width=True):
            st.session_state.page="dashboard"; st.rerun()
    with c:
        label="Submit Survey" if step==len(QUESTIONS)-1 else "Next"
        if st.button(label,type="primary",use_container_width=True):
            if selected is None:
                st.warning("Please select an option.")
            else:
                st.session_state.responses[qid]=selected
                if step<len(QUESTIONS)-1:
                    st.session_state.step+=1; st.rerun()
                else:
                    stage,scores,strength=calculate(st.session_state.responses)
                    save_survey(st.session_state.user["id"],st.session_state.responses,stage,scores)
                    st.session_state.last_result=(stage,scores,strength)
                    st.session_state.page="results"; st.rerun()

def results_page():
    stage,scores,match_strength=st.session_state.last_result
    content=STAGE_CONTENT[stage]
    header("Your Shopping Profile","Your strongest funnel stage is ready")
    st.markdown('<div class="hero">',unsafe_allow_html=True)
    st.caption("🏆 STRONGEST FUNNEL STAGE")
    st.markdown(f'<div class="stage">{stage}</div>',unsafe_allow_html=True)
    st.write(f"**Your score:** {scores[stage]:.1f}")
    st.markdown(f'<div class="metric">Match Strength: {match_strength:.0f}%</div>',unsafe_allow_html=True)
    st.write(content[0])
    st.markdown('</div>',unsafe_allow_html=True)

    left,right=st.columns(2)
    with left:
        st.markdown('<div class="tip">',unsafe_allow_html=True)
        st.subheader("💡 Personalized Tips")
        for tip in content[1]: st.write("✓ "+tip)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="offer">',unsafe_allow_html=True)
        st.subheader("🎁 Special Offer")
        st.markdown(f"**{content[3]}**")
        st.markdown('</div>',unsafe_allow_html=True)

    st.subheader("🛍 Picked For You")
    st.caption("Products selected using your strongest shopping stage")
    cols=st.columns(2)
    for i,p in enumerate(products_for_stage(stage)):
        name,category,price,rating,reviews,tags=p
        tag=("BEST MATCH" if i==0 else "TRENDING" if "trending" in tags
             else "BEST VALUE" if "value" in tags else
             "TOP RATED" if rating>=4.7 else "RECOMMENDED")
        with cols[i%2]:
            st.markdown('<div class="product">',unsafe_allow_html=True)
            st.markdown(f'<span class="badge">{tag}</span>',unsafe_allow_html=True)
            st.markdown(f"### 🛍️ {name}")
            st.caption(category.upper())
            st.write(f"⭐ {rating:.1f} • {reviews:,} reviews")
            st.markdown(f"**${price:.2f}**")
            why={
                "Awareness":"A great discovery pick for your browsing style.",
                "Interest":"Matches your current product-exploration mindset.",
                "Consideration":"Useful for comparing quality, value and reviews.",
                "Intent":"A strong match for someone close to buying.",
                "Purchase":"A solid choice for your purchase-ready profile.",
                "Loyalty":"A great pick for repeat shoppers looking for value."
            }.get(stage,"Selected based on your shopping profile.")
            st.caption("Why this matches you: "+why)
            st.markdown('</div>',unsafe_allow_html=True)

    st.write("")
    a,b=st.columns(2)
    with a:
        if st.button("← Dashboard",use_container_width=True):
            st.session_state.page="dashboard"; st.rerun()
    with b:
        if st.button("Retake Survey",type="primary",use_container_width=True):
            st.session_state.responses={}; st.session_state.step=0
            st.session_state.page="survey"; st.rerun()

def admin_page():
    header("Admin Dashboard","Overview of users, surveys and funnel predictions")
    if st.button("Sign Out"): logout()
    with sqlite3.connect(DB_NAME) as con:
        users=con.execute("SELECT id,username,created_at FROM users WHERE role='user' ORDER BY id").fetchall()
        surveys=con.execute("""SELECT s.id,u.username,s.timestamp,s.stage,s.responses,s.scores
                               FROM surveys s JOIN users u ON s.user_id=u.id ORDER BY s.id DESC""").fetchall()
    counts={s:0 for s in STAGES}
    for s in surveys:
        if s[3] in counts: counts[s[3]]+=1
    top_stage=max(STAGES,key=lambda s:counts[s]) if surveys else "—"
    st.markdown('<div class="card">',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    a.metric("Total Users",len(users))
    b.metric("Total Surveys",len(surveys))
    c.metric("Most Recorded Stage",top_stage)
    st.write(" | ".join(f"{s}: {counts[s]}" for s in STAGES))
    st.markdown('</div>',unsafe_allow_html=True)
    st.subheader("Survey Results")
    chosen=st.selectbox("Filter by Stage",["All Stages"]+STAGES)
    rows=[]
    for s in surveys:
        if chosen!="All Stages" and s[3]!=chosen: continue
        rows.append({"User":s[1],"Survey":s[0],"Date":s[2].replace("T"," ")[:19],
                     "Predicted Stage":s[3]})
    st.dataframe(rows,use_container_width=True,hide_index=True)

setup_db()
init_state()

if st.session_state.user is None:
    register_page() if st.session_state.page=="register" else login_page()
else:
    if st.session_state.user["role"]=="admin":
        admin_page()
    elif st.session_state.page=="dashboard":
        dashboard_page()
    elif st.session_state.page=="survey":
        survey_page()
    elif st.session_state.page=="results":
        results_page()
    else:
        dashboard_page()
