import pathlib


def dataset_summary(dataset_dir: Path):
    """
    数据按照 '类别: 训练图像数 | 训练标注数 | 验证图像数 | 验证标注数' 的格式横向打印。
    """

    hasLabel = True

    categories = [f'well{i}' for i in range(6)]
    counts = {category: {'train_images': 0, 'train_labels': 0, 'val_images': 0, 'val_labels': 0} for category in
              categories}

    images_path = pathlib.Path.joinpath(dataset_dir, 'images')
    labels_path = pathlib.Path.joinpath(dataset_dir, 'labels')

    if not images_path.exists() or not labels_path.exists():
        hasLabel = False
        allPictures = len(list(dataset_dir.glob('*.png')) + list(dataset_dir.glob('*.jpg')))
        return allPictures, hasLabel

    # 收集计数信息
    for category in categories:
        counts[category]['train_images'] = len(list((dataset_dir / 'images/train').glob(f'{category}_*.*')))
        counts[category]['train_labels'] = len(list((dataset_dir / 'labels/train').glob(f'{category}_*.txt')))
        counts[category]['val_images'] = len(list((dataset_dir / 'images/val').glob(f'{category}_*.*')))
        counts[category]['val_labels'] = len(list((dataset_dir / 'labels/val').glob(f'{category}_*.txt')))

    # 汇总信息
    allPictures = 0
    for category in categories:
        cat_counts = counts[category]
        allPictures += cat_counts['train_images'] + cat_counts['val_images']

    return allPictures, hasLabel

