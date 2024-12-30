import os  # gère les chemins de fichiers
import logging  # for debug

from django.http import JsonResponse  # pour renvoyer des réponses JSON
from django.conf import settings  #  obtenir le chemin de base du projet
from django.views.decorators.csrf import csrf_exempt # pour éviter de mettre token obligatoire dans requests TEMPORAIRE TODO : A CHANGER POUR SÉCURITÉ
from decouple import config
from pdf_2_script import main

# logger set up
logger = logging.getLogger(__name__)

ENVIRONMENT = config('ENVIRONMENT', default='production')
if ENVIRONMENT == 'local':
    FILE_UPLOAD_PATH = os.path.join(settings.BASE_DIR, 'uploaded_files')
else:
    FILE_UPLOAD_PATH = '/tmp'

# Vue pour uploader un fichier PDF
@csrf_exempt
def upload_pdf(request):
    logger.debug("on est rentré dans upload_pdf view")
    try:
        if request.method != 'POST':
                return JsonResponse({'error': 'Méthode non autorisée. Utilisez POST.'}, status=405)

        
        if 'file' not in request.FILES:
            logger.error("Aucun fichier trouvé voici ce qui a été reçu: %s", request.FILES)
            return JsonResponse({'error': 'Aucun fichier trouvé dans la requête.'}, status=400)
        
        uploaded_file = request.FILES['file']  
        
        if not uploaded_file.name.endswith('.pdf'):
                logger.error("Le fichier n'est pas un PDF.")
                return JsonResponse({'error': 'Seuls les fichiers PDF sont autorisés.'}, status=400)


        save_path = os.path.join(FILE_UPLOAD_PATH, uploaded_file.name) # chemin pour sauvegarder fichier, utilise uploaded_files path
        logger.debug(f"path du folder des fichiers uploader: {save_path}")
        
        if ENVIRONMENT == 'local' and not os.path.exists(FILE_UPLOAD_PATH):
            os.makedirs(FILE_UPLOAD_PATH)
            logger.debug(f"Le répertoire a été créé : {FILE_UPLOAD_PATH}")
        
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():  # divise fichier en morceaux pour éviter problèmes de mémoire
                destination.write(chunk)

        
        pdf_name = os.path.splitext(uploaded_file.name)[0]  # Get the PDF name without extension
        output_folder = os.path.join(settings.BASE_DIR, 'pdf_2_script', 'output_images')  # Folder for images

        logger.debug(f"Lancement du script pour traiter le fichier {uploaded_file.name}...")
        main.main(save_path, output_folder, pdf_name)


        return JsonResponse({'message': 'Ton fichier est rentré mon homme!', 'file_name': uploaded_file.name})
        
    except Exception as e:
        logger.error(f"Erreur lors de l'upload : {str(e)}")
        return JsonResponse({'error': f"Erreur interne : {str(e)}"}, status=500)
    
