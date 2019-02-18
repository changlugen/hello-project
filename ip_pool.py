import random


def get_ip():
    ip_pool = []
    with open("/Users/mac/PycharmProjects/西刺代理IP.txt", "r", encoding="utf-8") as fp:
        for item in fp:
            ip_pool.append(item.strip())
    ip_pool = [x.split(',')[0] for x in ip_pool]
    ip_type = [x.split(":")[0] for x in ip_pool]
    ip_list1 = []

    for i in range(len(ip_pool)):
        ip = {}
        ip[ip_type[i]] = ip_pool[i]
        ip_list1.append(ip)
    # print(ip_list1)
    return random.choice(ip_list1)


if __name__ == '__main__':
    print(get_ip())
