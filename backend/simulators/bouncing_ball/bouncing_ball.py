from .._base_simulator import BaseSimulator


class BouncingBall(BaseSimulator):
    GRAVITY_ACCEL = 9.8

    def __init__(self):
        super().__init__(self)

    def init(self):
        """初期化処理を行う
        """
        pass

    def update(self, dt):
        """更新処理を行う
        """
        pass

    def get_states():
        """状態(位置など)を返す
        """
        pass
