# Project1
### 모듈화 및 패키징을 위한 진행

---

__성능을 고려하지 않고 오직 모듈화와 패키징에만 초점을 맞춰서 진행하였습니다.__

1. 패키지의 디렉토리 구조

```
BaseModel
├── data
│   └── video
├── models
│   ├── best.pt
├── util
│   ├── __init__.py
│   └── detection.py
├── results
└── test
    └── test.ipynb
```

* data: 모델 추론의 입력값으로 사용할 영상 파일들이 저장되어 있는 폴더


* models: 추론에 사용될 사전 학습된 yolov5 모델이 저장되어 있는 폴더


* util: models 내 모델을 통해 영상 내 객체를 탐지하는 object detection을 진행하고

    결과를 .mp4 형태로 생성하는 detect모듈이 저장되어 있습니다.


* results: detction.py에 의해 생성된 결과 영상이 해당 폴더에 저장되게 됩니다.


* test: 해당 패키지가 정상적으로 작동하는지 확인하는 test.ipynb 파일을 포함하고 있습니다.