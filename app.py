import streamlit as st
from groq import Groq
import tempfile
import os
from datetime import datetime

# Initialize Groq client
API_KEY = "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"
client = Groq(api_key=API_KEY)

# App title and description
st.title("🎤 Advanced Text to Speech Converter")
st.markdown("Convert your text to natural-sounding speech with multiple voices and options.")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # Updated voice selection based on API's supported voices
    voice_options = {
        "Aaliyah-PlayAI": "Young female voice",
        "Adelaide-PlayAI": "Female voice",
        "Angelo-PlayAI": "Male voice",
        "Arista-PlayAI": "Female voice",
        "Atlas-PlayAI": "Male voice",
        "Basil-PlayAI": "Male voice",
        "Briggs-PlayAI": "Male voice",
        "Calum-PlayAI": "Male voice",
        "Celeste-PlayAI": "Female voice",
        "Cheyenne-PlayAI": "Female voice",
        "Chip-PlayAI": "Male voice",
        "Cillian-PlayAI": "Male voice",
        "Deedee-PlayAI": "Female voice",
        "Eleanor-PlayAI": "Female voice",
        "Fritz-PlayAI": "Male voice",
        "Gail-PlayAI": "Female voice",
        "Indigo-PlayAI": "Female voice",
        "Jennifer-PlayAI": "Female voice",
        "Judy-PlayAI": "Female voice",
        "Mamaw-PlayAI": "Female voice",
        "Mason-PlayAI": "Male voice",
        "Mikail-PlayAI": "Male voice",
        "Mitch-PlayAI": "Male voice",
        "Nia-PlayAI": "Female voice",
        "Quinn-PlayAI": "Female voice",
        "Ruby-PlayAI": "Female voice",
        "Thunder-PlayAI": "Male voice"
    }
    selected_voice = st.selectbox(
        "Select Voice",
        options=list(voice_options.keys()),
        format_func=lambda x: f"{x} ({voice_options[x]})"
    )
    
    # Speed control (if supported by API)
    speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
    
    # Audio format
    audio_format = st.radio(
        "Output Format",
        ["wav", "mp3"],
        index=0
    )

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    text = st.text_area(
        "Enter text to convert:",
        height=200,
        placeholder="Type or paste your text here...",
        help="Maximum 5000 characters"
    )

with col2:
    st.markdown("**Tips:**")
    st.markdown("- Use punctuation for natural pauses")
    st.markdown("- Keep sentences short for clarity")
    st.markdown("- 100-300 characters works best")

# Action buttons
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("🔊 Speak", help="Convert text to speech"):
        if not text.strip():
            st.warning("Please enter some text!")
        elif len(text) > 5000:
            st.error("Text exceeds 5000 character limit!")
        else:
            try:
                with st.spinner("Generating audio..."):
                    # Create the API request with only supported parameters
                    params = {
                        "model": "playai-tts",
                        "voice": selected_voice,
                        "response_format": audio_format,
                        "input": text,
                    }
                    
                    # Only include speed if it's not the default (1.0)
                    if speed != 1.0:
                        params["speed"] = speed
                    
                    response = client.audio.speech.create(**params)

                    # Extract audio bytes
                    audio_bytes = response.read()

                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(suffix=f".{audio_format}", delete=False) as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_file_path = tmp_file.name

                    # Display audio player
                    st.audio(tmp_file_path, format=f"audio/{audio_format}")
                    
                    # Download button
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    download_filename = f"tts_output_{timestamp}.{audio_format}"
                    
                    st.download_button(
                        label="⬇️ Download Audio",
                        data=audio_bytes,
                        file_name=download_filename,
                        mime=f"audio/{audio_format}",
                        help="Save the generated audio file"
                    )
                    
            except Exception as e:
                st.error(f"API Error: {e}")
                st.error("Please check your input and try again.")

with col2:
    if st.button("🧹 Clear", type="secondary"):
        text = ""

# History section
if 'history' not in st.session_state:
    st.session_state.history = []

if text.strip() and st.button("Speak"):
    st.session_state.history.append({
        "text": text[:100] + "..." if len(text) > 100 else text,
        "voice": selected_voice,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if st.session_state.history:
    with st.expander("📜 History (Last 5)"):
        for i, item in enumerate(st.session_state.history[-5:]):
            st.markdown(f"""
            **{i+1}. {item['timestamp']}**  
            Voice: *{item['voice']}*  
            Text: {item['text']}
            """)
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown("ℹ️ Note: Audio quality may vary based on text length and complexity.")