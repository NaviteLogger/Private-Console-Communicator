import client_functions

if __name__ == "__main__":
    client_socket = client_functions.connect_to_server()

    print("Connected to the server.")

    while True:
        # After establishing a connection with the server, prompt the user with a menu
        print("Welcome to the Private Console Communicator!")
        print("Please select an option:")
        print("1. Start a new conversation")
        print("2. Join a conversation")
        print("3. Exit")
        option = input("> ")

        if option == "1":
            # If the user selects option 1, start a new conversation
            print("Starting new conversation...")
