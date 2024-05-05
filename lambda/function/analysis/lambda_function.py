import json
import re
import os
from datetime import datetime

from pytube import YouTube
import openai
from langdetect import detect



AI_MODEL = "gpt-3.5-turbo"

def valid_request_key(req_body):
    if all(key in req_body.keys() for key in ['url']):
        return True
    return False

def is_youtube_url(url):
    # Regular expression to match YouTube URLs
    youtube_regex = (
        r"(https?://)?(www\.)?"
        "(youtube|youtu|youtube-nocookie)\.(com|be)/"
        "(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    # Compile the regex pattern
    pattern = re.compile(youtube_regex)
    # Check if the URL matches the pattern
    return pattern.match(url) is not None

def get_youtube_audio(url):
    output_folder = "/tmp"

    # 取得影片的音軌
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    # 下載音軌到指定的路徑
    result_array = url.split('=')
    video_id = ""
    if len(result_array) > 1:
        video_id = result_array[1]
    else:
        current_datetime = datetime.now()
        video_id = current_datetime.strftime("%Y%m%d_%H%M")
    print(video_id)
    
    audio_stream.download(
        output_path=output_folder, filename="%s.wav" % video_id)
    return "%s/%s.wav" % (output_folder, video_id)


def get_transcript(client, audio_file_path):
    audio_file = open(audio_file_path, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",
        prompt="")
    print(transcript)
    return transcript

def detect_language(text):
    try:
        language = detect(text)
        print(f"language: {language}")
        return language
    except:
        print(f"language: Unknown")
        return "Unknown"

def openai_chat(client, temperature, system_prompt, transcript):
    response = client.chat.completions.create(
        model=AI_MODEL,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": transcript
            }
        ]
    )
    return response.choices[0].message.content

def get_summary_cn(client, transcript):

    system_prompt = """
       你是一位協助招聘的助手。你的任務是，
       以滿分10分，將以下自我介紹的內容以清晰度、組織性、流暢度、適配度、表達能力、吸引力，％為權重、
       ，以此依據進行嚴格評分並給予各項指標建議與標示需要修改的語句，用結果填入下列JSON格式回傳
       回傳格式：
       {
           "clarity": {清晰度權重}, 
           "organization": {組織性權重}, 
           "fluency": {流暢度權重}, 
           "adaptability": {適配度權重}, 
           "expressiveness": {表達能力權重}, 
           "attractiveness": {吸引力權重},
           "suggestion": {對各項指標建議與標示需要修改的語句}
           
       }
    """
    summary = openai_chat(client, 0, system_prompt, transcript)
    return summary

def lambda_handler(event, context):
    # TODO implement
    client = openai.OpenAI()
    
    req_body = json.loads(event['body'])
    if valid_request_key(req_body):
        if is_youtube_url(req_body['url']):
            audio_file_path = get_youtube_audio(req_body['url'])
            transcript = get_transcript(client, audio_file_path)
            language = detect_language(transcript)
            summary = get_summary_cn(client, transcript)
            print(summary)
            return {
                'statusCode': 200,
                'body': json.dumps(f"{summary}")
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps("Non Youtube URL is not supported yet")
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps("Request body not validated.")
        }