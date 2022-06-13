from decimal import getcontext
import gspread

gc = gspread.service_account(filename='credentials.json')
sh = gc.open('Whatsapp')



# contacts = sh.worksheet('Contacts')
# res = contacts.get_all_records()
# res = contacts.get_all_values()
# res = contacts.row_values(1)
# res = contacts.col_values(1)
# res = contacts.get('1:3')
# print(res)

def get_contacts():
    contacts_sheet = sh.worksheet('Contacts')
    contacts = contacts_sheet.get_all_values()
    return contacts


def update_sheet(data):
    contacts_sheet = sh.worksheet('Contacts')
    contacts_sheet.update(data)

# update_sheet(data)
# data = ["Gaurav Taj", "LIG-965", "https://gauravpatel.live"]
# contacts.insert_row(data, 3)


