# Напишите функцию extract_emails(text), которая извлекает все адреса
# электронной почты из заданного текста и возвращает их в виде списка.

import re

text = "Contact us at in%fo@example.com or sup-p+ort@example.com for assistance."

result = re.findall(r"[\w._%+-]+@[\w.-]+\.[\w]{2,}", text)

print(result)
