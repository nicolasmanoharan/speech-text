import streamlit as st
import tempfile
import os
import whisper
from pydub import AudioSegment

# Initialisation de la page (étape) dans la session
if "page" not in st.session_state:
    st.session_state.page = 1

# Fonctions de navigation
def next_page():
    st.session_state.page += 1

def previous_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

# Titre principal
st.title("Audio transcription")

#############################################
# ÉTAPE 1 : Charger le fichier audio
#############################################
if st.session_state.page == 1:
    st.header("Étape 1 : Charger le fichier audio")

    uploaded_file = st.file_uploader("Chargez un fichier audio", type=["m4a", "mp4", "wav", "mp3"])
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file  # Sauvegarde dans la session
        st.write(f"📂 Fichier chargé : {uploaded_file.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
            temp_file.write(uploaded_file.read())
            # Sauvegarder le chemin du fichier temporaire dans la session
            st.session_state.temp_filename = temp_file.name
            next_page()
    col_nav = st.columns(2)
    with col_nav[0]:
        if st.button("Précédent"):
            previous_page()
    with col_nav[1]:
        # On ne permet d’avancer que si un fichier est chargé
        if st.button("Suivant"):
            if "uploaded_file" in st.session_state:
                next_page()
            else:
                st.warning("Veuillez charger un fichier audio avant de continuer.")
#############################################
# ÉTAPE 2 : Choisir le modèle Whisper
#############################################
elif st.session_state.page == 2:
    # Récupérer le chemin du fichier temporaire depuis la session
    temp_filename = st.session_state.get("temp_filename", None)
    st.header("Étape 2 : Choisir le modèle")
    st.info("Vous avez le choix entre différents modèles. Du Tiny plus rapide mais moins efficace au Large plus puissant mais plus lent")

    # Ajout d'un placeholder
    options = ["Sélectionnez un modèle", "tiny", "base", "small", "medium", "large"]
    model_size = st.selectbox("Sélectionnez le modèle Whisper", options)

    if model_size is not None :
        audio = AudioSegment.from_file(temp_filename)
        audio = audio[:30 * 1000]
        temp_wav = temp_filename.replace(os.path.splitext(temp_filename)[-1], ".wav")
        audio.export(temp_wav, format="wav")
        st.audio(temp_wav, format="audio/wav")
    if model_size != "Sélectionnez un modèle":
        st.session_state.model_size = model_size  # Sauvegarde dans la session
        st.write(f"📌 Modèle sélectionné : **{model_size}**")
                # Charger le modèle Whisper (en utilisant le modèle stocké dans la session)
        model = whisper.load_model(st.session_state.model_size)
        print(st.session_state.model_size)
        result = model.transcribe(temp_wav)
        st.success("✅ Transcription de validation terminée !")
        st.text_area("📜 Transcription :", result["text"], height=300)
        st.audio(temp_wav, format="audio/wav")
        st.info("Si la transcription vous convient passez à l'étape suivante")
        if st.button("Suivant"):
            next_page()
    else:
        st.warning("Veuillez sélectionner un modèle pour continuer.")


#############################################
# ÉTAPE 3 : Validation du modele
#############################################
elif st.session_state.page == 3:
    st.header("Étape 3 : Generalisation")

    # Récuparation du modèle selectionné dans la page 2
    model_size = st.session_state.get("model_size", None)

    #  Analyse du fichier audio avec le mode
    # Récupérer le fichier audio depuis la session
    temp_filename = st.session_state.get("temp_filename", None)

    if temp_filename is not None:
        try:
            # Message d'attente pour le chargement
            with st.spinner("⏳ Chargement du fichier audio en cours..."):
                # Chargement de l'audio avec Pydub
                audio = AudioSegment.from_file(temp_filename)
                duration_seconds = len(audio) / 1000  # Convertir la durée en secondes

                # Calculer le temps estimé basé sur les 30 secondes de test
                # Estimation : si 30 secondes prennent X secondes, alors la durée totale prendra (durée_totale/30) * X
                estimated_time = (duration_seconds / 30) * 15  # 15 secondes est une base pour 30s d'audio

                # Export en WAV pour Whisper
                temp_wav = temp_filename.replace(os.path.splitext(temp_filename)[-1], ".wav")
                audio.export(temp_wav, format="wav")

            # Affichage du fichier audio
            st.audio(temp_wav, format="audio/wav")

            # Message pour indiquer le début de l'analyse avec estimation
            st.info(f"🎯 L'analyse va commencer avec le modèle {model_size}.\nTemps estimé: environ {estimated_time:.1f} secondes")

            # Transcription avec le modèle sélectionné
            progress_bar = st.progress(0)
            status_text = st.empty()

            with st.spinner("🔍 Analyse et transcription en cours..."):
                # Simulation de la progression basée sur le temps estimé
                model = whisper.load_model(model_size)

                # Démarrer la transcription
                result = model.transcribe(temp_wav)

                # Affichage des résultats
                st.success("✅ Analyse et transcription terminées avec succès!")
                st.markdown("### 📝 Résultat de la transcription:")
                transcription_text = st.text_area("", result["text"], height=300)

                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger la transcription",
                    data=result["text"],
                    file_name="transcription.txt",
                    mime="text/plain"
                )

            if st.button("Suivant"):
                next_page()

        except Exception as e:
            st.error(f"❌ Erreur lors du traitement audio : {e}")
        finally:
            # Nettoyage des fichiers temporaires
            if os.path.exists(temp_wav):
                os.remove(temp_wav)

    else:
        st.warning("Aucun fichier audio trouvé. Veuillez retourner à l'étape précédente.")
#############################################
# ÉTAPE 4 : Prévisualisation et transcription
#############################################
elif st.session_state.page == 4:
    st.header("Étape 4 : End")

    st.write("La transcription est terminée. Que souhaitez-vous faire ensuite ?")

    if st.button("Nouvelle session"):
        st.session_state.page = 1
        st.experimental_rerun()
    else:
        st.success("Merci d'avoir utilisé notre service de transcription. Vous pouvez maintenant fermer cette page.")

    if st.button("Précédent"):
        previous_page()
