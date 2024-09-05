import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 28.63099
MY_LONG = 77.21715
USER = "mail"
PASSWORD = "password"


def is_loc():
    response1 = requests.get(url="http://api.open-notify.org/iss-now.json")
    response1.raise_for_status()
    data = response1.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT + 5 >= iss_latitude <= MY_LAT - 5 and MY_LONG + 5 >= iss_longitude <= MY_LONG - 5:
        return True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_night():
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if sunset <= time_now.hour or time_now.hour <= sunrise:
        return True


if is_loc() and is_night():
    while True:
        time.sleep(60)
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=USER, password=PASSWORD)
            connection.sendmail(
                from_addr=USER,
                to_addrs="sampleudemy2@yahoo.com",
                msg="Subject:Look Up!!\n\n Look there is the iss")
            connection.close()
