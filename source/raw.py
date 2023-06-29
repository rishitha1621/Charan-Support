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

