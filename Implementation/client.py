import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    while True:
        print("Welcome to the Cafeteria Recommendation Engine")
        print("1. Login")
        choice = input("Enter your choice: ")

        if choice == '1':
            user_id = input("Enter your user ID: ")
            user_password = input("Enter password: ")
            client.send(f"login,{user_id},{user_password}".encode('utf-8'))
            response = client.recv(4096).decode('utf-8')
            response_parts = response.split(',')
            if response_parts[0] == 'login_success':
                user_id, user_name, user_role = response_parts[1:]
                print(f"Welcome, {user_name}. You are logged in as {user_role}.")
                handle_user_menu(client, user_role)
            else:
                print(response_parts[1])
        else:
            print("Invalid choice. Please try again.")

def handle_user_menu(client, user_role):
    while True:
        if user_role == 'Admin':
            display_admin_menu()
        elif user_role == 'Chef':
            display_chef_menu()
        elif user_role == 'Employee':
            display_employee_menu()

        check_notifications(client)

        choice = input("Enter your choice: ")
        if choice not in ['1', '2', '3', '4', '5','6', '7']:
            break

        command = translate_choice_to_command(user_role, choice)
        if command:
            client.send(command.encode('utf-8'))
            response = client.recv(4096).decode('utf-8')
            print(f"{response}")

            if response == "logout_success":
                print("Logged out successfully.")
                break

            if user_role == 'Chef' and choice == '1':
                meal_type = input("Enter meal type (Breakfast, Lunch, Dinner): ")
                number_of_items = input("Enter the number of items to recommend: ")
                item_ids = input("Enter food item IDs to recommend (comma-separated): ")
                command = f"recommend_menu_items,{meal_type},{number_of_items},{item_ids.replace(' ', '')}"
                client.send(command.encode('utf-8'))
                response = client.recv(4096).decode('utf-8')
                print(f"{response}")

            if user_role == 'Employee' and choice == '2':
                client.send("display_ordered_items".encode('utf-8'))
                response = client.recv(4096).decode('utf-8')

                item_id = input("Enter the ID of the food item you want to give feedback on: ")
                comment = input("Enter your comment: ")
                rating = input("Enter your rating (1-5): ")
                command = f"provide_feedback,{item_id},{comment},{rating}"
                client.send(command.encode('utf-8'))
                response = client.recv(4096).decode('utf-8')
                print(f"{response}")

            if user_role == 'Employee' and choice == '3':
                client.send("display_menu_items".encode('utf-8'))
                response = client.recv(4096).decode('utf-8')

                item_id = input("Enter the ID of the food item you want to select as preference: ")
                command = f"select_preference,{item_id}"
                client.send(command.encode('utf-8'))
                response = client.recv(4096).decode('utf-8')
                print(f"{response}")

            if user_role == 'Employee' and choice == '4':
                item_id = input("Enter the ID of the food item you want to order: ")
                quantity = input("Enter the quantity: ")
                command = f"order_food_item,{item_id},{quantity}"
                client.send(command.encode('utf-8'))
                response = client.recv(4096).decode('utf-8')
                print(f"{response}")

            if user_role == 'Chef' and choice == '6':
                client.send("view_discard_menu_item_list".encode('utf-8'))
                response = client.recv(4096).decode('utf-8')
                if response.startswith("Low rated items:"):
                    delete_choice = input()
                    if delete_choice.lower() == "yes":
                        item_id = input("Enter the ID of the food item you want to delete: ")
                        client.send(f"delete_menu_item,{item_id}".encode('utf-8'))
                        delete_response = client.recv(4096).decode('utf-8')
                        print(f"\n{delete_response}")

def handle_view_discard_menu_item_list(client):
    client.send("view_discard_menu_item_list".encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    if response.startswith("Low rated items:"):
        print(response)
        delete_choice = input("Do you want to delete these items? (yes/no): ")
        if delete_choice.lower() == "yes":
            item_id = input("Enter the ID of the food item you want to delete: ")
            client.send(f"delete_menu_item,{item_id}".encode('utf-8'))
            delete_response = client.recv(4096).decode('utf-8')
            return delete_response
    return response


def check_notifications(client):
    client.send("get_notifications".encode('utf-8'))
    response = client.recv(4096).decode('utf-8')
    if response != "No new notifications.":
        print("\n--- New Notifications ---")
        print(response)
        print("------------------------\n")

def translate_choice_to_command(user_role, choice):
    if user_role == 'Admin':
        commands = {
            '1': 'register_user',
            '2': 'add_menu_item',
            '3': 'update_menu_item',
            '4': 'delete_menu_item',
            '5': 'display_menu_items',
            '6': 'logout'
        }
        if choice == '1':
            user_id = input("Enter new user's ID: ")
            user_name = input("Enter new user's name: ")
            user_password = input("Enter new user's password: ")
            print("Select role for the new user:")
            print("1. Admin  2. Chef  3. Employee")
            role_choice = input("Enter the number corresponding to the role: ")
            return f"register_user,{user_id},{user_name},{user_password},{role_choice}"
        elif choice == '2':
            name = input("Enter food item name: ")
            price = input("Enter food item price: ")
            availability = input("Enter food item availability (1 for available, 0 for not available): ")
            return f"add_menu_item,{name},{price},{availability}"
        elif choice == '3':
            item_name = input("Enter food item name to update: ")
            item_new_name = input("Enter new food item name: ")
            price = input("Enter food item price: ")
            availability = input("Enter food item availability (1 for available, 0 for not available): ")
            return f"update_menu_item,{item_name},{item_new_name},{price},{availability}"
        elif choice == '4':
            item_name = input("Enter the item name to delete: ")
            return f"delete_menu_item,{item_name}"
        elif choice == '5':
            return "display_menu_items"
        elif choice == '6':
            return "logout"

    elif user_role == 'Chef':
        commands = {
            '1': 'recommend_menu_items',
            '2': 'generate_monthly_feedback_report',
            '3': 'display_menu_items',
            '4': 'get_recommendations_from_feedback',
            '5': 'display_ordered_items',
            '6': 'view_discard_menu_item_list',
            '7': 'logout'
        }
        if choice == '1':
            return "get_recommendations_from_feedback"
        elif choice == '2':
            return "generate_monthly_feedback_report"
        elif choice == '3':
            return "display_menu_items"
        elif choice == '4':
            return "get_recommendations_from_feedback"
        elif choice == '5':
            return "display_ordered_items"
        elif choice == '6':
            return "view_discard_menu_item_list"
        elif choice == '7':
            return "logout"

    elif user_role == 'Employee':
        commands = {
            '1': 'display_recommended_menu',
            '2': 'provide_feedback',
            '3': 'select_preference',
            '4': 'order_food_item',
            '5': 'logout'
        }
        if choice == '1':
            return "display_recommended_menu"
        elif choice == '2':
            return "display_ordered_items"
        elif choice == '3':
            return "display_menu_items"
        elif choice == '4':
            return "display_recommended_menu"
        elif choice == '5':
            return "logout"
    return None

def display_admin_menu():
    print("\nAdmin Menu:")
    print("1. Register New User")
    print("2. Add Food Item")
    print("3. Update Food Item")
    print("4. Delete Food Item")
    print("5. Show available food items")
    print("6. Logout")

def display_chef_menu():
    print("\nChef Menu:")
    print("1. Recommend Menu Items")
    print("2. Generate Monthly Feedback Report")
    print("3. Show available food items")
    print("4. Get Recommendations from Feedback")
    print("5. View Ordered Items")
    print("6. View Discard Menu Item List")
    print("7. Logout")

def display_employee_menu():
    print("\nEmployee Menu:")
    print("1. Show available food items")
    print("2. Provide Feedback")
    print("3. Select Preference")
    print("4. Order Food")
    print("5. Logout")

if __name__ == "__main__":
    main()
