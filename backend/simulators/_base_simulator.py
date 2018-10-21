from abc import *


class BaseSimulator:

    def __init__(self):
        self._time = 0.
        self._is_running = False
        self._params = {}
        self.init()

    def run(self):
        """シミュレーションを開始する
        """
        self._is_running = True

    def stop(self):
        """シミュレーションを一時停止する
        """
        self._is_running = False

    def end(self):
        """シミュレーションを終了する
        MUST : 継承クラスで実装
        """
        self._is_running = False
        self.init()

    def set_params(params):
        """パラメータを設定する
        """
        self._params = params

    @abstractclassmethod
    def init(self):
        """初期化処理を行う
        MUST : 継承クラスで実装
        """
        raise NotImplementedError()

    @abstractclassmethod
    def update(self, dt):
        """更新処理を行う

        """
        raise NotImplementedError()

    @abstractclassmethod
    def get_states():
        """状態(位置など)を返す
        """
        raise NotImplementedError()
