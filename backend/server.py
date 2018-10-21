from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import yaml
import logging


app = Flask(__name__)
CORS(app)

simulator = None
conf = yaml.load(open('./conf/conf.yaml'))


@app.route('/get_simulators')
def get_simulators():
    simulators = list(conf['SIMULATORS'].keys())
    print(simulators)
    res = jsonify({'simulators': simulators})
    res.status_code = 200
    return res


@app.route('/set_simulator')
def set_simulator():
    simulator_name = request.args.get('simulator')
    module_name = conf['SIMULATORS'][simulator_name]['MODULE_NAME']
    class_name = conf['SIMULATORS'][simulator_name]['CLASS_NAME']
    module = __import__(module_name, globals(), locals(), [class_name], 0)
    simulator_class = getattr(module, class_name)
    simulator = simulator_class()
    res = Response()
    res.status_code = 200
    print(simulator)
    return res


@app.route('/run_simulation')
def run_simulation():
    """シミュレートを実行する
    """
    simulator_name = request.args.get('simulator')


@app.route('/stop_simulation')
def stop_simulation():
    """シミュレートを一時停止する
    """
    simulator.stop()


@app.route('/end_simulation')
def end_simulation():
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
    print('get_param_names : ', simulator_name)
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


@app.route('/get_objects')
def get_objects():
    simulator_name = request.args.get('simulator')
    objects = conf['SIMULATORS'][simulator_name]['OBJECTS']
    print(objects)
    res = jsonify({'objects': dict(objects)})
    res.status_code = 200
    return res


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
