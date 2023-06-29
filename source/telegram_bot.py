import os, telebot
from replit import db
from telebot import types
from source import data_processor
from pandasql import sqldf

class MafiaBot:
    def __init__(self):
        self.bot = telebot.TeleBot(os.environ['token'])
        print("Bot On Force....")

        @self.bot.message_handler(commands=['start'])
        def start(message):
            print(f"Bot working for user First name: {message.from_user.first_name} Last name: {message.from_user.last_name} and ID : {message.chat.id}")
            markup = types.ReplyKeyboardMarkup(row_width=2)
            markup.add(types.KeyboardButton("Start Shift"), types.KeyboardButton("End Shift"), types.KeyboardButton("MENU"))
            user_input = self.bot.reply_to(message, "Hey Earner, select an option", reply_markup=markup)
            self.bot.register_next_step_handler(user_input, self.start_handler)
        
        @self.bot.message_handler(commands=['sort'])
        def sorter(message):
            print(f"Bot working for user First name: {message.from_user.first_name} Last name: {message.from_user.last_name} and ID : {message.chat.id}")
            if (db[str(message.chat.id)]['Status']) == "Active":
                user_input = self.bot.send_message(message.chat.id,"Hello Amigo! Enter the data to be sorted")
                self.bot.register_next_step_handler(user_input, self.data_sorter)
            elif (db[str(message.chat.id)]['Status']) == "not_active":
                self.bot.send_message(message.chat.id, "shift status is not active!")

    def start_handler(self, user_input):
        result_dict = data_processor.cloud_database.get_db(user_input.chat.id)
        if result_dict:
            if user_input.text == "Start Shift" and result_dict['shift_status'] == 'not_active':
                self.bot.send_message(user_input.chat.id, "Activating the shift...") 
                data_processor.cloud_database.update_status(str(user_input.chat.id), 'Active')
                db[user_input.chat.id] = {"user_id" : user_input.chat.id,"Status" : "Active", "Shift_Tag" : data_processor.Utilities.generate_shift_tag()}
                self.bot.send_message(user_input.chat.id, "shift status updated to Active, Press here to --> /sort <--")
                
            elif user_input.text == "End Shift" and result_dict['shift_status'] == 'Active':  
                self.bot.send_message(user_input.chat.id, "De activating the Shift")
                user_work = data_processor.cloud_database.get_user_work(db[str(user_input.chat.id)]['Shift_Tag'])
                excel_path = f'excel/{data_processor.Utilities.generate_random_name()}excel_file.xlsx'
                query = f"SELECT * FROM user_work WHERE user_id='{user_input.chat.id}' and Shift_tag='{db[str(user_input.chat.id)]['Shift_Tag']}'"
                total_debit_query = f"SELECT SUM(amount) AS total_debit FROM user_work WHERE user_id='{user_input.chat.id}' and Shift_tag='{db[str(user_input.chat.id)]['Shift_Tag']}';"
                user_row = sqldf(query)
                total_debit = sqldf(total_debit_query)
                Total_transactions = len(user_row)
                remove_cols = ['ifsc','user_id','user_name', 'transaction_id', 'trans_time','trans_date','Shift_tag']
                for col in remove_cols:
                    user_row = user_row.drop([col], axis=1) 
                user_row.to_excel(excel_path, index=False)
                with open(excel_path, 'rb') as file:
                    self.bot.send_document(user_input.chat.id,file,caption="Excel file")
                os.remove(excel_path)
                self.bot.send_message(user_input.chat.id, f"Total Transactions : {Total_transactions}\n Total Debit Amount : {total_debit['total_debit'].iloc[0]}\n De-Activating the Shift Tag : {db[str(user_input.chat.id)]['Shift_Tag']}") 
                updater = data_processor.cloud_database.update_status(str(user_input.chat.id), 'not_active')
                if updater == True:
                    db[str(user_input.chat.id)]['Status'] = "not_active"
                    self.bot.send_message(user_input.chat.id, "Shift status updated to Non-Active State..") 
                else:
                    self.bot.send_message(user_input.chat.id, "Erro in Shift Ending....")    
            elif user_input.text == "MENU":
                self.bot.send_message(user_input.chat.id, "Under Devlopment!")
            else:
                self.bot.send_message(user_input.chat.id, f"Your Current Shift Mode is: {db[str(user_input.chat.id)]['Status']}\nsomething fishy, huh? Contact the Thug!")
        else:
            self.bot.send_message(user_input.chat.id, "Seems you are not Registered Contact Charan")
            print("Error at the user validator end - Beta Not Found")
        
    def data_sorter(self, user_input):
        information = data_processor.extract_info(user_input.text)
        for i,v in information.items():
            self.bot.send_message(user_input.chat.id,v)
        for_timestamp = data_processor.Utilities.get_time()
        information['trans_time'] = for_timestamp[0]
        information['trans_date'] = for_timestamp[1]
        information['user_id'] = user_input.chat.id
        information['transaction_id'] = data_processor.Utilities.transaction_id_generator()
        information['Shift_tag'] = db[str(user_input.chat.id)]['Shift_Tag']
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(types.KeyboardButton("Success"), types.KeyboardButton("Denied"), types.KeyboardButton("Pending"), types.KeyboardButton("Skipped"))
        user_input = self.bot.send_message(user_input.chat.id,"""To Update the transaction status. Select among the options...""", reply_markup=markup)
        self.bot.register_next_step_handler(user_input, self.get_status, information)
        return

    def get_status(self,user_input,  information):
        status_options = ['Success','Denied','Pending','Skipped']
        if user_input.text in status_options:
            self.bot.send_message(user_input.chat.id,"Updating the Record wait for a few seconds...")
            information['Status'] = user_input.text
            ting_try = data_processor.cloud_database.append_data(information)
            if ting_try == True:
                message_text = "Data updated in the DB\n\n" + "\n".join([f'{item} : {key}' for item, key in information.items()]) + "\n\nPress /start to restart"
                self.bot.send_message(5579239229, message_text)
                self.bot.send_message(user_input.chat.id,"Data Updated.. /sort")
            else:
                self.bot.send_message(user_input.chat.id,"Data Not Updated.. /sort")
        else:
            print("Got invalid status option")
        
    def run(self):
        self.bot.infinity_polling()

    