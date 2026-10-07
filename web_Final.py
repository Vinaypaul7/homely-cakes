import streamlit as st
import base64
from datetime import date
from pathlib import Path
import mysql.connector


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Homely Cakes",
    page_icon="🍰",
    layout="wide"
)


# ============================================================
# PATHS  (relative to this file, so it works anywhere)
# ============================================================

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
BACKGROUND_IMAGE = BASE_DIR / "image_3.png"

# Width (in pixels) of each cake picture on the Our Cakes page.
# Smaller number = smaller picture (try 200, 250, 300, 350).
CAKE_IMAGE_WIDTH = 250

# Choices shown in the "Occasion" dropdown on the checkout form.
OCCASIONS = [
    "Birthday",
    "Anniversary",
    "Wedding",
    "Baby Shower",
    "Festival",
    "Farewell / Graduation",
    "Just Because",
    "Other"
]


# ============================================================
# HELPER: CLEAN HTML FOR st.markdown
# ============================================================
# Markdown turns indented lines and blank lines inside HTML
# into plain text / code blocks. This removes both problems,
# so the HTML always renders properly.

def html(block):
    lines = [line.strip() for line in block.splitlines()]
    return "\n".join(line for line in lines if line)


# ============================================================
# HELPER: FULL-WIDTH IMAGE (works on old and new Streamlit)
# ============================================================
# Newer Streamlit uses use_container_width, older versions use
# use_column_width. This tries one and falls back to the other.

def show_full_width_image(path):
    try:
        st.image(path, use_container_width=True)
    except TypeError:
        st.image(path, use_column_width=True)


# ============================================================
# DATABASE
# ============================================================
# Before running this version, add the new column once:
#
#   ALTER TABLE orders
#   ADD COLUMN occasion VARCHAR(100) NULL AFTER delivery_date;

def get_connection():
    try:
        return mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"]
        )
    except mysql.connector.Error as error:
        st.error(f"❌ Could not connect to the database: {error}")
        return None


# ============================================================
# CSS
# ============================================================

st.markdown(
    html(
        """
<style>

/* ---------- Dark base background (so white text is always readable) ---------- */
.stApp {
    background-color: #2b1a1f;
}

/* ---------- Text colour ---------- */
.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6,
[data-testid="stRadio"] label,
.stButton button,
[data-baseweb="select"] * {
    color: #FFFFFF !important;
}

/* ---------- Hero ---------- */
.hero {
    background: rgba(0, 0, 0, 0.55);
    border-radius: 24px;
    padding: 50px 30px;
    margin: 40px auto 30px auto;
    max-width: 900px;
    text-align: center;
}

.hero-title {
    font-size: 56px;
    font-weight: 800;
    margin-bottom: 10px;
    color: #FFFFFF;
}

.hero-subtitle {
    font-size: 24px;
    margin-bottom: 25px;
    color: #FFE3EC;
}

.hero-text {
    font-size: 18px;
    line-height: 1.8;
    color: #FFFFFF;
}

/* ---------- Story / Contact box ---------- */
.story-section {
    background: rgba(0, 0, 0, 0.55);
    border-radius: 24px;
    padding: 40px 35px;
    margin: 30px auto;
    max-width: 900px;
}

.story-title {
    font-size: 34px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 20px;
    color: #FFFFFF;
}

.story-text {
    font-size: 18px;
    line-height: 1.9;
    color: #FFFFFF;
}

/* ---------- Section title ---------- */
.section-title {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    margin: 25px 0 30px 0;
    color: #FFFFFF;
}

/* ---------- Cake cards ---------- */
.cake-card {
    background: rgba(0, 0, 0, 0.45);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 18px;
    padding: 0;
    border: 1px solid rgba(255,255,255,0.12);
}

.cake-card img {
    width: 100% !important;
    height: 260px !important;
    object-fit: cover !important;
    display: block;
    border-radius: 0 !important;
}

.cake-name {
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    margin-top: 12px;
    color: #FFFFFF;
}

.cake-price {
    font-size: 20px;
    font-weight: 800;
    text-align: center;
    margin-top: 4px;
    color: #FFD1DC;
}

.cake-size {
    font-size: 14px;
    text-align: center;
    margin-bottom: 12px;
    color: #DDDDDD;
}

.qty-number {
    text-align: center;
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
    padding-top: 5px;
}

.cart-box {
    background: rgba(0, 0, 0, 0.55);
    border-radius: 20px;
    padding: 22px;
    margin: 30px 0;
}

.cart-title {
    font-size: 28px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 12px;
}

.cart-item {
    color: #FFFFFF;
    font-size: 16px;
    margin: 7px 0;
}

/* ---------- Admin box ---------- */
.admin-box {
    background: rgba(0, 0, 0, 0.55);
    border-radius: 20px;
    padding: 30px;
    margin: 20px auto;
    max-width: 700px;
    text-align: center;
}

.admin-title {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 12px;
    color: #FFFFFF;
}

.admin-text {
    font-size: 17px;
    line-height: 1.7;
    color: #FFFFFF;
}

/* ---------- Footer ---------- */
.footer {
    background: rgba(0, 0, 0, 0.55);
    border-radius: 20px;
    padding: 25px;
    margin-top: 50px;
    text-align: center;
}

.footer h3,
.footer p {
    color: #FFFFFF !important;
}

/* ---------- Mobile ---------- */
@media (max-width: 768px) {
    .hero-title { font-size: 38px; }
    .hero-subtitle { font-size: 19px; }
    .hero-text, .story-text { font-size: 16px; }
    .section-title { font-size: 30px; }
}

</style>
"""
    ),
    unsafe_allow_html=True
)


# ============================================================
# BACKGROUND (HOME PAGE)
# ============================================================

def set_home_background():

    if not BACKGROUND_IMAGE.exists():
        st.warning(
            "Background image not found. "
            "Please keep image_3.png next to web_Final.py"
        )
        return

    image_data = base64.b64encode(
        BACKGROUND_IMAGE.read_bytes()
    ).decode()

    st.markdown(
        f"""
<style>
.stApp {{
    background-image: url("data:image/png;base64,{image_data}");
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: scroll;
}}
</style>
""",
        unsafe_allow_html=True
    )


# ============================================================
# CAKE DATA
# ============================================================

def find_image(name):
    """
    Look for images/<name>.png, .jpg, .jpeg or .webp
    (any capital letters in the extension also work).
    Returns the path if found, otherwise a path that
    does not exist (the page then shows a 🎂 placeholder).
    """

    for file in IMAGE_DIR.glob(f"{name}.*"):

        if file.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
            return file

    return IMAGE_DIR / f"{name}.png"


# Change only the file name (without extension) on the "image" line
# if your pictures have different names.

cakes = [

    {
        "name": "Vanilla Cake",
        "price": 500,
        "image": find_image("vanilla")
    },

    {
        "name": "Strawberry Cake",
        "price": 500,
        "image": find_image("strawberry")
    },

    {
        "name": "Black Forest Cake",
        "price": 550,
        "image": find_image("black_forest")
    },

    {
        "name": "Chocolate Cake",
        "price": 600,
        "image": find_image("chocolate")
    },

    {
        "name": "Butterscotch Cake",
        "price": 550,
        "image": find_image("butterscotch")
    }

]


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "cart" not in st.session_state:
    st.session_state.cart = {}

# True while the customer-details form is open on the Cart page
if "checkout" not in st.session_state:
    st.session_state.checkout = False

# True for one run after an order is saved (to show the success message)
if "order_placed" not in st.session_state:
    st.session_state.order_placed = False


# ============================================================
# NAVIGATION
# ============================================================

PAGES = [
    "Home",
    "Our Cakes",
    "Cart",
    "Orders",
    "Contact Us"
]

# Safety: if the saved page no longer exists, go back to Home
if st.session_state.page not in PAGES:
    st.session_state.page = "Home"

selected_page = st.radio(
    "Navigation",
    PAGES,
    horizontal=True,
    index=PAGES.index(st.session_state.page),
    label_visibility="collapsed"
)

st.session_state.page = selected_page


# ============================================================
# HOME
# ============================================================

if st.session_state.page == "Home":

    set_home_background()

    st.markdown(
        html(
            """
<div class="hero">
<div class="hero-title">🍰 Homely Cakes</div>
<div class="hero-subtitle">Freshly baked with love, just like home ❤️</div>
<div class="hero-text">
<strong>Welcome to Homely Cakes!</strong>
<br><br>
Every cake is lovingly prepared with
quality ingredients, care and the warmth
of a homemade kitchen.
<br><br>
🎉 Birthdays &nbsp; • &nbsp;
💍 Anniversaries &nbsp; • &nbsp;
❤️ Special Moments
<br><br>
We make every celebration a little sweeter.
</div>
</div>
"""
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        html(
            """
<div class="story-section">
<div class="story-title">❤️ Our Story</div>
<div class="story-text">
Homely Cakes began with a simple love for
baking and a mother's care for her family.
<br><br>
Coming from a middle-class family, she started
baking cakes at home for her children.
What began as a small family tradition slowly
became something she truly loved.
<br><br>
She spent time learning, practicing and
improving her baking skills. Every recipe,
every cake and every mistake taught her
something new.
<br><br>
For her, making a cake was never only about
how it looked or tasted. She wanted every cake
to be prepared with the same care, cleanliness
and attention she would give when making food
for her own children.
<br><br>
That belief became the heart of
<strong>Homely Cakes</strong>.
<br><br>
Today, every cake is made with the feeling
of home — with care, quality ingredients,
cleanliness and lots of love.
<br><br>
<strong>
Because every customer deserves a cake
made with the same care as one made
for family. ❤️
</strong>
</div>
</div>
"""
        ),
        unsafe_allow_html=True
    )


# ============================================================
# OUR CAKES
# ============================================================

elif st.session_state.page == "Our Cakes":

    st.markdown(
        html(
            """
<div class="section-title">🎂 Our Cakes</div>
"""
        ),
        unsafe_allow_html=True
    )

    # Three cakes in one row
    columns = st.columns(3)

    for index, cake in enumerate(cakes):

        with columns[index % 3]:

            cake_name = cake["name"]
            current_quantity = st.session_state.cart.get(cake_name, 0)

            st.markdown(
                '<div class="cake-card">',
                unsafe_allow_html=True
            )

            # Cake picture — fills the card width with no extra padding
            if cake["image"].exists():

                show_full_width_image(str(cake["image"]))

            else:

                st.markdown(
                    html(
                        """
<div style="
    height:260px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:70px;
">
    🎂
</div>
"""
                    ),
                    unsafe_allow_html=True
                )

            st.markdown(
                html(
                    f"""
<div class="cake-name">{cake["name"]}</div>
<div class="cake-price">₹{cake["price"]}</div>
<div class="cake-size">Approx. 1 KG</div>
"""
                ),
                unsafe_allow_html=True
            )

            # Quantity controls
            q1, q2, q3 = st.columns([1, 1, 1])

            with q1:
                if st.button(
                    "−",
                    key=f"minus_{index}",
                    use_container_width=True
                ):
                    if current_quantity > 1:
                        st.session_state.cart[cake_name] = current_quantity - 1
                    elif current_quantity == 1:
                        del st.session_state.cart[cake_name]

                    st.rerun()

            with q2:
                st.markdown(
                    f'<div class="qty-number">{current_quantity}</div>',
                    unsafe_allow_html=True
                )

            with q3:
                if st.button(
                    "+",
                    key=f"plus_{index}",
                    use_container_width=True
                ):
                    st.session_state.cart[cake_name] = current_quantity + 1
                    st.rerun()

            # Add to cart
            if st.button(
                "🛒 Add to Cart",
                key=f"add_cart_{index}",
                use_container_width=True
            ):

                if current_quantity == 0:
                    st.session_state.cart[cake_name] = 1

                st.success(f"{cake_name} added to cart!")

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    # Cart summary
    st.markdown(
        """
<div class="cart-box">
<div class="cart-title">🛒 Your Cart</div>
""",
        unsafe_allow_html=True
    )

    if not st.session_state.cart:

        st.markdown(
            '<div class="cart-item">Your cart is empty.</div>',
            unsafe_allow_html=True
        )

    else:

        total = 0

        for cake in cakes:

            quantity = st.session_state.cart.get(
                cake["name"],
                0
            )

            if quantity > 0:

                item_total = cake["price"] * quantity
                total += item_total

                st.markdown(
                    f"""
<div class="cart-item">
    <strong>{cake["name"]}</strong>
    × {quantity}
    — ₹{item_total}
</div>
""",
                    unsafe_allow_html=True
                )

        st.markdown(
            f"""
<div class="cart-item" style="
    font-size:20px;
    font-weight:800;
    margin-top:15px;
">
    Total: ₹{total}
</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            "🗑️ Clear Cart",
            use_container_width=True
        ):

            st.session_state.cart = {}
            st.session_state.checkout = False
            st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    # Go to Cart button
    if st.button(
        "🛒 Go to Cart",
        use_container_width=True
    ):
        st.session_state.page = "Cart"
        st.rerun()


# ============================================================
# CART  (with Place Order + customer details)
# ============================================================

elif st.session_state.page == "Cart":

    st.markdown(
        html(
            """
<div class="section-title">🛒 Your Cart</div>
"""
        ),
        unsafe_allow_html=True
    )

    # Shown once after a successful order
    if st.session_state.order_placed:

        st.success(
            "🎉 Your order has been placed successfully! "
            "We will contact you shortly."
        )

        st.session_state.order_placed = False

    if not st.session_state.cart:

        st.info("Your cart is empty. Please add a cake from Our Cakes.")

        if st.button(
            "🎂 Go to Our Cakes",
            use_container_width=True
        ):
            st.session_state.page = "Our Cakes"
            st.rerun()

    else:

        total = 0

        for index, cake in enumerate(cakes):

            quantity = st.session_state.cart.get(
                cake["name"],
                0
            )

            if quantity <= 0:
                continue

            item_total = cake["price"] * quantity
            total += item_total

            col1, col2, col3, col4 = st.columns([1.2, 2.5, 1.5, 1.5])

            with col1:

                if cake["image"].exists():

                    st.image(
                        str(cake["image"]),
                        width=100
                    )

                else:

                    st.write("🎂")

            with col2:

                st.write(f"**{cake['name']}**")
                st.write(f"₹{cake['price']} × {quantity}")

            with col3:

                q1, q2, q3 = st.columns([1, 1, 1])

                with q1:

                    if st.button(
                        "−",
                        key=f"cart_minus_{index}"
                    ):

                        if quantity > 1:
                            st.session_state.cart[cake["name"]] = quantity - 1
                        else:
                            del st.session_state.cart[cake["name"]]

                        st.rerun()

                with q2:

                    st.write(
                        f"**{quantity}**"
                    )

                with q3:

                    if st.button(
                        "+",
                        key=f"cart_plus_{index}"
                    ):

                        st.session_state.cart[cake["name"]] = quantity + 1
                        st.rerun()

            with col4:

                st.write(
                    f"**₹{item_total}**"
                )

            st.divider()

        st.markdown(
            f"""
<div class="cart-box">
<div class="cart-title">Order Total: ₹{total}</div>
</div>
""",
            unsafe_allow_html=True
        )

        cart_col1, cart_col2, cart_col3 = st.columns(3)

        with cart_col1:

            if st.button(
                "🎂 Continue Shopping",
                use_container_width=True
            ):
                st.session_state.checkout = False
                st.session_state.page = "Our Cakes"
                st.rerun()

        with cart_col2:

            if st.button(
                "🗑️ Clear Cart",
                use_container_width=True
            ):
                st.session_state.cart = {}
                st.session_state.checkout = False
                st.rerun()

        with cart_col3:

            if st.button(
                "✅ Place Order",
                use_container_width=True
            ):
                st.session_state.checkout = True
                st.rerun()

        # ----------------------------------------------------
        # Customer details (appears after clicking Place Order)
        # ----------------------------------------------------

        if st.session_state.checkout:

            st.markdown(
                html(
                    """
<div class="section-title">📝 Your Details</div>
"""
                ),
                unsafe_allow_html=True
            )

            with st.form("checkout_form"):

                customer_name = st.text_input("Customer Name")

                phone = st.text_input("Phone Number")

                delivery_date = st.date_input(
                    "Delivery Date",
                    min_value=date.today()
                )

                occasion = st.selectbox(
                    "Occasion",
                    OCCASIONS
                )

                other_occasion = st.text_input(
                    "If Other, please specify",
                    placeholder="e.g. Housewarming"
                )

                address = st.text_area("Delivery Address")

                message = st.text_area(
                    "Additional Message",
                    placeholder="Any special instructions?"
                )

                confirm = st.form_submit_button("🍰 Confirm Order")

            if st.button("← Back", key="checkout_back"):
                st.session_state.checkout = False
                st.rerun()

            if confirm:

                if not customer_name.strip():

                    st.error("Please enter your name.")

                elif not phone.strip():

                    st.error("Please enter your phone number.")

                elif not address.strip():

                    st.error("Please enter your delivery address.")

                elif occasion == "Other" and not other_occasion.strip():

                    st.error("Please tell us the occasion.")

                else:

                    # Use the typed occasion when "Other" is chosen
                    final_occasion = (
                        other_occasion.strip()
                        if occasion == "Other"
                        else occasion
                    )

                    connection = get_connection()

                    if connection:

                        try:

                            cursor = connection.cursor()

                            query = """
                                INSERT INTO orders
                                (
                                    customer_name,
                                    phone,
                                    cake,
                                    quantity,
                                    delivery_date,
                                    occasion,
                                    address,
                                    message
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """

                            # One row per cake in the cart
                            for cake_name, qty in st.session_state.cart.items():

                                cursor.execute(
                                    query,
                                    (
                                        customer_name.strip(),
                                        phone.strip(),
                                        cake_name,
                                        qty,
                                        delivery_date,
                                        final_occasion,
                                        address.strip(),
                                        message.strip()
                                    )
                                )

                            connection.commit()

                            cursor.close()
                            connection.close()

                            st.session_state.cart = {}
                            st.session_state.checkout = False
                            st.session_state.order_placed = True
                            st.rerun()

                        except Exception as e:

                            st.error(f"❌ Could not place order: {e}")


# ============================================================
# ORDERS / ADMIN
# ============================================================

elif st.session_state.page == "Orders":

    st.markdown(
        html(
            """
<div class="section-title">🔐 Orders</div>
"""
        ),
        unsafe_allow_html=True
    )

    if not st.session_state.admin_logged_in:

        st.markdown(
            html(
                """
<div class="admin-box">
<div class="admin-title">🔐 Admin Access Only</div>
<div class="admin-text">
This section is exclusively for Homely Cakes administrators.
<br><br>
Please log in with your admin password
to view and manage customer orders.
</div>
</div>
"""
            ),
            unsafe_allow_html=True
        )

        admin_password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("🔓 Login", use_container_width=True):

            if admin_password == st.secrets["admin_password"]:

                st.session_state.admin_logged_in = True

                st.rerun()

            else:

                st.error("❌ Incorrect admin password.")

    else:

        st.success("✅ Admin logged in successfully.")

        if st.button("🚪 Logout"):

            st.session_state.admin_logged_in = False

            st.rerun()

        connection = get_connection()

        if connection:

            try:

                cursor = connection.cursor(dictionary=True)

                cursor.execute(
                    """
                    SELECT
                        order_id,
                        customer_name,
                        phone,
                        cake,
                        quantity,
                        delivery_date,
                        occasion,
                        address,
                        message,
                        order_status
                    FROM orders
                    ORDER BY order_id DESC
                    """
                )

                orders = cursor.fetchall()

                cursor.close()
                connection.close()

                if not orders:

                    st.info("📭 No customer orders yet.")

                else:

                    statuses = [
                        "Pending",
                        "Confirmed",
                        "Preparing",
                        "Out for Delivery",
                        "Delivered",
                        "Cancelled"
                    ]

                    for order in orders:

                        st.markdown("---")

                        st.subheader(f"🧾 Order #{order['order_id']}")

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(
                                f"**Customer:** {order['customer_name']}"
                            )

                            st.write(f"**Phone:** {order['phone']}")

                            st.write(f"**Cake:** {order['cake']}")

                            st.write(f"**Quantity:** {order['quantity']}")

                        with col2:

                            st.write(
                                f"**Delivery Date:** {order['delivery_date']}"
                            )

                            st.write(
                                f"**Occasion:** "
                                f"{order['occasion'] or 'Not specified'}"
                            )

                            st.write(f"**Address:** {order['address']}")

                            st.write(
                                f"**Message:** {order['message'] or 'None'}"
                            )

                        current_status = order["order_status"]

                        if current_status not in statuses:

                            current_status = "Pending"

                        new_status = st.selectbox(
                            "Order Status",
                            statuses,
                            index=statuses.index(current_status),
                            key=f"status_{order['order_id']}"
                        )

                        if new_status != current_status:

                            if st.button(
                                "Update Status",
                                key=f"update_{order['order_id']}"
                            ):

                                connection = get_connection()

                                if connection:

                                    try:

                                        cursor = connection.cursor()

                                        cursor.execute(
                                            """
                                            UPDATE orders
                                            SET order_status = %s
                                            WHERE order_id = %s
                                            """,
                                            (
                                                new_status,
                                                order["order_id"]
                                            )
                                        )

                                        connection.commit()

                                        cursor.close()
                                        connection.close()

                                        st.success(
                                            "✅ Order status updated."
                                        )

                                        st.rerun()

                                    except Exception as e:

                                        st.error(
                                            f"❌ Could not update order: {e}"
                                        )

            except Exception as e:

                st.error(f"❌ Could not load orders: {e}")


# ============================================================
# CONTACT US
# ============================================================

elif st.session_state.page == "Contact Us":

    st.markdown(
        html(
            """
<div class="section-title">📞 Contact Us</div>
"""
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        html(
            """
<div class="story-section">
<div class="story-title">🍰 Homely Cakes</div>
<div class="story-text">
<strong>📍 Location:</strong> Vijayawada, India
<br><br>
<strong>📞 Phone:</strong> +91 94916 86082
<br><br>
<strong>📧 Email:</strong> palanisamuelmanojdeee054@gmail.com
<br><br>
<strong>🕘 Opening Hours:</strong>
<br>
Monday - Saturday: 9:00 AM - 8:00 PM
<br>
Sunday: 10:00 AM - 6:00 PM
</div>
</div>
"""
        ),
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    html(
        """
<div class="footer">
<h3>Made With Love ❤️</h3>
<p>Delicious cakes for every special moment.</p>
<p>© 2026 Homely Cakes. All rights reserved.</p>
</div>
"""
    ),
    unsafe_allow_html=True
)