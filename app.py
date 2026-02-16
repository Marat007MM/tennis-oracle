import asyncio
import requests
import time
from datetime import datetime
from aiogram import Bot

# --- 1. НАСТРОЙКИ (ВСЁ ВКЛЮЧЕНО) ---
TELEGRAM_TOKEN = "8117388595:AAF7v_DYb0zR_MOMD@tlle3d4O1-35A"
CHAT_ID = "7180053524"
RAPID_API_KEY = "29d2b35e9fmsh083609010ee3bc1p13ef3cjsne0ee6b01ed6e"
RAPID_API_HOST = "tennis-api-atp-wta-itf.p.rapidapi.com"

bot = Bot(token=TELEGRAM_TOKEN)

# --- 2. МОЗГ СИСТЕМЫ (Твои формулы) ---
class TennisGuaiAI:
    def __init__(self):
        # Энергия Ци Мэнь (12 двухчасовок)
        self.qimen_cycle = [1.5, 0.7, 0.5, 1.2, 1.1, 1.4, 0.5, 1.3, 1.0, 0.8, 1.6, 0.5]

    def analyze(self, stats):
        try:
            # Математика: Dominance Ratio (из данных API)
            # stats ожидаем в виде словаря с данными матча
            w1_ret = stats.get('w1_break_points_won', 1)
            w2_ret = stats.get('w2_break_points_won', 1)
            dr = (w1_ret / 1) / (w2_ret / 1) # Упрощенная модель DR
            
            # Физика: Speed Decay
            curr_speed = stats.get('serve_speed', 180)
            decay = curr_speed / 200
            
            # Метафизика: Ци Мэнь (авто-час)
            q_power = self.qimen_cycle[int(datetime.now().hour / 2) % 12]
            
            # Итоговый скоринг
            win_score = (dr * 0.4) + (q_power * 0.4) + (decay * 0.2)
            
            if win_score > 1.43:
                return f"🔥 ПРОГНОЗ: ПОБЕДА 1 (Score: {win_score:.2f})"
            elif win_score < 0.82:
                return f"🔥 ПРОГНОЗ: ПОБЕДА 2 (Score: {win_score:.2f})"
            else:
                return f"⚠️ МАТЧ СЛОЖНЫЙ (Score: {win_score:.2f})"
        except Exception as e:
            return f"Ошибка анализа: {e}"

# --- 3. ФУНКЦИЯ ПОЛУЧЕНИЯ ДАННЫХ ---
def get_live_tennis_data():
    url = f"https://{RAPID_API_HOST}/tennis/v2/fixtures-live"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# --- 4. ГЛАВНЫЙ ЦИКЛ БОТА ---
async def main():
    ai = TennisGuaiAI()
    print("Бот Оракул запущен...")
    
    while True:
        data = get_live_tennis_data()
        if data and 'results' in data:
            for match in data['results']:
                # Берем данные матча и прогоняем через ИИ
                # В реальности тут нужно вытягивать конкретные stats
                result_text = ai.analyze(match)
                
                message = f"🎾 Матч: {match.get('player_1')} vs {match.get('player_2')}\n{result_text}"
                await bot.send_message(CHAT_ID, message)
                break # Пока берем один матч для теста
        
        await asyncio.sleep(300) # Проверка каждые 5 минут

if __name__ == "__main__":
    asyncio.run(main())
