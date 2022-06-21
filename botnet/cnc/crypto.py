import base64


def base_en(text):
	result = base64.b64encode(bytes(text, encoding = "utf8")).decode()
	return result

def base_de(text):
	result = base64.b64decode(bytes(text,encoding = "utf8")).decode()
	return result
