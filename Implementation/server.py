import socket
import threading
from User import User
from Admin import Admin
from Chef import Chef
from Employee import Employee
from Cafeteria import Menu
from Validation import Validation
from Database import connect_to_db
from notification import get_notifications

def check_user_id_exists(user_id):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        return bool(user)
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def handle_client(client_socket):
    user = None
    menu = Menu()

    print("Client connected")

    while True:
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if not data:
                break

            print(f"Received command: {data}")
            command, *params = data.split(',')

            if command == 'login':
                user_id, user_password = params
                user = User.login(user_id, user_password)

                if user:
                    response = f"login_success,{user.user_id},{user.user_name},{user.user_role}"
                else:
                    response = "login_failed,Invalid user ID or password."

            elif command == 'get_notifications':
                if user:
                    notifications = get_notifications(user.user_id)
                    response = '\n'.join(notifications) if notifications else "No new notifications."
                else:
                    response = "You need to log in first."

            elif user:
                if user.user_role == 'Admin':
                    admin = Admin(user.user_id, user.user_name)
                    response = handle_admin_commands(admin, command, params, menu)

                elif user.user_role == 'Chef':
                    chef = Chef(user.user_id, user.user_name)
                    response = handle_chef_commands(chef, command, params)

                elif user.user_role == 'Employee':
                    employee = Employee(user.user_id, user.user_name)
                    response = handle_employee_commands(employee, command, params, menu)
            else:
                response = "You need to log in first."

            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            response = f"An error occurred: {e}"
            print(response)
            client_socket.send(response.encode('utf-8'))

    client_socket.close()

def handle_admin_commands(admin, command, params, menu):
    print(f"Handling admin command: {command} with params: {params}")
    try:
        if command == 'register_user':
            if len(params) < 4:
                return "error,Not enough parameters for register_user"

            user_id, user_name, user_password, role_choice = params
            if check_user_id_exists(user_id):
                return "error,User ID already exists. Please enter a different ID."

            user_role = ['Admin', 'Chef', 'Employee'][int(role_choice) - 1]
            User.register(user_id, user_name, user_role, user_password)
            return "Registration successful."

        elif command == 'add_menu_item':
            if len(params) < 3:
                return "error,Not enough parameters for add_menu_item"

            name, price, availability = params
            admin.add_menu_item(name, float(price), int(availability))
            return "Food item added successfully."

        elif command == 'update_menu_item':
            if len(params) < 4:
                return "error,Not enough parameters for update_menu_item"

            item_name, item_new_name, price, availability = params
            response = admin.update_menu_item(item_name, item_new_name, float(price), int(availability))
            return response

        elif command == 'delete_menu_item':
            if len(params) < 1:
                return "error,Not enough parameters for delete_menu_item"

            item_name = params[0]
            response = admin.delete_menu_item(item_name)
            return response

        elif command == 'display_menu_items':
            return menu.display_menu_items()

        else:
            return "Invalid admin command."
    except ValueError:
        return "Invalid input. Please check your parameters."
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def handle_chef_commands(chef, command, params):
    print(f"Handling chef command: {command} with params: {params}")
    try:
        if command == 'recommend_menu_items':
            if len(params) < 2:
                return "error,Not enough parameters for recommend_menu_items"

            meal_type, number_of_items, *item_ids = params
            item_ids = list(map(int, item_ids))
            chef.recommend_menu_items(meal_type, int(number_of_items), item_ids)
            return "Menu items recommended successfully."

        elif command == 'generate_monthly_feedback_report':
            return chef.generate_monthly_feedback_report()

        elif command == 'get_recommendations_from_feedback':
            return chef.get_recommendations_from_feedback()

        elif command == 'display_menu_items':
            menu = Menu()
            return menu.display_menu_items()

        elif command == 'logout':
            return "logout_success"

        else:
            return "Invalid chef command."
    except ValueError:
        return "Invalid input. Please check your parameters."
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def handle_employee_commands(employee, command, params, menu):
    print(f"Handling employee command: {command} with params: {params}")
    try:
        if command == 'provide_feedback':
            if len(params) < 3:
                return "error,Not enough parameters for provide_feedback"

            item_id, comment, rating = params
            response = employee.provide_feedback(int(item_id), comment, float(rating))
            return response

        elif command == 'select_preference':
            if len(params) < 1:
                return "error,Not enough parameters for select_preference"

            item_id = params[0]
            response = employee.select_preference(int(item_id))
            return response

        elif command == 'display_menu_items':
            return menu.display_menu_items()

        elif command == 'display_recommended_menu':
            return menu.display_recommended_menu()
        
        elif command == 'order_food_item':
            if len(params) < 2:
                return "error,Not enough parameters for order_food_item"

            item_id, quantity = params
            response = employee.order_food_item(int(item_id), int(quantity))
            return response

        elif command == 'display_ordered_items':
            return employee.display_ordered_items()

        elif command == 'logout':
            return "logout_success"

        else:
            return "Invalid employee command."
    except ValueError:
        return "Invalid input. Please check your parameters."
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
