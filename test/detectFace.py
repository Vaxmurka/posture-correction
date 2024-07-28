def face(cap, face_detection, time, cv2, Image, ImageStat, sbc, AppOpen, MAX_time, setBrightness, timeStat, getStartTime):
    ret, frame = cap.read()
    timeWork = 0
    Shape = 0
    breakFlag = False
    valueCam, valueDisplay = 0, 0

    # Обнаружение лиц с помощью Mediapipe
    results = face_detection.process(frame)

    if results.detections:
        Is_face = True  # Человек появился
        if getStartTime:
            timeStat = time.monotonic()
            getStartTime = False
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape

            # Определение расстояния от экрана до глаз(очень сильно округленная площадь прямоугольника)
            Shape = (bboxC.width * iw) * int(bboxC.height * ih)
            Shape = int(Shape) // 1000
    else:
        Is_face = False  # Человек пропал
        getStartTime = True

    if Is_face:
        timeWork = time.monotonic() - timeStat
        if timeWork >= MAX_time:
            breakFlag = True
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.imwrite('cam.png', image)
        screen = Image.open('cam.png').convert('L')
        screen = ImageStat.Stat(screen)

        valueCam = int(screen.rms[0])
        valueDisplay = sbc.get_brightness()[0]

        if valueCam < 25:
             valueCam = 10
        elif 25 <= valueCam < 51:
            valueCam = 20
        elif 51 <= valueCam < 76:
            valueCam = 30
        elif 76 <= valueCam < 102:
            valueCam = 40
        elif 102 <= valueCam < 127:
            valueCam = 50
        elif 127 <= valueCam < 153:
            valueCam = 60
        elif 153 <= valueCam < 178:
            valueCam = 70
        elif 178 <= valueCam < 204:
            valueCam = 80
        elif 204 <= valueCam < 229:
            valueCam = 90
        elif valueCam >= 229:
            valueCam = 100

        # if setBrightness:
        #     if valueDisplay - valueCam > 40:
        #         # sbc.fade_brightness(valueCam, interval=5, increment=-2)
        #     if valueCam - valueDisplay < 20:
        #         # sbc.fade_brightness(valueCam, interval=5, increment=2)

        # sbc.set_brightness(valueCam)
    return Shape, timeStat, breakFlag, valueCam, valueDisplay, timeWork, getStartTime
