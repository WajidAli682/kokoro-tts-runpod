import runpod
from kokoro_onnx import Kokoro
import soundfile as sf
import io
import base64

# AI Model ko server ki memory mein load karna (NAYA v1.0)
try:
    # Yahan humne naye files ke naam de diye hain
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    print("Kokoro Model Loaded Successfully!")
except Exception as e:
    print(f"Model load karne mein error: {e}")
    kokoro = None

def handler(job):
    if not kokoro:
        return {"error": "Model is not loaded."}
        
    job_input = job['input']
    text = job_input.get("text", "Welcome to our AI Voice generator!")
    voice = job_input.get("voice", "af_bella") # Default voice
    speed = job_input.get("speed", 1.0)
    
    try:
        # Awaz Generate karna
        samples, sample_rate = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
        
        wav_io = io.BytesIO()
        sf.write(wav_io, samples, sample_rate, format='WAV')
        wav_io.seek(0)
        
        audio_base64 = base64.b64encode(wav_io.read()).decode('utf-8')
        
        return {
            "status": "success", 
            "audio_base64": audio_base64
        }
    except Exception as e:
        return {"error": str(e)}

# RunPod Serverless ko start karna
runpod.serverless.start({"handler": handler})