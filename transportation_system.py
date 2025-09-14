import pandas as pd
import numpy as np
import os

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)


# ------------------ FILE PATHS ------------------
ROUTES_FILE = "routes.csv"
BOOKINGS_FILE = "bookings.csv"
USERS_FILE = "users.csv"

# ------------------ LOAD DATA ------------------
def load_data():
    if os.path.exists(ROUTES_FILE):
        routes = pd.read_csv(ROUTES_FILE)
    else:
        routes = pd.DataFrame(columns=["RouteID", "From", "To", "Price", "Seats"])
        routes.to_csv(ROUTES_FILE, index=False)

    if os.path.exists(BOOKINGS_FILE):
        bookings = pd.read_csv(BOOKINGS_FILE)
    else:
        bookings = pd.DataFrame(columns=["BookingID", "ClientName", "RouteID", "SeatsBooked"])
        bookings.to_csv(BOOKINGS_FILE, index=False)

    if os.path.exists(USERS_FILE):
        users = pd.read_csv(USERS_FILE)
    else:
        users = pd.DataFrame(columns=["Username", "Password", "Role"])
        # Add default admin
        users.loc[len(users)] = ["adminkjk", "admin123", "admin"]
        users.to_csv(USERS_FILE, index=False)

    return routes, bookings, users


def save_data(routes, bookings, users):
    routes.to_csv(ROUTES_FILE, index=False)
    bookings.to_csv(BOOKINGS_FILE, index=False)
    users.to_csv(USERS_FILE, index=False)


# ------------------ ADMIN MENU ------------------
def admin_menu(routes, bookings, users):
    while True:
        print("\n#------PROJECT BY HASINI---------#\n")
        print("\n--- ADMIN MENU ---")
        print("1. View Routes")
        print("2. Add Route")
        print("3. Remove Route")
        print("4. View All Bookings")
        print("5. View All Users")
        print("6. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            print(routes if not routes.empty else "No routes available.")
        elif choice == "2":
            rid = int(input("Enter new Route ID: "))
            frm = input("From: ")
            to = input("To: ")
            price = float(input("Price: "))
            seats = int(input("Seats: "))
            routes.loc[len(routes)] = [rid, frm, to, price, seats]
            print("✅ Route Added Successfully!")
        elif choice == "3":
            rid = int(input("Enter Route ID to remove: "))
            routes = routes[routes["RouteID"] != rid]
            print("✅ Route Removed Successfully!")
        elif choice == "4":
            print(bookings if not bookings.empty else "No bookings yet.")
        elif choice == "5":
            print(users)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

        save_data(routes, bookings, users)
    return routes, bookings, users


# ------------------ CLIENT MENU ------------------
def client_menu(username, routes, bookings, users):
    while True:
        print("\n#------PROJECT BY HASINI---------#\n")
        print(f"\n--- CLIENT MENU ({username}) ---")
        print("1. View Routes")
        print("2. Search Route by City")
        print("3. Sort Routes by Price")
        print("4. Book Ticket")
        print("5. Cancel Booking")
        print("6. View My Bookings")
        print("7. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            print(routes if not routes.empty else "No routes available.")
        elif choice == "2":
            city = input("Enter city name: ")
            result = routes[(routes["From"].str.contains(city, case=False)) |
                            (routes["To"].str.contains(city, case=False))]
            print(result if not result.empty else "No routes found.")
        elif choice == "3":
            print(routes.sort_values("Price"))
        elif choice == "4":
            if routes.empty:
                print("No routes available!")
                continue
            print(routes)
            rid = int(input("Enter Route ID: "))
            seats = int(input("Enter seats to book: "))
            if rid in routes["RouteID"].values:
                available = routes.loc[routes["RouteID"] == rid, "Seats"].values[0]
                if seats <= available:
                    bid = np.random.randint(1000, 9999)
                    bookings.loc[len(bookings)] = [bid, username, rid, seats]
                    routes.loc[routes["RouteID"] == rid, "Seats"] -= seats
                    print(f"✅ Booking Successful! Booking ID: {bid}")
                else:
                    print("❌ Not enough seats.")
            else:
                print("❌ Invalid Route ID.")
        elif choice == "5":
            user_bookings = bookings[bookings["ClientName"] == username]
            print(user_bookings if not user_bookings.empty else "No bookings.")
            if not user_bookings.empty:
                bid = int(input("Enter Booking ID to cancel: "))
                if bid in bookings["BookingID"].values:
                    seats_back = bookings.loc[bookings["BookingID"] == bid, "SeatsBooked"].values[0]
                    rid = bookings.loc[bookings["BookingID"] == bid, "RouteID"].values[0]
                    routes.loc[routes["RouteID"] == rid, "Seats"] += seats_back
                    bookings = bookings[bookings["BookingID"] != bid]
                    print("✅ Booking Cancelled.")
                else:
                    print("❌ Invalid Booking ID.")
        elif choice == "6":
            user_bookings = bookings[bookings["ClientName"] == username]
            print(user_bookings if not user_bookings.empty else "No bookings yet.")
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

        save_data(routes, bookings, users)
    return routes, bookings, users


# ------------------ LOGIN / REGISTER ------------------
def login(users):
    print("\n#------PROJECT BY HASINI---------#\n")
    print("\n--- LOGIN ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    user = users[(users["Username"] == username) & (users["Password"] == password)]
    if not user.empty:
        return username, user["Role"].values[0]
    else:
        print("❌ Invalid credentials.")
        return None, None


def register(users):
    print("\n#------PROJECT BY HASINI---------#\n")
    print("\n--- REGISTER NEW CLIENT ---")
    username = input("Choose username: ")
    if username in users["Username"].values:
        print("❌ Username already exists.")
        return users
    password = input("Choose password: ")
    users.loc[len(users)] = [username, password, "client"]
    print("✅ Registration successful. You can now login.")
    save_data(routes, bookings, users)
    return users


# ------------------ MAIN PROGRAM ------------------
if __name__ == "__main__":
    routes, bookings, users = load_data()

    while True:
        print("\n#------PROJECT BY HASINI---------#\n")
        print("\n===== TRANSPORTATION SYSTEM =====")
        print("1. Login")
        print("2. Register (Client Only)")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            uname, role = login(users)
            if role == "admin":
                routes, bookings, users = admin_menu(routes, bookings, users)
            elif role == "client":
                routes, bookings, users = client_menu(uname, routes, bookings, users)
        elif choice == "2":
            users = register(users)
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice.")
