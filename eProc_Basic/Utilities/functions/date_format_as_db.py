# To convert date entered in search page to database field format
def convert_date_to_str(self, date_val):
    return date_val.replace("-", "") + "000000"