from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from visualize_data.ultralyticsapi.UseAndSave import model_run, save_results, clear_directory
import os
from pathlib import Path
import shutil
import zipfile


def list_models():
    models_path = Path(settings.MEDIA_ROOT) / 'models'
    return [model.name for model in models_path.iterdir() if model.is_file()]


def handle_uploaded_file(f, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def upload_and_infer(request):
    if request.method == 'POST':
        clear_directory(Path('media/save/inferred_images'))
        files = request.FILES.getlist('myfiles')
        selected_model = request.POST.get('model_selection')
        model_path = Path(settings.MEDIA_ROOT) / 'models' / selected_model
        results_list = []

        for f in files:
            filename = f.name
            uploaded_file_path = handle_uploaded_file(f, filename)
            if filename.endswith('.zip'):
                with zipfile.ZipFile(uploaded_file_path, 'r') as zip_ref:
                    extract_path = os.path.join(settings.MEDIA_ROOT, 'extracted')
                    zip_ref.extractall(extract_path)
                os.remove(uploaded_file_path)
                extracted_folder_path = Path(extract_path) / Path(filename).stem
                if extracted_folder_path.is_dir():
                    results = model_run(str(model_path), str(extracted_folder_path))
                else:
                    results = model_run(str(model_path), extract_path)
                shutil.rmtree(extracted_folder_path)
            else:
                results = model_run(str(model_path), uploaded_file_path)
                os.remove(uploaded_file_path)

            result_txt_path = os.path.join(settings.MEDIA_ROOT, 'save', 'results.txt')
            result_image_path = os.path.join(settings.MEDIA_ROOT, 'save', 'inferred_images')
            os.makedirs(os.path.dirname(result_txt_path), exist_ok=True)
            os.makedirs(result_image_path, exist_ok=True)

            file_with_cls = save_results(results, result_txt_path, result_image_path)
            results_list.extend(file_with_cls)

        models = list_models()
        return render(request, 'inference/inference_results.html', {'results': results_list, 'models': models})

    else:
        models = list_models()
        return render(request, 'inference/upload.html', {'models': models})
