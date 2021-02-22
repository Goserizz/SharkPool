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
    return active_workers


def balance_log(now_balance, now_earn):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open(log_file, mode='a') as f:
        f.writelines("{} balance: {}, +{} ETH.\n".format(now_time, now_balance, now_earn))


def earn_log(worker, hashrate, contri, earn, now_bal):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open(log_file, mode='a') as f:
        f.writelines("{} {}: 4h hashrate is {}, contributes {:.2f}% calculation, earns {} ETH.({})\n".format(now_time, worker, hashrate, contri, earn, now_bal))


if __name__ == '__main__':
    res_json = get_data()
    now_workers = get_workers(res_json)
    _, now_balance, _ = get_balance(res_json)
    print(now_workers)
    
    with open('datas.json', mode='r') as f:
        datas = json.load(f)
        balance = datas['balance']
        workers = datas['workers']
    
    print(type(now_balance))
    now_earn = now_balance - balance
    balance_log(now_balance, now_earn)
    whole_cal = 0
    
    for worker in now_workers:
        worker_name = worker['name']
        if worker_name not in workers:
            workers[worker_name] = 0
        whole_cal += worker['avg_30_hashrate']
    
    for worker in now_workers:
        worker_name = worker['name']
        hashrate = worker['avg_30_hashrate']
        contri = hashrate / whole_cal
        earn = now_earn * contri
        workers[worker_name] += earn
        earn_log(worker_name, hashrate, contri * 100, earn, worker[worker_name])
    
    with open('datas.json', mode='w') as f:
        ret_json = {'balance': now_balance, 'workers': workers}
        json.dump(ret_json, f)
    