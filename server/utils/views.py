import requests

from pollnicely_server import settings


# Create your views here.
def send_otp(message, mobile, sender="NICELY", template_id=settings.DLT_TEMPLATE_ID):
    """
    Send SMS to mobile number using configured SMS gateway.
    """
    isd = "91"
    try:
        authkey = settings.MSG91_PROD_KEYS
        url = 'http://api.msg91.com/api/sendhttp.php?authkey=' + authkey + '&mobiles=' + isd
        url += mobile
        url += '&message=' + str(message)
        url += '&sender=' + sender + '&route=4&DLT_TE_ID='
        url += template_id
        print(url)
        print(requests.request('GET', url))
        return True
    except Exception as e:
        print(str(e))
        return False
