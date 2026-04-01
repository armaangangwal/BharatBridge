import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from gtts import gTTS
import os

LANGUAGES = {
    "Bengali":  "bn",
    "Hindi":    "hi",
    "Tamil":    "ta",
    "Telugu":   "te",
    "Marathi":  "mr",
    "English":  "en",
}

st.set_page_config(page_title="BharatBridge", page_icon="🌐", layout="centered")

st.title("🌐 BharatBridge")
st.caption("AI-powered translation across India's languages")

st.markdown("### Enter text")
input_text = st.text_area(
    label="Type or paste text in any supported language",
    height=150,
    placeholder="Type here in Bengali, Hindi, Tamil, Telugu, Marathi, or English..."
)

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Translate from", options=["Auto-detect"] + list(LANGUAGES.keys()))

with col2:
    target_lang = st.selectbox("Translate to", options=list(LANGUAGES.keys()), index=2)

if "translated" not in st.session_state:
    st.session_state.translated = ""
    st.session_state.tgt_code = ""

if st.button("Translate", type="primary"):
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        try:
            if source_lang == "Auto-detect":
                detected_code = detect(input_text)
                detected_name = next(
                    (name for name, code in LANGUAGES.items() if code == detected_code),
                    detected_code
                )
                st.info(f"Detected language: **{detected_name}**")
                src_code = detected_code
            else:
                src_code = LANGUAGES[source_lang]

            tgt_code = LANGUAGES[target_lang]
            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)

            st.session_state.translated = translated
            st.session_state.tgt_code = tgt_code

        except Exception as e:
            st.error(f"Something went wrong: {e}")

if st.session_state.translated:
    st.markdown("### Translation")
    st.success(st.session_state.translated)

    if st.button("Read aloud"):
        tts = gTTS(text=st.session_state.translated, lang=st.session_state.tgt_code)
        audio_file = "output.mp3"
        tts.save(audio_file)
        st.audio(audio_file, format="audio/mp3")
        os.remove(audio_file)

st.markdown("---")
st.caption("Built in Kolkata, India · For everyone who has ever been lost in translation.")