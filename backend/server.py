from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import yaml
import logging
from lib.simulator_runner.multithread import SimulatorRunner


app = Flask(__name__)
CORS(app)

simulator_runner = SimulatorRunner()
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
    ip = request.remote_addr
    simulator_name = request.args.get('simulator')
    simulator_runner.create_simulator(
        ip,
        simulator_name,
        conf['SIMULATORS'][simulator_name]['MODULE_NAME'],
        conf['SIMULATORS'][simulator_name]['CLASS_NAME']
    )
    res = Response()
    res.status_code = 200
    return res


@app.route('/run_simulation')
def run_simulation():
    """シミュレートを実行する
    """
    ip = request.remote_addr
    simulator_name = request.args.get('simulator')
    simulator_runner.run(ip, simulator_name)
    res = Response()
    res.status_code = 200
    return res


@app.route('/stop_simulation')
def stop_simulation():
    """シミュレートを一時停止する
    """
    ip = request.remote_addr
    simulator_name = request.args.get('simulator')
    simulator_runner.stop(ip, simulator_name)
    res = Response()
    res.status_code = 200
    return res


@app.route('/finish_simulation')
def finish_simulation():
    """シミュレートを終了
    """
    ip = request.remote_addr
    simulator_name = request.args.get('simulator')
    simulator_runner.finish(ip, simulator_name)
    res = Response()
    res.status_code = 200
    return res


@app.route('/set_params')
def set_params():
    """パラメータをセットする。
    """
    args = dict(request.args)
    simulator_name = args.pop('simulator')
    data_type = args.pop('data_type')
    params = {}
    for key, val in args.items():
        if data_type[0] == 'numeric':
            params[key] = float(val[0])
    print(params)
    ip = request.remote_addr
    simulator_runner.set_params(ip, simulator_name[0], params)
    res = Response()
    res.status_code = 200
    return res


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
    res = jsonify({
        'objects': dict(objects)
    })
    res.status_code = 200
    return res


@app.route('/get_states')
def get_states():
    n = request.args.get('n', default=1)
    simulator_name = request.args.get('simulator')
    ip = request.remote_addr
    states = simulator_runner.get_states(ip, simulator_name, int(n))
    res = jsonify({
        'states': states
    })
    res.status_code = 200
    return res


@app.route('/get_states_definition')
def get_states_definition():
    simulator_name = request.args.get('simulator')
    stetes_definition = conf['SIMULATORS'][simulator_name]['STATES_DEFINITION']
    res = jsonify({
        'states_definition': dict(stetes_definition)
    })
    res.status_code = 200
    return res


@app.route('/get_states_streaming')
def get_states_streaming():
    simulator_name = request.args.get('simulator')
    ip = request.remote_addr
    streming_func = simulator_runner.get_states_streaming_func(ip, simulator_name)
    return Response(streming_func(), content_type='application/json')


@app.route('/init_simulation')
def init_simulation():
    ip = request.remote_addr
    simulator_name = request.args.get('simulator')
    simulator_runner.init(ip, simulator_name)
    res = Response()
    res.status_code = 200
    return res


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', threaded=True)
