from typing import Final

from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as message

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from KurzovaKalkulacka import KurzovaKalkulacka


class GUI():
    # staticke final premenne
    NAZOV: Final = "Kurzová kalkulačka"
    DEFAULT_FARBA: Final = "orange red"

    # urcuju ake meny budu prvotne zobrazene (premena Z meny --> DO meny)
    DEFAULT_FROM: Final = "EUR"
    DEFAULT_TO: Final = "CZK"

    ## ATRIBUTY ##
    # kurzova_kalkulacka - trieda, kt zabezbecuje premenu jednotlivych mien

    ## GUI ##
    # main_window - tkinter na ktorom su zobrazovane jednotlive elementy
    # label_intro - uvodny text, nazov aplikacie
    # label_date - obsahuje datum a čas z ktorého sú tieto kurzy načítané
    # entry_field - mnozstvo meny z ktorej je konvertovane
    # converted_field - konvertovany vysledok
    # from_currency_dropdown - zoznam mien Z ktorych je mozne konvertovat
    # to_currency_dropdown - zoznam mien DO ktorych je mozne konvertovat
    # btn_konvert - spusti kurzovu konverziu
    # btn_historia - zobrazi historiu kurzov (12 mesiacov dozadu)
    def __init__(self):
        self.to_currency_variable = None
        self.from_currency_variable = None
        self.kurzova_kalkulacka = KurzovaKalkulacka(self.DEFAULT_FROM)

        self.main_window = None
        self.label_intro = None
        self.label_date = None
        self.entry_field = None
        self.converted_field = None

        self.from_currency_dropdown = None
        self.to_currency_dropdown = None

        self.btn_konvert = None
        self.btn_historia = None

        self.init_gui()

    # slúži na inicializáciu grafických prvkov Tkinter-u
    def init_gui(self):
        # init self.window
        self.main_window = Tk()
        self.main_window.title(self.NAZOV)
        self.main_window.geometry("580x250")
        self.main_window.resizable(False, False)

        # init label_intro
        self.label_intro = Label(self.main_window, text=self.NAZOV, bg=self.DEFAULT_FARBA, fg="white",
                                 font="none 22 bold",
                                 relief=tk.RIDGE, borderwidth=10)
        self.label_intro.grid(row=0, column=1)

        # rozdeleny_datum:
        #   - rozdeleny_datum[0] = akutalRok
        #   - rozdeleny_datum[1] = aktualMesiac
        #   - rozdeleny_datum[2] = aktual den
        rozdeleny_datum = (self.kurzova_kalkulacka.data['date']).split('-')
        formatovany_datum = "{aktualDen}. {aktualMesiac}. {aktualRok}" \
            .format(aktualDen=rozdeleny_datum[2], aktualMesiac=rozdeleny_datum[1], aktualRok=rozdeleny_datum[0])

        # init self.label_date
        self.label_date = Label(self.main_window, text=f"Aktualny datum: " + formatovany_datum, relief=tk.GROOVE,
                                borderwidth=5)
        self.label_date.grid(row=1, column=1)

        # init self.entry_field
        self.entry_field = Entry(self.main_window, bd=3, relief=tk.RIDGE, justify=tk.CENTER, validate='key',
                                 validatecommand=(self.main_window.register(self.is_valid), '%P'))
        self.entry_field.grid(row=3, column=0)

        # init self.converted_field
        self.converted_field = Label(self.main_window, text='', fg='black', bg='white', relief=tk.RIDGE,
                                     justify=tk.CENTER, width=17, borderwidth=3)
        self.converted_field.grid(row=3, column=2)

        # init self.from_currency_variable a self.to_currency_variable
        self.from_currency_variable = StringVar(self.main_window)
        self.from_currency_variable.set(self.DEFAULT_FROM)  # default value
        self.to_currency_variable = StringVar(self.main_window)
        self.to_currency_variable.set(self.DEFAULT_TO)  # default value

        font = ("Courier", 12, "bold")
        self.main_window.option_add('*TCombobox*Listbox.font', font)
        self.from_currency_dropdown = ttk.Combobox(self.main_window, textvariable=self.from_currency_variable,
                                                   values=list(self.kurzova_kalkulacka.premenne_kurzy.keys()),
                                                   font=font,
                                                   state='readonly', width=12, justify=tk.CENTER)
        self.from_currency_dropdown.grid(row=2, column=0)

        self.to_currency_dropdown = ttk.Combobox(self.main_window, textvariable=self.to_currency_variable,
                                                 values=list(self.kurzova_kalkulacka.premenne_kurzy.keys()), font=font,
                                                 state='readonly', width=12, justify=tk.CENTER)
        self.to_currency_dropdown.grid(row=2, column=2)

        self.btn_konvert = Button(self.main_window, text="Convert", bg=self.DEFAULT_FARBA, fg="white",
                                  command=self.prevod)
        self.btn_konvert.config(font=('Courier', 10, 'bold'))
        self.btn_konvert.grid(row=2, column=1, rowspan=2)

        self.btn_historia = Button(self.main_window, text="Porovnanie kurzu mien za obdobie 12 mesiacov",
                                   command=self.historia)
        self.btn_historia.grid(row=4, column=1)

    # konvertuje z meny do meny a vysledok nastavi do self.converted_field
    def prevod(self):
        try:
            mnozstvo = float(self.entry_field.get())
            z_meny = self.from_currency_variable.get()
            do_meny = self.to_currency_variable.get()

            converted_amount = round(self.kurzova_kalkulacka.prevod(z_meny, do_meny, mnozstvo), 2)
            self.converted_field.config(text=str(converted_amount))
        except ValueError:
            message.showerror("Chyba!", "Nespravne zadana hodnota na prevod!")

    # overenie spravnosti zadania do entry_field
    @staticmethod
    def is_valid(overovany_string):
        # musi sa jednat o cislo ALEBO je prazdny string ALEBO obsahuje znaky '.', ','
        return (overovany_string.isdigit()) or (not overovany_string) or ('.' in overovany_string) or (
                ',' in overovany_string)

    # slúži na zobrazenie ďalšieho okna, kt. obsahuje graf pomocou knižnice Matplotlib
    # graf zobrazuje vyvoj druhej meny k pomeru vyvoja prvej meny
    def historia(self):
        hist_premenne_kurzy = self.kurzova_kalkulacka.historia(self.from_currency_variable.get(),
                                                               self.to_currency_variable.get())

        hist_window = Toplevel(self.main_window)
        hist_window.title("Vyvoj meny za 12 mesiacov")
        hist_window.geometry("800x400")
        hist_window.resizable(False, False)

        matplotlib.use("TkAgg")

        figure = Figure(figsize=(8, 4), dpi=100)
        figure.suptitle("Vývoj " + self.from_currency_variable.get() + " do " + self.to_currency_variable.get() + " (za posledný rok) graf")

        plot = figure.add_subplot(1, 1, 1)
        plot.plot(color="red", marker="o")

        plot.plot(hist_premenne_kurzy.get(self.kurzova_kalkulacka.KEY),
                  hist_premenne_kurzy.get(self.kurzova_kalkulacka.VALUE),
                  color="red", marker="o")
        figure.autofmt_xdate() # automatické naklonenie dátumov
        plot.grid() # zobrazenie mriežky

        canvas = FigureCanvasTkAgg(figure, hist_window)
        canvas.get_tk_widget().grid(row=0, column=0)

