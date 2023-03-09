import json
import random
import time

from resources.machines.base.cnc_machine_base import TxtMachineWorker
import concurrent.futures
from datetime import datetime, timedelta


def set_global():
    global config
    global pcs
    file = open("conf_file.json", 'r')
    config = json.load(file)
    pcs = 0


def line_method(worker, work_name, qtd_pcs):
    print(f'Line:{work_name}({qtd_pcs}un) starting....\n')
    for i in range(qtd_pcs):
        worker.make_part(work_name + f'__{i}')
    print(f'Line:{work_name}({qtd_pcs}un) end job....\n')
    return qtd_pcs


def enable_line(word):
    print(word)
    return 0


def machine_method(id_line, start_date):
    global config
    global pcs
    FILIAL_CODE = '0001'
    m_id = f'TxtWorker_Filial{FILIAL_CODE}__{id_line}'
    wjson = TxtMachineWorker(machine_id=m_id, work_name=f'Line{id_line}')
    job = 0
    exec_days = (datetime.now() + timedelta(days=1)) - start_date
    lines_working = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=(config.get('each_machine_line')),
                                               initializer=set_global) as factory_machines:
        for i in range(config.get('each_machine_line')):
            line_running = factory_machines.submit(enable_line, f'Machine n: {i} from{id_line} now is running...')
            lines_working[line_running] = f'{m_id}__{i}'
        while True:
            job += 1
            for l in concurrent.futures.as_completed(lines_working):
                work_name = f'machinejson_{lines_working[l]}_ln__job_{job}'
                if (exec_days.days % config.get('inconsistence').get('each_days')) == 0 and \
                        (24 % config.get('inconsistence').get('times_per_day')) == 0:
                    print('Tilit in factory.\n')
                    time.sleep(60 * config.get('inconsistence').get('inconsistency_duration'))
                try:
                    name = lines_working[l]
                    if not l.running():
                        qtd = random.randint(20, 30)
                        line = factory_machines.submit(line_method, wjson, work_name, qtd)
                        pcs += l.result()
                        lines_working.pop(l)
                        lines_working[line] = name
                    if l.done():
                        print(f'total parts buids: {pcs}\n')
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    set_global()
    start_date = datetime.now()
    work_nums = config.get('machine_number') * config.get('each_machine_line') + 1
    machines = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=work_nums, initializer=set_global) as factory:
        print('Factory now is open!')
        for machine_work in range(config.get('machine_number')):
            print(f'Initialize machine numer:{machine_work}')
            machine_running = factory.submit(machine_method, f'_{machine_work}', start_date)
            machines.append(machine_running)
        stopped_machines = 0
        for i in concurrent.futures.as_completed(machines):
            stopped_machines += 1
            print('Machine {i}, error: ', i.exception(), '\n')
            if stopped_machines == config.get('machine_number'):
                print('Factory was stoped..........\n')
