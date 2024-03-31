import datetime
from random import choice

import pymorphy3
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox

from test_page_ui import Ui_Form

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
user_ID = None


class TestForm(QWidget, Ui_Form):
    def __init__(self, data_base):
        super().__init__()
        self.setupUi(self)
        self.answer_variants.setStyleSheet("""
        QComboBox {color:#FFFFFF;
                    background:#001D3D;
                    border-radius:15px;
                    font-family:"Object Sans Heavy";
}
""")
        self.data_base = data_base
        self.test_result = 0
        self.parsers = None
        self.sings = None
        self.sing = None
        self.user_ID = None
        self.tag_dict = {'NOUN': 'существительное',
                         'ADJF': 'полное прилагательное',
                         'ADJS': 'краткое прилагательное',
                         'COMP': 'компаратив',
                         'VERB': 'глагол',
                         'INFN': 'глагол',
                         'PRTF': 'полное причастие',
                         'PRTS': 'краткое причастие',
                         'GRND': 'деепричастие',
                         'NUMR': 'числительное',
                         'ADVB': 'наречие',
                         'NPRO': 'местоимение',
                         'PRED': 'предикатив',
                         'PREP': 'предлог',
                         'CONJ': 'союз',
                         'PRCL': 'частица',
                         'INTJ': 'междометие',
                         'anim': 'одушевлённое',
                         'inan': 'неодушевлённое',
                         'masc': 'мужской род',
                         'femn': 'женский род',
                         'neut': 'средний род',
                         'ms-f': 'общий род',
                         'sing': 'единственное число',
                         'plur': 'множественное число',
                         'Sgtm': 'единственное число',
                         'Pltm': 'множественное число',
                         'Fixd': 'неизменяемое',
                         'nomn': 'именительный падеж',
                         'gent': 'родительный падеж',
                         'datv': 'дательный падеж',
                         'accs': 'винительный падеж',
                         'ablt': 'творительный падеж',
                         'loct': 'предложный падеж',
                         'Supr': 'превосходная степень',
                         'Qual': 'качественное',
                         'Anum': 'порядковое',
                         'Poss': 'притяжательное',
                         'perf': 'совершенный вид',
                         'impf': 'несовершенный вид',
                         'tran': 'переходный',
                         'intr': 'непереходный',
                         'Impe': 'безличный',
                         'Refl': 'возвратный',
                         '1per': '1-ое лицо',
                         '2per': '2-ое лицо',
                         '3per': '3-е лицо',
                         'pres': 'настоящее время',
                         'past': 'прошедшее время',
                         'futr': 'будущее время',
                         'indc': 'изъявительное наклонение',
                         'impr': 'повелительное наклонение',
                         'actv': 'действительный залог',
                         'pssv': 'страдательный залог',
                         'Coll': 'собирательное',
                         'Erro': 'опечатка'
                         }
        self.signs_dict = {
            "POS": ["часть речи", 'NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS',
                    'GRND', 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ'],
            "animacy": ["одушевлённость", "anim", "inan"],
            "aspect": ["вид", "perf", "impf"],
            "case": ["падеж", "nomn", "gent", "datv", "accs", "ablt", "loct"],
            "gender": ["род", "masc", "femn", "neut", "ms-f"],
            "mood": ["наклонение", "indc", "impr"],
            "number": ["число", "sing", "plur", "Sgtm", "Pltm"],
            "person": ["лицо", "1per", "2per", "3per"],
            "tense": ["время", "pres", "past", "futr"],
            "transitivity": ["переходность", "tran", "intr"],
            "voice": ["залог", "actv", "pssv"]}
        self.next_btn.clicked.connect(self.next_test)
        self.end_test_btn.clicked.connect(self.end_test)
        self.answer_btn.clicked.connect(self.answer)

    def test(self):
        self.answer_variants.clear()
        self.test_word = choice([i.word for i in pymorphy3.MorphAnalyzer().parse(
            choice(
                ["полить", "красивый", "машина", "лампа", "построить", "когда", "вечер", "зелёный", "металлический"]))[
            0].lexeme])
        self.parsers = [i for i in pymorphy3.MorphAnalyzer().parse(self.test_word) if
                        all([True if j not in ["Surn", "Name", "Patr"] else False for j in
                             str(i.tag).replace(" ", ",").split(",")])]
        self.signs = ["POS"]
        for i in self.parsers:
            if i.tag.animacy and "animacy" not in self.signs:
                self.signs.append("animacy")
            if i.tag.aspect and "aspect" not in self.signs:
                self.signs.append("aspect")
            if i.tag.case and "case" not in self.signs:
                self.signs.append("case")
            if i.tag.gender and "gender" not in self.signs:
                self.signs.append("gender")
            if i.tag.mood and "mood" not in self.signs:
                self.signs.append("mood")
            if i.tag.number and "number" not in self.signs:
                self.signs.append("number")
            if i.tag.person and "person" not in self.signs:
                self.signs.append("person")
            if i.tag.tense and "tense" not in self.signs:
                self.signs.append("tense")
            if i.tag.transitivity and "transitivity" not in self.signs:
                self.signs.append("transitivity")
            if i.tag.voice and "voice" not in self.signs:
                self.signs.append("voice")
        self.sign = choice(self.signs)
        self.word_label.setText(f"Слово для разбора: {self.test_word}")
        self.sign_label.setText(f"Выберите {self.signs_dict[self.sign][0]}")
        self.answer_variants.addItem("")
        self.answer_variants.addItems(list(dict.fromkeys([self.tag_dict[j] for j in self.signs_dict[self.sign][1:]])))

    def first_test(self):
        from enter_page import user_ID_1
        from registration_page import user_ID_2
        global user_ID
        self.user_ID = user_ID_1 or user_ID_2
        user_ID = self.user_ID
        self.test()

    def next_test(self):
        if self.answer_btn.isEnabled():
            self.answer_label.show()
            self.answer_label.setText("СНАЧАЛА НУЖНО ОТВЕТИТЬ")
            self.answer_label.setStyleSheet("background:#000814;color:#FFC300;border-radius:10px")
        else:
            self.test()
            self.answer_label.hide()
            self.answer_btn.setEnabled(True)
            self.answer_btn.setStyleSheet(
                "border:none;color:#FFFFFF;background:#001D3D;border-radius:15px;font-family:'Object Sans Heavy';")

    def answer(self):
        self.answer_label.show()
        if not self.answer_variants.currentText():
            self.answer_label.setText("ВЫБЕРИТЕ ВАРИАНТ ОТВЕТА")
            self.answer_label.setStyleSheet("background:#000814;color:#FFC300;border-radius:10px")
        else:
            for k in self.parsers:
                if eval(f"k.tag.{self.sign}"):
                    if self.answer_variants.currentText() == self.tag_dict[eval(f"k.tag.{self.sign}")]:
                        self.test_result = 1
                        break
            self.answer_btn.setStyleSheet(
                "color:#CCCCCC;background:#1D334A;border-radius:15px;font-family:'Object Sans Heavy';")
            self.answer_btn.setEnabled(False)
            if self.user_ID:
                date, time = str(datetime.datetime.now().date()), str(datetime.datetime.now().time()).split(".")[0]
                self.data_base.cursor().execute(
                    "INSERT INTO tests(user_ID, test_word, test_result, date, time) VALUES(?, ?, ?, ?, ?)",
                    (self.user_ID, self.test_word, self.test_result, date, time,))
                self.data_base.connection().commit()
            if self.test_result:
                self.answer_label.setText("ПРАВИЛЬНЫЙ ОТВЕТ")
                self.answer_label.setStyleSheet("background:#003566;color:#FFD60A;border-radius:10px")
            else:
                self.answer_label.setText("НЕПРАВИЛЬНЫЙ ОТВЕТ")
                self.answer_label.setStyleSheet("background:#000814;color:#FFC300;border-radius:10px")
            self.test_result = 0

    def end_test(self):
        if self.answer_btn.isEnabled():
            self.answer_label.setText("СНАЧАЛА НУЖНО ОТВЕТИТЬ")
            self.answer_label.setStyleSheet("background:#000814;color:#FFC300;border-radius:10px")
        else:
            self.end_test_dialog = QMessageBox(self)
            answer = self.end_test_dialog.question(self, '', "Вы дейстительно хотите завершитьо тест?",
                                                   QMessageBox.Yes | QMessageBox.No)

            if answer == self.end_test_dialog.Yes:
                self.parent().setCurrentIndex(6)
                self.test()
                self.answer_label.hide()
                self.answer_btn.setEnabled(True)
                self.answer_btn.setStyleSheet(
                    "border:none;color:#FFFFFF;background:#001D3D;border-radius:15px;font-family:'Object Sans Heavy';")
