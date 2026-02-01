import requests
import time

DATACENTER = 'SGP' # VỊ TRÍ SERVER MUỐN CHECK
PLAN_CODE = 'vps-2025-model1' # CẤU HÌNH VPS MUỐN CHECK
TELEGRAM_BOT_TOKEN = 'BOT_TOKEN' # TOKEN BOT TELEGRAM
TELEGRAM_USER_ID = 'USER_ID' # ID NGƯỜI NHẬN THÔNG BÁO

API_URL = "https://eu.api.ovh.com/v1/vps/order/rule/datacenter?ovhSubsidiary=FR&planCode=" + PLAN_CODE

def check():
    try:
        data = requests.get(API_URL, timeout=10).json()
        for dc in data.get('datacenters', []):
            if dc.get('datacenter') == DATACENTER:
                status = dc.get('linuxStatus')
                print(f"{DATACENTER}: {status}")
                return status == 'available'
    except Exception as e:
        print(f"Lỗi: {e}")
    return False

def notify(msg):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={'chat_id': TELEGRAM_USER_ID, 'text': msg}
    )

while True:
    if check():
        notify(f"🚨 VPS {DATACENTER} có hàng!")
    time.sleep(10)
