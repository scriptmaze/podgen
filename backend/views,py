from django.http import JsonResponse  # pour renvoyer des réponses JSON
import os  # gère les chemins de fichiers
from django.conf import settings  #  obtenir le chemin de base du projet

# Vue pour uploader un fichier PDF
def upload_pdf(request):
    if request.method == 'POST' and 'file' in request.FILES:  
        uploaded_file = request.FILES['file']  
        save_path = os.path.join(settings.BASE_DIR, 'uploaded_files', uploaded_file.name)  # chemin pour sauvegarder fichier
        
        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():  # divise fichier en morceaux pour éviter problèmes de mémoire
                destination.write(chunk)

        return JsonResponse({'message': 'Ton fichier est rentré mon homme!', 'file_name': uploaded_file.name})  
    
    return JsonResponse({'error': "Upload a fail :( Checker la requête."}, status=400)
