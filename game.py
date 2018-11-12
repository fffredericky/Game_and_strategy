"""
A class of all game move
"""
from typing import Any
from strategy import interactive_strategy
from game_state_checker import SSGstate, CGState


class Game:
    """
    general game class contains all general functions a game can do
    """

    def __init__(self, player_turn: bool) -> None:
        """
        initialize a new game
        """
        if player_turn:
            self.current_player = 'p1'
        else:
            self.current_player = 'p2'

    def get_instructions(self) -> str:
        """
        get instructions for player.
        """
        raise NotImplementedError("must implement a subclass!")

    def is_over(self, current_state) -> bool:
        """
        only return true when player has no valid/possible move
        """
        raise NotImplementedError("must implement a subclass!")

    def is_winner(self, player) -> bool:
        """
        annonce the winner of the game
        """
        raise NotImplementedError("must implement a subclass!")

    def current_strategy(self, game: Any) -> Any:
        """
        return current strategy for the player
        """
        return interactive_strategy(game)

    def str_to_move(self, move):
        """
        convert str to int and make the move
        """
        raise NotImplementedError("must implement a subclass!")


class SubtractSquareGame(Game):
    """
    Subtract Square Game class contains functions for Subtract Square
    """

    def __init__(self, player_turn: bool) -> None:
        """
        initialize a new game
        >>> a = SubtractSquareGame(True)
        >>> a.current_player
        p1
        """
        Game.__init__(self, player_turn)
        start_value = int(input('Please enter a starting value: '))
        self.current_state = SSGstate(self.current_player, start_value)

    def get_instructions(self) -> str:
        """
        get instructions for player.
        """
        ssgstrategy = 'Players take turns subtracting square numbers from ' \
                      'the starting number. The winner is the person who ' \
                      'subtract to 0.'
        return ssgstrategy

    def is_over(self, current_state: SSGstate) -> bool:
        """
        only return true when player has no valid/possible move
        >>> game = SubtractSquareGame(True)
        >>> game.current_state.current_value = 20
        >>> game.is_over(game.current_state)
        False
        >>> game.current_state.current_value = 0
        >>> game.is_over(game.current_state)
        True
        """
        return current_state.current_value == 0

    def is_winner(self, player: str) -> bool:
        """
        annonce the winner of the game
        >>> a = SubtractSquareGame(True)
        >>> a.current_state.current_value = 0
        >>> a.is_winner('p1')
        True
        >>> a.is_winner('p2')
        False
        """
        return self.current_state.current_value == 0 and \
               self.current_state.current_player != player

    def str_to_move(self, move: str) -> int:
        """
        convert str to int and make the move
        """
        move_to_make = int(move)
        return move_to_make


class ChopsticksGame(Game):
    """
    chopsticks game class contains all functions for the game
    """

    def __init__(self, player_turn: bool) -> None:
        """
        initialize a new game
        """
        Game.__init__(self, player_turn)
        player_hand = [1, 1, 1, 1]
        self.current_state = CGState(self.current_player, player_hand)

    def get_instructions(self) -> str:
        """
        get instructions for player.
        """
        cgst = 'Players take turns adding the values of one of their hands ' \
               'to one of their opponents(modulo 5). A hand with a total of ' \
               '5 (or 0; 5 modulo 5) is considered \'dead\'. The first ' \
               'player to have two dead hands is the loser.'
        return cgst

    def is_over(self, current_state: CGState) -> bool:
        """
        only return true when player has no valid/possible move
        >>> game = ChopsticksGame(True)
        >>> game.current_state.player_finger = [2, 3, 0, 0]
        >>> game.is_over(game.current_state)
        True
        >>> game2 = ChopsticksGame(True)
        >>> game2.current_state.player_finger = [0, 3, 4, 0]
        >>> game2.is_over(game2.current_state)
        False
        """
        return (current_state.p1_left == 0 and current_state.p1_right == 0) or \
               (current_state.p2_left == 0 and current_state.p2_right == 0)

    def is_winner(self, player: str) -> bool:
        """
        annonce the winner of the game
        >>> game = ChopsticksGame(True)
        >>> game.current_state.player_finger = [1, 2, 5, 5]
        >>> game.is_winner('p1')
        True
        >>> game.is_winner('p2')
        False
        """
        if player == 'p1':
            return self.current_state.p2_left == 0 and \
                   self.current_state.p2_right == 0
        return self.current_state.p1_left == 0 and \
               self.current_state.p1_right == 0

    def str_to_move(self, move: str) -> str:
        """
        convert input tp proper output
        >>> game = ChopsticksGame(True)
        >>> game.str_to_move('ll')
        ll
        >>> game.str_to_move('rr')
        rr
        >>> game2 = ChopsticksGame(False)
        >>> game2.str_to_move('ll')
        ll
        """
        return move


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config="a1_pyta.txt")
