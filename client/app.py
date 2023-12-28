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

            # Generate a unique string for the other user to join the conversation
            conversation_id = client_functions.generate_conversation_id(24)

            # Print back the conversation ID to the user
            print(f"Your conversation ID is {conversation_id}")
            print("Please share this ID with the person you want to have a conversation with.")

            # Generate an RSA key pair for the client
            private_key, serialized_public_key = client_functions.generate_key_pair_for_client()

        elif option == "/join":
            # If the user selects option 2, join an existing conversation
            print("Joining conversation...")

        elif option == "/exit":
            # If the user selects option 3, exit the program
            print("Exiting...")
            break
