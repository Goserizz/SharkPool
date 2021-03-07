import argparse
import json
import time


def log(log_info, datas):
    now_time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
    with open('account.log', mode='a') as f:
        f.writelines('{} {}\n'.format(now_time, log_info))
        f.writelines('Now Balance: ' + str(datas) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Account Management")
    parser.add_argument('operation', type=str, help="Performing Operation: clear | deposit | withdraw | info | sell")
    parser.add_argument('-u', '--user', type=str, help="Account Name")
    parser.add_argument('-a', '--amount', type=float, help="ETH Amount")
    parser.add_argument('-n', '--note', type=str, help="Additional Description")
    args = parser.parse_args()

    with open('account.json', mode='r') as f:
        datas = json.load(f)
    if args.operation == 'clear':
        if args.user:
            datas[args.user] = 0
            info = "User {}'s balance is set to 0.".format(args.user)
            print(info)
            log(info, datas)
        else:
            for user in datas.keys():
                datas[user] = 0
                info = "User {}'s balance is set to 0. ({})".format(user, args.note)
                print(info)
                log(info, datas)
    elif args.operation == 'deposit':
        user = args.user
        if user not in datas.keys():
            print("No {} Found.".format(user))
            exit()
        amount = args.amount
        if amount <= 0:
            print("Invalid ETH Amount.")
            exit()
        datas[user] += amount
        info = "User {} deposits {} (now {}) ETH. ({})".format(user, amount, datas[user], args.note)
        print(info)
        log(info, datas)
    elif args.operation == 'withdraw':
        user = args.user
        if user not in datas.keys():
            print("No {} Found.".format(user))
            exit()
        amount = args.amount
        if amount <= 0:
            print("Invalid ETH Amount.")
            exit()
        if amount > datas[user]:
            print("Insufficient Funds.")
            exit()
        datas[user] -= amount
        info = "User {} withdraws {} (now {}) ETH. ({})".format(user, amount, datas[user], args.note)
        print(info)
        log(info, datas)
    elif args.operation == 'info':
        tot_amount = 0
        for user in datas.keys():
            tot_amount += datas[user]
        print("Total Amount: {:.3f} mETH.".format(tot_amount * 1000))
        print("Name\tAmount/mETH\tShare/%")
        for user in datas.keys():
            print("{}\t{:.3f}\t\t{:.2f}".format(user, datas[user] * 1000, datas[user] / tot_amount * 100))
    elif args.operation == 'sell':
        amount = args.amount
        tot_amount = 0
        for user in datas.keys():
            tot_amount += datas[user]
        tot_remain = tot_amount - amount
        for user in datas.keys():
            datas[user] = datas[user] / tot_amount * tot_remain
        info = "Sells {} ETH. Remains {} ETH now. ({})".format(amount, tot_remain, args.note)
        print(info)
        log(info, datas)
    else:
        exit()
    
    if args.operation != 'info':
        with open('account.json', mode='w') as f:
            json.dump(datas, f)
        