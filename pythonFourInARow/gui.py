#############################################################################
# FILE: gui.py
# WRITERS: Ayal Meitar, ayal.meitar, 309981215, Shahar Nahum, shaharna13,
# 313586877
# EXERCISE: intro2cs ex12 2017-2018
# DESCRIPTION: the file includes the gui for connect four game, each function
# of the gui is described bellow
#############################################################################

#############################################################################
# imports
############################################################

import ai
from tkinter import *
from game import *
from tkinter import messagebox
from communicator import *

############################################################
# Constants
############################################################
DRAW_TITLE = "Draw"

DRAW_MASSEGE = "the board is full there is no winner"

SECOND_PLAYER_COLOR = "yellow"

FIRST_PLAYER_COLOR = "red"

WIN_TITLE = "WE HAVE A WINNER"

WIN_MSG = "has won the game"

ROW_SIZE = 6
COL_SIZE = 7

IP_PLACE = 3

PORT = 2

PLAYER_TYPE = 1

MAX_PORT = 65535

ARGUMENTS_ERROR = "Illegal program arguments"

NUMBER_OF_SERVER_ARGUMENTS = 2
NUMBER_OF_CLIENT_ARGUMENTS = 3


class ConnectFour:
    """
    represents a class of the Gui for connect four
    """

    def __init__(self, parent, port, ip=None, is_ai=False):
        self.game = Game()
        self.parent = parent
        self.who_am_i = None
        ############################################################
        # UI
        ############################################################
        board_frame = Frame(self.parent, cursor="hand2")
        self.canvas_grid = self.create_discs(board_frame)
        board_frame.pack(side=BOTTOM)
        self.first_player_label = Label(parent, text="Player One turn",
            bg="lime green", font=("ariel", 10, "bold"), height=1)
        self.second_player_label = Label(parent, text="PLAYER TWO",
            font=("ariel", 10, "bold"), height=1, bg="red")
        self.create_dots_frame()
        ###########################################################
        # communication
        ##########################################################
        if ip:
            self.who_am_i = self.game.PLAYER_TWO
        else:
            self.who_am_i = self.game.PLAYER_ONE
        self.__communicator = Communicator(parent, port, ip)
        self.__communicator.connect()
        self.__communicator.bind_action_to_message(self.response_message)
        ###############################################################
        # AI
        ##############################################################
        if is_ai:  # defining the ai player. Else the attribute is non.
            self.ai_value = ai.AI()
        else:
            self.ai_value = None
        if self.who_am_i == self.game.PLAYER_ONE and self.ai_value:
            # if the AI should play the first move
            self.ai_value.find_legal_move(self.game, self.__add_disc)

    def create_dots_frame(self):
        """
        the function creates the widgets above the frame of the board.
        :return:
        """
        dots_frame = LabelFrame(self.parent)
        photo = PhotoImage(file="homer_round.png")
        dot1 = (Label(self.parent, image=photo))
        dot1.photo = photo
        player_two_label = self.second_player_label
        player_two_label.grid_remove()
        player_two_label.pack(side=RIGHT)
        photo = PhotoImage(file="merge_round.png")
        dot2 = (Label(self.parent, image=photo))
        dot2.photo = photo
        dot1.pack(side=LEFT)
        dot2.pack(side=RIGHT)
        dots_frame.pack(side=BOTTOM)
        text_frame = LabelFrame(self.parent)
        player_one_label = self.first_player_label
        player_one_label.pack(side=LEFT)
        header_label = Label(self.parent, text="Connect Four",
            font=("david", 20, "italic"))
        if self.who_am_i == self.game.PLAYER_ONE:
            player_label = Label(self.parent, text="You are player One",
            font=("david", 16, "italic"))
        else:
            player_label = Label(self.parent, text="You are player Two",
                font=("david", 14, "bold"))
        header_label.pack()
        player_label.pack()
        text_frame.pack(side=TOP)

    def create_discs(self, parent):
        """
        the function crates a 2D grid so that each spot will be a canvas that
        includes an oval, and will have it's own indexes
        :param parent:
        :return: the canvas
        """
        canvas = []
        for i in range(ROW_SIZE):
            e = []
            for j in range(COL_SIZE):
                photo = PhotoImage(file="full_donut.png")
                e.append(Label(parent, image=photo))
                e[j].photo = photo
            canvas.append(e)
        for i in range(ROW_SIZE):
            for j in range(COL_SIZE):
                self.bind_press(canvas, i, j)
        return canvas

    def bind_press(self, canvas, i, j):
        """
        the function binds a press and a hoover to every button.
        :param canvas:
        :param i:
        :param j:
        :return:
        """
        canvas[i][j].grid(row=i, column=j)
        canvas[i][j].bind("<Button-1>", lambda x: self.button_press(j))
        canvas[i][j].bind("<Enter>", lambda x: self.button_hoover(j))
        canvas[i][j].bind("<Leave>", lambda x: self.button_hoover_out(j))

    def button_hoover(self, j):
        """
        The function deals with the hoovering in the column
        :param j:
        :return:
        """
        for i in range(ROW_SIZE):
            if self.game.get_board()[i][j] is None:
                photo = PhotoImage(file="full_donut_hoover.png")
                self.canvas_grid[i][j].configure(image=photo)
                self.canvas_grid[i][j].photo = photo

    def button_hoover_out(self, j):
        """
        The function deals with the hoovering out from the column
        :param j:
        :return:
        """
        for i in range(ROW_SIZE):
            if self.game.get_board()[i][j] is None:
                photo = PhotoImage(file="full_donut.png")
                self.canvas_grid[i][j].configure(image=photo)
                self.canvas_grid[i][j].photo = photo

    def button_press(self, i):
        """
        the function binds a press action to the add disc function while
        verifying that the player who made the move is the one allowed to.
        :return:
        """
        if self.game.get_current_player() == self.who_am_i \
                and self.game.is_game_on:
            self.__add_disc(i)

    def __add_disc(self, i):
        """
        the function adds a yellow disc if player one puts a disc, and a red
        disc if the second player puts a disc
        :return:
        """
        row, col = None, None
        try:
            row, col = self.game.make_move(i)
        except IllegalMove:
            messagebox.showerror("INVALID MOVE", "invalid move")
        if row is not None and col is not None:
            if self.game.get_current_player() != self.who_am_i:
                self.__communicator.send_message(i)
            if self.game.get_current_player() == self.game.PLAYER_TWO:
                photo = PhotoImage(file="homer_round.png")
                self.canvas_grid[row][col].configure(image=photo)
                self.canvas_grid[row][col].photo = photo
                self.first_player_label.config(text="PLAYER ONE", bg="red")
                self.second_player_label.config(text="Player Two turn",
                    bg="lime green")
            else:
                photo = PhotoImage(file="merge_round.png")
                self.canvas_grid[row][col].configure(image=photo)
                self.canvas_grid[row][col].photo = photo
                self.second_player_label.config(text="PLAYER TWO", bg="red")
                self.first_player_label.config(text="Player One turn",
                    bg="lime green")
            winner, location_list = self.game.get_winner()
            if winner is not None:
                if winner == self.game.PLAYER_ONE:
                    self.color_winning_discs(location_list)
                    player = "player ONE"
                    messagebox.showinfo(WIN_TITLE, player + " " + WIN_MSG)
                elif winner == self.game.PLAYER_TWO:
                    self.color_winning_discs(location_list)
                    player = "player TWO"
                    messagebox.showinfo(WIN_TITLE, player + " " + WIN_MSG)
                else:
                    messagebox.showinfo(DRAW_TITLE, DRAW_MASSEGE)

    def color_winning_discs(self, winning_location_list):
        """
        The function gets a list of the winning discs and paints them in green.
        :param winning_location_list:
        :return:
        """
        print(winning_location_list)
        for x, y in winning_location_list:
            photo = PhotoImage(file="win.png")
            self.canvas_grid[y][x].configure(image=photo)
            self.canvas_grid[y][x].photo = photo

    ####################################################################
    def response_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator.
        :param text:
        :return: None.
        """
        if text:
            column = int(text)
            self.__add_disc(column)
            if self.ai_value and self.game.is_game_on:
                self.ai_value.find_legal_move(self.game, self.button_press)
        else:
            self.response_message(None)


def check_args(argv):
    """
    The function checks if the input is valid
    :param argv:
    :return: the function returns true if the input is valid and else otherwise
    """
    if len(argv) != NUMBER_OF_SERVER_ARGUMENTS + 1 and len(
            argv) != NUMBER_OF_CLIENT_ARGUMENTS + 1 or int(argv[2]) > MAX_PORT:
        #  checks if the number of arguments is ok
        print(ARGUMENTS_ERROR)
        return False
