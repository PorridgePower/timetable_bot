# Timetable Telegram bot

Bot providing users with an up-to-date class schedule.

## Features

* Allows users to view the current schedule of classes in different subsidiary;
* Support subscriptions to subsidiaries and receiving notifications if timetable was changed.

## Usage

1. Install requirements
`pip install -r requirements.txt`

2. Create Google Sheets table

![изображение](https://user-images.githubusercontent.com/62947325/217818036-01f7ff16-d5be-4936-bebc-65ac9f344eee.png)

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

![изображение](https://user-images.githubusercontent.com/62947325/217820301-4f9e6015-ac13-44bb-868f-32d4e007a530.png)

2. Get timetable

![изображение](https://user-images.githubusercontent.com/62947325/217820441-a3e3078f-650c-4cc0-b116-6f99b528b2a1.png)

3. And sunscribe

![изображение](https://user-images.githubusercontent.com/62947325/217820676-4d5b5a7d-899c-4455-bb6e-6027798d53cb.png)


## TODOs
- [ ] Dabadase integration
- [ ] Unsubscribing
- [ ] Pretty table view
