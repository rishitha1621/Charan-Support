
def data_separator(user_input):
    print(f"Working for {user_input.chat.id}")
    try:
        dataa = user_input.text.split('\n')
        data_list2 = [x for x in dataa[:-1] if x != '']
        result = {}
        for data in data_list2:
            if ':' in data:
                result = {
                    i.split(':')[0].strip().lower(): i.split(':')[1].strip()
                    for i in data_list2
                }
            elif '：' in data:
                result = {
                    i.split('：')[0].lower(): i.split('：')[1].strip()
                    for i in data_list2
                }
        result['amount'] = dataa[-1]
        for key, value in result.items():
            bot.send_message(user_input.chat.id, value)
        for_timestamp = get_time()
        result['trans_time'] = for_timestamp[0]
        result['trans_date'] = for_timestamp[1]
        result['user_id'] = user_input.chat.id
        result['transaction_id'] = transaction_id_generator()
        matter = bot.send_message(
            user_input.chat.id,
            """To Update the transaction status reply with 1: Success, 2: Denied, 3: Pending, 4: Skipped"""
        )
        bot.register_next_step_handler(matter, get_status, result)
    except Exception as e:
        bot.send_message(
            user_input.chat.id,
            f"An error occurred data_separator function: {str(e)}")
    return


def get_status(user_input, data_dict):
    status_options = {
        '1': 'Success',
        '2': 'Denied',
        '3': 'Pending',
        '4': 'Skipped'
    }
    try:
        if user_input.text in status_options:
            data_dict['Status'] = status_options[user_input.text]
        else:
            bot.send_message(
                user_input.chat.id,
                "Invalid status option. Please enter a valid option (1-4).")
    except ValueError as e:
        bot.send_message(
            user_input.chat.id,
            f"An error occurred in get_status function >: {str(e)}")
    update_status(user_input, data_dict)


def update_status(user_input, data_dict):
    bot.send_message(user_input.chat.id,
                     " Updating the Data Base Please Wait...")
    confirmation = append_data(data_dict)
    if confirmation == True:
        message_text = "Data updated in the DB\n\n"
        for item, key in data_dict.items():
            message_text += f'{item} : {key}\n'
        message_text += "\n\nPress /start to restart"
        bot.send_message(5579239229, message_text)
        bot.send_message(user_input.chat.id, "Press /start to restart")
    else:
        bot.send_message(user_input.chat.id,
                         f"An Error In append_data function : {confirmation}")
        bot.send_message(user_input.chat.id, "Press /start to restart")
    return


        
    def data_sorter(self, user_input):
        information = data_processor.extract_info(user_input.text)
        if information:
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
        else:
            self.bot.send_message(user_input.chat.id,"No pattern Found For the text, Please enter the amount")
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
            self.bot.send_message(5579239229, user_input.text)