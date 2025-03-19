import cv2
from PIL import Image
import base64
from io import BytesIO

from lab13.AES.AES import AES
from lab13.CTR import CTR


class ImageStrTransformer:
    def image_to_base64(self, image_path:str):
        """
            Преобразует изображение в строку Base64.

            :param image_path: Путь к изображению.
            :return: Строка Base64.
            """
        # Открываем изображение
        with Image.open(image_path) as img:
            # Преобразуем изображение в байты
            buffered = BytesIO()
            img.save(buffered, format="PNG")  # Сохраняем в формате PNG
            img_bytes = buffered.getvalue()

        # Кодируем байты в Base64
        base64_str = base64.b64encode(img_bytes).decode('utf-8')
        return base64_str

    def base64_to_image(self,base64_str: str, output_path: str) -> None:
        """
        Преобразует строку Base64 обратно в изображение и сохраняет его.

        :param base64_str: Строка Base64.
        :param output_path: Путь для сохранения изображения.
        """
        # Декодируем Base64 строку в байты
        img_bytes = base64.b64decode(base64_str)

        # Сохраняем байты как изображение
        with open(output_path, "wb") as img_file:
            img_file.write(img_bytes)

if __name__ == '__main__':
    cbc = CTR(AES())
    image_path = "images.jpg"
    image_transformer = ImageStrTransformer()
    base64_str = image_transformer.image_to_base64(image_path)
    print("Base64 строка:", base64_str)
    encrypted_string = cbc.encrypt(base64_str)
    print("Зашифрованная строка",encrypted_string)
    decode_string = cbc.decrypt(encrypted_string)
    print("Расшифрованная строка",decode_string)
    image_transformer.base64_to_image(decode_string,"result.jpg")
    image = cv2.imread("result.jpg")
    resized_image = cv2.resize(image, (1000, 600))
    cv2.imshow("result", resized_image)
    cv2.waitKey(0)