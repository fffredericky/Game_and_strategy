"""
A game state checker
"""
from typing import Any, List


class State:
    """
    checker class to give player game state/feedback
    """

    def __init__(self, current_player: str) -> None:
        """
        initialize a new game state for a game
        """
        self.current_player = current_player
        self.move = []

    def __str__(self) -> str:
        """
        return a string representation of the game state
        """
        raise NotImplementedError("must implement a subclass!")

    def __eq__(self, other):
        """
        compare the current game state to other
        """
        raise NotImplementedError("must implement a subclass!")

    def get_possible_moves(self):
        """
        get possible moves for player.
        """
        raise NotImplementedError("must implement a subclass!")

    def get_current_player_name(self) -> str:
        """
        get current player's name.
        """
        return self.current_player

    def make_move(self, move_to_make):
        """
        make a move
        """
        raise NotImplementedError("must implement a subclass!")


class SSGstate(State):
    """
    a subclass contains every function for checking the game state for \
    SubtractSquareGame
    """

    def __init__(self, current_player: str, start_value: int) -> None:
        """
        initialize a new game state for a game
        >>> a = SSGstate('p1')
        >>> a.current_player
        p1
        """
        State.__init__(self, current_player)
        self.current_value = start_value

    def __str__(self) -> str:
        """
        return a string representation of the game state
        >>> game_state = SSGstate('p2', 20)
        >>> print(game_state)
        Current Player: Player 2 - Current Value: 20
        """
        if self.current_player == 'p1':
            return 'Current Player: {} - Current Value: {}'.format(
                'Player 1', str(self.current_value))
        return 'Current Player: {} - Current Value: {}'.format(
            'Player 2', str(self.current_value))

    def __eq__(self, other: Any) -> bool:
        """
        compare the current game state to other
        >>> a = SSGstate('p1')
        >>> b = SSGstate('p2')
        >>> a == b
        False
        """
        return type(self) == type(other) and self.current_player == other.\
            current_player and self.current_value == other.current_value and \
               self.move == other.move and self.current_value == \
               other.current_value

    def get_possible_moves(self) -> List[int]:
        """
        get possible moves for player.
        >>> a = SSGstate('p1')
        >>> a.current_value = 20
        >>> a.get_possible_moves()
        [1, 4, 9, 16]
        >>> a = SSGstate('p1')
        >>> a.current_value = 1
        >>> a.get_possible_moves()
        [1]
        """
        if self.current_value != 0:
            self.move.append(1)
            for i in range(1, self.current_value):
                if i ** 2 <= self.current_value and i ** 2 not in self.move:
                    self.move.append(i ** 2)
        return self.move

    def is_valid_move(self, move) -> bool:
        """
        check if player's move is valid
        """
        return move in self.move

    def make_move(self, move_to_make: str) -> "SSGstate":
        """
        make a move and return the new state
        """
        if self.current_player == 'p1':
            new_state = SSGstate('p2', self.current_value - int(move_to_make))
        else:
            new_state = SSGstate('p1', self.current_value - int(move_to_make))
        return new_state


class CGState(State):
    """
    checker class to give player game state/feedback
    """

    def __init__(self, current_player: str, player_hand: List[int]) -> None:
        """
        initialize a new game state for a game
        >>> game = CGState('p1', [1, 1, 1, 1])
        >>> game.player_finger
        [1, 1, 1, 1]
        >>> game = CGState('p2', [3, 4, 0, 2])
        >>> game.player_finger
        [3, 4, 0, 2]
        >>> game.p1_left
        3
        """
        State.__init__(self, current_player)
        self.p1_left = player_hand[0]
        self.p1_right = player_hand[1]
        self.p2_left = player_hand[-2]
        self.p2_right = player_hand[-1]
        self.player_finger = player_hand

    def __str__(self) -> str:
        """
        return a string representation of the game state
        >>> game = CGState('p1', [1, 1, 1, 1])
        >>> print(game)
        Current Player: Player 1, Player 1: 1 - 1, Player 2: 1 - 1
        """
        if self.current_player == 'p1':
            return 'Current Player: Player 1, Player 1: {} - {}, Player 2: ' \
                   '{} - {}'.format(self.p1_left, self.p1_right,
                                    self.p2_left, self.p2_right)
        return 'Current Player: Player 2, Player 1: {} - {}, Player 2: {} - ' \
               '{}'.format(self.p1_left, self.p1_right, self.p2_left,
                           self.p2_right)

    def __eq__(self, other: Any) -> bool:
        """
        compare the current game state to other
        >>> game = CGState('p1', [1, 1, 1, 1])
        >>> game2 = SSGstate('p1', 10)
        >>> game == game2
        False
        >>> game3 = CGState('p1', [1, 1, 1, 1])
        >>> game == game3
        True
        """
        return type(self) == type(other) and self.current_player == \
               other.current_player and self.p2_right == other.p2_right \
               and self.p2_left == other.p2_left and self.p1_right == \
               other.p1_right and self.p1_left == other.p1_left and \
               self.move == other.move

    def is_valid_move(self, move) -> bool:
        """
        check if player's move is valid
        """
        return move in self.move

    def get_possible_moves(self) -> List[str]:
        """
        get possible moves for player.
        >>> game_state = CGState('p1', [0, 1, 0, 1])
        >>> game_state.get_possible_moves()
        ['rr']
        >>> game_state2 = CGState('p1', [3, 4, 0, 2])
        >>> game_state2.get_possible_moves()
        ['lr', 'rr']
        >>> game_state3 = CGState('p1', [0, 0, 1, 2])
        >>> game_state3.get_possible_moves()
        []
        """
        self.move = ['ll', 'lr', 'rl', 'rr']
        if self.current_player == 'p1':
            self.get_possible_movesp1()
        elif self.current_player == 'p2':
            self.get_possible_movesp2()
        return self.move

    def get_possible_movesp2(self) -> None:
        """
        modify possible moves list for player 2.
        """
        if self.player_finger[0] == 0:
            self.move.remove('ll')
            self.move.remove('rl')
        if self.player_finger[1] == 0:
            self.move.remove('lr')
            self.move.remove('rr')
        if self.player_finger[2] == 0:
            if 'lr' in self.move:
                self.move.remove('lr')
            if 'll' in self.move:
                self.move.remove('ll')
        if self.player_finger[3] == 0:
            if 'rl' in self.move:
                self.move.remove('rl')
            if 'rr' in self.move:
                self.move.remove('rr')

    def get_possible_movesp1(self) -> None:
        """
        modify possible moves list for player 1.
        """
        if self.player_finger[0] == 0:
            self.move.remove('ll')
            self.move.remove('lr')
        if self.player_finger[1] == 0:
            self.move.remove('rl')
            self.move.remove('rr')
        if self.player_finger[2] == 0:
            if 'rl' in self.move:
                self.move.remove('rl')
            if 'll' in self.move:
                self.move.remove('ll')
        if self.player_finger[3] == 0:
            if 'lr' in self.move:
                self.move.remove('lr')
            if 'rr' in self.move:
                self.move.remove('rr')

    def make_move(self, move: str) -> "CGState":
        """
        make a move
        >>> game_state = CGState('p1', [1, 2, 3, 4])
        >>> new_game_state = game_state.make_move('ll')
        >>> new_game_state.current_player
        'p2'
        >>> new_game_state.player_finger
        [1, 2, 4, 4]
        """
        if self.current_player == 'p1':
            if move == 'll':
                return CGState('p2', [self.p1_left, self.p1_right,
                                      (self.p1_left + self.p2_left) % 5,
                                      self.p2_right])
            elif move == 'lr':
                return CGState('p2', [self.p1_left, self.p1_right,
                                      self.p2_left, (self.p1_left +
                                                     self.p2_right) % 5])
            elif move == 'rr':
                return CGState('p2', [self.p1_left, self.p1_right, self.p2_left,
                                      (self.p1_right + self.p2_right) % 5])
            return CGState('p2', [self.p1_left, self.p1_right,
                                  (self.p1_right + self.p2_left) % 5,
                                  self.p2_right])
        if move == 'll':
            return CGState('p1', [(self.p1_left + self.p2_left) % 5,
                                  self.p1_right, self.p2_left, self.p2_right])
        elif move == 'rl':
            return CGState('p1', [(self.p1_left + self.p2_right) % 5,
                                  self.p1_right, self.p2_left, self.p2_right])
        elif move == 'rr':
            return CGState('p1', [self.p1_left,
                                  (self.p1_right + self.p2_right) % 5,
                                  self.p2_left, self.p2_right])
        p1l = self.p1_left
        p1r = (self.p1_right + self.p2_left) % 5
        p2l = self.p2_left
        p2r = self.p2_right
        return CGState('p1', [p1l, p1r, p2l, p2r])


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
