from abc import *


class BaseSimulator:

    def __init__(self):
        self._time = 0.

    @abstractclassmethod
    def run(self):
        """シミュレーションを開始する
        MUST : 継承クラスで実装
        """
        raise NotImplementedError()

    @abstractclassmethod
    def stop(self):
        """シミュレーションを一時停止する
        MUST : 継承クラスで実装
        """
        raise NotImplementedError()

    @abstractclassmethod
    def end(self):
        """シミュレーションを終了する
        MUST : 継承クラスで実装
        """
        raise NotImplementedError()

    @abstractclassmethod
    def init(self):
        """初期化処理を行う
        MUST : 継承クラスで実装
        """
        raise NotImplementedError()

    @abstractclassmethod
    def get_states():
        """状態(位置など)を返す
        """
        raise NotImplementedError()

    def set_params(params):
        """パラメータを設定する
        """
        self._params = params