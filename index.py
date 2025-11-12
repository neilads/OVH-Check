import requests
import time
import sys

SLEEP_TIME = 10
API_BASE_URL = "https://ca.api.ovh.com/v1/vps/order/rule/datacenter"
OVH_SUBSIDIARY = "WE"
PLAN_CODE = 'vps-2025-model1'
DATACENTER = 'SGP' # VỊ TRÍ SERVER MUỐN CHECK
TELEGRAM_BOT_TOKEN = 'BOT_TOKEN' # TOKEN BOT TELEGRAM
TELEGRAM_USER_ID = 'USER_ID' # ID NGƯỜI NHẬN THÔNG BÁO

def check_available():
    try:
        url = f"{API_BASE_URL}?ovhSubsidiary={OVH_SUBSIDIARY}&planCode={PLAN_CODE}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        datacenters = data.get('datacenters', [])
        
        for dc in datacenters:
            if dc.get('datacenter', '').upper() == DATACENTER.upper():
                return dc.get('status') == 'available'
        return False
    except:
        return False

def send_telegram_notification(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': TELEGRAM_USER_ID,
            'text': message
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except:
        return False

def main():
    try:
        while True:
            is_available = check_available()
            
            if is_available:
                message = "🚨 VPS 1 - Singapore đã có hàng!"
                send_telegram_notification(message)
            # Bỏ comment để để test bot
            # else:
            #     message = "🚨 VPS 1 - Singapore đã hết hàng!"
            #     send_telegram_notification(message)
            
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
