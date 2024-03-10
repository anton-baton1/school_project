from flask import Flask, render_template, request
import pymorphy3
from forms.analyze_form import AnalyzeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


# login_manager = LoginManager()
# login_manager.init_app(app)
# db_session.global_init("db/blogs.db")


@app.route("/", methods=["POST", "GET"])
def index():
    form = AnalyzeForm()
    analyzes = []
    if form.validate_on_submit():
        tag_dict = {'NOUN': 'существительное',
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
        word = form.input_word.data.strip()
        morph = pymorphy3.MorphAnalyzer().parse(word)
        flag = False
        if word.isalpha():
            parsers = [i for i in morph if all(
                [True if j not in ["Surn", "Name", "Patr", "UNKN", "Slng"] else False for j in
                 str(i.tag).replace(" ", ",").split(",")])]
            for q, k in enumerate(parsers):
                if len(k.methods_stack) == 1 and str(k.methods_stack[0][0]) == "DictionaryAnalyzer()":
                    parser = str(k.tag).replace(" ", ",").split(",")
                    s = [tag_dict[j] for j in parser if j in tag_dict]
                    s.insert(1, f"н.ф - {k.normal_form}")

                    if "существительное" in s:
                        noun = pymorphy3.MorphAnalyzer().parse(k.normal_form)[0]

                        if (noun.tag.gender == "femn" or noun.tag.gender == "masc") and (
                                noun.word.endswith("а") or noun.word.endswith("я")):
                            s.append("I склонение")
                        elif noun.tag.gender == "masc" or (
                                noun.tag.gender == "neut" and (noun.word.endswith("о") or noun.word.endswith("е"))):
                            s.append("II склонение")
                        elif noun.tag.gender == "femn" and noun.word.endswith("ь"):
                            s.append("III склонение")

                    elif "глагол" in s:
                        normal_form = k.normal_form
                        if normal_form.endswith(("ся", "сь")):
                            s.append("возвратный")
                            normal_form = normal_form[:-2]
                        verb = pymorphy3.MorphAnalyzer().parse(normal_form)[0]

                        if (verb.word.endswith("ить") or verb.word in (
                                "держать", "зависеть", "терпеть", "слышать", "смотреть", "обидеть", "видеть", "дышать",
                                "ненавидеть", "вертеть", "гнать")) and verb.word not in ("брить", "стелить"):
                            s.append("II спряжение")
                        else:
                            s.append("I спряжение")
                    analyzes.append(", ".join(s))
                    flag = True
        if not word.isalpha() or not flag:
            form.input_word.errors.append("Некорректный ввод")
    return render_template("base.html", form=form, title="qwe", analyzes=analyzes)


if __name__ == '__main__':
    app.run(port=9999)
