import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import sklearn
import numpy as np
from sklearn.ensemble import RandomForestClassifier

with open('data/model.pickle', 'rb') as f:
    model = pickle.load(f)

X = pd.read_csv('data/X.csv')
X_train, X_test = train_test_split(X, test_size=0.3, random_state=20, shuffle=True)
object = StandardScaler()
X_train.iloc[:, [0, 3, 4]] = object.fit_transform(X_train.iloc[:, [0, 3, 4]])
X = None
X_test = None
X_train = None

import streamlit as st
from PIL import Image
img = Image.open('data/img_1.jpeg')

st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Кредитный скоринг",
        page_icon=img
)

st.markdown("# Кредитный скоринг")
st.markdown("##### *Узнай о своей возможности получить кредит уже сегодня!*")

st.image(img, width = 500)
st.sidebar.header('Ваши данные')
age = st.sidebar.slider("Возраст", min_value=18, max_value=100, value=30,
                            step=1)

dependents = st.sidebar.slider("Количество иждивенцев на попечении", min_value=0, max_value=20, value=0,
                            step=1)

loans = st.sidebar.slider("Количество текущих открытых кредитов или кредитных карт", min_value=0, max_value=100, value=0,
                            step=1)

income = st.sidebar.number_input("Ежемесячный доход")

debt = st.sidebar.number_input("Ежемесячные расходы (выплаты по долгам, алименты, расходы на жилье)")

number_30_59 = st.sidebar.slider("Сколько раз за последние 2 года у Вас наблюдалась просрочка оплаты по кредиту от 30 до 59 дней?",
                                 min_value=0, max_value=100, value=0, step=1)

number_60_89 = st.sidebar.slider("Сколько раз за последние 2 года у Вас наблюдалась просрочка оплаты по кредиту от 60 до 89 дней?",
                                 min_value=0, max_value=100, value=0, step=1)

number_90 = st.sidebar.slider("Сколько раз у Вас наблюдалась просрочка оплаты по кредиту 90 дней и более?",
                                 min_value=0, max_value=100, value=0, step=1)

balance = st.sidebar.number_input("Общий баланс средств на всех Ваших картах и счетах")

credit_cards = st.sidebar.number_input("Сумма кредитных лимитов по всем кредитным картам")

if income != 0:
    ratio = debt/income
else:
    ratio = debt / 0.0000001

if age < 21:
    group_age = 1
elif (age >= 21) and (age < 35):
    group_age = 2
elif (age >= 35) and (age < 50):
    group_age = 3
elif (age >= 50) and (age < 65):
    group_age = 4
else:
    group_age = 5

if credit_cards != 0:
    RUUL = balance/credit_cards
else:
    RUUL = balance

if loans < 11:
    credit_group = 1
elif (loans >= 11) and (loans < 15):
    credit_group = 2
elif (loans >= 15) and (loans < 19):
    credit_group = 3
elif (loans >= 19) and (loans < 28):
    credit_group = 4
else:
    credit_group = 5

user = pd.DataFrame(columns=['RevolvingUtilizationOfUnsecuredLines', 'age',
                             'NumberOfTime30-59DaysPastDueNotWorse', 'DebtRatio', 'MonthlyIncome',
                             'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
                             'NumberOfTime60-89DaysPastDueNotWorse', 'NumberOfDependents',
                             'RealEstateLoansOrLines', 'GroupAge'])

user_data = {'RevolvingUtilizationOfUnsecuredLines': RUUL,
             'age': age,
             'NumberOfTime30-59DaysPastDueNotWorse': number_30_59,
             'DebtRatio': ratio,
             'MonthlyIncome': income,
             'NumberOfOpenCreditLinesAndLoans': loans,
             'NumberOfTimes90DaysLate': number_90,
             'NumberOfTime60-89DaysPastDueNotWorse': number_60_89,
             'NumberOfDependents': dependents,
             'RealEstateLoansOrLines': credit_group,
             'GroupAge': group_age}

user = user._append(user_data, ignore_index=True)
user_show = pd.DataFrame(columns=['Возраст', 'Иждивенцы', 'Кредиты', 'Доход', 'Расходы', 'Просрочки 30-59 дней',
                                  'Просрочки 60-89 дней', 'Просрочки от 90 дней', 'Текущий баланс',
                                  'Лимит по кредитным картам'])

user_show_data = {'Возраст': age,
                  'Иждивенцы': dependents,
                  'Кредиты': loans,
                  'Доход': income,
                  'Расходы': debt,
                  'Просрочки 30-59 дней': number_30_59,
                  'Просрочки 60-89 дней': number_60_89,
                  'Просрочки от 90 дней': number_90,
                  'Текущий баланс': balance,
                  'Лимит по кредитным картам': credit_cards}

user_show = user_show._append(user_show_data, ignore_index=True)

st.write("## Ваши данные")
st.write(user_show)

user.iloc[:, [0, 3, 4]] = object.transform(user.iloc[:, [0, 3, 4]])

p = model.predict(user)
st.write("## Решение банка")

if p == 0:
    st.write('Мы можем выдать Вам кредит! Поздравляем!')
else:
    st.write('К сожалению, мы не можем выдать Вам кредит :-(')






