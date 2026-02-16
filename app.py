import asyncio
import requests
from datetime import datetime
from aiogram import Bot

# --- НАСТРОЙКИ ---
TOKEN = "8117388595:AAF7v_DYb0zR_MOMD@tlle3d4O1-35A"
CHAT_ID = "7180053524"
RAPID_KEY = "29d2b35e9fmsh083609010ee3bc1p13ef3cjsne0ee6b01ed6e"

bot = Bot(token=TOKEN)

class SuperOracle:
    def __init__(self):
        # Энергия Ци Мэнь (12 стражей часа)
        self.qimen_map = [1.5, 0.7, 0.5, 1.2, 1.1, 1.4, 0.5, 1.3, 1.0, 0.8, 1.6, 0.5]

    def get_abstract_dr(self, match):
        """Логика Tennis Abstract: расчет Dominance Ratio (DR)"""
        try:
            # Вытягиваем % выигранных очков на приеме и подаче
            w1_ret = float(match.get('w1_return_pts_won', 40))
            w2_serv_lost = 100 - float(match.get('w2_service_pts_won', 60))
            dr = (w1_ret / 100) / (max(w2_serv_lost, 1) / 100)
            return dr
        except: return 1.0

    def get_ai_context(self, match):
        """Контекст AI: оценка мотивации и покрытия"""
        surface = match.get('surface', 'hard').lower()
        # ИИ-фильтр: на грунте DR важнее, на траве — эйсы
        return 1.1 if surface == 'clay' else 1.0

    def get_qimen(self):
        """Метафизический бонус часа"""
        hour_idx = int(datetime.now().hour / 2) % 12
        return self.qimen_map[hour_idx]

    def final_decision(self, match):
        dr = self.get_abstract_dr(match)
        ai_factor = self.get_ai_context(match)
        qimen = self.get_qimen()

        # Итоговая формула Оракула
        # (DR * Контекст ИИ) + Ци Мэнь
        total_score = (dr * ai_factor * 0.6) + (qimen * 0.4)

        if total_score > 1.45:
            return f"🔥 СИГНАЛ: ВХОД НА П1 (Score: {total_score:.2f})"
        elif total_score < 0.85:
            return f"🔥 СИГНАЛ: ВХОД НА П2 (Score: {total_score:.2f})"
        return None

async def run_monitoring():
    oracle = SuperOracle()
    print("--- СУПЕР-ОРАКУЛ (AI + ABSTRACT + QIMEN) ЗАПУЩЕН ---")
    
    while True:
        try:
            url = "https://tennis-api-atp-wta-itf.p.rapidapi.com"
            headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "tennis-api-atp-wta-itf.p.rapidapi.com"}
            
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                results = res.json().get('results', [])
                for m in results:
                    signal = oracle.final_decision(m)
                    if signal:
                        msg = f"🎾 {m.get('player_1')} vs {m.get('player_2')}\n{signal}"
                        await bot.send_message(CHAT_ID, msg)
            
            # Ждем 15 минут, чтобы не платить за RapidAPI (бесплатный лимит 100 запр/сут)
            await asyncio.sleep(900)
            
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(run_monitoring())

