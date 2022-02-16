from typing import Final

import requests
import datetime


class KurzovaKalkulacka:
    # id na zaklade ktoreho je možné pristúpiť k dátam na stránke https://www.exchangerate-api.com/docs/overview
    API_ID: Final = "742ddf231a3aeacbdbb09cf5"

    # data - nacitana stranka prekonvertovana pomocou .json() do jsonFile. Tieto data su ulozene v premennej
    # premenne_kurzy - jednotlivych mien, defaultne nacitane pre EUR
    def __init__(self, zaciatocnaMena):
        self.premenne_kurzy = None
        self.data = None
        self.inicializuj(zaciatocnaMena)

    # inicializuje AKTUALNU konverziu meny na zaklade @param naZakladeMeny
    # naZakladeMeny = "USD": {"USD":1,"AED":3.67,"AFN":99.65,"ALL":107.53, ... }
    # naZakladeMeny = "EUR": {"EUR":1,"AED":4.18,"AFN":112.41,"ALL":121.25, ... }
    def inicializuj(self, naZakladeMeny):
        urlData = "https://api.exchangerate-api.com/v4/latest/" + naZakladeMeny

        response = requests.get(urlData)
        # odpoved zo servera obsahuje v sebe spravu 'error', to zn. ze response nebola uspesna!
        if "error" in response.text:
            raise KeyError("Zadana mena z ktorej mala byt robena konverzia NIE JE spravna!")
        self.data = response.json()
        self.premenne_kurzy = self.data['rates']

    # metóda spraví prevod zadaneho množstva meny do premieňanej meny
    def prevod(self, from_currency, to_currency, amount):
        self.inicializuj(from_currency)
        return round(amount * self.premenne_kurzy[to_currency], 4)

    KEY: Final = "dátum"
    VALUE: Final = "hodnota"

    # vráti dictionary kurzu meny base_currency DO to_currency
    # "dátum" : ['2022/01/31', '2021/12/31', '2021/11/30', ...]
    # "hodnota" : [24.4823, 24.9436, 25.6689, ... ]
    def historia(self, base_currency, to_currency):
        today = datetime.date.today()

        hist_premenne_kurzy = {
            self.KEY: [],
            self.VALUE: []
        }
        for i in range(12):
            # presun na posledny den v mesiaci
            first = today.replace(day=1)
            today = first - datetime.timedelta(days=1)

            urlData = "https://v6.exchangerate-api.com/v6/" + self.API_ID + "/history/" + base_currency
            urlData += "/" + today.strftime('%Y/%m/%d')

            response = requests.get(urlData)
            # odpoved zo servera obsahuje v sebe spravu 'error', to zn. ze response nebola uspesna!
            if "error" in response.text:
                raise KeyError("Zadana mena kt. vypisujes historiu NIE JE spravna!")

            data = response.json()
            helper = data['conversion_rates']

            hist_premenne_kurzy[self.KEY].append(today.strftime('%Y/%m/%d'))
            hist_premenne_kurzy[self.VALUE].append(helper[to_currency])

        return hist_premenne_kurzy
