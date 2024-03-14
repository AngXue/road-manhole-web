from django.shortcuts import render
from .models import YolovModel
from onnxapi.imagePredictor import ImagePredictor
from onnxapi.analysisDataSet import dataset_summary


def get_available_names(request):
    """
    从数据库中查询所有模型名
    :param request:
    :return:
    """

    model_names = YolovModel.objects.all().values_list('name', flat=True)
    return render(request, 'index.html', {'models': model_names})


def select_model(request):
    """
    选择模型
    :param request:
    :return:
    """

    # 获取模型名
    model_name = request.POST.get('model_name')
    if not model_name:
        return render(request, 'index.html', {'result': False, 'msg': '模型名不能为空'})

    # 检查模型是否存在
    try:
        YolovModel.objects.get(name=model_name)
    except YolovModel.DoesNotExist:
        return render(request, 'index.html', {'result': False, 'msg': '模型不存在'})

    return render(request, 'index.html', {'result': True})


def get_model_overview(request):
    """
    获取模型概览信息
    :param request:
    :return:
    """

    model_name = request.POST.get('model_name')
    if not model_name:
        return render(request, 'index.html', {'result': False, 'msg': '模型名不能为空'})

    # 从数据库中查询模型信息
    yolov_model = YolovModel.objects.get(name=model_name)

    # 返回模型信息
    return render(request, 'index.html', {'result': True,
                                          'model_acid': yolov_model.acid,
                                          'model_size': yolov_model.size,
                                          'model_parameter': yolov_model.parameter})


def get_model_perfor(request):
    """
    获取模型性能信息
    :param request:
    :return:
    """

    model_name = request.POST.get('model_name')
    if not model_name:
        return render(request, 'index.html', {'result': False, 'msg': '模型名不能为空'})

    # 从数据库中查询模型信息
    model = YolovModel.objects.get(name=model_name)

    # TODO: 获取模型性能图路径

    # 返回模型信息
    return render(request, 'index.html', {'result': True})


def select_data_path(request):
    """
    选择数据集路径
    """

    data_path = request.POST.get('dataPath')

    if not data_path:
        return render(request, 'index.html', {'result': False, 'msg': '数据集路径不能为空'})
    elif not os.path.exists(data_path):
        return render(request, 'index.html', {'result': False, 'msg': '数据集路径不存在'})

    # TODO: 从数据集路径中获取样本图像路径 sample_path

    return render(request, 'index.html', {'result': True,
                                          'data_path': data_path,
                                          'sample_path': sample_path})


def pre_analysis(request):
    """
    统计需预测数据集
    """

    data_path = request.POST.get('data_path')

    all_pictures, has_label = dataset_summary(data_path)

    return render(request, 'index.html', {'result': True,
                                          'pic_mums': all_pictures,
                                          'hasLabel': has_label})


def start_detect(request):
    """
    开始预测
    """

    model_name = request.POST.get('model_name')
    data_path = request.POST.get('data_path')
    has_label = request.POST.get('has_label')

    model = YolovModel.objects.get(name=model_name)

    # predictor = ImagePredictor(model.path)
    # if has_label:
    #     image_paths = [str(p) for p in (Path(data_path).glob('*.jpg') + Path(image_dir).glob('*.png'))]
    #     predictor.predict_multiple_images(image_paths, 'detectResults')
    # else:
    #     predictor.predict_multiple_images(image_paths, 'detectResults')
    # TODO: 分析数据目录形式

    return render(request, 'index.html', {'result': True})


def get_detect_status(request):
    """
    获取预测状态
    """
    return render(request, 'index.html', {'result': True})


def get_detect_result(request):
    """
    获取预测结果统计
    """
    return render(request, 'index.html', {'result': True})


def get_samples_path(request):
    """
    获取样本图路径
    """
    return render(request, 'index.html', {'result': True})


def get_detect_model_perfor(request):
    """
    获取模型预测性能图
    """
    return render(request, 'index.html', {'result': True})
