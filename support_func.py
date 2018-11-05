# Based on the request of the project
# Need to achieve a baseline algorithem
# This file will design a minimax algorithem with Alpha-Beta Pruning

# Most part of the code is referred to the one mentioned in the lecture

from isolation.isolation import _WIDTH, _HEIGHT

def alpha_beta_search(state, _id, depth=3):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.
    
    You can ignore the special case of calling this function
    from a terminal state.
    """

    def min_value(state, alpha, beta, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if state.terminal_test():
            return state.utility(_id)
        if depth <= 0: return score(state, _id)
        v = float("inf")
        for a in state.actions():
            v = min(v, max_value(state.result(a), alpha, beta, depth-1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v
    
    def max_value(state, alpha, beta, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if state.terminal_test():
            return state.utility(_id)
        if depth <= 0: return score(state, _id)
        v = float("-inf")
        for a in state.actions():
            v = max(v, min_value(state.result(a), alpha, beta, depth-1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = None
    for a in state.actions():
        v = min_value(state.result(a), alpha, beta, depth-1)
        alpha = max(alpha, v)
        if v > best_score:
            best_score = v
            best_move = a
    return best_move

def score(state, _id):
    own_loc = state.locs[_id]
    opp_loc = state.locs[1 - _id]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties)



