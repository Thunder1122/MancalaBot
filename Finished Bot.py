# File: Player.py
# Author(s) names AND netid's: Tushar Chandra, tac311; Vyas Alwar, vaa143; Trent Cwiok, tbc808
# Date: 4/22/2016
# Group work statement: "All group members were present and contributing during all work
# on this project."
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from random import *
from decimal import *
from copy import *
from MancalaBoard import *
import time

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """

        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s

        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """

        # hardcode the first couple of moves that have been proven to be optimal

        # If we're P1 and it's the first move, make move 3 then move 6 on the extra turn
        if board.P1Cups == [4] * 6 and board.P2Cups == [4] * 6 and self.num == 1:
            return INFINITY, 3

        # second move for the above scenario
        if board.P1Cups == [4, 4, 0, 5, 5, 5] and board.P2Cups == [4] * 6 and board.scoreCups[0] == 1 and self.num == 1:
            return INFINITY, 6

        # response to counterplays to the above opening strategy, again assuming we're P1
        if board.P1Cups == [4, 4, 0, 5, 5, 0] and board.P2Cups[0] == 0 and self.num == 1:
            # if we made the move above, and they move 1 or 2-1, then their first cup is empty.
            # we play defensively and move our 5th cup            
            return INFINITY, 5

        # another response to counterplays to the above opening strategy, again assuming we're P1
        if board.P1Cups[0] == 5 and board.scoreCups[1] == 2 and board.P2Cups[0] == 5 and self.num == 1:
            # if we made the move above, they move 2-!1 iff the above conditions hold
            # in this case, their first cup has 5 stones, and we can raid it with our first cup
            return INFINITY, 1

        # If we're P2, then if they play 3-6, the best response is 2-1 
        if board.P1Cups == [4, 4, 0, 5, 5, 0] and board.P2Cups == [5, 5, 5, 5, 4, 4] and self.num == 2:
            return INFINITY, 2

        # second move for this scenario
        if board.P1Cups == [4, 4, 0, 5, 5, 0] and board.P2Cups == [5, 0, 6, 6, 5, 5] and self.num == 2:
            return INFINITY, 1

        start = time.clock()
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValueAB(nb, ply-1, turn, -INFINITY, INFINITY)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s

            # cutoff after 10 seconds
            if time.clock() - start > 10:
                break

        print time.clock() - start

        #return the best score and move so far
        return score, move

    def maxValueAB(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValueAB(nextBoard, ply-1, turn, alpha, beta)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
                if score > beta:
                    return score

            alpha = max(alpha, score)

        return score
    
    def minValueAB(self, board, ply, turn, alpha, beta):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValueAB(nextBoard, ply-1, turn, alpha, beta)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
                if score < alpha:
                    return score

            beta = min(beta, score)

        return score
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "p", self.num, " chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "p", self.num, " chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "p", self.num, " chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.

            # Use the alpha-beta pruning

            val, move = self.alphaBetaMove(board, 9)
            print "p", self.num, " chose move", move, " with value", val
            return move

        else:
            print "Unknown player type"
            return -1


# Note, you should change the name of this player to be your netid
class tbc808(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):
        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board

        # HEURISTICS:
        # 1. (Stones in my mancala - stones in theirs)
        # 2. How close the opponent is to winning 
        #    calculated as 25 - (stones in their mancala)
        #    where higher means they have fewer stones and are
        #    farther away from winning.   
        # 3. Multiplier for having a move that will give you 
        #    an extra turn. 

        if self.num == 1: # player 1
            p1score = (board.scoreCups[0] - board.scoreCups[1]) #1
            p1score += (25 - board.scoreCups[1]) #2
            for i in range(6): #3
                if board.P1Cups[i] == abs((i + 1) - 6):
                    p1score *= 1.5

            return p1score

        else: # player 2
            p2score = (board.scoreCups[1] - board.scoreCups[0]) #1
            p2score += (25 - board.scoreCups[0]) #2
            for i in range(6): #3
                if board.P2Cups[i] == abs((i + 1) - 6):
                    p2score *= 1.5
          
            return p2score