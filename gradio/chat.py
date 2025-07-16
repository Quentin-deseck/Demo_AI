import os
from dotenv import load_dotenv
import openai
import gradio as gr
import requests
from PIL import Image
import io

load_dotenv()  # Charge les variables du fichier .env

# 🗝️ Clé API (via variable d'environnement)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 💬 Fonction pour parler à GPT
def chat_with_gpt(message, history):
    # Convertir l'historique Gradio au format OpenAI
    messages = [{"role": "system", "content": "Tu es un assistant utile. Si l'utilisateur demande de générer une image, réponds avec 'IMAGE_REQUEST:' suivi de la description de l'image."}]
    
    # Ajouter l'historique des messages
    for msg in history:
        if msg["role"] == "user":
            messages.append({"role": "user", "content": msg["content"]})
        elif msg["role"] == "assistant":
            messages.append({"role": "assistant", "content": msg["content"]})

    # Ajouter le nouveau message
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        
        reply = response.choices[0].message.content
        
        # Vérifier si c'est une demande d'image
        if "IMAGE_REQUEST:" in reply:
            image_description = reply.split("IMAGE_REQUEST:")[1].strip()
            return generate_image(message, image_description, history)
        
        # Ajouter à l'historique au format Gradio
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        
        return history, "", None  # Retourner l'historique, vider le champ de texte, pas d'image
        
    except Exception as e:
        error_msg = f"Erreur: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return history, "", None

# 🎨 Fonction pour générer une image
def generate_image(user_message, image_description, history):
    try:
        # Générer l'image avec DALL-E
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Récupérer l'URL de l'image
        image_url = response.data[0].url
        
        # Télécharger l'image
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        
        # Ajouter à l'historique
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": f"J'ai généré une image basée sur: {image_description}"})
        
        return history, "", image
        
    except Exception as e:
        error_msg = f"Erreur lors de la génération d'image: {str(e)}"
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": error_msg})
        return history, "", None

# 🖼️ Fonction pour générer une image directement
def generate_image_direct(prompt, history):
    if not prompt.strip():
        return history, "", None
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        
        # Ajouter à l'historique du chat
        history.append({"role": "user", "content": f"🎨 Générer une image: {prompt}"})
        history.append({"role": "assistant", "content": f"Image générée avec succès pour: {prompt}"})
        
        return history, "", image
        
    except Exception as e:
        error_msg = f"Erreur lors de la génération d'image: {str(e)}"
        history.append({"role": "user", "content": f"🎨 Générer une image: {prompt}"})
        history.append({"role": "assistant", "content": error_msg})
        return history, "", None

# 🎨 Interface Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 ChatGPT + 🎨 DALL-E avec Gradio")
    gr.Markdown("💬 **Chat**: Pose tes questions ou demande de générer une image  \n🎨 **Image**: Génère directement une image avec une description")
    
    with gr.Row():
        with gr.Column(scale=1):
            chatbot = gr.Chatbot(
                label="💬 Assistant", 
                type="messages",
                height=400,
                show_copy_button=True
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    label="Message",
                    placeholder="Écris ton message (ex: 'génère une image d'un chat dans l'espace')",
                    scale=4
                )
                submit_btn = gr.Button("📤 Envoyer", scale=1)
            
            clear_btn = gr.Button("🧹 Effacer le chat")
        
        with gr.Column(scale=1):
            image_output = gr.Image(
                label="🎨 Image générée",
                height=400,
                show_download_button=True
            )
            
            image_prompt = gr.Textbox(
                label="Description de l'image",
                placeholder="Décris l'image que tu veux générer...",
                lines=3
            )
            
            generate_img_btn = gr.Button("🎨 Générer l'image", variant="primary")
            
            gr.Markdown("### 💡 Exemples de prompts:")
            gr.Markdown("""
            - Un chat astronaute flottant dans l'espace
            - Une ville futuriste au coucher du soleil
            - Un dragon amical dans une forêt enchantée
            - Une tasse de café fumante sur un bureau vintage
            """)

    # Événements pour le chat
    msg.submit(chat_with_gpt, [msg, chatbot], [chatbot, msg, image_output])
    submit_btn.click(chat_with_gpt, [msg, chatbot], [chatbot, msg, image_output])
    
    # Événements pour la génération d'image directe
    generate_img_btn.click(generate_image_direct, [image_prompt, chatbot], [chatbot, image_prompt, image_output])
    image_prompt.submit(generate_image_direct, [image_prompt, chatbot], [chatbot, image_prompt, image_output])
    
    # Événement pour effacer
    clear_btn.click(lambda: ([], "", None, ""), None, [chatbot, msg, image_output, image_prompt])

# 🚀 Lancer
if __name__ == "__main__":
    demo.launch(
        share=False,  # Mettre à True pour créer un lien public
        debug=True,   # Afficher les erreurs détaillées
        show_error=True
    )