import os  # gère les chemins de fichiers
import logging  # for debug

from django.http import JsonResponse  # pour renvoyer des réponses JSON
from django.conf import settings  #  obtenir le chemin de base du projet
from django.views.decorators.csrf import csrf_exempt # pour éviter de mettre token obligatoire dans requests TEMPORAIRE TODO : A CHANGER POUR SÉCURITÉ

# logger set up
logger = logging.getLogger(__name__)

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


        save_path = os.path.join('/tmp', uploaded_file.name) # chemin pour sauvegarder fichier, utilise temp path de render
        logger.debug(f"path du folder des fichiers uploader: {save_path}")
        
        upload_dir = os.path.dirname(save_path)
        if not os.path.exists(upload_dir):   #crée chemin pour save fichier temp si n'existe pas
            os.makedirs(upload_dir)
        
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():  # divise fichier en morceaux pour éviter problèmes de mémoire
                destination.write(chunk)

        
        logger.info(f"Fichier uploadé avec succès : {uploaded_file.name}")
        return JsonResponse({'message': 'Ton fichier est rentré mon homme!', 'file_name': uploaded_file.name})
        
    except Exception as e:
        logger.error(f"Erreur lors de l'upload : {str(e)}")
        return JsonResponse({'error': f"Erreur interne : {str(e)}"}, status=500)
    
