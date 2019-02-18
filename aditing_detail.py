import re
from lxml import etree
import pandas as pd


def get_Insight(html):
    #dongca
    html_etree = etree.HTML(html)
    first_table = html_etree.xpath(
        '//table[@class="form conf_tab"]/tr[8]/td[@class="item_input"]/table[1]/tr[2]/child::*/text()')
    # print(first_table)
    second_table = html_etree.xpath(
        '//table[@class="form conf_tab"]/tr[8]/td[@class="item_input"]/table[2]/tr[2]/child::*/text()')
    # print(second_table)
    insight_dict = {'insight:', first_table}
    insight_index = ['贷款放款总订单数', '贷款机构数', '贷款逾期订单数',
                     '最近一次贷款时间', '近1个月贷款笔数', '近2个月贷款笔数', '近3个月贷款笔数']
    return insight_dict


def get_xuexin(html):
    # 学信信息
    detail_compile = re.compile(r'<td><b>姓名:</b>(\w+)</td>', re.S)
    xuexin_name = re.findall(detail_compile, html)  # 姓名
    if len(xuexin_name) > 0 and xuexin_name[0] != 'XXX':
        xuexin_name = xuexin_name[0]
        detail_compile = re.compile(r'<td><b>性别:</b>(\w+)</td>', re.S)
        xuexin_sexy = re.findall(detail_compile, html)[0]  # 性别
        detail_compile = re.compile(r'<td><b>学制:</b>(.*?)</td>', re.S)
        xuexin_year = re.findall(detail_compile, html)[0]  # 学制
        detail_compile = re.compile(r'<td><b>学习形式:</b>(\w+)</td>', re.S)
        xuexin_type = re.findall(detail_compile, html)[0]  # 学习形式
        detail_compile = re.compile(r'<td><b>学籍状态:</b>(.*?)</td>', re.S)
        xuexin_statu = re.findall(detail_compile, html)[0]  # 学籍状态
        detail_compile = re.compile(r'<td><b>学历:</b>(\w+)</td>', re.S)
        xuexin_xueli = re.findall(detail_compile, html)[0]  # 学历
    else:
        xuexin_name = None
        xuexin_sexy = None
        xuexin_year = None
        xuexin_type = None
        xuexin_statu = None
        xuexin_xueli = None

    # detail_compile = re.compile(r'<td><b>性别:</b>(\w+)</td>', re.S)
    # xuexin_sexy = re.findall(detail_compile, html)[0]  #性别
    # detail_compile = re.compile(r'<td><b>学制:</b>(.*?)</td>', re.S)
    # xuexin_year = re.findall(detail_compile, html)[0]  #学制
    # detail_compile = re.compile(r'<td><b>学习形式:</b>(\w+)</td>', re.S)
    # xuexin_type = re.findall(detail_compile, html)[0]  #学习形式
    # detail_compile = re.compile(r'<td><b>学籍状态:</b>(.*?)</td>', re.S)
    # xuexin_statu = re.findall(detail_compile, html)[0]  #学籍状态
    # detail_compile = re.compile(r'<td><b>学历:</b>(\w+)</td>', re.S)
    # xuexin_xueli = re.findall(detail_compile, html)[0]  #学历
    xuexin_detail = [xuexin_name, xuexin_sexy, xuexin_year, xuexin_type, xuexin_statu, xuexin_xueli]
    # print(xuexin_detail)
    xuexin_dict = {'学信信息': xuexin_detail}
    # print(xuexin_dict)
    return xuexin_dict


def get_communicate(html):
    # 通讯信息
    detail_compile = re.compile(r'<b>通讯录条数:</b>(\d+) <a href=', re.S)
    commu_numb = re.findall(detail_compile, html)[0]  # 通讯录条数
    detail_compile = re.compile(r'&nbsp;余额：(.*?)<br>', re.S)
    commu_balance = re.findall(detail_compile, html)[0]  # 余额
    detail_compile = re.compile(r'<b>入网时间:</b>(.*?)<br>', re.S)
    use_duration = re.findall(detail_compile, html)[0]  # 入网时长
    detail_compile = re.compile(r'<b>近六个月通话总条数:</b>(\d+) <a href=', re.S)
    six_commu_num = re.findall(detail_compile, html)[0]  # 近六个月通话总条数
    detail_compile = re.compile(r'<b>通话详单月数:</b>(\d) <a href=', re.S)
    month_count = re.findall(detail_compile, html)[0]  # 入网时长
    commu_detail = [commu_numb, commu_balance, use_duration, six_commu_num, month_count]
    commu_dict = {'通讯信息': commu_detail}
    # print(commu_dict)
    return commu_dict


#亲人认证通话次数
def get_family_identity(html):
    detail_compile = re.compile(r'<span >\w+ 在通话详单中出现 (\d+) 次 </span>', re.S)
    family_identity1 = re.findall(detail_compile, html)  #亲人认证通话次数
    if len(family_identity1) > 0:
        family_identity1 = family_identity1[0]
    else:
        family_identity1 = None
    detail_compile = re.compile(r'<br>\s+<span >\w+ 在通话详单中出现 (\d+) 次 </span>', re.S)
    family_identity2 = re.findall(detail_compile, html)  #亲人认证通话次数
    if len(family_identity2) > 0:
        family_identity2 = family_identity2[0]
    else:
        family_identity2 = None
    appear_times = [family_identity1, family_identity2]
    family_identity_dict = {'亲人认证通话次数': appear_times}
    # print(family_identity_dict)
    return family_identity_dict


def get_credit91(html):
    # 91
    detail_compile = re.compile(r'>申请借款 (\d+) 笔</td>', re.S)
    apply_times = re.findall(detail_compile, html)  # 申请笔数
    # print(apply_times)
    if len(apply_times) > 0:
        apply_times = apply_times[0]
        detail_compile = re.compile(r'<td>批贷已放款 (\d+) 笔</td>', re.S)
        loan_times = re.findall(detail_compile, html)[0]  # 批贷笔数
        detail_compile = re.compile(r'>拒绝贷款 (\d+) 笔</td>', re.S)
        refuse_times = re.findall(detail_compile, html)[0]  # 拒绝笔数
        detail_compile = re.compile(r'<td>已还清 (\d+) 笔</td>', re.S)
        payok = re.findall(detail_compile, html)[0]  # 还清笔数
        detail_compile = re.compile(r'<td>还款中 (\d+) 笔</td>', re.S)
        payment = re.findall(detail_compile, html)[0]  # 还款中笔数
        detail_compile = re.compile(r'>目前欠款 (.*?) 元</td>', re.S)
        money = re.findall(detail_compile, html)[0]  # 目前欠款
    else:
        apply_times = None
        loan_times = None
        refuse_times = None
        payok = None
        payment = None
        money = None
    credit_detail = [apply_times, loan_times, refuse_times, payok, payment, money]
    credit91_dict = {'91credit': credit_detail}
    # print(credit91_dict)
    return credit91_dict
