import argparse
import json
import time
import os


def log(log_info, datas):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open('account.log', mode='a') as f:
        f.writelines('{} {}\n'.format(now_time, log_info))
        f.writelines('Now Balance: ' + str(datas) + '\n')


def save(datas):
    with open('account.json', mode='w') as f:
        json.dump(datas, f)
    os.system("git add account.*")
    os.system('git commit -m "balance update"')
    os.system("git push -u origin main")


def clear(user, note):
    with open('account.json', mode='r') as f:
        datas = json.load(f)
    if user:
        datas[user] = 0
        info = "User {}'s balance is set to 0.".format(user)
        print(info)
        log(info, datas)
    else:
        for user in datas.keys():
            datas[user] = 0
            info = "User {}'s balance is set to 0. ({})".format(user, note)
            print(info)
            log(info, datas)
    save(datas)


def deposit(user, amount, note):
    with open('account.json', mode='r') as f:
        datas = json.load(f)
    if user not in datas.keys():
        print("No {} Found.".format(user))
        return()
    amount = args.amount
    if amount <= 0:
        print("Invalid ETH Amount.")
        return()
    datas[user] += amount
    info = "User {} deposits {} (now {}) ETH. ({})".format(user, amount, datas[user], note)
    print(info)
    log(info, datas)
    save(datas)


def withdraw(user, amount, note):
    with open('account.json', mode='r') as f:
        datas = json.load(f)
    if user not in datas.keys():
        print("No {} Found.".format(user))
        return()
    if amount <= 0:
        print("Invalid ETH Amount.")
        return()
    if amount > datas[user]:
        print("Insufficient Funds.")
        return()
    datas[user] -= amount
    info = "User {} withdraws {} (now {}) ETH. ({})".format(user, amount, datas[user], note)
    print(info)
    log(info, datas)
    save(datas)


def sell(amount, note):
    with open('account.json', mode='r') as f:
        datas = json.load(f)
    tot_amount = 0
    for user in datas.keys():
        tot_amount += datas[user]
    if amount > tot_amount:
        print('Not Enough ETH.')
        return
    tot_remain = tot_amount - amount
    for user in datas.keys():
        datas[user] = datas[user] / tot_amount * tot_remain
    info = "Sells {} ETH. Remains {} ETH now. ({})".format(amount, tot_remain, note)
    print(info)
    log(info, datas)
    save(datas)


def show_info():
    with open('account.json', mode='r') as f:
        datas = json.load(f)
    tot_amount = 0
    for user in datas.keys():
        tot_amount += datas[user]
    print("Total Amount: {:.3f} mETH.".format(tot_amount * 1000))
    print("Name\tAmount/mETH\tShare/%")
    for user in datas.keys():
        print("{}\t{:.3f}\t\t{:.2f}".format(user, datas[user] * 1000, datas[user] / tot_amount * 100))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Account Management")
    parser.add_argument('operation', type=str, help="Performing Operation: clear | deposit | withdraw | info | sell")
    parser.add_argument('-u', '--user', type=str, help="Account Name")
    parser.add_argument('-a', '--amount', type=float, help="ETH Amount")
    parser.add_argument('-n', '--note', type=str, help="Additional Description")
    args = parser.parse_args()

    if args.operation == 'clear':
        clear(args.user, args.note)
    elif args.operation == 'deposit':
        deposit(args.user, args.amount, args.note)
    elif args.operation == 'withdraw':
        withdraw(args.user, args.amount, args.note)
    elif args.operation == 'info':
        show_info()
    elif args.operation == 'sell':
        sell(args.amount, args.note)
    else:
        exit()
        