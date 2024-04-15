from random import choice

import pymorphy3
from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from data import db_session
from data.users import User
from forms.analyze_form import AnalyzeForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'school_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")

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
            'Coll': 'собирательное'
            }
signs_dict = {
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


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=["POST", "GET"])
def index():
    form = AnalyzeForm()
    analyzes = []
    if form.validate_on_submit():
        word = form.input_word.data.strip()
        form.input_word.data = word.capitalize()
        morph = pymorphy3.MorphAnalyzer().parse(word)
        parsers = [i for i in morph if all([j not in ["Surn", "Name", "Patr", "UNKN", "Slng", "Erro"] for j in
                                            str(i.tag).replace(" ", ",").split(",")]) and i.score >= 0.2]
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

                elif "компаратив" in s:
                    s[0] = "прилагательное"
                    s.append("сравнительная степень")
                analyzes.append(", ".join(s))
            else:
                form.input_word.errors.append("Некорректный ввод")
                break
        if not parsers:
            form.input_word.errors.append("Некорректный ввод")
    return render_template("index.html", form=form, title="Главная", analyzes=analyzes)


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            form.email.errors.append("Пользователь с этой почтой уже существует")
        if form.password.data != form.repeat_password.data:
            form.repeat_password.errors.append("Пароли не совпадают")
        if not db_sess.query(User).filter(
                User.email == form.email.data).first() and form.password.data == form.repeat_password.data:
            new_user = User(email=form.email.data)
            new_user.set_password(form.password.data)
            db_sess.add(new_user)
            db_sess.commit()
            return redirect("/login")
    return render_template("register.html", form=form, title="Регистрация")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            form.login_email.errors.append("Пользователь не найден")
        elif not user.check_password(form.password.data):
            form.password.errors.append("Неверный пароль")
        else:
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form, title="Вход")


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/test/", methods=["GET", "POST"])
def test():
    global parsers, sign
    test_word = choice([i.word for i in pymorphy3.MorphAnalyzer().parse(choice(
        ["полить", "красивый", "машина", "лампа", "построить", "когда", "вечер", "зелёный", "металлический"]))[
        0].lexeme])
    parsers = [i for i in pymorphy3.MorphAnalyzer().parse(test_word) if all(
        [True if j not in ["Surn", "Name", "Patr"] else False for j in str(i.tag).replace(" ", ",").split(",")])]
    signs = ["POS"]
    for i in parsers:
        if i.tag.animacy and "animacy" not in signs:
            signs.append("animacy")
        if i.tag.aspect and "aspect" not in signs:
            signs.append("aspect")
        if i.tag.case and "case" not in signs:
            signs.append("case")
        if i.tag.gender and "gender" not in signs:
            signs.append("gender")
        if i.tag.mood and "mood" not in signs:
            signs.append("mood")
        if i.tag.number and "number" not in signs:
            signs.append("number")
        if i.tag.person and "person" not in signs:
            signs.append("person")
        if i.tag.tense and "tense" not in signs:
            signs.append("tense")
        if i.tag.transitivity and "transitivity" not in signs:
            signs.append("transitivity")
        if i.tag.voice and "voice" not in signs:
            signs.append("voice")
    sign = choice(signs)
    params = {"word": test_word,
              "sign": signs_dict[sign][0],
              "variants": list(dict.fromkeys([tag_dict[j].capitalize() for j in signs_dict[sign][1:] if
                                              j not in ("COMP", "PREP", "CONJ", "PRCL", "INTJ", "PRED")])),
              "title": "Тест"}
    return render_template("test.html", **params)


@app.route("/check_answer/", methods=["POST"])
def check_answer():
    correct_answers = set()
    for k in parsers:
        if eval(f"k.tag.{sign}"):
            correct_answer = tag_dict[eval(f"k.tag.{sign}")]
            correct_answers.add(correct_answer)
            if request.json["answer"].lower() == correct_answer or (request.json["answer"].lower() in (
            "полное прилагательное", "краткое прилагательное") and correct_answers == "компаратив"):
                return jsonify(status="ok", correct_answers=list(correct_answers))
    return jsonify(status="wrong", correct_answers=list(correct_answers))


if __name__ == '__main__':
    db_sess = db_session.create_session()
    app.run(port=9999)
