# 🎬 Multimedia Converter Pro (ArgOs Edition)

Una herramienta potente, rápida y minimalista diseñada exclusivamente para **ArgOs Platinum**. Convertí videos, extraé audio y comprimí archivos multimedia con un solo clic, utilizando todo el poder de `ffmpeg` bajo una interfaz moderna.

## 🚀 Características Principales

* **Conversión Ultra Rápida**: Soporte para MP4, MKV, MOV y AVI.
* **Audio Master**: Extraé audio de cualquier video a MP3 o FLAC en alta calidad.
* **Compresión Inteligente**: Reducí el peso de tus archivos para WhatsApp o Discord sin perder calidad visual.
* **Interfaz Platinum**: Diseñado con GTK4 y Libadwaita para una integración perfecta con el escritorio.
* **Procesamiento por Lotes**: (Si lo tiene) Arrastrá y soltá múltiples archivos.

---

## 📸 Capturas de Pantalla

<img width="1440" height="900" alt="Captura de pantalla_2026-02-28_20-57-00" src="https://github.com/user-attachments/assets/032e577c-8980-456a-99ae-d8a8547dc32a" />
<img width="1440" height="900" alt="Captura de pantalla_2026-02-28_20-55-27" src="https://github.com/user-attachments/assets/dbebe662-c28b-498a-8b15-a84ca4d2c607" />
<img width="1440" height="900" alt="Captura de pantalla_2026-02-28_20-54-54" src="https://github.com/user-attachments/assets/2dcd47af-5674-4d34-8e83-f62eadf26d68" />
<img width="1440" height="900" alt="Captura de pantalla_2026-02-28_20-54-30" src="https://github.com/user-attachments/assets/876069b6-39e9-48b3-b50c-d94ac820c9d8" />
<img width="1440" height="900" alt="Captura de pantalla_2026-02-28_21-01-12" src="https://github.com/user-attachments/assets/7a47cafb-7cd9-4926-a0cc-feb97c555548" />



⚙️ Cómo funciona

Seleccioná el archivo que querés transformar.

Elegí el formato de salida o el preset de compresión.

Dale a "Convertir" y dejá que ArgOs haga la magia.

💡 Tips de Rendimiento
Para videos 4K, se recomienda usar el Modo Gamer de OpenDash para priorizar los procesos de CPU.

Si vas a comprimir, recordá que el formato H.265 ofrece el mejor equilibrio entre peso y calidad.

- Tipo	Formatos	Engine:

- Video	MP4, MKV, AVI, MOV	FFMPEG (H.264/H.265)
- Audio	MP3, WAV, FLAC, OGG	FFMPEG (libmp3lame)
Web	WebM, GIF	FFMPEG (VP9)

🤝 Contribuir
¿Tenés una idea para mejorar el conversor?

Hacé un Fork del proyecto.

Creá una rama con tu mejora: git checkout -b feature/MejoraIncreible.

Mandá un Pull Request.

Desarrollado por Tavo para el ecosistema ArgOs Platinum. 🇦🇷

## 🛠️ Instalación en ArgOs / Debian

Asegurate de tener las dependencias necesarias instaladas:

- sudo apt update
- sudo apt install python3-gi gir1.2-gtk-4.0 gir1.2-adw-1 ffmpeg
- 
Cloná el repositorio y ejecutalo:

git clone [https://github.com/tu-usuario/multimedia-converter-pro.git](https://github.com/tu-usuario/multimedia-converter-pro.git)
cd multimedia-converter-pro
python3 converter.py

### Método Recomendado (.deb)
Si sos usuario de **ArgOs Platinum**, simplemente descargá el paquete `.deb` de la sección de [Releases](https://github.com/Tavo78ok/Multimedia-Converter-Pro/releases) e instalalo con:

sudo apt install ./multimedia-converter-pro_1.0_amd64.deb




