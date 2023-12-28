import client_functions

if __name__ == "__main__":
    client_socket = client_functions.connect_to_server()

    print("Connected to the server.")

    while True:
        # After establishing a connection with the server, prompt the user with a menu
        print("Welcome to the Private Console Communicator!")