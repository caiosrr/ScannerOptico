import cv2
import numpy as np

class Camera:
    def __init__(self, camera_index=1):
        self.cam = cv2.VideoCapture(camera_index)
        self.frames_list = []

    def show_image(self):# IMAGEM SEM CORTES 480X640
        validacao, frame = self.cam.read()
        if validacao:
            # Obtém as dimensões da imagem
            altura, largura = frame.shape[:2]
            # Retorna a imagem completa sem cortes
            return frame
        else:
            return None

    def show_image1x1(self, margin=20): # A imagem inicial é 480x640 e a final é 440x440
        validacao, frame = self.cam.read()
        if validacao:
            # Obtém as dimensões da imagem
            altura, largura = frame.shape[:2]
            nova_altura = altura - 2 * margin
            nova_largura = largura - 2 * margin
            # Garante que as novas dimensões sejam válidas
            if nova_altura > 0 and nova_largura > 0:
                # Corta a margem de cada lado
                frame_cortado = frame[margin:altura - margin, margin:largura - margin]
                menor_dimensao = min(nova_altura, nova_largura) # Determina a menor dimensão
                frame_cortado = frame_cortado[:menor_dimensao, :menor_dimensao] # Ajusta a imagem para que as dimensões sejam iguais à menor dimensão
                return frame_cortado
            else:
                print("Margem muito grande para as dimensões da imagem.")
                return None
        else:
            return None

    def save(self, filename, frame):
        cv2.imwrite(filename, frame)
        print(f"Imagem salva como {filename}")

    def mean_img(self, number_frames):
        if self.frames_list:
            mean_frame = np.mean(self.frames_list, axis=0).astype(np.uint8)
            filename = rf"teste\mean_image_{number_frames}_frames.png"
            cv2.imwrite(filename, mean_frame)
            print(f"Imagem média salva em {filename}")
        else:
            print("Nenhum frame capturado para calcular a média")

    def release(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def increase_saturation(self, frame, saturation_scale=1.5):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_scale, 0, 255)
        saturated_frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return saturated_frame

if __name__ == "__main__":
    camera = Camera()
    img_counter = 0
    number_frames = 0
    while True:
        frame = camera.show_image1x1()
        if frame is None:
            break
        frame = camera.increase_saturation(frame)
        cv2.imshow("Frame", frame)  # Exibe a imagem processada
        key = cv2.waitKey(5) & 0xFF
        if key == 112:  # Tecla 'p'
            camera.save(f"Frame_{img_counter}_2.png", frame)
            img_counter += 1
        if key == 109:  # Tecla 'm'
            camera.frames_list.append(frame)
            number_frames += 1
        if key == 27:  # Tecla 'Esc'
            break
    camera.mean_img(number_frames)
    camera.release()