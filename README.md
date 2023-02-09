# Timetable Telegram bot

Bot providing users with an up-to-date class schedule.

## Features

* Allows users to view the current schedule of classes in different subsidiary;
* Support subscriptions to subsidiaries and receiving notifications if timetable was changed.

## Usage

1. Install requirements
`pip install -r requirements.txt`

2. Create Google Sheets table

![изображение](https://user-images.githubusercontent.com/62947325/217827041-ce18a3e5-7e54-470e-ab4b-b21244dcfe2e.png)

3. Enable Google API 

4. Create Service Account and put `service_account.json` to yout sources

5. Set enviroment variables:
```
TELEGRAM_TOKEN=<your bot token>
SPREADSHEET_ID = <Sheet ID>
RANGE_NAME = <cells range>
```

6. Run:
`python3 timetablebot.py`

## Examples

1. Start interactive with bot

![изображение](https://user-images.githubusercontent.com/62947325/217826930-f1063b8f-9a5b-4901-b35d-e5ee01891ece.png)

2. Get timetable

![изображение](https://user-images.githubusercontent.com/62947325/217820441-a3e3078f-650c-4cc0-b116-6f99b528b2a1.png)

3. Sunscribe

![изображение](https://user-images.githubusercontent.com/62947325/217820676-4d5b5a7d-899c-4455-bb6e-6027798d53cb.png)

4. And wait for notifications

![изображение](https://user-images.githubusercontent.com/62947325/217831915-2a08a268-bc6d-4da7-94ab-caa3a556c215.png)

## TODOs
- [ ] Dabadase integration
- [ ] Unsubscribing
- [ ] Pretty table view
