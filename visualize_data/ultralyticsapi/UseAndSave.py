import os
import torch
import shutil
from PIL import Image
from pathlib import Path
from ultralytics import YOLO


def clear_directory(directory: Path):
    """
    清理指定目录，如果目录不存在，则先创建它。
    """
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)
    else:
        for item in directory.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()


def model_run(model_path, data_path, conf=0.25, iou=0.45):
    """
    对给定的模型和数据集运行YOLO对象检测。
    :param iou:
    :param conf:
    :param model_path: 模型路径
    :param data_path: 数据集路径
    :return: 检测结果
    """
    model = YOLO(model_path)
    return model(data_path, conf=conf, iou=iou, half=True, augment=True, agnostic_nms=True)


def save_results(results, result_txt_path, result_image_path):
    """
    保存所有对象检测结果
    :param results: 检测结果
    :param result_txt_path: 保存结果的txt文件路径
    :param result_image_path: 保存结果的图片文件夹路径
    :return: 保存的文件名和类别
    """
    file_with_cls = []

    if os.path.exists(result_txt_path):
        os.remove(result_txt_path)

    with open(result_txt_path, 'a') as file:
        for i, r in enumerate(results):
            im_bgr = r.plot()
            im_rgb = Image.fromarray(im_bgr[..., ::-1])

            # 取完整路径的文件名
            file_name = r.path.split('/')[-1]

            save_path = os.path.join(result_image_path, f'{file_name}')
            im_rgb.save(save_path)

            data = [
                {
                    'cls': int(box.cls.item()),
                    'conf': box.conf.item(),
                    'xyxy': [round(coordinate) for coordinate in box.xyxy.tolist()[0]],
                    'filename': file_name
                }
                for box in r.boxes
            ]

            # 提取类别
            cls_list = []
            for item in data:
                cls_list.append(item['cls'])
            file_with_cls.append({'filename': file_name, 'cls': cls_list})

            for item in data:
                # 格式化每行的数据，并以空格分隔
                line = f"{item['filename']}\t{item['cls']}\t{item['conf']}\t{' '.join(map(str, item['xyxy']))}\n"
                # 写入文件
                file.write(line)

            print(f'{i + 1}: {save_path}')
            # r.show()

    return file_with_cls
