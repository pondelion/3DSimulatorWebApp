from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import yaml
import logging


app = Flask(__name__)
CORS(app)

simulator = None
conf = yaml.load(open('../conf/conf.yaml'))


@app.route('/get_simulators')
def simulators():
    simulators = list(conf['SIMULATORS'].keys())
    print(simulators)
    res = jsonify({'simulators': simulators})
    res.status_code = 200
    return res


@app.route('/run_simulation')
def run():
    """シミュレートを実行する
    """
    simulator_name = request.args.get('simulator')


@app.route('/stop_simulation')
def stop():
    """シミュレートを一時停止する
    """
    simulator.stop()


@app.route('/end_simulation')
def end():
    """シミュレートを終了
    """
    simulator.end()
    del simulator
    simulator = None


@app.route('/set_params')
def set_params():
    """パラメータをセットする。
    """
    params = request.args.get('params')
    simulator.set_params(params)


@app.route('/get_param_names')
def get_param_names():
    """指定のシミュレータのパラメータ名リストを返す。
    """
    simulator_name = request.args.get('simulator')
    print(simulator_name)
    try:
        param_names = conf['SIMULATORS'][simulator_name]['PARAM_NAMES']
    except Exception as e:
        print(e)
        res = jsonify({
            'error': e
        })
        res.status_code = 500
        return res
    res = jsonify({'param_names': dict(param_names)})
    res.status_code = 200
    return res


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
