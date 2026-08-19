class ObjectDetector:
    def __init__(self):
        self.model = None

    def detect(self, frame) -> list[dict]:
        """
        Retorna os objetos encontrados no frame.

        Futuramente pode ser integrado com:
        - YOLO
        - PyTorch
        - TensorFlow
        """

        if self.model is None:
            return []

        results = self.model(frame)

        return results
