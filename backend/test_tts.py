from deepgram import DeepgramClient

dg = DeepgramClient("test")

print(type(dg.speak))
print(dir(dg.speak))