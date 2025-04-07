# 📬 Notification Service (FastAPI + Twilio)

This REST service uses a Twilio API to send notifications through SMS
It exposes the endpoint `/notify` which accepts a phone number, a message and sends it.

---

## 🚀 Fonctionnalities

- ✅ REST API with [FastAPI](https://fastapi.tiangolo.com/)
- 📲 Sends SMS with [Twilio](https://www.twilio.com/)
- 🔐 Configuration with `.env` file
- 🐳 Deployable with Docker

---

## 🗂️ Service Structure

notification_service/
├── app/
│ ├── main.py # API entrypoint
│ └── notifier/
│   ├── service.py # SMS-sending function
│   └── config.py # Reading .env file
├── requirements.txt # Python dependencies
├── Dockerfile # Docker image
├── README.md
└── .env

---

## 🔧 Requirements

- Python 3.8+
- A Twilio account ([https://twilio.com/](https://twilio.com/))
- A configured Twilio phone number
- A `.env` file containing :

```env

TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=SKxxxxxxxxxxxxxxxxxxxxxxxx

TWILIO_PHONE_NUMBER=+12089132515
