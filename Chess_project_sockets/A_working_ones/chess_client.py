# Chess Project with AI and Sockets.

import sys
import chess # ONLY FOR OPENINGS, FOR CONVERSION
import subprocess
import time
import random
import copy
import customtkinter as ctk, customtkinter
from tkinter import messagebox
import csv

import tkinter as tk 
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk

import socket
import threading


customtkinter.set_appearance_mode("light") # or dark.
customtkinter.set_default_color_theme("dark-blue")



class HomePage(tk.Frame):
    """
    Home page of the chess application.
    """
    def __init__(self, master=None):
        """
        Initialize the home page.

        The function self.create_widgets is called
            it creates GUI widgets such as buttons.
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Create widgets for the home page.
        """
        self.label = ctk.CTkLabel(self, text="Home Page", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.button1 = ctk.CTkButton(self, text="Settings", command=self.show_Settings_Page)
        self.button1.pack(pady=5)

        self.button2 = ctk.CTkButton(self, text="Chess game", command=self.show_Chess_Game_Page)
        self.button2.pack(pady=5)

        self.button1 = ctk.CTkButton(self, text="Play online", command = self.show_waiting_page)
        self.button1.pack(pady=5)

        self.help_button = ctk.CTkButton(self, text="Help", command=self.show_help_page)
        self.help_button.pack(pady=5)

    def show_Settings_Page(self):
        """
        Open Settings Page
        """
        self.pack_forget()  # Hide the current page
        Settings_Page(self.master)  

    def show_Chess_Game_Page(self):
        """
        Open Chess_Game_Page page
        """
        self.pack_forget()  # Hide the current page
        Chess_Game_Page(self.master)  
    
    def show_waiting_page(self):
        """
        Open waiting page, you connect to server here
        and then went for an opponent.
        """
        self.pack_forget()  # Hide the current page
        WaitingPage(self.master)  
    
    def show_help_page(self):
        """
        Open Help page
        """
        self.pack_forget()  # Hide the current page
        Help_Page(self.master)  # Show the help page

    # Create a new page, call the create_widgets function
    # To call GUI to be added to the page.


class Help_Page(tk.Frame):
    """
    Represents the help page of the application.
    """
    def __init__(self, master=None):
        """
        Initialize the help page.
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    # This function creates the text and other gui on this page.
    def create_widgets(self):
        """
        Creates the widgets for help page
        """
        self.label = ctk.CTkLabel(self, text="Help Page", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.instructions_label = ctk.CTkLabel(self, text="Welcome to the help page.\n\n"
                                                          "In this chess game, you can choose from three different difficulty levels: Easy, Medium, and Hard.\n\n"
                                                          "Here's what each difficulty level means:\n\n"
                                                          "1. Easy: The AI opponent makes simple moves by randomly choosing legal moves.\n\n"
                                                          "2. Medium: The AI opponent is greedy and will take any piece seen and it is suitable for intermediate players.\n\n"
                                                          "3. Hard: The AI opponent makes advanced moves and is suitable for experienced players.\n"
                                                          "the AI will use a csv file of openings to start its game\n"
                                                          "Also use the min-max algorithm at a depth of 2 otherwise to choose\n"
                                                          "Its moves\n\n"
                                                          "Feel free to choose the difficulty level that best matches your skill level.\n\n"
                                                          "When playing an online game ensure you click the go back to home button and\n"
                                                          "Do not close the window or the server will crash. The other player also won be notified\n"
                                                          "Close the window when in the homepage, not a online game."
                                                          )
        self.instructions_label.pack(pady=5)

        self.back_button = ctk.CTkButton(self, text="Back to Home", command=self.show_home_page)
        self.back_button.pack(pady=5)

    def show_home_page(self):
        """
        Show the home page
        """
        self.pack_forget()  # Hide the current page
        HomePage(self.master)  # Show the home page


class Settings_Page(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.difficulty = tk.StringVar()
        self.have_settings_been_saved = False
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text="Settings", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.top_frame = customtkinter.CTkFrame(master = self,height = 1)
        self.top_frame.pack(fill="both",expand=True)


        self.skill_label = ttk.Label(self, text="Enter difficulty of ai below")
        self.skill_label.pack(pady=5)

        self.easy_button = ttk.Radiobutton(self, text="Easy", variable=self.difficulty, value="v1")
        self.easy_button.pack(pady=5)
        self.medium_button = ttk.Radiobutton(self, text="Medium", variable=self.difficulty, value="v2")
        self.medium_button.pack(pady=5)
        self.hard_button = ttk.Radiobutton(self, text="Hard", variable=self.difficulty, value="v3")
        self.hard_button.pack(pady=5)

        # Start of player vs player code
        # Create a string var to keep track of on or off.
        # by default its on
        self.switch_var = customtkinter.StringVar(self,value="on")

        # Create switch
        my_switch = customtkinter.CTkSwitch(self,text="Play against player?",command = self.switcher,
            variable=self.switch_var, onvalue="on",offvalue="off")
        my_switch.pack(pady=5)

        # Label for if the switch is on or off.
        self.my_label = customtkinter.CTkLabel(self,text="on")
        self.my_label.pack(pady=5)

        #end of pvp code

        self.save_button1 = ctk.CTkButton(self, text="Save", command=self.save_settings)
        self.save_button1.pack(pady=10)


        self.back_button1 = ctk.CTkButton(self, text="Back to Home", command=self.check_and_go_home)
        self.back_button1.pack(pady=5)

    def switcher(self):
        self.my_label.configure(text=self.switch_var.get())

    def save_settings(self):
        selected_difficulty = self.difficulty.get()
        print(selected_difficulty)
        selected_mode = self.switch_var.get()
        
        with open("settings.txt", "w") as file:
            file.write(selected_difficulty+","+selected_mode)
        print("Settings saved!")  
        self.have_settings_been_saved = True
        with open("settings.txt", "r") as file:
            contents = file.read()
            print("Content of settings.txt after saving:"+contents)

    def check_and_go_home(self):
        if self.have_settings_been_saved:
            self.show_home()
        else:
            # Prompt the user with a message box
            if messagebox.askyesno("Unsaved Changes", "Are you sure you want to leave without saving?"):
                # User clicked Yes, go back to home
                self.show_home()

    def show_home(self):
        self.pack_forget()  # Hide the current page
        HomePage(self.master)  # Show the Home Page

class WaitingPage(tk.Frame):
    """
    Represents the waiting page where 
    the player waits for another player to 
    join the game.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.waiting = True  # Flag to indicate if waiting for players
        self.pack()
        self.create_widgets()
        self.connect_to_server()
        
    
    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Waiting for another player...", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.cancel_waiting_button = ctk.CTkButton(self, text="Cancel Waiting / Go back to home", command = self.cancel_waiting)
        self.cancel_waiting_button.pack(pady=5)

    # Connect to server, currently set to localhost
    def connect_to_server(self):
        """
        Connect to the server and start waiting 
        for players.
        If no server is found, ask if they would like
        to run the server directly.
        """
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(("127.0.0.1", 5000))  # Connect to the server local host
            print("Connected to server")
            threading.Thread(target=self.wait_for_players).start()  # Start a thread to wait for players
        except ConnectionRefusedError:
            if messagebox.askyesno("Connection Failed", "Failed to connect to the server. Would you like to run the server? (If you haven't already)"):
                # If user clicks Yes, run the chess server
                self.run_server()
            else:
                # If user clicks No, go back to the home page
                self.cancel_waiting()
            
    def run_server(self):
        try:
            subprocess.Popen(["python", "chess_server.py"]) # !!! CHANGE
            messagebox.showinfo("The server is running", "You will be redirected back to the home page")
            self.cancel_waiting()

        except Exception as e:
            messagebox.showinfo("An error occurred while running the server:", e)
            self.cancel_waiting()
    
    def wait_for_players(self):
        while self.waiting:
            try:
                message = self.client.recv(1024).decode("utf-8")  # Wait for messages from the server
                # Once the message below is recieved, start the chess game.
                if message.startswith("Starting player:"):
                    self.label.configure(text="Two players connected. Starting the game...")
                    time.sleep(1)
                    # Read message and assign role.
                    _,starting_player,player_role=message.split(":")
                    starting_player = starting_player.split(",")[0]
                    self.player_role = player_role
                    self.starting_player = starting_player

                    self.open_game_page()
                    break
            except Exception as e:
                print("An error occurred while waiting for players: ", e) 
                break

    def open_game_page(self):
        self.pack_forget()  # Hide the current page
        # Show Page 2 - Tic_tac_toe
        Chess_Game_Page(self.master,True,self.player_role,self.starting_player,self.client) 

    def cancel_waiting(self):
        """
        Cancel waiting for players and return to the home page.
        """
        self.waiting = False
        if self.client:
            self.client.close()
            print("Connection with the server has been closed")
        self.waiting = False  # Stop waiting for players
        self.pack_forget()  # Hide the current page
        HomePage(self.master)

class Chess_Game_Page(tk.Frame):
    def __init__(self, master=None, Online_status=None,player_role=None,starting_player=None,client=None):
    
        super().__init__(master)
        self.winner_of_game = None
        self.waiting = True

        # openings variables
        self.stop_opening_moves_from_db = False
        self.opening_sequence_memory = []

        self.Online_status = False
        print(f"Online status: {Online_status}")
        if Online_status == True:
            self.client = client
            self.starting_player = starting_player
            self.player_role = player_role
            self.Online_status = True
            self.disabled_buttons = False
        
        
        

        self.empty_image = ImageTk.PhotoImage(Image.open("chess pieces\\all pieces\\Oxygen.png").convert("RGBA"))
        self.master = master
        self.opening_moves_count = 0
        self.opening_board = chess.Board()
        self.pack()
        self.create_widgets()

        

        if self.Online_status == True:
            
            if self.starting_player != self.player_role:
                self.disable_buttons() 
            threading.Thread(target=self.wait_for_moves).start()
            self.disable_close_button()

    def game_over(self):
        """
        Handle game over scenario 
        and display the winner.
        """
        if self.winner_of_game != None:
            messagebox.showinfo("Game Over", f"The game is over. {self.winner_of_game} wins!")
        time.sleep(1)
        if self.canvas:
            self.canvas.destroy()
        if self.Online_status == True:
            self.client.close()
        self.show_home()  # 521 is the function.
    
    def show_home(self):
        self.pack_forget()  # Hide the current page
        HomePage(self.master)  # Show the Home Page


    def back_to_home(self):
        # Check if its online.
        if self.Online_status == True:
            self.waiting = False
            self.client.close()
            print("Connection with the server has been closed")
            self.enable_close_button()
        # Check if canvas is not None before destroying?
        if self.canvas:
            self.canvas.destroy()
        self.show_home()
        

    # If its an online button closing the window will have a warning
    def disable_close_button(self):
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def enable_close_button(self):
        self.master.protocol("WM_DELETE_WINDOW",self.close_window)
     
    def close_window(self):
        sys.exit()
    
    def on_closing(self):
        if messagebox.askokcancel("WARNING!", "Please do not quit this way or the server will crash!\n"
                                  "Please go back using the home button to disconnect from the server safely\n"
                                  "and then close the window\n\n"
                                  "Click Yes to close the window regardless - NOT RECOMMENDED!"):
            self.client.close()
            sys.exit()

    # If its an online game, disable buttons for the player whos not their turn
    def disable_buttons(self):
        for row in range(8):
            for col in range(8):
                self.buttons[row][col].config(state=tk.DISABLED)
        #self.label_turn.configure(text="It is not your turn")
        self.disabled_buttons = True
    
    def enable_buttons(self):
        for row in range(8):
            for col in range(8):
                self.buttons[row][col].config(state=tk.NORMAL)
        #self.label_turn.configure(text="It is not your turn")
        self.disabled_buttons = False

    def wait_for_moves(self):
        while self.waiting:
            try:
                message = self.client.recv(1024).decode("utf-8")  # Wait for messages from the server
                print(message)
                if message.startswith("Move:"):
                    print(f"Disabled buttons: {self.disabled_buttons}")
                    if self.disabled_buttons == True:

                        from_row, from_col, to_row, to_col = map(int, message.split(",")[1:]) # Extract row and column from message
                        self.enable_buttons()
                        # ENABLE BUTTONS THEN MOVE
                        self.move_piece(from_row, from_col, to_row,to_col)
                        self.switch_player_turn()
                elif message == "Your opponent has disconnected. Game ended.":
                        messagebox.showinfo("Opponent Disconnected", "Your opponent has disconnected. Game ended.")
                        self.back_to_home()  
                        break
            except Exception as e:
                print("An error occurred while waiting for players:", e)  # Add this line for debugging
                break

    def create_widgets(self):
        if hasattr(self.master, 'WaitingPage'):
            self.master.waiting_page.pack_forget()
            print("FORGOTTEN")

        self.label = ttk.Label(self, text="Chess game", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.back_button = ttk.Button(self, text="Back to Home", command=self.back_to_home)
        self.back_button.pack(pady=5)

        self.place_chessboard()
    
    def place_chessboard(self):
        self.pre_move = True
        self.current_player = "white"
        self.checkmate = False
        self.stalemate = False

        # Select AI

        # Read file
        with open("settings.txt", "r") as file:
            contents = file.read()

        settings = contents.split(",") 
        version_of_ai = settings[0]  # easy medium hard
        self.game_mode = settings[1] # pvp or ai 

        print(version_of_ai)
        print(self.game_mode)

        if (version_of_ai == "" and self.game_mode == "off"):
            self.game_mode = "on"
            print(self.game_mode)

        if version_of_ai == "v1":
            self.ai_is_on = True
            self.ai_v2_is_on = False
            self.ai_v3_is_on = False
        elif version_of_ai == "v2":
            self.ai_is_on = False
            self.ai_v2_is_on = True
            self.ai_v3_is_on = False

        elif version_of_ai == "v3":
            self.ai_is_on = False
            self.ai_v2_is_on = False
            self.ai_v3_is_on = True
            print("Hardest AI is on")

        self.chessboard = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--","--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
        ]


        self.canvas = tk.Canvas(width=400, height=400)
        
       
        light_color = "#f0d9b5"
        dark_color = "#b58863"
        piece_names = [
            "white-bpawn", "white-bishop", "white-knight", "white-rook", "white-queen",
            "white-king", "black-bpawn", "black-bishop", "black-knight", "black-rook", "black-queen", "black-king", "Oxygen"
        ]

        self.piece_images = {}
        

        self.buttons = [[None] * 8 for _ in range(8)] 
        
        for piece_name in piece_names:
            image_path = f"chess pieces\\all pieces\\{piece_name}.png"
            image = Image.open(image_path).convert("RGBA")
            self.piece_images[piece_name] = image 
        
        for row in range(8):
            for col in range(8): # light colour first
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                
                if row in [1]:
                    piece_name = "black-bpawn" 
                elif row in [6]:
                    piece_name = "white-bpawn" 
                elif row in [0] and (col == 0 or col ==7):
                    piece_name = "black-rook" 
                elif row in [0] and (col == 1 or col ==6):
                    piece_name = "black-knight" 
                elif row in [0] and (col == 2 or col == 5):
                    piece_name = "black-bishop" 
                elif row in [0] and (col == 3):
                    piece_name = "black-queen" 
                elif row in [0] and (col == 4):
                    piece_name = "black-king" 
                elif row in [7] and (col == 0 or col ==7):
                    piece_name = "white-rook" 
                elif row in [7] and (col == 1 or col ==6):
                    piece_name = "white-knight" 
                elif row in [7] and (col == 2 or col == 5):
                    piece_name = "white-bishop" 
                elif row in [7] and (col == 3):
                    piece_name = "white-queen" 
                elif row in [7] and (col == 4):
                    piece_name = "white-king" 
                else:
                    piece_name = "Oxygen"
                print(piece_name)
                
                if piece_name != None:
                    piece_image = self.piece_images[piece_name].resize((30, 30))
                    button_image = ImageTk.PhotoImage(piece_image)
                    button = tk.Button(self.canvas, width=100, height=40, bg=color,
                                   command=lambda r=row, c=col: self.on_square_click(r, c), image=button_image)
                    button.image = button_image  
                else:
                    button = tk.Button(self.canvas, width=14, height=3, bg=color,
                                   command=lambda r=row, c=col: self.on_square_click(r, c))

                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        self.canvas.pack()

    
    def convert_coordinates_to_alegbraic(self,coordinates):
    # example coordinates = [(6,0),(4,0)] - (Just a visulisation)
        algebraic_moves = []
        Loop = 0
        while Loop != 2:

            # Convert from move 
            # Lets do rows up and down first.
            number_of_from = 8 - coordinates[Loop][0] 
            print(number_of_from)

            # Column left and right second
            # They need to be letter
            
            conversion_dict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
            letter_of_from = conversion_dict.get(coordinates[Loop][1])
            print(letter_of_from)

            print(f"{letter_of_from}{number_of_from}")


            final_coordinate = str(letter_of_from)+str(number_of_from)
            algebraic_moves.append(final_coordinate)
            Loop += 1
        combined_string = ''.join(algebraic_moves)
        return combined_string  
    
    def add_move_to_board(self,coordinates_processed):
        # adds moves to board and prints them
        move = chess.Move.from_uci(coordinates_processed)
        move_in_chess_notation = self.opening_board.san(move)
        print(move_in_chess_notation)
        self.opening_board.push_san(move_in_chess_notation)
        return move_in_chess_notation  
    
    def read_column_from_csv(self,column_names):
        data = []
        last_element = column_names[-1]
        next_column_name = last_element[:-1]+"b"
        print(next_column_name)
        with open('high_elo_opening.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if len(self.opening_sequence_memory) == 1: #like e4
                for row in reader:
                    if row[column_names[0]] == self.opening_sequence_memory[0]:
                      if row[next_column_name] not in data and row[next_column_name] != "" and row[next_column_name] != "O-O": # No castling, the other type isnt present in csv.
                        data.append(row[next_column_name])

            if len(self.opening_sequence_memory) == 3: #like e4
                for row in reader:
                    if row[column_names[0]] == self.opening_sequence_memory[0] and row[column_names[1]] == self.opening_sequence_memory[1] and row[column_names[2]] == self.opening_sequence_memory[2]:
                      if row[next_column_name] not in data and row[next_column_name] != "":
                        data.append(row[next_column_name])

            if len(self.opening_sequence_memory) == 5: #like e4
                for row in reader:
                    if row[column_names[0]] == self.opening_sequence_memory[0] and row[column_names[1]] == self.opening_sequence_memory[1] and row[column_names[2]] == self.opening_sequence_memory[2] and row[column_names[3]] == self.opening_sequence_memory[3] and row[column_names[4]] == self.opening_sequence_memory[4]:
                      if row[next_column_name] not in data and row[next_column_name] != "":
                        data.append(row[next_column_name])
                

            if len(self.opening_sequence_memory) == 7: #like e4
                for row in reader:
                    if row[column_names[0]] == self.opening_sequence_memory[0] and row[column_names[1]] == self.opening_sequence_memory[1] and row[column_names[2]] == self.opening_sequence_memory[2] and row[column_names[3]] == self.opening_sequence_memory[3] and row[column_names[4]] == self.opening_sequence_memory[4] and row[column_names[5]] == self.opening_sequence_memory[5] and row[column_names[6]] == self.opening_sequence_memory[6]:
                      if row[next_column_name] not in data and row[next_column_name] != "":
                        data.append(row[next_column_name])
        return data
    
    def convert_alebraic_to_coordinates(self,alebraic):
        print(f"This is alebraic {alebraic}")
        print(f"This is board, /n{self.opening_board}")
        coordinates = str(self.opening_board.parse_san(alebraic))
        print(coordinates)
        # I additionally need to play this move on the canvas or the code will break.
        self.opening_board.push_san(alebraic)
        print(self.opening_board)

        return coordinates    
    
    def move_to_tuple(self,move):
        column_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        from_square = (8 - int(move[1]), column_map[move[0]])
        to_square = (8 - int(move[3]), column_map[move[2]])
        return [from_square, to_square]
    
    def generate_column_names(self,opening_moves_count):
        column_names = []
        for i in range(1, opening_moves_count + 1):
            column_names.append(f"move{i}w")
            if i != opening_moves_count:
                column_names.append(f"move{i}b")
        return column_names
    
    def on_square_click(self, row, col):
        print(f"Button clicked: Row {row}, Column {col}")
        print(f"Its {self.current_player}'s turn")
        if self.pre_move == True:
            print("You are moving the piece on this square to...")
            self.selected_start = (row, col)
            self.pre_move = False
            self.button_from2 = self.buttons[row][col]
            self.original_color = self.button_from2.cget("bg")
            self.button_from2.config(bg="green")

            all_current_moves = self.get_all_possible_moves()
            possible_moves_for_selected_piece = []
            self.highlighted_buttons = []

            for move in all_current_moves:
                if move[0] == (row, col):
                    possible_moves_for_selected_piece.append(move)
           
            print("Possible moves:", possible_moves_for_selected_piece)

            # Highlight possible moves
            for move_row,move_col in possible_moves_for_selected_piece:
                print(move_row, move_col)
                print(move_col)
                button = self.buttons[move_col[0]][move_col[1]]
                self.highlighted_buttons.append((move_col, button.cget("bg")))
                
                #highlighted_buttons.append((move, button.cget("bg")))
                
                self.buttons[move_col[0]][move_col[1]].config(bg="yellow")
                print(f"{self.highlighted_buttons}")
            # for loop for finding other possible moves for that piece.
            #possible_moves_for_selected_piece = self.get_all_possible_moves()
        else:
            self.button_from2.config(bg = self.original_color)

            for button, original_color in self.highlighted_buttons:
                print(button)
                self.buttons[button[0]][button[1]].config(bg=original_color)


            from_row, from_col = self.selected_start
            print("You are moving it to this square",from_row, from_col)
            to_row, to_col = row, col
            # Before moving we need to check if the move is legal
            # First question is what piece are we moving?

            '''
            We are using this validation
            '''
            all_current_moves = self.get_all_possible_moves()
            print(all_current_moves)

            move = to_row,to_col,from_row,from_col
            # Moving
            if ((from_row,from_col),(to_row,to_col)) not in all_current_moves:
                print("Illegal move")
                self.pre_move = True
            else:
                self.move_piece(from_row, from_col, to_row, to_col)
                print("Piece should be moved")
                self.switch_player_turn()
                if self.game_mode == "on" and self.Online_status != True:
                    pass

                elif self.Online_status == True:
                    self.client.sendall(f"Move:,{from_row},{from_col},{to_row},{to_col}".encode("utf-8"))
                    self.disable_buttons()

                elif self.ai_is_on == True and self.current_player == "black":
                    self.ai_is_on = True
                    possible_moves = self.get_all_possible_moves()
                    #possible_moves[random.randint(0,len(possible_moves)-1)]
                    selected_move = random.choice(possible_moves)
                    from_row, from_col = selected_move[0]
                    to_row, to_col = selected_move[1]
                    if self.winner_of_game == None:
                        self.move_piece(from_row, from_col, to_row, to_col)
                        self.switch_player_turn()

                elif self.ai_v2_is_on == True and self.current_player == "black":
                    best_move_v2 = self.smarter_chess_ai()# Find best move using eval.
                    from_row, from_col = best_move_v2[0]
                    to_row, to_col = best_move_v2[1]
                    if self.winner_of_game == None:
                        self.move_piece(from_row, from_col, to_row, to_col)
                        print(f"I made a move {from_row, from_col}")
                        print(f"To the place {to_row, to_col}")
                        self.switch_player_turn()
                
                elif self.ai_v3_is_on == True and self.current_player == "black":
                    if self.opening_moves_count != 4 and self.stop_opening_moves_from_db == False:
                        self.opening_moves_count += 1
                        # Turn old move into standard chess notation
                        converted_to_list_for_openings = [(from_row,from_col),(to_row,to_col)]
                        chess_notation_coords = self.convert_coordinates_to_alegbraic(converted_to_list_for_openings)
                        single_chess_noation = self.add_move_to_board(chess_notation_coords)

                        print(single_chess_noation)

                        list_of_columns_in_csv = self.generate_column_names(self.opening_moves_count)
                        
                        print(list_of_columns_in_csv)

                        # Input the list of moves by white and black.
                        self.opening_sequence_memory.append(single_chess_noation)
                        

                        next_moves= self.read_column_from_csv(list_of_columns_in_csv) # move inputted is chessnoted
                        print(next_moves)
                        if next_moves != []:
                            random_chosen_opening = random.choice(next_moves)
                            self.opening_sequence_memory.append(random_chosen_opening) # should have two moves now.

                            final_move = self.convert_alebraic_to_coordinates(random_chosen_opening)
                            best_move_v3 = final_move
                            print(f"This is best move v3 {best_move_v3}")
                            best_move_v3 = self.move_to_tuple(best_move_v3)
                        else:
                            print("No move found in opening database")
                            best_move_v3 = self.min_max()
                            self.stop_opening_moves_from_db = True
                    else:
                        best_move_v3 = self.min_max()

                    from_row, from_col = best_move_v3[0]
                    to_row, to_col = best_move_v3[1]
                    if self.winner_of_game == None:
                        self.move_piece(from_row, from_col, to_row, to_col)
                        print(f"I made a move {from_row, from_col}")
                        print(f"To the place {to_row, to_col}")
                        self.switch_player_turn()

                self.pre_move = True

    def switch_player_turn(self):
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"

    def get_all_possible_moves(self):
        self.moves = []
        for r in range(len(self.chessboard)):
            for c in range(len(self.chessboard[r])):
                turn = self.chessboard[r][c][0]
                if (turn == "w" and self.current_player == "white") or \
                    (turn == "b" and self.current_player == "black"):
                    piece = self.chessboard[r][c][1]
                    if piece == "p":
                        self.get_pawn_moves(r,c, self.moves)
                    elif piece == "r":
                        self.get_rook_moves(r,c, self.moves)
                    elif piece == "n":
                         self.get_knight_moves(r,c, self.moves)
                    elif piece == "b":
                         self.get_bishop_moves(r,c, self.moves)
                    elif piece == "q":
                        self.get_queen_moves(r,c, self.moves)
                    elif piece == "k":
                        self.get_king_moves(r,c, self.moves)
        return self.moves
    
    def get_pawn_moves(self, r, c, moves):
        if self.current_player == "white":
            #print("White to move")
            if self.chessboard[r-1][c] == "--": # 1 square
                self.moves.append(((r,c),(r-1,c)))
                if r == 6 and self.chessboard[r-2][c] == "--":
                    self.moves.append(((r,c),(r-2,c)))
            if c-1 >= 0:
                if self.chessboard[r-1][c-1][0] == "b":
                    self.moves.append(((r,c),(r-1,c-1)))
            if c+1 <= 7:
                if self.chessboard[r-1][c+1][0] == "b":
                    self.moves.append(((r,c),(r-1,c+1)))
        else:
            #print("Black to move")
            if self.chessboard[r+1][c] == "--": # 1 square
                self.moves.append(((r,c),(r+1,c)))
                if r == 1 and self.chessboard[r+2][c] == "--":
                    self.moves.append(((r,c),(r+2,c)))
            if c-1 >= 0:
                if self.chessboard[r+1][c-1][0] == "w":
                    self.moves.append(((r,c),(r+1,c-1)))
            if c+1 <= 7:
                if self.chessboard[r+1][c+1][0] == "w":
                    self.moves.append(((r,c),(r+1,c+1)))

    
    def get_rook_moves(self,r,c,moves): # row, column
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up , left, down, right
        if self.current_player == "white":
            enemy = "b" 
        else:
            enemy = "w"
        if self.current_player == "white" or "black":
            for d in directions:
                for i in range(1,8): # rooks move 1 to 7 squares
                    end_row, end_col = r + i * d[0], c + i * d[1]

                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if self.chessboard[end_row][end_col] == "--":
                            self.moves.append(((r,c),(end_row,end_col)))
                        elif self.chessboard[end_row][end_col][0] == enemy:
                            self.moves.append(((r,c),(end_row,end_col)))
                            break
                        else: 
                            break 
                    else:
                        break
                
        else:
            print("Black to move rook")
    
    def get_knight_moves(self,r,c,moves):
        directions = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        if self.current_player == "white":
            ally = "w"
        else:
            ally = "b"
        for d in directions:
            end_row, end_col = r + d[0], c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                # can should be make sure its not an ally, no need for blank
                if self.chessboard[end_row][end_col] == "--":
                    self.moves.append(((r,c),(end_row,end_col)))
                elif self.chessboard[end_row][end_col][0] != ally:
                    self.moves.append(((r,c),(end_row,end_col)))
            

    def get_bishop_moves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #up left, up right, down left, down right
        if self.current_player == "white":
            enemy = "b" 
        else:
            enemy = "w"
        for d in directions:
                for i in range(1,8): # rooks move 1 to 7 squares
                    end_row, end_col = r + i * d[0], c + i * d[1]

                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if self.chessboard[end_row][end_col] == "--":
                            self.moves.append(((r,c),(end_row,end_col)))
                        elif self.chessboard[end_row][end_col][0] == enemy:
                            self.moves.append(((r,c),(end_row,end_col)))
                            break
                        else: 
                            break 
                    else:
                        break
    def get_queen_moves(self,r,c,moves):
        self.get_bishop_moves(r,c,moves)
        self.get_rook_moves(r,c,moves)
    
    def get_king_moves(self,r,c,moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if self.current_player =="white":
            ally = "w" 
        else:
            ally = "b"
        for d in directions:
            end_row, end_col = r + d[0], c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.chessboard[end_row][end_col][0] != ally:
                    self.moves.append(((r,c),(end_row,end_col)))

    def get_all_possible_moves1(self,board, t_player):
        self.moves = []
        for r in range(len(board)):
            for c in range(len(board[r])):
                turn = board[r][c][0]
                if (turn == "w" and t_player == "white") or \
                    (turn == "b" and t_player == "black"):
                    piece = board[r][c][1]
                    if piece == "p":
                        self.get_pawn_moves1(r,c, self.moves,board,t_player)
                    elif piece == "r":
                        self.get_rook_moves1(r,c, self.moves,board,t_player)
                    elif piece == "n":
                         self.get_knight_moves1(r,c, self.moves,board,t_player)
                    elif piece == "b":
                         self.get_bishop_moves1(r,c, self.moves,board,t_player)
                    elif piece == "q":
                        self.get_queen_moves1(r,c, self.moves,board,t_player)
                    elif piece == "k":
                        self.get_king_moves1(r,c, self.moves,board,t_player)
        return self.moves
    
    def get_pawn_moves1(self, r, c, moves,board,t_player):
        if t_player == "white":
            if board[r-1][c] == "--": # 1 square
                self.moves.append(((r,c),(r-1,c)))
                if r == 6 and board[r-2][c] == "--":
                    self.moves.append(((r,c),(r-2,c)))
            if c-1 >= 0:
                if board[r-1][c-1][0] == "b":
                    self.moves.append(((r,c),(r-1,c-1)))
            if c+1 <= 7:
                if board[r-1][c+1][0] == "b":
                    self.moves.append(((r,c),(r-1,c+1)))
        else:
            #print("Black to move")
            if board[r+1][c] == "--": # 1 square
                self.moves.append(((r,c),(r+1,c)))
                if r == 1 and board[r+2][c] == "--":
                    self.moves.append(((r,c),(r+2,c)))
            if c-1 >= 0:
                if board[r+1][c-1][0] == "w":
                    self.moves.append(((r,c),(r+1,c-1)))
            if c+1 <= 7:
                if board[r+1][c+1][0] == "w":
                    self.moves.append(((r,c),(r+1,c+1)))

    
    def get_rook_moves1(self,r,c,moves,board,t_player): # row, column
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up , left, down, right
        if t_player == "white":
            enemy = "b" 
        else:
            enemy = "w"
        if t_player == "white" or "black":
            for d in directions:
                for i in range(1,8): # rooks move 1 to 7 squares
                    end_row, end_col = r + i * d[0], c + i * d[1]

                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if board[end_row][end_col] == "--":
                            self.moves.append(((r,c),(end_row,end_col)))
                        elif board[end_row][end_col][0] == enemy:
                            self.moves.append(((r,c),(end_row,end_col)))
                            break
                        else: 
                            break 
                    else:
                        break
                
        else:
            print("Black to move rook")
    
    def get_knight_moves1(self,r,c,moves,board,t_player):
        directions = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        if t_player == "white":
            ally = "w"
        else:
            ally = "b"
        print(self.current_player)
        print(ally)
        for d in directions:
            end_row, end_col = r + d[0], c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                # can should be make sure its not an ally, no need for blank
                if board[end_row][end_col] == "--":
                    self.moves.append(((r,c),(end_row,end_col)))
                elif board[end_row][end_col][0] != ally:
                    self.moves.append(((r,c),(end_row,end_col)))
            

    def get_bishop_moves1(self,r,c,moves,board,t_player):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1)) #up left, up right, down left, down right
        if t_player == "white":
            enemy = "b" 
        else:
            enemy = "w"
        for d in directions:
                for i in range(1,8): # rooks move 1 to 7 squares
                    end_row, end_col = r + i * d[0], c + i * d[1]

                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if board[end_row][end_col] == "--":
                            self.moves.append(((r,c),(end_row,end_col)))
                        elif board[end_row][end_col][0] == enemy:
                            self.moves.append(((r,c),(end_row,end_col)))
                            break
                        else: 
                            break 
                    else:
                        break
    def get_queen_moves1(self,r,c,moves,board,t_player):
        self.get_bishop_moves1(r,c,moves,board,t_player)
        self.get_rook_moves1(r,c,moves,board,t_player)
    
    def get_king_moves1(self,r,c,moves,board,t_player):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        if t_player =="white": # was white before
            ally = "w" 
        else:
            ally = "b"
        for d in directions:
            end_row, end_col = r + d[0], c + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                # can should be make sure its not an ally, no need for blank
                if board[end_row][end_col][0] != ally:
                    self.moves.append(((r,c),(end_row,end_col)))
    




    def move_piece(self,from_row, from_col, to_row, to_col):
        button_from = self.buttons[from_row][from_col]
        button_to = self.buttons[to_row][to_col]
        # update button with image using configurations
        # make the to be the same image as the from button.
        button_to.config(image=button_from.cget('image'))
        #image_path1 = f"A_working_ones\\chess pieces\\all pieces\\Oxygen.png"
        image_path1 = f"chess pieces\\all pieces\\Oxygen.png"
        image1 = Image.open(image_path1).convert("RGBA")
        image2 = ImageTk.PhotoImage(image1)
        button_from.config(image=self.empty_image)#.cget('image'))
        #print("Now a button is ruined.")
        old_value = self.chessboard[from_row][from_col] 
        print("This is old piece/value:",old_value)
        self.chessboard[from_row][from_col] = "--"
        piece_getting_captured = self.chessboard[to_row][to_col] 
        self.chessboard[to_row][to_col] = old_value
        for row in self.chessboard:
            print(row)

        # End game if king is captured
        # Check if a piece is captured
        if piece_getting_captured != "--":
            # Check if the captured piece is a king
            if piece_getting_captured == "bk":
                # A king is captured, end the game
                self.winner_of_game = "white"
                self.game_over()
            elif piece_getting_captured == "wk":
                # A king is captured, end the game
                self.winner_of_game = "black"
                self.game_over()




    def is_path_clear_horizontal(self,row,start_col,end_col):
        # We are moving across the cols. 
        # first find the direction
        direction = 1 if start_col < end_col else -1
        for col in range(start_col + direction, end_col, direction):
            if self.chessboard[row][col] != 0:
                return False
        return True
    
    def is_path_clear_vertical(self,col,start_row,end_row):
        # We are moving across the cols. 
        # first find the direction
        direction = 1 if start_row < end_row else -1
        for row in range(start_row + direction, end_row, direction):
            if self.chessboard[row][col] != 0:
                return False
        return True
    
    def is_path_clear_diagonal(self,start_row,start_col,end_row,end_col):
        # up or down
        # if i start row 3 and go up to 1. then where i started is
        # more than end. for up
        direction_vert = -1 if start_row < end_row else 1
        direction_hori = 1 if start_col < end_col else -1

        row, col = start_row + direction_hori, start_col + direction_vert
        while row != end_row and col != end_col:
            print(row)
            print(col)
            if self.chessboard[row][col] != 0:
                print(self.chessboard[row][col])
                print("You failed its not diagonal")
                return False
            row += direction_hori
            col += direction_vert

        return True

    def chess_ai(possible_moves):
        # random moves.
        possible_moves[random.randint(0,len(possible_moves)-1)]
        
    def smarter_chess_ai(self):
        # We need a scoring system
        # This evaluation only looks at the material and not the pieces postion
        scoring = {
            'p': 10,
            'n': 30,
            'b': 30,
            'r': 50,
            'q': 90,
            'k': 9000
        }    
        possible_moves = self.get_all_possible_moves()
        best_moves = []
        best_evaluation = None
        print("This is copied boards")
        for move in possible_moves:
            chess_board_copy = copy.deepcopy(self.chessboard)
            # make the move
            from_row, from_col = move[0][0],move[0][1]
            to_row, to_col = move[1][0],move[1][1]
            chess_board_copy[to_row][to_col] = chess_board_copy[from_row][from_col]
            chess_board_copy[from_row][from_col] = "--"
            #for x in range(7):
            #    print(chess_board_copy[x])

            move_evaluation = self.evaluate_board(chess_board_copy, scoring)
            if best_evaluation is None:
                best_evaluation = move_evaluation
                best_moves.append(move)
            elif move_evaluation >= best_evaluation and self.current_player == "white":
                best_evaluation = move_evaluation
                best_moves.append(move)
            else:
                if  move_evaluation == best_evaluation:
                    print(f"equal move evalutation:{move_evaluation}")
                    best_moves.append(move)
                elif  move_evaluation < best_evaluation:
                    print(f"Old Best evalutation:{best_evaluation}")
                    best_evaluation = move_evaluation
                    print(f"New Best evalutation:{best_evaluation}")
                    best_moves.clear()
                    best_moves.append(move)


            # move_evaluation is postitve for white, negative for black.
        print(f"Best moves: f{best_moves}")
        best_move = best_moves[random.randint(0,len(best_moves)-1)]
        return best_move
        # Find best moves then 
        # pick one randomly if theres multiple with the same evaluation score.

    def evaluate_board(self,chess_board_copy, scoring):
        evaluation = 0
        total_eval = 0
        for r in range(len(chess_board_copy)):
            for c in range(len(chess_board_copy[r])):
                
                piece = chess_board_copy[r][c] #imagine wq
                if piece != "--":
                    evaluation = scoring.get(piece[1])
                    # The two lines below make the ai smarted. it works but is dumber
                    # without them.
                    position_evaluation = self.evaluate_piece_position(chess_board_copy,r,c)
                    evaluation = evaluation + position_evaluation
                    if piece[0] == "b":
                        evaluation = evaluation*-1
                    total_eval = evaluation + total_eval
                    #if total_eval == -20:
                        #print(piece)
        return total_eval
                    
    # The function assess's the position of a specific piece on the board
    def evaluate_piece_position(self,chess_board_copy, r,c):
        """
        Look at place in the copied board in r c. get its position value
        return position value.
        """
        pawn_array = [[0,  0,  0,  0,  0,  0,  0,  0],
                [5,  5,  5,  5,  5,  5,  5,  5],
                [1,  1,  2,  3,  3,  2,  1,  1],
                [0.5,  0.5, 1, 2.5, 2.5,  1,  0.5,  0.5],
                [0,  0,  0, 2, 2,  0,  0,  0],
                [0.5, -0.5, -1,  0,  0, -1, -0.5,  0.5],
                [0.5, 1, 1,-2, -2, 1, 1,  0.5],
                [0,  0,  0,  0,  0,  0,  0,  0]]

        knight_array =  [
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2, 0, 0, 0, 0, -2, -4],
            [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
            [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
            [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
            [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
            [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5]
        ]
        bishop_array = [
            [-2, -1, -1, -1, -1, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
            [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 1, 1, 1, 1, 1, 1, -1],
            [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
            [-2, -1, -1, -1, -1, -1, -1, -2]
        ]

        rook_array = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0.5, 1, 1, 1, 1, 1, 1, 0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
            [0, 0, 0, 0.5, 0.5, 0, 0, 0]
        ]

        queen_array = [
            [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
            [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
            [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
            [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
            [-1, 0, 0.5, 0, 0, 0, 0, -1],
            [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
        ]
        # Maybe king might change at differnet points of the game.
        king_array = [
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-2, -3, -3, -4, -4, -3, -3, -2],
            [-1, -2, -2, -2, -2, -2, -2, -1],
            [2, 2, 0, 0, 0, 0, 2, 2],
            [2, 3, 1, 0, 0, 1, 3, 2]
        ]
        # rook, pawn, king, aren't symmetrical.
        piece_dict = {
            "pawn": pawn_array,
            "knight": knight_array,
            "bishop": bishop_array,
            "rook": rook_array,
            "queen": queen_array,
            "king": king_array
        }

        team = chess_board_copy[r][c][0]
        piece = chess_board_copy[r][c][1]
        if piece == "p":
            piece = "pawn"
        elif piece == "n":
            piece = "knight"
        elif piece == "b":
            piece = "bishop"
        elif piece == "r":
            piece = "rook"
        elif piece == "q":
            piece = "queen"
        elif piece == "k":
            piece = "king"
        
        look_here = piece_dict[piece]
        team = chess_board_copy[r][c][0]
        if team == 'b':
            r = 7 - r
        value = look_here[r][c]
        return value
        
    #min_max 
    def min_max(self):
        scoring = {
            'p': 10,
            'n': 30,
            'b': 30,
            'r': 50,
            'q': 90,
            'k': 9000
        }
        best_move = []
        best_score = float('+inf')

        min_max_score =  float('inf')

        opponent_max_score = float('-inf')
        # Assume that black is the AI
        # Get blacks possible moves

        blacks_moves = self.get_all_possible_moves()
        # We now have all of blacks possible moves
        # It knows its blacks turn and the board
        # Now we loop each of blacks moves

        # lets store the current board as copy
        original_board = copy.deepcopy(self.chessboard)

        for move in blacks_moves:
            # Here we need to get all of white's moves for
            # each of blacks moves. so if each had 2 moves.
            # black has 2, white has 4.

            board = copy.deepcopy(original_board)

            # First make the move onto a deepcopied board.
            from_row, from_col = move[0][0],move[0][1]
            to_row, to_col = move[1][0],move[1][1]
            board[to_row][to_col] = board[from_row][from_col]
            board[from_row][from_col] = "--"

            white_moves = self.get_all_possible_moves1(board,"white")
            #print(f"These are whites, moves {white_moves}")

            opponent_max_score = float('-inf')

            for w_move in white_moves:
                temp_board = copy.deepcopy(board)
                from_row, from_col = w_move[0][0],w_move[0][1]
                to_row, to_col = w_move[1][0],w_move[1][1]
                temp_board[to_row][to_col] = temp_board[from_row][from_col]
                temp_board[from_row][from_col] = "--"

                #evulate board.
                
                move_evaluation = self.evaluate_board(temp_board, scoring)
                #print(f"This is move evaluation {move_evaluation}")

                # white is trying to get the maximum score so look for the biggest
                if move_evaluation > opponent_max_score:
                    opponent_max_score = move_evaluation

                # undo the move
            print(f"This is white max score {opponent_max_score}")
            if opponent_max_score < min_max_score:
                min_max_score = opponent_max_score
                best_move.clear()
                best_move.append(move)
                print(f"Best move is {best_move}")
            
            if opponent_max_score == min_max_score:
                min_max_score = opponent_max_score
                best_move.append(move)
                print(f"Best move is {best_move}")  # Thats not white max score lol.
            

            board = copy.deepcopy(original_board)
        print("Printing best move...")
        print(f"{best_move}")
        best_move = best_move[random.randint(0,len(best_move)-1)]
        return best_move

def main():
    root = tk.Tk()
    root.title("Chess application made with tkinter for gui.")
    root.geometry("1200x800")  # Fixed window size to make the app work consistently
    root.resizable(False, False)


    home_page = HomePage(master=root)

    root.mainloop()


if __name__ == "__main__":
    main()
