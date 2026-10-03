import streamlit as st
import base64
from pathlib import Path
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"],
        port=st.secrets["mysql"]["port"]
    )

def save_order(
    customer_name,
    phone,
    cake,
    quantity,
    delivery_date,
    address,
    message
):
    connection = get_connection()

    cursor = connection.cursor()

    query = """
        INSERT INTO orders
        (
            customer_name,
            phone,
            cake,
            quantity,
            delivery_date,
            address,
            message
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        customer_name,
        phone,
        cake,
        quantity,
        delivery_date,
        address,
        message
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()


def update_order_status(order_id, new_status):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE orders
        SET order_status = %s
        WHERE order_id = %s
    """

    cursor.execute(query, (new_status, order_id))
    connection.commit()

    cursor.close()
    connection.close()

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Homely Cakes",
    page_icon="🍰",
    layout="wide"
)


# =========================================================
# GLOBAL TEXT COLOR
# =========================================================
# =========================================================
# GLOBAL TEXT COLOR — WHITE
# =========================================================

st.markdown(
    """
    <style>

    /* All normal text */
    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #FFFFFF !important;
    }

    /* Navigation */
    [data-testid="stRadio"] label {
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton button {
        color: #FFFFFF !important;
    }

    /* Input labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label,
    .stDateInput label {
        color: #FFFFFF !important;
    }

    /* Selectbox text */
    [data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CAKE DATA
# =========================================================

cakes = [
    {
        "name": "Vanilla Cake",
        "description": "Soft and delicious vanilla cake for every occasion.",
        "price": 500,
        "emoji": "🍰"
    },
    {
        "name": "Strawberry Cake",
        "description": "Fresh strawberry flavor with creamy frosting.",
        "price": 500,
        "emoji": "🍓"
    },
    {
        "name": "Black Forest Cake",
        "description": "Chocolate cake with cream and cherries.",
        "price": 550,
        "emoji": "🍒"
    },
    {
        "name": "Chocolate Cake",
        "description": "Rich chocolate cake with creamy chocolate frosting.",
        "price": 600,
        "emoji": "🍫"
    }
]

cake_names = [cake["name"] for cake in cakes]


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

# Admin login status
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "selected_cake" not in st.session_state:
    st.session_state.selected_cake = "Vanilla Cake"


# =========================================================
# FUNCTIONS
# =========================================================

def select_cake(cake_name):
    """
    Select a cake and open the Order Cake page.
    """

    st.session_state.selected_cake = cake_name
    st.session_state.page = "Order Cake"


def set_home_background():
    """
    Set the uploaded bakery image as the
    Home page background.
    """

    image_path = Path("image_3.png")

    if not image_path.exists():

        st.warning(
            "Background image not found. "
            "Please check images/image2.png"
        )

        return


    # Read image
    image_data = base64.b64encode(
        image_path.read_bytes()
    ).decode()


    # Apply background
    st.markdown(
        f"""
        <style>

        .stApp {{

            background-image:
                url(
                    "data:image/png;base64,{image_data}"
                );

            background-size: cover;

            background-position: center center;

            background-repeat: no-repeat;

            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# NAVIGATION
# =========================================================

menu = st.radio(
    "Navigation",

    [
        "Home",
        "Our Cakes",
        "Order Cake",
        "Orders",
        "Contact Us"
    ],

    horizontal=True,

    index=[
        "Home",
        "Our Cakes",
        "Order Cake",
        "Orders",
        "Contact Us"
    ].index(st.session_state.page),

    label_visibility="collapsed"
)


st.session_state.page = menu


# =========================================================
# HOME PAGE
# =========================================================

if menu == "Home":

    # -----------------------------------------------------
    # HOME BACKGROUND
    # -----------------------------------------------------

    set_home_background()


    # -----------------------------------------------------
    # SPACE
    # -----------------------------------------------------

    st.write("")
    st.write("")
    st.write("")


    # -----------------------------------------------------
    # MAIN HOME CONTENT
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )


    with col2:

        st.title("🍰 Homely Cakes")


        st.subheader(
            "Freshly baked with love, just like home ❤️"
        )


        st.write("")


        st.write(
            """
            Welcome to Homely Cakes!

            Every cake is lovingly prepared with
            quality ingredients, care and the warmth
            of a homemade kitchen.

            From birthdays and anniversaries to
            simple moments of happiness, we make
            every celebration a little sweeter.
            """
        )


        st.write("")


        # -------------------------------------------------
        # HOME BUTTONS
        # -------------------------------------------------

        button1, button2 = st.columns(2)


        with button1:

            if st.button(
                "🎂 Explore Our Cakes",
                use_container_width=True
            ):

                st.session_state.page = "Our Cakes"

                st.rerun()


        with button2:

            if st.button(
                "🛒 Order Your Cake",
                use_container_width=True
            ):

                st.session_state.page = "Order Cake"

                st.rerun()


    # -----------------------------------------------------
    # HOME FEATURES
    # -----------------------------------------------------

    st.write("")
    st.write("")
    st.write("")


    st.subheader(
        "Why Choose Homely Cakes? ❤️"
    )


    feature1, feature2, feature3 = st.columns(3)


    with feature1:

        st.write("🥚")

        st.subheader(
            "Fresh Ingredients"
        )

        st.write(
            "Quality ingredients carefully chosen "
            "for every cake."
        )


    with feature2:

        st.write("❤️")

        st.subheader(
            "Made With Love"
        )

        st.write(
            "Every cake is prepared with the warmth "
            "and love of home."
        )


    with feature3:

        st.write("🎂")

        st.subheader(
            "Freshly Baked"
        )

        st.write(
            "Fresh cakes prepared specially for "
            "your celebration."
        )


# =========================================================
# OUR CAKES PAGE
# =========================================================

elif menu == "Our Cakes":

    st.title("🎂 Our Cakes")


    st.write(
        "Choose your favorite cake for your special occasion."
    )


    st.divider()


    # -----------------------------------------------------
    # VANILLA + STRAWBERRY
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        cake = cakes[0]


        st.subheader(
            f"{cake['emoji']} {cake['name']}"
        )


        st.write(
            cake["description"]
        )


        st.markdown(
            f"### ₹{cake['price']}"
        )


        if st.button(
            "🛒 Order Vanilla Cake",
            key="vanilla_button",
            use_container_width=True
        ):

            select_cake(cake["name"])

            st.rerun()


    with col2:

        cake = cakes[1]


        st.subheader(
            f"{cake['emoji']} {cake['name']}"
        )


        st.write(
            cake["description"]
        )


        st.markdown(
            f"### ₹{cake['price']}"
        )


        if st.button(
            "🛒 Order Strawberry Cake",
            key="strawberry_button",
            use_container_width=True
        ):

            select_cake(cake["name"])

            st.rerun()


    st.divider()


    # -----------------------------------------------------
    # BLACK FOREST + CHOCOLATE
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        cake = cakes[2]


        st.subheader(
            f"{cake['emoji']} {cake['name']}"
        )


        st.write(
            cake["description"]
        )


        st.markdown(
            f"### ₹{cake['price']}"
        )


        if st.button(
            "🛒 Order Black Forest Cake",
            key="blackforest_button",
            use_container_width=True
        ):

            select_cake(cake["name"])

            st.rerun()


    with col2:

        cake = cakes[3]


        st.subheader(
            f"{cake['emoji']} {cake['name']}"
        )


        st.write(
            cake["description"]
        )


        st.markdown(
            f"### ₹{cake['price']}"
        )


        if st.button(
            "🛒 Order Chocolate Cake",
            key="chocolate_button",
            use_container_width=True
        ):

            select_cake(cake["name"])

            st.rerun()


# =========================================================
# ORDER CAKE PAGE
# =========================================================

elif menu == "Order Cake":

    st.title("🛒 Order Your Cake")


    st.write(
        "Tell us what cake you would like for your special day."
    )


    st.divider()


    # -----------------------------------------------------
    # CUSTOMER INFORMATION
    # -----------------------------------------------------

    customer_name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )


    phone = st.text_input(
        "Phone Number",
        placeholder="Enter your phone number"
    )


    # -----------------------------------------------------
    # CAKE SELECTION
    # -----------------------------------------------------

    selected_index = cake_names.index(
        st.session_state.selected_cake
    )


    cake = st.selectbox(
        "Choose Cake",
        cake_names,
        index=selected_index
    )


    st.session_state.selected_cake = cake


    # -----------------------------------------------------
    # QUANTITY
    # -----------------------------------------------------

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        max_value=10,
        value=1
    )


    # -----------------------------------------------------
    # DELIVERY DATE
    # -----------------------------------------------------

    delivery_date = st.date_input(
        "Delivery Date"
    )


    # -----------------------------------------------------
    # ADDRESS
    # -----------------------------------------------------

    address = st.text_area(
        "Delivery Address",
        placeholder="Enter your complete delivery address"
    )


    # -----------------------------------------------------
    # SPECIAL INSTRUCTIONS
    # -----------------------------------------------------

    message = st.text_area(
        "Special Instructions",
        placeholder="Example: Happy Birthday Rahul 🎉"
    )


    st.write("")

# -----------------------------------------------------
# -----------------------------------------------------
# PLACE ORDER
# -----------------------------------------------------

    if st.button(
        "🎂 Place Order",
        use_container_width=True
    ):

        if customer_name and phone and address:

            try:

                save_order(
                    customer_name,
                    phone,
                    cake,
                    quantity,
                    delivery_date,
                    address,
                    message
                )

                st.success(
                    "🎉 Your order has been received and saved!"
                )

                st.subheader(
                    "📋 Order Details"
                )

                st.write(
                    f"**Customer:** {customer_name}"
                )

                st.write(
                    f"**Phone:** {phone}"
                )

                st.write(
                    f"**Cake:** {cake}"
                )

                st.write(
                    f"**Quantity:** {quantity}"
                )

                st.write(
                    f"**Delivery Date:** {delivery_date}"
                )

                st.write(
                    f"**Delivery Address:** {address}"
                )

                if message:

                    st.write(
                        f"**Special Instructions:** {message}"
                    )

            except mysql.connector.Error as error:

                st.error(
                    f"Could not save the order: {error}"
                )

        else:

            st.error(
                "Please enter your name, phone number "
                "and delivery address."
            )


# =========================================================
# ORDERS PAGE
# =========================================================

elif menu == "Orders":

    st.title("🔐 Admin Orders")

    if not st.session_state.admin_logged_in:

        st.write("Please login to view and manage customer orders.")

        admin_password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("🔓 Login", use_container_width=True):

            if admin_password == st.secrets["admin_password"]:

                st.session_state.admin_logged_in = True
                st.rerun()

            else:

                st.error("❌ Incorrect password.")

    else:

        st.success("✅ Admin logged in")

        if st.button("🔒 Logout", use_container_width=True):

            st.session_state.admin_logged_in = False
            st.rerun()

        st.divider()

        st.subheader("📋 Customer Orders")

        try:

            connection = get_connection()

            query = """
                SELECT
                    order_id,
                    customer_name,
                    phone,
                    cake,
                    quantity,
                    delivery_date,
                    address,
                    message,
                    order_status
                FROM orders
                ORDER BY order_id DESC
            """

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            order_data = cursor.fetchall()

            cursor.close()
            connection.close()

            if order_data:

                st.success(f"Total Orders: {len(order_data)}")

                statuses = [
                    "Pending",
                    "Confirmed",
                    "Preparing",
                    "Ready",
                    "Delivered",
                    "Cancelled"
                ]

                for order in order_data:

                    with st.expander(
                        f"Order #{order['order_id']} — {order['customer_name']} — {order['cake']}"
                    ):

                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(f"**Customer:** {order['customer_name']}")
                            st.write(f"**Phone:** {order['phone']}")
                            st.write(f"**Cake:** {order['cake']}")
                            st.write(f"**Quantity:** {order['quantity']}")
                            st.write(f"**Delivery Date:** {order['delivery_date']}")

                        with col2:
                            st.write(f"**Address:** {order['address']}")
                            if order['message']:
                                st.write(f"**Instructions:** {order['message']}")

                            current_status = order['order_status'] or "Pending"

                            if current_status not in statuses:
                                current_status = "Pending"

                            new_status = st.selectbox(
                                "Order Status",
                                statuses,
                                index=statuses.index(current_status),
                                key=f"status_{order['order_id']}"
                            )

                            if st.button(
                                "💾 Update Status",
                                key=f"update_{order['order_id']}",
                                use_container_width=True
                            ):

                                try:
                                    update_order_status(
                                        order['order_id'],
                                        new_status
                                    )
                                    st.success(
                                        f"Order #{order['order_id']} updated to {new_status}."
                                    )
                                    st.rerun()

                                except mysql.connector.Error as error:
                                    st.error(f"Could not update order: {error}")

            else:

                st.info("No orders have been received yet.")

        except mysql.connector.Error as error:

            st.error(f"Database error: {error}")


# =========================================================
# CONTACT US PAGE
# =========================================================

elif menu == "Contact Us":


    st.title("📞 Contact Us")


    st.write(
        "We would love to make your special occasion sweeter. ❤️"
    )


    st.divider()


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "🍰 Homely Cakes"
        )


        st.write(
            "📍 Vijayawada, India"
        )


        st.write(
            "📞 +91 94916 86082"
        )


        st.write(
            "📧 sweetcakes@example.com"
        )


    with col2:

        st.subheader(
            "🕐 Business Hours"
        )


        st.write(
            "Monday - Saturday: 9:00 AM - 8:00 PM"
        )


        st.write(
            "Sunday: 10:00 AM - 6:00 PM"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "🍰 Homely Cakes — Homemade with love, baked with care ❤️"
)
