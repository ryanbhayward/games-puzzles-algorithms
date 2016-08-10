from games_puzzles_algorithms.choose \
    import choose_legal_action_uniformly_randomly
from games_puzzles_algorithms.players.mcts.mcts_agent \
    import UctNode, MctsAgent, uniform_random_roll_out_policy
from math import sqrt, log


class RaveNode(UctNode):
    
    def __init__(self, action=None, parent=None, acting_player=None, rave_limit=300):
        super(RaveNode, self).__init__(action, parent, acting_player)
        self.rave_N = 0
        self.rave_Q = 0
        self.rave_limit=rave_limit
        self.generator = RaveNode
        
        def ucb(self, explore=0):
            """Return the upper confidence bound of this node.
    
            The parameter `explore` specifies how much the value should favor
            nodes that have yet to be thoroughly explored versus nodes that
            seem to have a high win rate. `explore` is set to zero by default
            which means that the action with the highest winrate will have
            the greatest value.
            """
            if self.is_root():
                raise UctNode.RootNodeError("ucb is undefined for the root")
            elif self.N == 0:
                if explore == 0:
                    return 0
                else:
                    return INF
            else:
                alpha = max(0, self.rave_limit - self.N / self.rave_limit)
                value = self.Q * (1 - alpha) / self.N
                value += self.rave_Q * alpha / self.rave_N
                return value + explore * sqrt(2 * log(self.parent.N) / self.N)
    
        def lcb(self, explore=0):
            """Return the lower confidence bound of this node.
    
            The parameter `explore` specifies how much the value should favor
            nodes that have yet to be thoroughly explored versus nodes that
            seem to have a high win rate. `explore` is set to zero by default
            which means that the action with the highest winrate will have
            the greatest value.
            """
            # unless explore is set to zero, maximally favor unexplored nodes
            if self.is_root():
                raise UctNode.RootNodeError("lcb is undefined for the root")
            elif self.N == 0:
                return 0
            else:
                alpha = max(0, self.rave_limit - self.N / self.rave_limit)
                value = self.Q * (1 - alpha) / self.N
                value += self.rave_Q * alpha / self.rave_N
                return value - explore * sqrt(2 * log(self.parent.N) / self.N)            
        
    def backup(self, score=0, rave_moves={}):
        """Update the node statistics on the path from the passed node to
        root to reflect the value of the given `simulation_statistics`.
        """        
        self.N += 1
        self.Q += -score
        if self.acting_player in rave_moves:
            for child in self._children:
                if child.action in rave_moves[self.acting_player]:
                    child.rave_N += 1
                    child.rave_Q += score
        if self.parent:
            self.parent.backup(score=-score, rave_moves=rave_moves)  
            

class RaveAgent(MctsAgent):
    """A Monte Carle Tree Search Agent with Rapid Action Value Estimation."""
    
    def __init__(self,
                 node_generator=RaveNode,
                 exploration=1,
                 num_iterations=-1):
        super(RaveAgent, self).__init__(node_generator, exploration,
                                        num_iterations)    
    
    def roll_out(self, state, player_of_interest,
                 roll_out_policy=uniform_random_roll_out_policy, rave_moves={}):
        """
        Simulate a play-out from the passed game state, `state`.

        Return roll out statistics from the perspective of
        `player_of_interest`.
        """
        if state.is_terminal():
            return {'score': state.score(player_of_interest),
                    'rave_moves': state.rave_moves()}
        else:
            outcome = None
            action = roll_out_policy(state)
            with state.play(action):
                outcome = self.roll_out(state, player_of_interest)
            return outcome       