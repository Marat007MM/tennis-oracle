import streamlit as st
import asyncio
import requests
import time
from datetime import datetime
from aiogram import Bot

# --- 1. НАСТРОЙКИ (ОБЯЗАТЕЛЬНО ЗАПОЛНИ) ---
TELEGRAM_TOKEN = "8117380595:AAF7uV_DYdb0zR_dOMD6htlle3d4Ole8j4A"
CHAT_ID = "7100053524"
bot = Bot(token=TELEGRAM_TOKEN)

# --- 2. МОЗГ СИСТЕМЫ (Winner + Total + Qi Men) ---
class TennisGodAI:
    def __init__(self):
        # Энергия Ци Мэнь (12 двухчасовок)
        self.qimen_cycle = [1.5, 0.7, 0.5, 1.2, 1.1, 1.4, 0.8, 1.3, 1.0, 0.9, 1.6, 0.5]

    def analyze(self, m):
        try:
            # Математика: Dominance Ratio
            dr = (m['won_ret'] / m['total_ret']) / (m['lost_serv'] / m['total_serv'])
            # Физика: Speed Efficiency (Decay)
            decay = m['curr_speed'] / m['avg_speed']
            # Метафизика: Ци Мэнь (авто-час)
            q_power = self.qimen_cycle[(datetime.now().hour // 2) % 12]
            
            # Итоговый скоринг
            win_score = (dr * 0.4) + (q_power * 0.4) + (decay * 0.2)
            
            # Логика Исходов
            winner_txt = "⏳ ЖДЕМ"
            if win_score > 1.48: winner_txt = f"🔥 ПОБЕДА {m['p1']}"
            elif win_score < 0.82: winner_txt = f"❄️ ПОБЕДА {m['p2']}"

            # Логика Тоталов
            total_txt = "⚖️ ТОТАЛ: НОРМА"
            if decay > 0.98 and dr < 1.1: total_txt = "📈 СИГНАЛ: ТБ (БОЛЬШЕ)"
            elif decay < 0.92 or dr > 1.55: total_txt = "📉 СИГНАЛ: ТМ (МЕНЬШЕ)"

            # Риск-менеджмент
            risk = "ЗЕЛЕНЫЙ"
            if decay < 0.91: risk = "🚨 ПРОДАТЬ (CASH OUT)!"

            return winner_txt, total_txt, risk, round(win_score, 2)
        except Exception:
            return "ОШИБКА ДАННЫХ", "НЕТ", "СЕРЫЙ", 1.0

# --- 3. ФУНКЦИЯ ОТПРАВКИ (С защитой от ошибок) ---
async def send_to_tg(text):
    try:
        await bot.send_message(CHAT_ID, text, parse_mode="Markdown")
    except Exception as e:
        st.error(f"Ошибка Телеграм: {e}")

# --- 4. ИНТЕРФЕЙС И МОНИТОРИНГ ---
st.set_page_config(layout="wide", page_title="Tennis Oracle Bot 2026")
st.title("🎾 Tennis Oracle: Autonomous Winners & Totals")

if 'alerts_history' not in st.session_state:
    st.session_state.alerts_history = {}

oracle = TennisGodAI()

# Имитация входящих матчей (Замени на requests.get к API в будущем)
live_matches = [
    {"id": "m1", "p1": "Djokovic", "p2": "Alcaraz", "won_ret": 22, "total_ret": 40, "lost_serv": 6, "total_serv": 45, "curr_speed": 184, "avg_speed": 195},
    {"id": "m2", "p1": "Sinner", "p2": "Medvedev", "won_ret": 14, "total_ret": 35, "lost_serv": 12, "total_serv": 38, "curr_speed": 198, "avg_speed": 192}
]

cols = st.columns(len(live_matches))

for i, m in enumerate(live_matches):
    win, tot, risk, score = oracle.analyze(m)
    with cols[i]:
        with st.container(border=True):
            st.header(f"{m['p1']} vs {m['p2']}")
            st.subheader(f"Исход: {win}")
            st.write(f"Тотал: **{tot}**")
            st.markdown(f"**Риск: {risk}**")
            st.progress(min(score/2, 1.0), text=f"Уверенность: {score}")

            # АВТО-ОТПРАВКА В ТГ (Только если статус новый)
            current_status = f"{win}_{tot}_{risk}"
            if current_status != st.session_state.alerts_history.get(m['id']):
                if "ПОБЕДА" in win or "СИГНАЛ" in tot or "ПРОДАТЬ" in risk:
                    msg = f"🎾 *{m['p1']} - {m['p2']}*\n🏆 {win}\n📊 {tot}\n🛡 Риск: {risk}\n📈 Score: {score}"
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(send_to_tg(msg))
                    st.session_state.alerts_history[m['id']] = current_status
                    st.toast(f"Сигнал по {m['p1']} отправлен!")

st.divider()
st.caption(f"Последнее обновление: {datetime.now().strftime('%H:%M:%S')}. Работает на базе Tennis Abstract & Qi Men.")

# Рефреш страницы каждые 30 секунд
time.sleep(30)
st.rerun()
