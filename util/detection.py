import cv2
import numpy as np
import torch
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import pytesseract

class Detection():
    def __init__(self, model_name='best.pt'):
        self.model_name = model_name
        self.colors = [(0, 255, 255), (0, 0, 255)]  # 클래스별 색상 지정 (0: 정상, 1: 불법)

    def draw_korean_text(self, pil_image, text, position, font_path='arial.ttf', font_size=20, color=(255, 255, 255)):
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)
        draw.text(position, text, font=font, fill=color)
        return pil_image

    def get_video(self, video_path, output_path):
        # 모델 로드
        model_path = Path('models') / self.model_name
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)

        # 클래스 이름 목록 로드
        class_names = model.names

        # 영상 로드
        video_path = video_path
        cap = cv2.VideoCapture(str(video_path))

        # 저장할 동영상 정보 설정
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

        # 객체 검출 및 결과 저장
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = model([frame])

            # 결과를 이미지에 표시
            for result in results.xyxy[0]:
                if result[-1] > 0.3:
                    class_id = int(result[-2])
                    color = self.colors[class_id]  # 해당 클래스에 대한 색상
                    cv2.rectangle(frame, (int(result[0]), int(result[1])),
                                  (int(result[2]), int(result[3])), color, 2)

                    # 클래스 이름 추가
                    class_name = class_names[class_id]
                    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    pil_image = self.draw_korean_text(pil_image, class_name, (int(result[0]), int(result[1]) - 25), font_path='/System/Library/Fonts/Supplemental/AppleGothic.ttf', color=color)
                    frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

            # 결과를 저장할 영상에 쓰기
            out.write(frame)

        cap.release()
        out.release()
        print(f'Result video saved at {output_path}')
