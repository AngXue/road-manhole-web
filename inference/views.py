from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from visualize_data.ultralyticsapi.UseAndSave import model_run, save_results, clear_directory
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
        clear_directory(Path('media/save/inferred_images'))
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

                # 解压后文件所在的目录
                # 假设zip文件中的目录结构与zip文件名相同
                extracted_folder_path = Path(extract_path) / Path(filename).stem

                # 检查解压后是否存在这样的目录
                if extracted_folder_path.is_dir():
                    # 如果存在，则传递这个目录给模型
                    results = model_run(MODEL_PATH, str(extracted_folder_path))
                else:
                    # 如果不存在，可能zip文件中直接就是文件，没有嵌套目录
                    results = model_run(MODEL_PATH, extract_path)

                # 删除解压后的文件夹和文件
                if extracted_folder_path.exists():
                    # 删除解压出来的文件夹
                    shutil.rmtree(extracted_folder_path)
                else:
                    # 如果解压后的是单个文件而不是目录，则删除单个文件
                    for item in Path(extract_path).iterdir():
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
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
