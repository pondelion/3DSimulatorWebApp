import requests
from .._base_simulator import BaseSimulator


class MaterialViewer(BaseSimulator):

    def __init__(self):
        self._MP_API_KEY = os.getenv('MATERIALS_PROJECT_API_KEY')
        self._API_URL = {
            'structure': 'https://www.materialsproject.org/rest/v2/materials/{element}/vasp/structure?API_KEY={API_KEY}'
        }

    def init(self):
        pass

    def _request_structure(self, element):
        res = requests.get(self._API_URL['structure'].format(element=element, API_KEY=self._MP_API_KEY))
        return res

    def _parse_structure(res):
        structure = res.json()['response'][0]['structure']
