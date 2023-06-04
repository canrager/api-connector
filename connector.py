# %%
import os
import requests
import openai
from google.cloud import texttospeech

# %% Set name of output files
run_name = "pirates_journey"

# %% Set Keys
with open("openaik.txt", "r") as file:
    openai.api_key = file.readline().strip()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file.readline()

# %% OpenAI Text Generation
out = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a foolish captain of crew of pirates who just returned from a wild journey.",
        },
        {"role": "user", "content": "What did you encounter on your journey?"},
    ],
)
text = out.choices[0].message.content
print(text)

with open(f"./outputs/{run_name}", "a") as file:
    file.write(text)


# %% Google Text to Speech
def synthesize_text(text):
    """Synthesizes speech from the input string of text."""

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-AU",
        name="en-AU-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    fname = f"./outputs/{run_name}.mp3"
    with open(fname, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{fname}"')


synthesize_text(text=text)

# %%
