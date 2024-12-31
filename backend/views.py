import os  # gère les chemins de fichiers
import logging  # for debug

from django.http import JsonResponse  # pour renvoyer des réponses JSON
from django.conf import settings  #  obtenir le chemin de base du projet
from django.views.decorators.csrf import csrf_exempt # pour éviter de mettre token obligatoire dans requests TEMPORAIRE TODO : A CHANGER POUR SÉCURITÉ
from decouple import config
from backend.pdf_2_script import main

# logger set up
logger = logging.getLogger(__name__)

ENVIRONMENT = config('ENVIRONMENT', default='production')

# Vue pour uploader un fichier PDF
@csrf_exempt
def upload_pdf(request):
    
    if ENVIRONMENT == 'local':
        TEMP_FILES_PATH = os.path.join(settings.BASE_DIR, 'TEMPORARY_FILES_FOLDER')
        os.makedirs(TEMP_FILES_PATH)
        logger.debug(f"Le répertoire a été créé : {TEMP_FILES_PATH}")
    else:
        TEMP_FILES_PATH = '/tmp'
        
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

        save_dir = os.path.join(TEMP_FILES_PATH, 'uploaded_files')  # Parent directory for uploaded files
        os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

        save_path = os.path.join(save_dir, uploaded_file.name)  # Full file path for the uploaded file
        logger.debug(f"path du fichier uploadé: {save_path}")

    
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():  # divise fichier en morceaux pour éviter problèmes de mémoire
                destination.write(chunk)

        
        pdf_name = os.path.splitext(uploaded_file.name)[0]  # Get the PDF name without extension
        output_folder = os.path.join(TEMP_FILES_PATH, 'png_oputput_folder', 'output_images')  # Folder for images

        logger.debug(f"Lancement du script pour traiter le fichier {uploaded_file.name}...")
        main.main(save_path, output_folder, pdf_name)


        return JsonResponse({'message': 'Ton fichier est rentré mon homme!', 'file_name': uploaded_file.name})
        
    except Exception as e:
        logger.error(f"Erreur lors de l'upload : {str(e)}")
        return JsonResponse({'error': f"Erreur interne : {str(e)}"}, status=500)
    
