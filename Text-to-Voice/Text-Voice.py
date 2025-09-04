from elevenlabs import ElevenLabs

api_key = ""#create a elevenlabs account and paste your api key here

client = ElevenLabs(api_key=api_key)

voices = client.voices.get_all()
for v in voices.voices:
    print(f"{v.name} - {v.voice_id}")

voice_id = "cgSgspJ2msm6clMCkdW9"  

audio = client.text_to_speech.convert(
    voice_id=voice_id,
    model_id="eleven_multilingual_v2",
    text="",#enter the text that you want to convert to voice 
    output_format="mp3_44100"
)

with open("voiceover.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)