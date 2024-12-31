import os  # File path handling
import logging  # For logging errors and information
import shutil  # To delete temporary folders
from django.http import JsonResponse  # To send JSON responses
from django.conf import settings  # To get the project's BASE_DIR
from django.views.decorators.csrf import csrf_exempt  # To bypass CSRF (temporary, for dev purposes)
from decouple import config
from backend.pdf_2_script import main

# Logger setup
logger = logging.getLogger(__name__)

# Environment setup
ENVIRONMENT = config('ENVIRONMENT', default='production')
if ENVIRONMENT == 'local':
    TEMP_FILES_PATH = os.path.join(settings.BASE_DIR, 'TEMPORARY_FILES_FOLDER')
    os.makedirs(TEMP_FILES_PATH, exist_ok=True)
    logger.debug(f"Temporary files directory created: {TEMP_FILES_PATH}")
else:
    TEMP_FILES_PATH = '/tmp'

# View for uploading a PDF and generating a podcast
@csrf_exempt
def upload_pdf(request):
    logger.debug("Entered the upload_pdf view")
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Méthode non autorisée. Utilisez POST.'}, status=405)

        # Check if a file is present in the request
        if 'file' not in request.FILES:
            logger.error("No file found in the request.")
            return JsonResponse({'error': 'Aucun fichier trouvé dans la requête.'}, status=400)

        uploaded_file = request.FILES['file']

        # Validate file type
        if not uploaded_file.name.endswith('.pdf'):
            logger.error("The uploaded file is not a PDF.")
            return JsonResponse({'error': 'Seuls les fichiers PDF sont autorisés.'}, status=400)

        # Save the uploaded file to a temporary path
        uploaded_folder = os.path.join(TEMP_FILES_PATH, 'uploaded_files')
        os.makedirs(uploaded_folder, exist_ok=True)

        save_path = os.path.join(uploaded_folder, uploaded_file.name)
        logger.debug(f"Path to save the uploaded file: {save_path}")

        with open(save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Process the PDF and generate a podcast
        pdf_name = os.path.splitext(uploaded_file.name)[0]  # Get the PDF name without extension
        output_folder = os.path.join(TEMP_FILES_PATH, 'png_output_folder', 'output_images')
        logger.debug(f"Launching script to process the file {uploaded_file.name}...")

        main.main(save_path, output_folder, pdf_name)

        podcast_path = f"{settings.MEDIA_URL}podcast_output_folder/GoogleTTS/full_audio_output/podcast.mp3"
        return JsonResponse({'message': 'Podcast generated successfully!', 'podcast_path': podcast_path})


    except Exception as e:
        logger.error(f"Error during upload and processing: {str(e)}")
        return JsonResponse({'error': f"Erreur interne : {str(e)}"}, status=500)
