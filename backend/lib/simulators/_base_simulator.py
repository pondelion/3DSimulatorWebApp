from abc import *
import json
from ..utils.util import load_params


class BaseSimulator:

    def __init__(self, simulator_name):
        self._MAX_HISTORY = 10000
        self._time = 0.
        self._simulator_name = simulator_name
        self._is_running = False
        self._params = {}
        self._minimal_dt = 0.01
        self._is_finished = False
        self._params = load_params(self._simulator_name)
        self.init()

    def run(self):
        """シミュレーションを開始する
        """
        self._is_running = True

    def stop(self):
        """シミュレーションを一時停止する
        """
        self._is_running = False

    def finish(self):
        """シミュレーションを終了する
        MUST : 継承クラスで実装
        """
        self._is_running = False
        self.init()

    def set_params(self, params):
        """パラメータを設定する
        """
        for key, val in params.items():
            self._params[key] = val
        self._on_update_params()

    @property
    def is_running(self):
        return self._is_running

    @property
    def minimal_dt(self):
        return self._minimal_dt

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
    def get_states(self, n=1):
        """最新状態(位置など)をn個返す
        """
        raise NotImplementedError()

    def get_states_streaming(self):
        while True:
            yield json.dumps(self.get_states())

    def _on_update_params(self):
        pass
