import os, pytz, time, json, random, gspread, string, re
from datetime import datetime
import pandas as pd
from google.oauth2.service_account import Credentials

class Utilities:
    get_time = lambda: (datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S'), datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d')) # --> Get's Indian time zone time 
    transaction_id_generator = lambda : f"{int(time.time())}-{random.randint(1, 100000)}" # --> Generates transaction id
    generate_shift_tag = lambda: ''.join(random.choices(string.ascii_uppercase, k=4) + random.choices(string.digits, k=3)) # --> creates a name with 3 digits 
    generate_random_name = lambda: ''.join(random.choices(string.ascii_lowercase, k=4)) # --> Generate random name for excel , In future the above function can be merged into this .. for enhnacemnt

class cloud_database:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds_json_data = json.loads(os.environ['g_creds'])
    creds = Credentials.from_service_account_info(info=creds_json_data, scopes=scope)

    def get_db(user_id):
        client = gspread.authorize(cloud_database.creds)
        worksheet = client.open('Authorized_bots').sheet1
        try:
            cell = worksheet.find(str(user_id))
            row = cell.row
            row_data = worksheet.row_values(row)
            colls = ['user_id', 'user_name', 'Phone number', 'account', 'start_date', 'end_date', 'shift_status', 'amount_available']
            data_dict = dict(zip(colls, row_data))
            worksheet = None
            return data_dict
        except gspread.CellNotFound:
            print(f"User ID {user_id} not found in the worksheet")
            return None
       

    def append_data(data_dict):
        try:
            # Updating transaction
            print("Data in Sheets is Trying to Update...")
            user_data = cloud_database.get_db(data_dict['user_id'])
            data_dict['user_name'] = user_data.get('user_name')
            available_amount =  user_data.get('amount_available')
            data_dict['cut_amount'] = int(available_amount) - int(data_dict['amount'])
            data_dict['Status'] = data_dict.get('Status')
            values = [data_dict.get(key) for key in ['account', 'amount', 'bank', 'ifsc', 'name',
                                                     'trans_time', 'trans_date', 'user_id', 'user_name',
                                                     'Status', 'transaction_id', 'Shift_tag','cut_amount']]
            client = gspread.authorize(cloud_database.creds)
            worksheet = client.open('transactions_recorder').sheet1
            worksheet.append_row(values)
            print("Data in Sheets is Updated Successfully...")
            # Updating amount
            if data_dict['Status'] == 'Success':
                a_update = cloud_database.update_data(data_dict['user_id'], 'amount_available', data_dict['cut_amount'])
                if a_update == True:
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            print(e)

    def get_user_work(shift_tag):
        client = gspread.authorize(cloud_database.creds)
        worksheet = client.open('transactions_recorder').sheet1
        data = worksheet.get_all_values()
        headers = data.pop(0)
        dframe = pd.DataFrame(data, columns=headers)
        return dframe
      
    def update_data(user_id, field, new_value):
        print(f"Updating {field}...")
        client = gspread.authorize(cloud_database.creds)
        worksheet = client.open('Authorized_bots').sheet1
        try:
            cell = worksheet.find(str(user_id))
            column_index = worksheet.find(field).col
            worksheet.update_cell(cell.row, column_index, new_value)
            print(f"{field} Updated successfully")
            return True
        except gspread.CellNotFound:
            print(f"User ID {user_id} not found in the worksheet")
            return False

def extract_info(text):
    patterns = [ re.compile(r"Name:\s*(?P<name>.+?)\s+Account/Address:\s*(?P<account>\d+)\s+Bank:\s*(?P<bank>.+?)\s+IFSC:\s*(?P<ifsc>\w+)\s+Help me transfer the amount：(?P<amount>\d+)"),
        re.compile(r"Name：\s*(?P<name>.+?)\s*account：\s*(?P<account>\d+)\s*Bank：\s*(?P<bank>.+?)\s*IFSC：\s*(?P<ifsc>\w+)\s*\n(?P<amount>\d+)"),
        re.compile(r"Name:\s*(?P<name>.+?)\s*account:\s*(?P<account>\d+)\s*Bank:\s*(?P<bank>.+?)\s*IFSC:\s*(?P<ifsc>\w+)\s*Help me transfer the amount：(?P<amount>\d+)"),
        re.compile(r"Name:\s*(?P<name>.+?)\s*account:\s*(?P<account>\d+)\s*Bank:\s*(?P<bank>.+?)\s*IFSC:\s*(?P<ifsc>\w+)\s*(?P<amount>\d+)"),
        re.compile(r"Name:\s*(?P<name>.+?)\s*Account Number:\s*(?P<account>\d+)\s*IFSC Code:\s*(?P<ifsc>\w+)\s*(?P<bank>.+?)\s*(?P<amount>\d+)"),
        re.compile(r"Name：(?P<name>.*?)\n\nAccount：(?P<account>.*?)\n\nBank：(?P<bank>.*?)\n\nIFSC：(?P<ifsc>.*?)\n\n(?P<amount>\d+)"),
        re.compile(r"Name：(?P<name>.+?)\s*Account/Address：(?P<account>\d+)\s*Bank：(?P<bank>.+?)\s*IFSC：(?P<ifsc>\w+)\s*(?P<amount>\d+)"),
        re.compile(r"Bank Account Name\s*:\s*(?P<name>.+)\nBank Account Number\s*:\s*(?P<account>\d+)\nBank Name\s*:\s*(?P<bank>.+)\nIFSC:\s*(?P<ifsc>\w+)\nHelp me transfer the amount\s*：\s*(?P<amount>\d+)"),
        re.compile(r"Bank Account Name\s*:\s*(?P<name>.+)\s+Bank Account Number\s*:\s*(?P<account>\d+)\s+Bank Name\s*:\s*(?P<bank>.+)\s+IFSC:\s*(?P<ifsc>\w+)\s+Help me transfer the amount\s*：\s*(?P<amount>\d+)"),
        re.compile(r"Name：(?P<name>.+?)\s+Account：(?P<account>\d+)\s+Bank：(?P<bank>.+?)\s+IFSC：(?P<ifsc>\w+)\s+(?P<amount>\d+)"),
        re.compile(r"Bank Account Name\s*:\s*(?P<name>.+)\nBank Account Number\s*:\s*(?P<account>\d+)\nBank Name\s*:\s*(?P<bank>.+)\nIFSC:\s*(?P<ifsc>\w+)\nHelp me transfer the amount\s*：\s*(?P<amount>\d+)"),
        re.compile(r'Bank Account Name\s*:\s*(?P<name>\w+)\nBank Account Number\s*:\s*(?P<account>\d+)\nBank Name\s*:\s*(?P<bank>\w+\s*\w*)\nIFSC\s*:\s*(?P<ifsc>[A-Z0-9]+)\n(?P<amount>\d+)'),
        re.compile(r"Name:\s*(?P<name>.+?)\nAccount/Address:\s*(?P<account>\d+)\nBank:\s*(?P<bank>.+?)\nIFSC:\s*(?P<ifsc>.+?)\n(?P<amount>\d+)")]  
        
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            info = match.groupdict()
            info['amount'] = int(info['amount'])
            return info
    return False