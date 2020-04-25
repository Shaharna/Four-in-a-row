#############################################################################
# FILE: game.py
# WRITERS: Ayal Meitar, ayal.meitar, 309981215, Shahar Nahum, shaharna13,
# 313586877
# EXERCISE: intro2cs ex12 2017-2018
# DESCRIPTION: The file includes the class Ai, which represents the computers
# game logic
#############################################################################

#############################################################################
# imports
#############################################################################
import random
############################################################################
# Constants
#############################################################################
COL_SIZE = 7
EMPTY_SPOT = None


class AI:

    EXCEPTION_NO_POSSIBLE_AI_MOVE = "No possible AI moves."

    def find_legal_move(self, g, func, timeout=None):
        """
        The function randomize a value between 0 to 6 which is also a legal
        move. Then the function sends it to the function received.
        :param g:
        :param func:
        :param timeout:
        :return:
        """
        error_set = set()
        col = random.randrange(0, 7, 1)
        while g.get_board()[0][col] != EMPTY_SPOT and len(error_set) < \
                COL_SIZE:
            error_set.add(col)
            col = random.randrange(0, 7, 1)
        if len(error_set) == COL_SIZE:
            raise NoPossibleMove(self.EXCEPTION_NO_POSSIBLE_AI_MOVE)
        else:
            func(col)


class NoPossibleMove(Exception):
    """
    The exception raised when there are no possible AI move
    """
    pass
