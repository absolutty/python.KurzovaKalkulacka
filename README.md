# Kurzová kalkulačka

Aplikácia kurzová kalkulačka slúži primárne na prevod jednej FIAT meny na druhú. <br>
Dáta sú načítavané live, z API https://www.exchangerate-api.com. Týmto spôsobom vieme zabezpečiť presnú
konverziu meny.

![Ilustrácia GUI](https://github.com/absolutty/python.KurzovaKalkulacka/blob/master/img/img-1.PNG)

Ďalej je možné si pozrieť rok nazad vývoj meny ku danej mene (napr. EUR --> USD). <br>
Tieto dáta sú následne vykreslované pomocou knižnice **Matplotlib**

Možno bude potrebné doinštalovať tieto knižnice pre správne fungovanie aplikácie:

```python
pip install matplotlib
pip install requests
pip install pandas
pip install numpy
```
