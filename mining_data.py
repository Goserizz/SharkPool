from bs4 import BeautifulSoup
import requests
import json
import time


eth_address = '0x06519c33453b8b45c0884f48355602c17bf59d4e'
url = "https://www.beepool.org/get_miner?coin=eth&wallet={}".format(eth_address)
log_file = 'log'


def get_data():
    response = requests.get(url)
    return json.loads(response.text)


def get_balance(res_json):
    balance = res_json['data']['account']['balance']
    all_balance = res_json['data']['account']['all_balance']
    pay_balance = res_json['data']['account']['pay_balance']
    return balance, all_balance, pay_balance

def get_workers(res_json):
    active_workers = res_json['data']['miner']['activeWorkers']['list']
    inactive_workers = res_json['data']['miner']['inactiveWorkers']['list']
    return active_workers + inactive_workers


def balance_log(now_balance, now_all_balance, now_earn):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open(log_file, mode='a') as f:
        f.writelines("{} balance: {}, all_balance: {}, +{} ETH.\n".format(now_time, now_balance, now_all_balance, now_earn))


def earn_log(worker, hashrate, contri, earn, now_bal):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open(log_file, mode='a') as f:
        f.writelines("{} {}: 4h hashrate is {}, contributes {:.2f}% calculation, earns {}({} total) ETH.\n".format(now_time, worker, hashrate, contri, earn, now_bal))


def settle_log(worker, deposit, remains):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open(log_file, mode='a') as f:
        f.writelines("{} Settlement: {} deposits {} ETC, remains {} ETC.\n".format(now_time, worker, deposit, remains))


def del_log(worker):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open(log_file, mode='a') as f:
        f.writelines("{} Deletion: {} is inactive and settled, deleted.\n".format(now_time, worker))


if __name__ == '__main__':
    res_json = get_data()
    print(res_json)
    now_workers = get_workers(res_json)
    now_balance, now_all_balance, _ = get_balance(res_json)
    
    with open('datas.json', mode='r') as f:
        datas = json.load(f)
        balance = datas['balance']
        all_balance = datas['all_balance']
        workers = datas['workers']
    
    now_earn = now_all_balance - all_balance
    balance_log(now_balance, now_all_balance, now_earn)
    whole_cal = 0
    
    for worker in now_workers:
        if worker['avg_30_hashrate'] == 0:
            continue
        worker_name = worker['name']
        if worker_name not in workers:
            workers[worker_name] = 0
        whole_cal += worker['avg_30_hashrate']

    settle_workers = list()
    
    for worker in now_workers:
        if worker['avg_30_hashrate'] == 0:
            continue
        worker_name = worker['name']
        hashrate = worker['avg_30_hashrate']
        contri = hashrate / whole_cal
        earn = now_earn * contri
        workers[worker_name] += earn
        if contri > 0:
            earn_log(worker_name, hashrate, contri * 100, earn, workers[worker_name])
        if now_balance < balance:
            remains = now_balance * contri
            deposit = workers[worker_name] - remains
            workers[worker_name] = remains
            settle_log(worker_name, deposit, remains)
            settle_workers.append(worker_name)
    
    if now_balance < balance:
        for worker_name in workers.keys():
            if worker_name in settle_workers:
                continue
            settle_log(worker_name, workers[worker_name], 0)
            workers[woerker_name] = 0
    
    del_workers = list()
    for worker_name in workers.keys():
        if workers[worker_name] == 0:
            del_workers.append(worker_name)
    for worker_name in del_workers:
        workers.pop(worker_name)
        del_log(worker_name)


    with open('datas.json', mode='w') as f:
        ret_json = {'balance': now_balance, 'all_balance': now_all_balance, 'workers': workers}
        json.dump(ret_json, f) 
