import os, pytz, time, json, random, gspread, re, string
from datetime import datetime
import pandas as pd
from google.oauth2.service_account import Credentials

class Utilities:
    
    get_time = lambda: (datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'), datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')) # --> Get's Indian time zone time 
    
    transaction_id_generator = lambda : f"{int(time.time())}-{random.randint(1, 100000)}" # --> Generates transaction id
    
    generate_shift_tag = lambda: ''.join(random.choices(string.ascii_uppercase, k=4) + random.choices(string.digits, k=3)) # --> creates a name with 3 digits 
    
    generate_random_name = lambda: ''.join(random.choices(string.ascii_lowercase, k=4)) # --> Generate random name for excel , In future the above function can be merged into this .. for enhnacemnt


def extract_info(text):
    pattern2 = r"Name:\s*(?P<name>.+?)\s+Account/Address:\s*(?P<account>\d+)\s+Bank:\s*(?P<bank>.+?)\s+IFSC:\s*(?P<ifsc>\w+)\s+Help me transfer the amount：(?P<amount>\d+)"
    pattern = r"Name：\s*(?P<name>.+?)\s*account：\s*(?P<account>\d+)\s*Bank：\s*(?P<bank>.+?)\s*IFSC：\s*(?P<ifsc>\w+)\s*\n(?P<amount>\d+)"
    pattern3 = r"Name:\s*(?P<name>.+?)\s*account:\s*(?P<account>\d+)\s*Bank:\s*(?P<bank>.+?)\s*IFSC:\s*(?P<ifsc>\w+)\s*Help me transfer the amount：(?P<amount>\d+)"
    pattern4 = r"Name:\s*(?P<name>.+?)\s*account:\s*(?P<account>\d+)\s*Bank:\s*(?P<bank>.+?)\s*IFSC:\s*(?P<ifsc>\w+)\s*(?P<amount>\d+)"
    pattern5 = r"Name:\s*(?P<name>.+?)\s*Account Number:\s*(?P<account>\d+)\s*IFSC Code:\s*(?P<ifsc>\w+)\s*(?P<bank>.+?)\s*(?P<amount>\d+)"
    
    match = re.search(pattern, text) or re.search(pattern2, text) or re.search(pattern3, text) or re.search(pattern4, text) or re.search(pattern5, text)
    if match:
        info = match.groupdict()
        info['amount'] = int(info['amount'])
        return info
    else:
        print("text :", text)
        return {"Response" : "Dead Response"}

class cloud_database:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds_json = json.loads(os.environ['g_creds'])
    creds = Credentials.from_service_account_info(info=creds_json, scopes=scope)

    
    def get_db(user_id):
        client = gspread.authorize(cloud_database.creds)
        worksheet = client.open('Authorized_bots').sheet1
        try:
            cell = worksheet.find(str(user_id))
            row = cell.row
            row_data = worksheet.row_values(row)
            colls = ['user_id', 'user_name', 'Phone number', 'account', 'start_date', 'end_date', 'shift_status']
            data_dict = dict(zip(colls, row_data))
            return data_dict
        except gspread.CellNotFound:
            print(f"User ID {user_id} not found in the worksheet")
            return None
    
    
    def update_status(user_id, new_status):
        print("Updating mode...")
        client = gspread.authorize(cloud_database.creds)
        worksheet = client.open('Authorized_bots').sheet1
        try:
            cell = worksheet.find(user_id)
            column_index = worksheet.find('shift_status').col
            worksheet.update_cell(cell.row, column_index, new_status)
            print("Updated successfully")
            return True
        except gspread.CellNotFound:
            print(f"User ID {user_id} not found in the worksheet")
            return False

    def append_data(data_dict):
        try:
            print("Data in Sheets is Trying to Update...")
            user_data = cloud_database.get_db(data_dict['user_id'])
            data_dict['user_name'] = user_data.get('user_name')
            data_dict['Status'] = data_dict.get('Status')
            values = [data_dict.get(key) for key in ['account', 'amount', 'bank', 'ifsc', 'name',
                                                     'trans_time', 'trans_date', 'user_id', 'user_name',
                                                     'Status', 'transaction_id', 'Shift_tag']]
            client = gspread.authorize(cloud_database.creds)
            worksheet = client.open('transactions_recorder').sheet1
            worksheet.append_row(values)
            print("Data in Sheets is Updated Successfully...")
            return True
        except Exception as e:
            return e

    def get_user_work(shift_tag):
        client = gspread.authorize(cloud_database.creds)
        worksheet = client.open('transactions_recorder').sheet1
        data = worksheet.get_all_values()
        headers = data.pop(0)
        dframe = pd.DataFrame(data, columns=headers)
        return dframe



# colls = ['account', 'amount', 'bank', 'ifsc', 'name', 'trans_time', 'trans_date', 'user_id', 'user_name', 'Status', 'transaction_id', 'Shift_tag']







    # pattern1 = r"Name：\s*(.+)\s*account：\s*(\d+)\s*Bank：\s*(.+)\s*IFSC：\s*(\w+)\s*Help me transfer the amount：(\d+)"
    # pattern2 = r"Name：\s*(.+)\s*account：\s*(\d+)\s*Bank：\s*(.+)\s*IFSC：\s*(\w+)\s*(\d+)"
    # pattern3 = r'Name：\s*(.+)\s*account：\s*(\d+)\s*Bank：\s*(.+)\s*IFSC：\s*(\w+)\s*(\d+)'