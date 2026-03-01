# 🎬 Multimedia Converter Pro (ArgOs Edition)

Una herramienta potente, rápida y minimalista diseñada exclusivamente para **ArgOs Platinum**. Convertí videos, extraé audio y comprimí archivos multimedia con un solo clic, utilizando todo el poder de `ffmpeg` bajo una interfaz moderna.

---

## 🚀 Características Principales

* **Conversión Ultra Rápida**: Soporte para MP4, MKV, MOV y AVI.
* **Audio Master**: Extraé audio de cualquier video a MP3 o FLAC en alta calidad.
* **Compresión Inteligente**: Reducí el peso de tus archivos para WhatsApp o Discord sin perder calidad visual.
* **Interfaz Platinum**: Diseñado con GTK4 y Libadwaita para una integración perfecta con el escritorio.
* **Procesamiento por Lotes**: (Si lo tiene) Arrastrá y soltá múltiples archivos.

---

## 📸 Capturas de Pantalla

> [!TIP]
> ¡Agregá acá una captura de tu app funcionando para que los usuarios se enamoren!
> `![Preview](https://link-a-tu-captura.jpg)`

---

## 🛠️ Instalación en ArgOs / Debian

Asegurate de tener las dependencias necesarias instaladas:

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 ffmpeg
Cloná el repositorio y ejecutalo:

Bash
git clone [https://github.com/tu-usuario/multimedia-converter-pro.git](https://github.com/tu-usuario/multimedia-converter-pro.git)
cd multimedia-converter-pro
python3 converter.py
