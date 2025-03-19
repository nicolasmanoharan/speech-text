# Application de Transcription Audio avec Whisper

Cette application Streamlit permet de transcrire des fichiers audio en texte en utilisant le modèle Whisper. L'application offre une interface utilisateur intuitive et guidée pour la transcription audio.

## Fonctionnalités

- Support de multiples formats audio (m4a, mp4, wav, mp3)
- Choix entre différents modèles Whisper (tiny, base, small, medium, large)
- Prévisualisation audio avant transcription complète
- Interface progressive en 4 étapes
- Téléchargement de la transcription en format texte
- Estimation du temps de traitement

## Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/nicolasmanoharan/speech-text
cd speech-totext
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Dépendances principales

```txt
streamlit
whisper
pydub
```

## Utilisation

1. Lancez l'application :
```bash
streamlit run app.py
```

2. Suivez les étapes dans l'interface :

   - **Étape 1** : Chargez votre fichier audio
   - **Étape 2** : Choisissez le modèle Whisper
   - **Étape 3** : Attendez la transcription complète
   - **Étape 4** : Téléchargez votre transcription

## Guide des modèles Whisper

- **tiny** : Le plus rapide, précision basique
- **base** : Bon équilibre vitesse/précision
- **small** : Meilleure précision, temps modéré
- **medium** : Haute précision, plus lent
- **large** : Meilleure précision, le plus lent

## Déploiement sur Azure

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2Fazure-quickstart-templates%2Fmaster%2Fquickstarts%2Fmicrosoft.web%2Fwebapp-linux-node%2Fazuredeploy.json)

1. Cliquez sur le bouton "Deploy to Azure" ci-dessus
2. Configurez votre environnement Azure
3. Déployez l'application
4. Configurez les variables d'environnement si nécessaire

## Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créez votre branche de fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## Support

Pour toute question ou problème :
- Ouvrez une issue dans le dépôt GitHub
- Consultez la documentation de [Streamlit](https://docs.streamlit.io/)
- Consultez la documentation de [Whisper](https://github.com/openai/whisper)

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
