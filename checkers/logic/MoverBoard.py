from checkers.logic.CheckersBoard import CheckersBoard
from typing import List, Tuple
import numpy as np
import itertools as it
from checkers.logic.bb_utils import print_bb
from checkers.CheckersConstants import CheckersConstants as ccs
from tqdm import tqdm


class MoverBoard(CheckersBoard):
    """
        Expands CheckersBoard: it is the board as seen from the moving player's perspective, regardless of color.
        More convenient for training the models.
        By convention, self.W are the moving pieces
    """

    def __init__(self, data_folder: str = None, board: CheckersBoard = None):
        super().__init__(data_folder, board)
        """
        self.np_board = np.zeros((8,4))
        self.np_board[0:3, :] = 1
        self.np_board[5:8, :] = -1
        """

    def can_move(self) -> bool:
        return self.bb_m.get_n_moves_possible(self.W, self.B, self.K, ccs.WHITE_TURN) > 0


    def reverse(self) -> None:
        tmp = self.W
        
        self.W = self.bb_m.bb_reverse(self.B)
        self.B = self.bb_m.bb_reverse(tmp)
        self.K = self.bb_m.bb_reverse(self.K)

    def get_canonical_perspective(self, turn: int) -> CheckersBoard:
        #return the board with white side on top

        ret = None
        if turn == ccs.BLACK_TURN:
            self.reverse()  
            ret = CheckersBoard(board=self)
            self.reverse()
        else:
            ret = CheckersBoard(board=self)
        return ret

    def generate_movers_and_moves(self) -> Tuple[np.ndarray, np.ndarray]:
        movers, moves, k_movers, k_moves = self._white_moves()
        jumpers, jumps, k_jumpers, k_jumps = self._white_jumps()

        ret_movers = []
        ret_moves = []

        n=1
        if jumpers != 0 or k_jumpers!=0:
            while n& 0xFFFFFFFF != 0:
                if n&jumpers != 0 or n&k_jumpers != 0:
                    iterator_j = self.dict_wj[n][0] if n&k_jumpers ==0 else it.chain(self.dict_wj[n][0], self.dict_bj[n][0])
                    iterator_m = self.dict_wj[n][1] if n&k_jumpers ==0 else it.chain(self.dict_wj[n][1], self.dict_bj[n][1])
                    for j, m in zip(iterator_j, iterator_m):
                        if j&jumps!= 0 and (self.B^self.K) & ~m != 0 or j&k_jumps != 0 and self.B & ~m != 0:
                            ret_movers.append(n)
                            ret_moves.append(j)
                n = n<<1
            return np.array(ret_movers), np.array(ret_moves)
        
        while n & 0xFFFFFFFF != 0:
            if n & movers != 0 or n & k_movers != 0:
                iterator = self.dict_wm[n] if n & k_movers == 0 else it.chain(self.dict_wm[n], self.dict_bm[n])
                for m in iterator:
                    if m & moves != 0 or m & k_moves != 0:
                        ret_movers.append(n)
                        ret_moves.append(m)
            n = n<<1

        return np.array(ret_movers), np.array(ret_moves)


    def generate_next(self) -> List[CheckersBoard]:
        movers, moves, k_movers, k_moves = self._white_moves()
        jumpers, jumps, k_jumpers, k_jumps = self._white_jumps()

        ret = []
        
        n=1

        if jumpers != 0 or k_jumpers != 0:
            while n & 0xFFFFFFFF !=0:
                if n & jumpers != 0 or n & k_jumpers !=0:
                    iterator_j = self.dict_wj[n][0] if n&k_jumpers ==0 else it.chain(self.dict_wj[n][0], self.dict_bj[n][0])
                    iterator_m = self.dict_wj[n][1] if n&k_jumpers ==0 else it.chain(self.dict_wj[n][1], self.dict_bj[n][1])
                    for j,m in zip(iterator_j, iterator_m):
                        if j&jumps!=0 and (self.B ^ self.K) & ~m != 0 and n&self.K == 0:
                            to_add = CheckersBoard()
                            to_add.W, to_add.B, to_add.K = self.bb_m.apply_jump(self.W, n, j, m, self.B, self.K, False)
                            ret.append(to_add)
                        elif j&k_jumps != 0 and self.B & ~m != 0:
                            to_add = CheckersBoard()
                            to_add.W, to_add.B, to_add.K = self.bb_m.apply_jump(self.W, n, j, m, self.B,  self.K, True)
                            ret.append(to_add)
                n=n<<1
            return ret
    
        while n & 0xFFFFFFFF != 0:
            if n & movers != 0 or n & k_movers != 0:
                iterator = self.dict_wm[n] if n & k_movers == 0 else it.chain(self.dict_wm[n], self.dict_bm[n])
                for m in iterator:
                    if m & moves != 0 or m & k_moves != 0:
                        to_add = CheckersBoard()
                        to_add.W, to_add.K = self.bb_m.apply_move(self.W, n, m, self.K, n& k_movers != 0)
                        to_add.B = self.B
                        ret.append(to_add)
            n = n<<1

        return ret

    def generate_games(self, nmbr_generated_game: int, canon: bool = True) -> Tuple[list[CheckersBoard], list[int], np.ndarray, np.ndarray]:
        boards_list = self.generate_next()
        turns_list = [ccs.WHITE_TURN for b in boards_list]
        branching_position = 0
        cur_turn = ccs.WHITE_TURN
	
        print("generating games")
        pbar = tqdm(total=nmbr_generated_game)
        while len(boards_list) < nmbr_generated_game:
            temp = len(boards_list)-1
            for i in range(branching_position, len(boards_list)):
                cur_board = MoverBoard(board=boards_list[i])
                cur_board.reverse()
                if cur_board.can_move():
                    next_gen = cur_board.generate_next()
                    next_turns = [cur_turn for b in next_gen]
                    boards_list += next_gen
                    turns_list+=next_turns
                    pbar.update(len(next_turns))
            branching_position = temp
            cur_turn = ccs.WHITE_TURN if cur_turn == ccs.BLACK_TURN else ccs.BLACK_TURN

        pbar.close()
        # calculate/save heuristic metrics for each game state
        metrics	= np.zeros((0, 6))
        winning = np.zeros((0, 1))

        print("processing games")
        for board, turn in tqdm(zip(boards_list[:nmbr_generated_game], turns_list[:nmbr_generated_game])):
            canon_b = MoverBoard(board = board).get_canonical_perspective(turn) if canon else MoverBoard(board=board)
            temp = canon_b.get_metrics()

            metrics = np.vstack((metrics, temp[1:]))
            winning = np.vstack((winning, temp[0]))

        
        return boards_list[:nmbr_generated_game], turns_list[:nmbr_generated_game], metrics, winning

