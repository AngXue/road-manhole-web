from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from visualize_data.ultralyticsapi.UseAndSave import model_run, save_results
import os
from pathlib import Path
import shutil
import zipfile

# 模型路径
MODEL_PATH = 'maybe-the-end2.pt'


def handle_uploaded_file(f, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path


def upload_and_infer(request):
    if request.method == 'POST':
        files = request.FILES.getlist('myfiles')
        results_list = []

        for f in files:
            # 保存文件
            filename = f.name
            uploaded_file_path = handle_uploaded_file(f, filename)
            # 判断文件类型（单个图片或压缩包）
            if filename.endswith('.zip'):
                # 解压缩
                with zipfile.ZipFile(uploaded_file_path, 'r') as zip_ref:
                    extract_path = os.path.join(settings.MEDIA_ROOT, 'extracted')
                    zip_ref.extractall(extract_path)
                # 删除原压缩包
                os.remove(uploaded_file_path)
                # 执行批量推理
                results = model_run(MODEL_PATH, extract_path)
            else:
                # 执行单个图片推理
                results = model_run(MODEL_PATH, uploaded_file_path)
                # 删除原图片
                os.remove(uploaded_file_path)

            # 保存结果，并生成结果列表
            result_txt_path = os.path.join(settings.MEDIA_ROOT, 'save', 'results.txt')
            result_image_path = os.path.join(settings.MEDIA_ROOT, 'save', 'inferred_images')
            os.makedirs(os.path.dirname(result_txt_path), exist_ok=True)
            os.makedirs(result_image_path, exist_ok=True)

            file_with_cls = save_results(results, result_txt_path, result_image_path)
            results_list.extend(file_with_cls)

        # 返回渲染的结果页面，展示所有推理结果
        return render(request, 'inference/inference_results.html', {'results': results_list})

    # 对于GET请求或未包含文件的POST请求，展示上传页面
    return render(request, 'inference/upload.html')
