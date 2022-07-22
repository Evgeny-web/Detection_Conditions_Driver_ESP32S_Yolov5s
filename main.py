import winsound
import torch
import cv2
import numpy as np
import re


model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp3/weights/last.pt', force_reload=True)


def object_detection_on_image():
    # url = 'http://192.168.43.24/cam-hi.jpg'
    frame_nums_awake = 0
    frame_nums_drowsy = 0
    frame_nums_sleep = 0
    signal_condition = 0

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        # img_resp = urllib.request.urlopen(url)
        # imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        # frame = cv2.imdecode(imgnp, -1)
        ret, frame = cap.read()

        # Получаем данные после работы модели
        result = model(frame)

        # Создаем область интереса в новом окне
        img = frame[:, :]
        img = cv2.blur(img, (75, 75))

        # Получаем id класса, чтобы дальше работать с состоянием класса
        tn = str(result.xyxy)
        datas = get_class_id_model(tn)
        x = datas[0]
        y = datas[1]
        x2 = datas[2]
        y2 = datas[3]
        class_id = datas[4]
        try:
            img[y-75: y2+75, x-75: x2+75] = frame[y-75: y2+75, x-75: x2+75]
            cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)
            if class_id == 15:
                cv2.putText(img, "Awake", (x, y-15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            if class_id == 16:
                cv2.putText(img, "Drowsy", (x, y-15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            if class_id == 17:
                cv2.putText(img, "Sleep", (x, y-15), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        except Exception:
            pass

        # Считываем количество кадров с Awake
        if class_id == 15:
            frame_nums_awake += 1
            if frame_nums_awake > 75:
                signal_condition = 0
                frame_nums_awake = 0
                frame_nums_drowsy = 0
                frame_nums_sleep = 0

        # Считываем количество кадров с Drowsy
        if class_id == 16:
            frame_nums_drowsy += 1
            if frame_nums_drowsy > 50:
                signal_condition = 1
                frame_nums_awake = 0
                frame_nums_drowsy = 0
                frame_nums_sleep = 0

        # Считываем количество кадров с Sleep
        if class_id == 17:
            frame_nums_sleep += 1
            if frame_nums_sleep > 20:
                signal_condition = 2
                frame_nums_awake = 0
                frame_nums_drowsy = 0
                frame_nums_sleep = 0

        # Рисуем и пишем предупреждение
        if signal_condition == 0:
            cv2.rectangle(img, (20, 20), (125, 60), (0, 255, 0), -1)
            cv2.putText(img, "All ok", (25, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        if signal_condition == 1:
            cv2.rectangle(img, (20, 20), (210, 60), (0, 255, 255), -1)
            cv2.putText(img, "Dont sleep", (25, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        if signal_condition == 2:
            cv2.rectangle(img, (20, 20), (330, 60), (0, 0, 255), -1)
            cv2.putText(img, "Wake UP, Warning", (25, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            duration = 10
            freq = 1000
            winsound.Beep(freq, duration)


        # Получаем изобаражение с камеры
        cv2.imshow('Frame', img)
        # cv2.imshow('YOLO', np.squeeze(result.render()))

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def get_class_id_model(sstr):
    try:
        list_variables_model = [float(i) for i in re.findall(r'-?\d+\.?\d*', sstr)]

        # достанем x, y, w, h, class_id
        if len(list_variables_model) > 6:
            x = int(list_variables_model[0] * 10 ** int(list_variables_model[1]))
            y = int(list_variables_model[2] * 10 ** int(list_variables_model[3]))
            w = int(list_variables_model[4] * 10 ** int(list_variables_model[5]))
            h = int(list_variables_model[6] * 10 ** int(list_variables_model[7]))
            class_id = int(list_variables_model[10] * 10 ** int(list_variables_model[11]))
        else:
            x = int(list_variables_model[0])
            y = int(list_variables_model[1])
            w = int(list_variables_model[2])
            h = int(list_variables_model[3])
            class_id = int(list_variables_model[5])

        # Выводим номер класса
        # print("Class_id: ", class_id)

    except Exception:
        x = None
        y = None
        w = None
        h = None
        class_id = None

    datas = []
    datas.append(x)
    datas.append(y)
    datas.append(w)
    datas.append(h)
    datas.append(class_id)

    return datas


def main():
    object_detection_on_image()


if __name__ == "__main__":
    main()