import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from aiogram import Bot

# --- НАСТРОЙКИ ---
TOKEN = "8117388595:AAF7v_DYb0zR_MOMD@tlle3d4O1-35A"
CHAT_ID = "7180053524"

bot = Bot(token=TOKEN)

class UltimateOracle:
    def __init__(self):
        # Энергия Ци Мэнь (12 двухчасовых сеансов)
        self.qimen_cycle = [1.5, 0.7, 0.5, 1.2, 1.1, 1.4, 0.5, 1.3, 1.0, 0.8, 1.6, 0.5]

    def get_free_stats(self):
        """Здесь будет логика парсинга Flashscore. Пока используем тестовый фид."""
        try:
            # Имитация получения данных с Tennis Abstract / Flashscore
            return [{"p1": "Djokovic", "p2": "Alcaraz", "dr": 1.25, "momentum": 80}]
        except:
            return []

    def analyze(self, match):
        # 1. Данные Tennis Abstract (Dominance Ratio)
        dr = match.get("dr", 1.0)
        
        # 2. Контекст ИИ (Импульс матча)
        ai_factor = 1.1 if match.get("momentum", 50) > 70 else 1.0
        
        # 3. Ци Мэнь (Энергия часа)
        hour_idx = int(datetime.now().hour / 2) % 12
        qimen_power = self.qimen_cycle[hour_idx]
        
        # Итоговая формула победы (DR 40% + AI 30% + Qimen 30%)
        score = (dr * 0.4) + (ai_factor * 0.3) + (qimen_power * 0.3)
        
        if score > 1.42:
            return f"🔥 ОРАКУЛ: ПОБЕДА П1 (Анализ: {score:.2f})"
        elif score < 0.85:
            return f"🔥 ОРАКУЛ: ПОБЕДА П2 (Анализ: {score:.2f})"
        return f"⌛ Ожидание сигнала... (Текущий балл: {score:.2f})"

async def main():
    oracle = UltimateOracle()
    # Отправляем тестовое сообщение в ТГ при старте
    await bot.send_message(CHAT_ID, "🚀 Супер-Оракул запущен и начинает мониторинг!")
    
    while True:
        matches = oracle.get_free_stats()
        for m in matches:
            prediction = oracle.analyze(m)
            if prediction:
                text = f"🎾 {m['p1']} vs {m['p2']}\n{prediction}"
                await bot.send_message(CHAT_ID, text)
        
        await asyncio.sleep(900) # Проверка каждые 10 минут

if __name__ == "__main__":
    asyncio.run(main())




