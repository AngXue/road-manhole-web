class ImagePredictor:
    def __init__(self, model_path, input_size=640, conf_threshold=0.25, nms_threshold=0.45, class_names=None):
        self.model_path = model_path
        self.input_size = input_size
        self.conf_threshold = conf_threshold
        self.nms_threshold = nms_threshold
        self.class_names = class_names if class_names else []
        self.ort_session = ort.InferenceSession(model_path)
        self.input_name = self.ort_session.get_inputs()[0].name
        self.output_name = self.ort_session.get_outputs()[0].name

    def preprocess(self, img_path):
        # 使用相同的预处理方法，YOLOv5在训练时使用的
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.input_size, self.input_size))
        image = image.astype(np.float32) / 255.0  # 归一化到[0,1]
        image = np.transpose(image, (2, 0, 1))  # 调整通道顺序为CHW
        image = np.expand_dims(image, axis=0)  # 添加批量维度BCHW
        return image

    def predict(self, image):
        outputs = self.ort_session.run([self.output_name], {self.input_name: image})
        return outputs[0]

    def postprocess(self, outputs):
        batch_results = []
        for output in outputs:
            boxes = []
            confidences = []
            class_ids = []

            for detection in output[0]:
                objectness_score = detection[4]  # 对象存在概率
                scores = detection[5:]  # 类别得分
                class_id = np.argmax(scores)
                confidence = scores[class_id] * objectness_score

                if confidence > self.conf_threshold:
                    center_x, center_y, width, height = detection[0:4]
                    x_min = int(center_x - (width / 2))
                    y_min = int(center_y - (height / 2))
                    x_max = int(center_x + (width / 2))
                    y_max = int(center_y + (height / 2))

                    boxes.append([x_min, y_min, x_max, y_max])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

            indices = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)

            # 根据返回的indices类型来适当处理
            if len(indices) == 0:
                final_indices = []  # 没有边界框被选中
            else:
                if isinstance(indices, np.ndarray):
                    final_indices = indices.flatten().tolist()  # 转换为Python列表
                elif isinstance(indices[0], tuple):
                    final_indices = [i[0] for i in indices]  # 解包元组
                else:
                    final_indices = indices  # 直接使用indices

            final_boxes = [boxes[i] for i in final_indices]
            final_class_ids = [class_ids[i] for i in final_indices]
            final_confidences = [confidences[i] for i in final_indices]
            batch_results.append((final_boxes, final_class_ids, final_confidences))

        return batch_results

    def draw_boxes_and_save(self, img_path, predictions, save_path):
        # 加载原始图像
        image = cv2.imread(img_path)

        orig_height, orig_width = image.shape[:2]  # 使用cv2.imread加载的原始图像尺寸
        model_height, model_width = self.input_size, self.input_size

        # 计算缩放因子
        scale_x = orig_width / model_width
        scale_y = orig_height / model_height

        final_boxes, final_class_ids, final_confidences = predictions[0]

        # 对final_boxes中的每个边界框坐标进行反缩放
        scaled_final_boxes = []
        for box in final_boxes:
            x_min, y_min, x_max, y_max = box
            x_min = int(x_min * scale_x)
            y_min = int(y_min * scale_y)
            x_max = int(x_max * scale_x)
            y_max = int(y_max * scale_y)
            scaled_final_boxes.append([x_min, y_min, x_max, y_max])

        # 使用反缩放后的边界框进行绘制
        for box, class_id, confidence in zip(scaled_final_boxes, final_class_ids, final_confidences):
            x_min, y_min, x_max, y_max = box
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            label = f"{self.class_names[class_id]}: {confidence:.2f}"
            cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imwrite(save_path, image)

    def predict_single_image(self, img_path, save_path=None):
        image = self.preprocess(img_path)
        outputs = self.predict(image)
        predictions = self.postprocess([outputs])
        if save_path:
            self.draw_boxes_and_save(img_path, predictions, save_path)
        return predictions

    def predict_multiple_images(self, img_paths, results_dir):
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        for img_path in img_paths:
            save_path = os.path.join(results_dir, os.path.basename(img_path))
            self.predict_single_image(img_path, save_path)
