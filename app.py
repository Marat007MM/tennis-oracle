import asyncio
import requests
from datetime import datetime
from aiogram import Bot

# --- 1. НАСТРОЙКИ (Твои данные) ---
TELEGRAM_TOKEN = "8117388595:AAF7v_DYb0zR_MOMD@tlle3d4O1-35A"
CHAT_ID = "7180053524"
RAPID_API_KEY = "29d2b35e9fmsh083609010ee3bc1p13ef3cjsne0ee6b01ed6e"
RAPID_API_HOST = "tennis-api-atp-wta-itf.p.rapidapi.com"

bot = Bot(token=TELEGRAM_TOKEN)

class TennisOraclePro:
    def __init__(self):
        # Энергия Ци Мэнь Дунь Цзя (12 периодов)
        self.qimen_energy = [1.5, 0.7, 0.5, 1.2, 1.1, 1.4, 0.5, 1.3, 1.0, 0.8, 1.6, 0.5]

    def calculate_dr(self, stats):
        """Расчет Dominance Ratio и силы подачи"""
        try:
            # Данные из Tennis Abstract / Betsapi через RapidAPI
            w1_ret_won = stats.get('w1_return_pts_won_pct', 40)
            w2_serv_lost = 100 - stats.get('w2_service_pts_won_pct', 60)
            
            # Формула DR
            dr = (w1_ret_won / 100) / (max(w2_serv_lost, 1) / 100)
            
            # Aces vs Double Faults (Коэффициент надежности)
            aces = stats.get('w1_aces', 0)
            df = stats.get('w1_double_faults', 0)
            serve_reliability = (aces + 1) / (df + 1)
            
            return dr, serve_reliability
        except:
            return 1.0, 1.0

    def get_qimen(self):
        """Текущая метафизическая сила часа"""
        hour_idx = int(datetime.now().hour / 2) % 12
        return self.qimen_energy[hour_idx]

    def analyze_match(self, match):
        dr, reliability = self.calculate_dr(match)
        q_power = self.get_qimen()
        
        # Интегральный показатель ИИ (Context AI)
        # Объединяем DR (40%), Ци Мэнь (40%) и надежность подачи (20%)
        final_score = (dr * 0.4) + (q_power * 0.4) + (reliability * 0.2)
        
        if final_score > 1.45:
            return f"🔥 ВХОД: ПОБЕДА 1 (DR: {dr:.2f}, Qi: {q_power})"
        elif final_score < 0.75:
            return f"🔥 ВХОД: ПОБЕДА 2 (DR: {dr:.2f}, Qi: {q_power})"
        return None

async def monitor_live():
    oracle = TennisOraclePro()
    print("Мониторинг LIVE (Tennis Abstract + Ци Мэнь) запущен...")
    
    while True:
        url = f"https://{RAPID_API_HOST}/tennis/v2/fixtures-live"
        headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": RAPID_API_HOST}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for match in data.get('results', []):
                    prediction = oracle.analyze_match(match)
                    if prediction:
                        text = f"🎾 {match.get('player_1')} vs {match.get('player_2')}\n{prediction}"
                        await bot.send_message(CHAT_ID, text)
            elif response.status_code == 429:
                print("Лимит RapidAPI исчерпан. Ждем...")
        except Exception as e:
            print(f"Ошибка: {e}")
            
        await asyncio.sleep(600) # Проверка каждые 10 минут, чтобы сберечь лимиты

if __name__ == "__main__":
    asyncio.run(monitor_live())

