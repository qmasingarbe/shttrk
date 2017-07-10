# Voici 4 exemples d'utilisation de shttrk du plus simple au plus compliqué.

### 1. commentsCouter : compter le nombre de commentaire par utilisateurs
Script qui scan un projet shotTracker, recupère tous les commentaires et compte le nombre de commentaires postés par personne.
*Les bandeaux roses autopostés quand on change un tag sont également comptés comme commentaires.*

### 2. thumbnailUpdateFromFile : updater les miniatures des assets depuis un dossier windows
Script qui scan les assets d'un projet + un dossier sur le disque dur. Si une image contenu dans le dossier à le même nom qu'un asset, le script remplace l'ancienne vignette par l'image.

### 3. screenShotMaya : poster un screenshot du viewport directement de maya
Script *(pour maya python)* qui génère une fenêtre proposant de choisir un projet et un asset. Le script post alors un screenshot du viewport maya (playblast sur une frame) dans l'asset selectionné en l'attachant à un nouveau commentaire.
![Image of mayaScreenshot](https://github.com/qmasingarbe/shttrk/blob/master/examples/mayaScreenshotExample.JPG)

### 4. shotGunStudio : copier des assets de shotGun à shotTracker
Script qui scan un projet shotGun et récupère les infos des assets. Il va ensuite recréer ces assets dans shotTracker. Les infos prises en comptes pour le moment sont sont le nom de l'asset, sa description, sa vignette, son type (sg_asset_type) et son status d'avancement (sg_status_list). Le script crée les tags manquant, récupère les vignettes, etc... *Si les assets sont déjà créés, le script update simplement les infos.*
