import streamlit as st
import tempfile
import os
import whisper
from pydub import AudioSegment

st.title("🎵 Lecture et Transcription Audio avec Whisper")

# 📌 Choix du modèle Whisper
model_size = st.selectbox(
    "Sélectionnez le modèle Whisper",
    ["tiny", "base", "small", "medium", "large"]
)

st.write(f"📌 Modèle sélectionné : **{model_size}**")

# 📌 Uploader de fichiers audio
uploaded_file = st.file_uploader("Chargez un fichier audio", type=["m4a", "mp4", "wav", "mp3"])

# 📌 Stocker le mode (Normal / Test) dans la session
if "mode" not in st.session_state:
    st.session_state.mode = "normal"

# 📌 Affichage des boutons pour changer de mode
col1, col2 = st.columns(2)
with col1:
    if st.button("🔊 Mode Normal", use_container_width=True):
        st.session_state.mode = "normal"

with col2:
    if st.button("⏱ Mode Test (30 sec)", use_container_width=True):
        st.session_state.mode = "test"

# 📌 Affichage du mode actif
st.write(f"🎚 Mode actuel : **{st.session_state.mode}**")

if uploaded_file is not None:
    st.write(f"📂 Fichier chargé : {uploaded_file.name}")

    # 📌 Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_filename = temp_file.name

    # 📌 Charger l'audio avec Pydub
    try:
        audio = AudioSegment.from_file(temp_filename)

        # 📌 Mode Test : Couper aux 30 premières secondes
        if st.session_state.mode == "test":
            st.write("⏱ Mode Test : Lecture des 30 premières secondes")
            audio = audio[:30 * 1000]  # 30 secondes en millisecondes

        # 📌 Sauvegarde en WAV pour Whisper
        temp_wav = temp_filename.replace(os.path.splitext(temp_filename)[-1], ".wav")
        audio.export(temp_wav, format="wav")

        # 📌 Lecture du fichier audio
        st.audio(temp_wav, format="audio/wav")

    except Exception as e:
        st.error(f"❌ Erreur lors du traitement audio : {e}")

    # 📌 Bouton pour lancer la transcription
    if st.button("🔠 Transcrire l'audio avec Whisper"):
        with st.spinner("🔍 Transcription en cours..."):
            try:
                # 📌 Chargement du modèle Whisper
                model = whisper.load_model(model_size)

                # 📌 Transcription de l'audio
                result = model.transcribe(temp_wav)

                # 📌 Affichage du texte transcrit
                st.success("✅ Transcription terminée !")
                st.text_area("📜 Transcription :", result["text"], height=300)

            except Exception as e:
                st.error(f"❌ Erreur lors de la transcription : {e}")

    # 📌 Suppression des fichiers temporaires
    os.remove(temp_wav)
    os.remove(temp_filename)
