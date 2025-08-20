from gradio_client import Client

client = Client("https://4beab4013c36a8ec16.gradio.live/")
result = client.predict(
		m="Tell me about Canada.",
		h=[],
		api_name="/user_send"
)
print(result)
