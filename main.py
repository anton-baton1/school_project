import pymorphy3
from flask import Flask, render_template, redirect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from data import db_session
from data.users import User
from forms.analyze_form import AnalyzeForm
from forms.login_form import LoginForm
from forms.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/blogs.db")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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
        form.input_word.data = word.capitalize()
        morph = pymorphy3.MorphAnalyzer().parse(word)
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
            else:
                form.input_word.errors.append("Некорректный ввод")
                break
    return render_template("index.html", form=form, title="Главная", analyzes=analyzes)


@app.route("/register", methods=["GET", "POST"])
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


@app.route("/login", methods=["GET", "POST"])
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    db_sess = db_session.create_session()
    user = User(email="q")
    user.set_password("q")
    db_sess.add(user)
    db_sess.commit()

    app.run(port=9999)
