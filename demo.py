from svoice.separate import *
import scipy.io as sio
from scipy.io.wavfile import write
import gradio as gr
import os
from transformers import AutoProcessor, pipeline
from optimum.onnxruntime import ORTModelForSpeechSeq2Seq
from glob import glob
from azure.storage.blob import BlobServiceClient
import shutil
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import streamlit as st
import torch

def input_audio(folder_name, audio_file, original_filename):
    
    if os.path.isfile(audio_file):
# Perform some operations on the file
        blobConnection = "DefaultEndpointsProtocol=https;AccountName=facebookresear4437532754;AccountKey=Brktu/gs0m+SZhAKN+M03YvMoQNJVjkKdA6JZJe3KRmIYkI2Xh8aPYYmxekFrU/JE4PGwvPxTmAV+AStLsLDgg==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(blobConnection)
        container_client = blob_service_client.get_container_client("azureml")
        
        # Generate a unique blob name (e.g., using a timestamp)
        # original_filename = 'test3.wav'
        blob_name = f"{folder_name}/{original_filename}"

        # Upload the audio file to Azure Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        with open(audio_file, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        expiration_time = datetime.utcnow() + timedelta(days=365)

        # Generate a SAS token for the blob with read permission and the calculated expiration time
        sas_token = generate_blob_sas(
        blob_client.account_name,
        blob_client.container_name,
        blob_client.blob_name,
        account_key=blob_service_client.credential.account_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiration_time
        )

        sas_url = f"{blob_client.url}?{sas_token}"

    return sas_url

def separator(audio_file):
    inputs = {}
    outputs= {}

    filename = audio_file.split('/')[-1]
    folder_name = filename.split('.')[0]
    output_path = os.path.join('./input/', filename)
    # shutil.copy(audio_file, output_path)

    input_url = input_audio(folder_name, output_path, filename)
    inputs[filename] = input_url
    separate_demo(mix_dir="./input")

    separated_files = glob(os.path.join('separated', "*.wav"))
    separated_files = [f for f in separated_files if filename not in f]

    for file in separated_files:
        filename = file.split('/')[-1]
        output_url = input_audio(folder_name, file, filename)

        outputs[filename] = output_url
        
    return inputs, outputs
    # for file in sorted(separated_files):
    #     separated_audio = sio.wavfile.read(file)
    #     outputs['transcripts'].append(speech_recognition_pipeline(separated_audio[1])['text'])

    # return sorted(separated_files) + outputs['transcripts']
    
def set_example_audio(example: list) -> dict:
    return gr.Audio.update(value=example[0])

def upload_file():

    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file is not None:

        file_name = uploaded_file.name
        file_ext = os.path.splitext(file_name)[1]
        unique_name = str(file_name) + file_ext
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return file_path
    else:
        return None

torch.cuda.empty_cache()
load_model()
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
os.makedirs('input', exist_ok=True)
os.makedirs('separated', exist_ok=True)

# print("Loading ASR model...")
# processor = AutoProcessor.from_pretrained("openai/whisper-small")
# if not os.path.exists("whisper_checkpoint"):
#     model = ORTModelForSpeechSeq2Seq.from_pretrained("openai/whisper-small", from_transformers=True)#.to('cuda')
#     speech_recognition_pipeline = pipeline(
#     "automatic-speech-recognition",
#         model=model,
#         feature_extractor=processor.feature_extractor,
#         tokenizer=processor.tokenizer,
#     )
#     os.makedirs('whisper_checkpoint', exist_ok=True)
#     model.save_pretrained("whisper_checkpoint")
# else:
#     model = ORTModelForSpeechSeq2Seq.from_pretrained("whisper_checkpoint", from_transformers=False)#.to('cuda')
#     speech_recognition_pipeline = pipeline(
#     "automatic-speech-recognition",
#         model=model,
#         feature_extractor=processor.feature_extractor,
#         tokenizer=processor.tokenizer,
#     )
# print("Whisper ASR model loaded.")

# def separator(audio, rec_audio, example):


st.title("Svoice")
UPLOAD_FOLDER = "/mnt/facebook_research/svoice_demo/input"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

for f in glob('input/*'):
    os.remove(f)
for f in glob('separated/*'):
    os.remove(f)

file_path = upload_file()
print(file_path)
if file_path is not None:
    st.success(f"File uploaded successfully")

    inputs, outputs = separator(str(file_path))
    st.header("Input")
    keys= inputs.keys()
    for input_filename in keys:
        input_url = inputs[input_filename]
        st.markdown(f"[{input_filename}]({input_url})")

    st.header("Output")

    keys= outputs.keys()
    keys = sorted(keys)
    for output_filename in keys:
        output_url = outputs[output_filename]
        st.markdown(f"[{output_filename}]({output_url})")
        
else:
    st.info("No file uploaded")

torch.cuda.empty_cache()
