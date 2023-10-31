from checkers.AI.CheckersAI import CheckersAI
from checkers.logic.CheckersBoard import CheckersBoard
from checkers.logic.MoverBoard import MoverBoard
from checkers.AI.BoardModel import BoardModel
import numpy as np
import tensorflow as tf
import os
from checkers.logic.bb_utils import bb_to_np_compact
import numpy as np
from checkers.CheckersConstants import CheckersConstants as ccs

class DeepQAI(CheckersAI):
    def __init__(self, color: int, model_folder: str):
        super().__init__(color)

        self.model = BoardModel()
        metrics_path = os.path.join(model_folder, "reinforced",  "board_model.ckpt")
        status = self.model.load_weights(metrics_path)
        status.expect_partial()
    
    def _transform(self, b: MoverBoard) -> np.ndarray:
        return bb_to_np_compact(b.W, b.B, b.K).flatten()

    def get_next_state(self) -> MoverBoard:
        boards = self.board.generate_next()
        boards_np = list(map(self._transform, boards))
        boards_np = np.array(boards_np)

        preds = self.model.predict_on_batch(boards_np)

        move_i = np.argmax(preds) if self.color == ccs.WHITE_TURN else np.argmin(preds)
        
        return MoverBoard(board=boards[move_i])

    def evaluate_state(self) -> float:
        board_np = np.array([self._transform(self.board)])
        pred = self.model.predict_on_batch(board_np)
        return pred[0]