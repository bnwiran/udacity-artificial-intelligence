
from sample_players import DataPlayer

_WIDTH = 11
_HEIGHT = 9

class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
     
        depth = 1
        while True:
            action = self.__next_move(state, depth)
            self.queue.put(action)
            depth += 1
            
    
    def __next_move(self, state, depth):
        alpha = float("-inf")
        beta = float("inf")
        best_score = float("-inf")
        best_move = None
        for a in state.actions():
            v = self.__min_value(state.result(a), alpha, beta, depth-1)
            alpha = max(alpha, v)
            if v >= best_score:
                best_score = v
                best_move = a
                
        return best_move
    
        
    def __min_value(self, state, alpha, beta, depth):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if state.terminal_test():
            return state.utility(self.player_id)
        
        if depth <= 0:
            return self.__h(state)

        v = float("inf")
        for a in state.actions():
            v = min(v, self.__max_value(state.result(a), alpha, beta, depth-1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v


    def __max_value(self, state, alpha, beta, depth):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if state.terminal_test():
            return state.utility(self.player_id)
        
        if depth <= 0:
            return self.__h(state) 

        v = float("-inf")
        for a in state.actions():
            v = max(v, self.__min_value(state.result(a), alpha, beta, depth-1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    
    
    def __h(self, state):
        available0 = state.liberties(state.locs[self.player_id])
        available1 = state.liberties(state.locs[1-self.player_id])
        
        on_border0 = [ind for ind in available0 if self.__is_loc_on_border(ind)]
        on_border1 = [ind for ind in available1 if self.__is_loc_on_border(ind)]
        
        return 2*(len(available0) - len(on_border0)) - 3*(len(available1) - len(on_border1))
    
    
    def __is_loc_on_border(self, ind):
        loc = (ind % (_WIDTH+2), ind // (_WIDTH+2))
        if loc[0] == 0 or loc[1] == 0:
            return True
        
        if (loc[0] + 1) >= _WIDTH:
            return True
        
        if (loc[1] + 1) >= _HEIGHT:
            return True
        
        return False