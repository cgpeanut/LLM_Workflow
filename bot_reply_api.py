from gradio_client import Client

client = Client("https://4beab4013c36a8ec16.gradio.live/")
result = client.predict(
		h=[],
		temperature=0.3,
		num_ctx=2048,
		api_name="/bot_reply"
)
print(result)
