import os
from gtts import gTTS

def split_text(text, max_chars=200):
    """Split text into smaller chunks if it exceeds gTTS limit."""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_tts(content, company_name):
    # Replace spaces with underscores and sanitize the company name
    sanitized_name = "".join(c if c.isalnum() or c == "_" else "_" for c in company_name.strip().replace(" ", "_"))
    
    # Define the path to save the audio file in the static folder
    output_path = os.path.join("static", f"{sanitized_name}.mp3")

    # Check if content is too long and split if necessary
    text_chunks = split_text(content, max_chars=200)
    
    # Merge audio chunks if text is too long
    audio_files = []
    for idx, chunk in enumerate(text_chunks):
        temp_path = os.path.join("static", f"{sanitized_name}_{idx}.mp3")
        tts = gTTS(text=chunk, lang='hi')
        tts.save(temp_path)
        audio_files.append(temp_path)
    
    # Merge audio files if there are multiple chunks
    if len(audio_files) == 1:
        os.rename(audio_files[0], output_path)
    else:
        with open(output_path, 'wb') as final_audio:
            for file in audio_files:
                with open(file, 'rb') as f:
                    final_audio.write(f.read())
                os.remove(file)
    
    print(f"TTS output saved as {output_path}")
    return output_path
