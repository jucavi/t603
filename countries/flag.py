import requests

url = 'https://restcountries.com/v3.1/'
    
def get_flag(flag):
    return flag.encode('ascii',"backslashreplace")

    
flag = '''🇦🇫'''
encode_flag = get_flag(flag)
print(encode_flag.decode().upper())
