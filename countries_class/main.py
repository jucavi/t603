import requests as req


# res=req.get(url).json()

user = ""

while user != "q":
    print("1. Buscar país")
    user = input(": ")
    if user == "1":
        country_name = input("País: ")
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        res = req.get(url).json()[0]
        country_lang = list(res["languages"].values())[0]
        print(f'Capital: {res["capital"][0]}')
        print(f'Población: {res["population"]}')
        print(f'Superficie: {res["area"]}')
        print(f'Lenguaje: {country_lang}')
        input("...")