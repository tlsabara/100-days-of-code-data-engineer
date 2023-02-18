from datetime import datetime
import time
import os
from pathlib import Path
from random import randint, choice
import json
from abc import ABC, abstractmethod
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

SAVE_DIR = Path(os.path.abspath(os.curdir))

class Machine(ABC):
    type = 'abc'
    def __init__(self, machine_id, machine_ip='0.0.0.0/0', work_name='Project1') -> None:
        self.base_model = {
            'time': 0,
            'machine_id': machine_id,
            'ip_machine': machine_ip,
            'work_model_name': work_name,
            'work_model_weight': 0,
            'work_model_height': 0,
            'work_model_width': 0,
            'work_model_error_margin': 0.0001,
            'work_model_total_time': 0
        }
        self.save_folder = SAVE_DIR / f'machine_{self.type}_{machine_id}'

    def _core_generator(self):
        export_model = self.base_model.copy()
        self.save_folder.mkdir(parents=True, exist_ok=True)

        virtual_duration = randint(1, 5)
        start_work = datetime.now()
        time.sleep(virtual_duration)
        virtual_error = randint(1, 1000) / 10000
        work_model_weight = 100 + (randint(1, 50)/10)
        work_model_height = 20 + (randint(1, 50)/10)
        work_model_width = 40 + (randint(1, 50)/10)

        export_model["time"] = start_work.strftime('%Y-%m-%d-%H-%M-%S')
        export_model["work_model_weight"] = work_model_weight
        export_model["work_model_height"] = work_model_height
        export_model["work_model_width"] = work_model_width
        export_model["work_model_error_margin"] = virtual_error
        total_time = datetime.now() - start_work
        export_model["work_model_total_time"] = total_time.total_seconds()

        self.export_model = export_model

    @abstractmethod
    def _work_report(self, filename):
        ...

    def make_part(self, filename):
        self._core_generator()
        self._work_report(filename)


class JsonMachineWorker(Machine):
    type = 'json'
    def _work_report(self, filename):
        jsonstring = json.dumps(self.export_model, indent=4, sort_keys=True, default=str)
        with open(self.save_folder / f'{filename}.{self.type}', 'w') as file:
            file.writelines(jsonstring)


class XmlMachineWorker(Machine):
    type = 'xml'
    def _work_report(self, filename):
        xml = dicttoxml(self.export_model)
        with open(self.save_folder / f'{filename}.{self.type}', 'w') as file:
            file.writelines(parseString(xml).toprettyxml())


class TxtMachineWorker(Machine):
    type = 'txt'
    def _work_report(self, filename):
        # Este worker gera arquivos com falha
        junk_str = [f'{k}:{v} | ' if choice((True,False,True,True)) else f'{k}: | ' for k, v in self.export_model.items()]

        with open(self.save_folder / f'{filename}.{self.type}', 'w') as file:
            file.writelines(junk_str)



if __name__ == '__main__':
    wjson = JsonMachineWorker(machine_id='JsonWorkerFilial1',work_name='ProjectA')
    wxml = XmlMachineWorker(machine_id='XmlWorkerFilial1',work_name='ProjectB')
    wtxt = TxtMachineWorker(machine_id='TxtWorkerFilial1',work_name='ProjectB')
    for i in range(10):
        wjson.make_part(f'wjson_{i}')
        wxml.make_part(f'wxml_{i}')
        wtxt.make_part(f'wtxt_{i}')
