import streamlit as st
from PIL import Image
import random
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

# --- Données des cartes ---
cartes = [
    {"nom": "Tom", "age": "11 ans", "desc": "Intello", "type": "Éclair", "photo": "tom.jpg", "rare": False},
    {"nom": "Eléïa", "age": "13 ans", "desc": "Belle", "type": "Rose doré", "photo": "eléïa.jpg", "rare": False},
    {"nom": "Matys", "age": "9 ans", "desc": "Mignon", "type": "Dragon", "photo": "matys.jpg", "rare": False},
    {"nom": "Maman", "age": "39 ans", "desc": "La meilleure", "type": "Amour", "photo": "maman.jpg", "rare": True},
    {"nom": "Éric", "age": "36 ans", "desc": "Mon héro", "type": "Force", "photo": "éric.jpg", "rare": False},
    {"nom": "Maya", "age": "62 ans", "desc": "Affectueuse", "type": "Chat", "photo": "maya.jpg", "rare": False},
    {"nom": "Papick", "age": "65 ans", "desc": "Drôle", "type": "Grand Schtroumpf", "photo": "papick.jpg", "rare": True},
    {"nom": "Tonton", "age": "37 ans", "desc": "Drôle", "type": "Cool", "photo": "tonton.jpg", "rare": False},
    {"nom": "Sandra", "age": "40 ans", "desc": "Enfant", "type": "Amour", "photo": "sandra.jpg", "rare": False},
    {"nom": "Laëtitia", "age": "10 ans", "desc": "Funny", "type": "Rose doré", "photo": "leatitia.jpg", "rare": False},
    {"nom": "Lolo", "age": "5 ans", "desc": "Le plus petit", "type": "Malin", "photo": "lolo.jpg", "rare": False},
]

# --- Session state pour garder l'album ---
if "collection" not in st.session_state:
    st.session_state.collection = []

if "carte_actuelle" not in st.session_state:
    st.session_state.carte_actuelle = None

st.title("🎴 Jeu de cartes familiales")

# --- Tirage aléatoire avec rareté ---
def tirer_carte():
    tirage = random.choices(
        cartes,
        weights=[10 if c['rare'] else 90 for c in cartes],
        k=1
    )[0]
    st.session_state.carte_actuelle = tirage
    st.session_state.collection.append(tirage)

# --- Génération PDF ---
def imprimer_carte(carte):
    fichier = f"{carte['nom']}.pdf"
    doc = SimpleDocTemplate(fichier)
    styles = getSampleStyleSheet()
    contenu = [
        Paragraph(f"<b>{carte['nom']} ({carte['age']})</b>", styles['Title']),
        RLImage(carte["photo"], width=200, height=200),
        Spacer(1, 12),
        Paragraph(f"Description : {carte['desc']}", styles['Normal']),
        Paragraph(f"Type : {carte['type']}", styles['Normal']),
        Paragraph(f"{'RARE !' if carte['rare'] else ''}", styles['Normal']),
    ]
    doc.build(contenu)
    st.success(f"PDF créé : {fichier}")
    return fichier

# --- Boutons de tirage ---
if st.button("🎲 Tirer une carte"):
    tirer_carte()

# --- Affichage de la carte actuelle ---
carte = st.session_state.carte_actuelle
if carte:
    col1, col2 = st.columns([1,2])
    with col1:
        img = Image.open(carte["photo"]).resize((200,200))
        st.image(img, caption="RARE !" if carte["rare"] else "", width=200)
    with col2:
        st.subheader(f"{carte['nom']} ({carte['age']})")
        st.write(f"Description : {carte['desc']}")
        st.write(f"Type : {carte['type']}")
        if st.button("🖨️ Imprimer cette carte"):
            fichier_pdf = imprimer_carte(carte)

# --- Affichage album ---
st.subheader("📖 Album familial")
cols = st.columns(4)
for i, c in enumerate(st.session_state.collection):
    with cols[i%4]:
        img = Image.open(c["photo"]).resize((100,100))
        st.image(img, caption=f"{c['nom']} {'⭐' if c['rare'] else ''}", width=100)
