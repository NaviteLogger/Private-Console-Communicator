import client_functions

if __name__ == "__main__":
    client_socket = client_functions.connect_to_server()

    print("Connected to the server.")

    while True:
        # After establishing a connection with the server, prompt the user with a menu
        print("Welcome to the Private Console Communicator!")
        print("Please select an option :")
        print("/start: Start a new conversation")
        print("/join: Join a conversation")
        print("/exit: Exit")
        option = input("> ")

        if option == "/start":
            # If the user selects option 1, start a new conversation
            print("Starting new conversation...")

        elif option == "/join":
            # If the user selects option 2, join an existing conversation
            print("Joining conversation...")

        elif option == "/exit":
            # If the user selects option 3, exit the program
            print("Exiting...")
            break
