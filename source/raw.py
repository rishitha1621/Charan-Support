import os
import pytz
import time
import json
import random
import gspread
import re
import string
from datetime import datetime
import pandas as pd
from google.oauth2.service_account import Credentials
import logging


class Utilities:
    @staticmethod
    def get_time():
        current_time = datetime.now(pytz.timezone('Asia/Kolkata'))
        return current_time.strftime('%H:%M:%S'), current_time.strftime('%Y-%m-%d')

    @staticmethod
    def transaction_id_generator():
        timestamp = int(time.time())
        random_number = random.randint(1, 100000)
        return f"{timestamp}-{random_number}"

    @staticmethod
    def generate_shift_tag():
        return ''.join(random.choices(string.ascii_uppercase, k=4) + random.choices(string.digits, k=3))

    @staticmethod
    def generate_random_name():
        return ''.join(random.choices(string.ascii_lowercase, k=4))


class CloudDatabase:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    def __init__(self, creds_json):
        self.creds = Credentials.from_service_account_info(info=creds_json, scopes=self.scope)

    def get_db(self, user_id):
        try:
            client = gspread.authorize(self.creds)
            worksheet = client.open('Authorized_bots').sheet1
            cell = worksheet.find(str(user_id))
            row_data = worksheet.row_values(cell.row)
            columns = ['user_id', 'user_name', 'Phone number', 'account', 'start_date', 'end_date', 'shift_status']
            return dict(zip(columns, row_data))
        except gspread.CellNotFound:
            logging.warning(f"User ID {user_id} not found in the worksheet")
            return None

    def update_status(self, user_id, new_status):
        try:
            client = gspread.authorize(self.creds)
            worksheet = client.open('Authorized_bots').sheet1
            cell = worksheet.find(user_id)
            column_index = worksheet.find('shift_status').col
            worksheet.update_cell(cell.row, column_index, new_status)
            logging.info("Updated successfully")
            return True
        except gspread.CellNotFound:
            logging.warning(f"User ID {user_id} not found in the worksheet")
            return False

    def append_data(self, data_dict):
        try:
            client = gspread.authorize(self.creds)
            worksheet = client.open('transactions_recorder').sheet1
            user_data = self.get_db(data_dict['user_id'])
            data_dict['user_name'] = user_data.get('user_name')
            values = [data_dict.get(key) for key in ['account', 'amount', 'bank', 'ifsc', 'name',
                                                     'trans_time', 'trans_date', 'user_id', 'user_name',
                                                     'Status', 'transaction_id', 'Shift_tag']]
            worksheet.append_row(values)
            logging.info("Data in Sheets is updated successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to update data in Sheets: {e}")
            return False

    def get_user_work(self, shift_tag):
        try:
            client = gspread.authorize(self.creds)
            worksheet = client.open('transactions_recorder').sheet1
            data = worksheet.get_all_values()
            headers = data.pop(0)
            return pd.DataFrame(data, columns=headers)
        except Exception as e:
            logging.error(f"Failed to retrieve user work: {e}")
            return pd.DataFrame()


def extract_info(text):
    patterns = [
        re.compile(r


# def extract_info(text):
#     pattern2 = r"Name:\s*(?P<name>.+?)\s+Account/Address:\s*(?P<account>\d+)\s+Bank:\s*(?P<bank>.+?)\s+IFSC:\s*(?P<ifsc>\w+)\s+Help me transfer the amount：(?P<amount>\d+)"
#     pattern = r"Name：\s*(?P<name>.+?)\s*account：\s*(?P<account>\d+)\s*Bank：\s*(?P<bank>.+?)\s*IFSC：\s*(?P<ifsc>\w+)\s*\n(?P<amount>\d+)"
#     pattern3 = r"Name:\s*(?P<name>.+?)\s*account:\s*(?P<account>\d+)\s*Bank:\s*(?P<bank>.+?)\s*IFSC:\s*(?P<ifsc>\w+)\s*Help me transfer the amount：(?P<amount>\d+)"
#     pattern4 = r"Name:\s*(?P<name>.+?)\s*account:\s*(?P<account>\d+)\s*Bank:\s*(?P<bank>.+?)\s*IFSC:\s*(?P<ifsc>\w+)\s*(?P<amount>\d+)"
#     pattern5 = r"Name:\s*(?P<name>.+?)\s*Account Number:\s*(?P<account>\d+)\s*IFSC Code:\s*(?P<ifsc>\w+)\s*(?P<bank>.+?)\s*(?P<amount>\d+)"
#     pattern6 = r"Name：(?P<name>.*?)\n\nAccount：(?P<account>.*?)\n\nBank：(?P<bank>.*?)\n\nIFSC：(?P<ifsc>.*?)\n\n(?P<amount>\d+)"
#     pattern7 = r"Name：(?P<name>.+?)\s*Account/Address：(?P<account>\d+)\s*Bank：(?P<bank>.+?)\s*IFSC：(?P<ifsc>\w+)\s*(?P<amount>\d+)"

#     patterns = [pattern, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7]

#     for pattern in patterns:
#         match = re.search(pattern, text)
#         if match:
#             info = match.groupdict()
#             info['amount'] = int(info['amount'])
#             return info

#     print("text :", text)
#     return {"Response": "Dead Response"}

