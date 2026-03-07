# 🚀 Portfolio Django — [Ton Nom]

Portfolio personnel ultra-moderne développé avec **Django 5.1**, glassmorphism design, dark/light mode, et animations fluides.

## 🎯 Stack Technique

- **Backend**: Django 5.1, Django REST Framework, Python 3.11+
- **Frontend**: Vanilla CSS (Glassmorphism), Vanilla JS ES6+, Devicons
- **Base de données**: SQLite (dev) / PostgreSQL (prod)
- **Déploiement**: WhiteNoise, Docker-ready

---

## ⚡ Installation Rapide

### 1. Cloner / télécharger le projet
```bash
cd D:\MH\monportfolio
```

### 2. Créer et activer l'environnement virtuel
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer l'environnement
```bash
# Copier le fichier d'exemple
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac

# Éditer .env avec vos valeurs
```

### 5. Migrations & données de démo
```bash
python manage.py migrate
python manage.py loaddata portfolio/fixtures/demo_data.json
```

### 6. Créer le superutilisateur admin
```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

### 🌐 URLs
- **Portfolio** : http://127.0.0.1:8000/
- **Admin** : http://127.0.0.1:8000/admin/

---

## 🎨 Personnalisation

### Changer le nom / infos
Rechercher `[Ton Nom]` dans les fichiers suivants et remplacer :
- `templates/portfolio/base.html` (navbar logo, footer, meta)
- `templates/portfolio/index.html` (hero, about, contact)

### Ajouter vos projets
1. Aller sur http://127.0.0.1:8000/admin/
2. Section **Projets** → Ajouter un projet
3. Renseigner titre, description, problème, solution, impact, image, liens

### Ajouter vos compétences
1. Section **Compétences** → Ajouter
2. Choisir la catégorie, niveau (1-100), icône Devicon, couleur

---

## 📁 Structure du Projet

```
monportfolio/
├── manage.py
├── requirements.txt
├── .env.example
├── docker-compose.yml
├── monportfolio/
│   ├── settings.py        # Configuration Django
│   ├── urls.py            # URLs principal
│   └── wsgi.py
├── portfolio/             # App principale
│   ├── models.py          # Skill, Project, ContactMessage
│   ├── views.py           # Class-Based Views
│   ├── admin.py           # Admin personnalisé
│   ├── forms.py           # Formulaire de contact
│   ├── urls.py
│   ├── fixtures/
│   │   └── demo_data.json # 10 skills + 6 projets
│   └── static/portfolio/
│       ├── css/style.css  # Glassmorphism + Dark mode
│       └── js/main.js     # Animations + Interactions
└── templates/
    └── portfolio/
        ├── base.html      # Layout général
        ├── index.html     # Single-page portfolio
        ├── 404.html
        └── 500.html
```

---

## 🚀 Déploiement (Render/Railway/Heroku)

```bash
python manage.py collectstatic --noinput
```

Définir en production :
```
DEBUG=False
SECRET_KEY=votre-cle-secrete-longue-et-aleatoire
ALLOWED_HOSTS=votre-domaine.com
```

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## ✅ Features

- [x] Dark/Light mode (localStorage)
- [x] Responsive mobile-first (hamburger menu)
- [x] Typing animation hero
- [x] Animated stats counters
- [x] Skill radial progress bars (SVG)
- [x] Skill & Project filterable tabs
- [x] Project detail modals
- [x] Contact form fonctionnel (enregistré en DB + email)
- [x] Admin Django personnalisé
- [x] Scroll reveal animations
- [x] SEO meta + schema.org
- [x] Custom 404/500 pages
- [x] WhiteNoise static files

---

*© 2026 [Ton Nom] — Yaoundé, Cameroun 🇨🇲*
