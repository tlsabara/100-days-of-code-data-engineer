import random
import time

from resources.machines.base.cnc_machine_base import JsonMachineWorker
import concurrent.futures
from datetime import datetime, timedelta


def set_global(args):
    global sval
    global config
    global pcs
    sval = args
    config = {
        'machine_number': 4,
        'each_machine_line': 3,
        'machine_prefix_name': 'JSONMACHINE_FORK1',
        'inconsistence': {
            'each_days': 3,
            'times_per_day': 4,
            'inconsistency_duration': 15
        }
    }
    pcs = 0
def line_method(worker, work_name, qtd_pcs):
    print(f'\nLine:{work_name}({qtd_pcs}un) iniciado....\n')
    for i in range(qtd_pcs):
        worker.make_part(work_name + f'__{i}')
        print('New part: ', work_name + f'__{i}')
        pcs +=1
    print(f'\nLine:{work_name}({qtd_pcs}un) finalizado....\n')


def machine_method(id_line, start_date, config):
    FILIAL_CODE = '0001'
    m_id = f'JsonWorker_Filial{FILIAL_CODE}__{id_line}'
    wjson = JsonMachineWorker(machine_id=m_id, work_name=f'Line{id_line}')
    job = 0
    exec_days = (datetime.now() + timedelta(days=1)) - start_date
    lines_working = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=(config.get('machine_number')), initializer=set_global) as factory_machines:
        for i in range(config.get('each_machine_line')):
            line_running = factory_machines.submit(print, f'Machine n: {i} now is running...')
            lines_working.append(line_running)
        while True:
            work_name = f'machinejson_{m_id}_job_{job}'
            for i in concurrent.futures.as_completed(lines_working):
                # if not i.running():
                if (exec_days.days % config.get('inconsistence').get('each_days')) == 0 and \
                        (24 % config.get('inconsistence').get('times_per_day')) == 0:
                    time.sleep(60 * config.get('inconsistence').get('inconsistency_duration'))
                job += 1
                try:
                    lines_working.remove(i)
                    time.sleep(1)
                    print('New Job.....')
                    line = factory_machines.submit(line_method, wjson, work_name, random.randint(10, 30))
                    while not line.running():
                        time.sleep(0.5)
                        print('peças atuais:', pcs)
                        print('finishing......')
                    lines_working.append(line)
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    start_date = datetime.now()
    work_nums =  + config.get('each_machine_line') - 1
    machines = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=(config.get('machine_number')*3), initializer=set_global) as factory:
        print('Factory now is open!')
        for machine_work in range(config.get('machine_number')):
            print(f'Ligando máquina!  mch:{machine_work}')
            machine_running = factory.submit(machine_method, f'_{machine_work}', start_date, config)
            machines.append(machine_running)
        for i in concurrent.futures.as_completed(machines):
            print(i.exception())



