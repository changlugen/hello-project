from pymongo import MongoClient
from Config import *
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
client = MongoClient(MONGO_URL, 27017)
db = client[MONGO_DB]
dbtb = db[MONGO_TABLE_LOAN]


def first():
    data = dbtb.find()
    each_row = [list(items.values())[1][0][0][0:-1] for items in data]
    # print(each_row)
    array0 = np.array(each_row)
    # print(array0.shape[1])
    # print(array0.shape[0])
    # rows = array0.shape[0]
    column_name = ['id', 'loan_type', 'user', 'limit', 'channel', 'interest', 'loan_duration',
                   'status', 'yes_or_no', 'loan_time', 'phone_type', 'apply_type']
    df_index = [i for i in range(1, array0.shape[0]+1)]
    df = pd.DataFrame(array0, index=df_index, columns=column_name)
    # print(df)
    return df


def get_loan_history():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_history = [list(list(each.values())[0][0].values())[0] for each in each_row]
    loan_history_array = np.array(loan_history)
    column_name = ['逾期次数', '逾期总天数', '催收总次数']
    df_index = [i for i in range(1, loan_history_array.shape[0]+1)]
    df_loan_history = pd.DataFrame(loan_history_array, index=df_index, columns=column_name)
    # print(loan_history)
    # print(df_loan_history)
    return df_loan_history


def get_loan_xuexin():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_xuexin = [list(list(each.values())[0][1].values())[0] for each in each_row]
    # print(loan_xuexin)
    loan_xuexin_array = np.array(loan_xuexin)
    column_name = ['xuexin_name', 'xuexin_sexy', 'xuexin_year', 'xuexin_type', 'xuexin_statu', 'xuexin_xueli']
    df_index = [i for i in range(1, loan_xuexin_array.shape[0] + 1)]
    df_loan_xuein = pd.DataFrame(loan_xuexin_array, index=df_index, columns=column_name)
    # print(df_loan_xuein)
    return df_loan_xuein


def get_loan_identify():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_identify = [list(list(each.values())[0][2].values())[0] for each in each_row]
    # print(loan_xuexin)
    loan_identify_array = np.array(loan_identify)
    column_name = ['identify_sex', 'identify_minzu', 'identify_birth', 'identify_city']
    df_index = [i for i in range(1, loan_identify_array.shape[0] + 1)]
    df_loan_identify = pd.DataFrame(loan_identify_array, index=df_index, columns=column_name)
    # print(df_loan_identify)
    return df_loan_identify


def get_loan_communication():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_communication = [list(list(each.values())[0][3].values())[0] for each in each_row]
    # print(loan_xuexin)
    loan_communication_array = np.array(loan_communication)
    column_name = ['commu_num', 'commu_balance', 'use_duration', 'six_commu_num', 'month_count']
    df_index = [i for i in range(1, loan_communication_array.shape[0] + 1)]
    df_loan_communication = pd.DataFrame(loan_communication_array, index=df_index, columns=column_name)
    # print(df_loan_communication)
    return df_loan_communication


def get_familyIdentity():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_familyIdentity = [list(list(each.values())[0][4].values())[0] for each in each_row]
    # print(loan_xuexin)
    loan_familyIdentity_array = np.array(loan_familyIdentity)
    column_name = ['family_identity1', 'family_identity2']
    df_index = [i for i in range(1, loan_familyIdentity_array.shape[0] + 1)]
    df_loan_familyIdentity = pd.DataFrame(loan_familyIdentity_array, index=df_index, columns=column_name)
    # print(df_loan_familyIdentity)
    return df_loan_familyIdentity


def get_loan_91():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_91 = [list(list(each.values())[0][5].values())[0] for each in each_row]
    # print(loan_xuexin)
    loan_91_array = np.array(loan_91)
    column_name = ['apply_times', 'loan_times', 'refuse_times', 'payok', 'payment', 'money']
    df_index = [i for i in range(1, loan_91_array.shape[0] + 1)]
    df_loan_91 = pd.DataFrame(loan_91_array, index=df_index, columns=column_name)
    # print(df_loan_91)
    return df_loan_91


def get_loan_insight():
    data = dbtb.find()
    each_row = [list(items.values())[1][1] for items in data]
    # print(each_row)
    loan_insight = [list(list(each.values())[0][6].values())[0] for each in each_row]
    # print(loan_xuexin)
    loan_insight_array = np.array(loan_insight)
    column_name = ['贷款放款总订单数', '贷款机构数', '贷款逾期订单数',
                     '最近一次贷款时间', '近1个月贷款笔数', '近2个月贷款笔数', '近3个月贷款笔数',
                   '最大逾期金额范围', '最长逾期天数', '最后一次逾期时间', '当前逾期机构数']
    df_index = [i for i in range(1, loan_insight_array.shape[0] + 1)]
    df_loan_insight = pd.DataFrame(loan_insight_array, index=df_index, columns=column_name)
    print(df_loan_insight)
    return df_loan_insight


def write_to_csv(dataframe, df_loan_history, df_loan_xuein, df_loan_identify, df_loan_communication,
                 df_loan_familyIdentity, df_loan_91, df_loan_insight):
    if not os.path.exists('/Users/mac/Desktop/loanData.csv'):
        dataframe.to_csv('/Users/mac/Desktop/loanData.csv', encoding='utf_8_sig')
        print('loanData成功保存到csv!')
    else:
        print("loanData文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_history.csv'):
        df_loan_history.to_csv('/Users/mac/Desktop/loan_history.csv', encoding='utf_8_sig')
        print('loan_history成功保存到csv!')
    else:
        print("loan_history文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_xuein.csv'):
        df_loan_xuein.to_csv('/Users/mac/Desktop/loan_xuein.csv', encoding='utf_8_sig')
        print('loan_xuein成功保存到csv!')
    else:
        print("loan_xuein文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_identify.csv'):
        df_loan_identify.to_csv('/Users/mac/Desktop/loan_identify.csv', encoding='utf_8_sig')
        print('loan_identify成功保存到csv!')
    else:
        print("loan_identify文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_communication.csv'):
        df_loan_communication.to_csv('/Users/mac/Desktop/loan_communication.csv', encoding='utf_8_sig')
        print('loan_communication成功保存到csv!')
    else:
        print("loan_communication文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_familyIdentity.csv'):
        df_loan_familyIdentity.to_csv('/Users/mac/Desktop/loan_familyIdentity.csv', encoding='utf_8_sig')
        print('loan_familyIdentity成功保存到csv!')
    else:
        print("loan_familyIdentity文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_91.csv'):
        df_loan_91.to_csv('/Users/mac/Desktop/loan_91.csv', encoding='utf_8_sig')
        print('loan_91成功保存到csv!')
    else:
        print("loan_91文件已存在!")

    if not os.path.exists('/Users/mac/Desktop/loan_insight.csv'):
        df_loan_insight.to_csv('/Users/mac/Desktop/loan_insight.csv', encoding='utf_8_sig')
        print('loan_insight成功保存到csv!')
    else:
        print("loan_insight文件已存在!")


def main():
    dataframe = first()
    # print(dataframe)
    df_loan_history = get_loan_history()
    # print(loan_history)
    df_loan_xuexin = get_loan_xuexin()
    # print(loan_xuexin)
    df_loan_identify = get_loan_identify()
    # print(loan_identify)
    df_loan_communication = get_loan_communication()
    df_loan_familyIdentity = get_familyIdentity()
    df_loan_91 = get_loan_91()
    df_loan_insight = get_loan_insight()

    write_to_csv(dataframe, df_loan_history, df_loan_xuexin, df_loan_identify, df_loan_communication,
                 df_loan_familyIdentity, df_loan_91, df_loan_insight)


if __name__ == '__main__':
    each_row_list = []
    main()
