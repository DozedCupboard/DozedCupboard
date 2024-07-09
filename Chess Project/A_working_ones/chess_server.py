import socket
import threading
import random
import time

class Chess_Server:
    def __init__(self, host, port):
        """
        Initialize the Chess_Server class with host and port.
        Args:
            host (str): IP address or hostname.
            port (int): Port number to listen on.
        Variables:
            self.clients: List of people connected to the server
                used to send message to the correct people.
            self.LISTENER_LIMIT: Maximum number of people that can be connected
                at one time     
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.LISTENER_LIMIT = 2


    def handle_client(self, conn, player):
        """
        Handle communication with each client in a separate thread.
        Args:
            conn (socket): Connection object for the client.
            player (int): Player number (1 or 2).
        """
        try:
            while True:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                print(f"Received data from Player {player}: {data}")
                # Process received data (e.g., handle move)
                # Send updated game state to other player
                other_player = 1 if player == 2 else 2
                other_conn = self.clients[other_player - 1]
                other_conn.sendall(data.encode("utf-8"))
            conn.close()

        except Exception as e:
            print(f"Player {player} disconnected.")
            if len(self.clients) != 0:
                self.clients.remove(conn)
            if len(self.clients) == 1:
                remaining_player_conn = self.clients[0]
                remaining_player_conn.sendall("Your opponent has disconnected. Game ended.".encode("utf-8"))
                remaining_player_conn.close()
                self.clients.remove(remaining_player_conn)
                print(" Opponent disconnected. Game ended.")
   


    def start(self):
        """
        Start the server and handle connections from players.
        """
        
        self.server_socket.bind(("", self.port))
        self.server_socket.listen(self.LISTENER_LIMIT)  # Listen for two players # set at init
        print("Server started. Waiting for players...")
        while len(self.clients) < 2:
            conn, addr = self.server_socket.accept()
            print(f"Player {len(self.clients) + 1} connected: {addr}")
            self.clients.append(conn)
            threading.Thread(target=self.handle_client, args=(conn, len(self.clients),)).start()

        print("All players connected. Game started.")

        starting_player = "White"  # Choose starting player
        self.current_turn = starting_player # Starting player is there turn
        for idx, client in enumerate(self.clients):
            player_role = "White" if idx == 0 else "Black"  # Assign roles to players
            # Two messages, 1 message for each player
            client.sendall(f"Starting player:{starting_player},Your role:{player_role}".encode("utf-8"))


if __name__ == '__main__':
    server = Chess_Server("0.0.0.0", 5000)
    server.start()




#server = Chess_Server("127.0.0.1", 5000)