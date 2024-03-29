# LitRevu

## Description
Notre nouvelle application, **LitRevu**, permet de demander ou publier des critiques de livres ou d’articles. L’application présente trois cas d’utilisation principaux :

- La publication des critiques de livres ou d’articles.
- La demande des critiques sur un livre ou sur un article particulier.
- La recherche d’articles et de livres intéressants à lire, en se basant sur les critiques des autres.

## Prérequis
Pour exécuter ce projet, vous aurez besoin d'avoir installé Python, Docker, et Git sur votre machine.

## Installation et Exécution

### Avec un Environnement Virtuel Python
1. **Cloner le dépôt Git** :

 ```
git clone https://github.com/PalexM/litrevu.git
```
 ```
cd litrevu
 ```
2. **Créer et activer un environnement virtuel** :
- Sous Windows :
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
- Sous Unix ou MacOS :
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Installer les dépendances** :
 ```
pip install -r requirements.txt
 ```
4. **Initialiser la base de données** :
 ```
python manage.py migrate
 ```

5. **Lancer le script** :
 ```
python crm.py

 ```

**Schema Base de donnees**

![schema Base de donnees](schema_db.png)





