import time
from bot_scripts.twitter import Twitter

"""
Settings are in config.py
"""

main = Twitter()
keywords = ["#Healthybones", "#HealhyAging", "#Longevity", "#Fractures", "Osteoporosis", "Bone health", "Bone fractures", "Senior care", "Aging",
            "Primary Care", "Care providers", "Women’s health", "Sports medicine", "Physical therapy", "Rheumatology", "Health care", "Digital Health", "Health innovation", "Gerontology"]

for keyword in keywords:
    main.reply_to_keyword(keyword, 20)

