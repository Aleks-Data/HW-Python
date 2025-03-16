import re

text = "Contact us at in%fo@example.com or sup-p+ort@example.com for assistance."

result = re.findall(r"[\w._%+-]+@[\w.-]+\.[\w]{2,}", text)
print(result)