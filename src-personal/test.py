import requests as rq

webhookURL = 'https://chat.googleapis.com/v1/spaces/AAAAaBileJo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=FFrC6t9XgrHAZMfZvkWnt5YQ_Tr__01JGly9n5kOFPk'
webhook_url = webhookURL

message = f"Priority measure exceeded 5 for ticket id:{1002}. Immediate action required!"
payload = {
            'text': message
        }
response = rq.post(webhook_url, json=payload)
print(response.status_code)
print(response)

