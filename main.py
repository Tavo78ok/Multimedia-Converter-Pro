#!/usr/bin/env python3
import sys
import os
import threading
import subprocess
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, GLib, Adw, Gdk

class ConverterWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 👇 ACÁ VA EL CSS
        css = b"""
        button.iniciar {
            background: #3584e4;
            color: white;
            border-radius: 8px;
        }
        button.iniciar:hover {
            background: #1c71d8;
        }
        button.iniciar:active {
            background: #1a5fb4;
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # 👇 y recién después sigue tu código normal
        self.set_title("Multimedia Converter Pro v1.0.6")
        self.set_default_size(720, 720)

        self.files_data = []
        self.is_running = False
        self.current_process = None

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)

        header = Adw.HeaderBar()
        main_box.append(header)

        self.btn_add = Gtk.Button(icon_name="list-add-symbolic", tooltip_text="Añadir")
        self.btn_add.connect("clicked", self.on_add_clicked)
        header.pack_start(self.btn_add)

        self.btn_clear = Gtk.Button(icon_name="edit-clear-all-symbolic", tooltip_text="Limpiar")
        self.btn_clear.connect("clicked", self.on_clear_clicked)
        header.pack_start(self.btn_clear)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content_box.set_margin_top(15); content_box.set_margin_bottom(15)
        content_box.set_margin_start(15); content_box.set_margin_end(15)
        main_box.append(content_box)

        # --- AJUSTES PREMIUM RECUPERADOS ---
        group_config = Adw.PreferencesGroup(title="Parámetros Técnicos (Full Control)")
        content_box.append(group_config)

        self.format_row = Adw.ComboRow(title="Formato de Destino")
        self.format_row.set_model(Gtk.StringList.new([
            "MP4 (H.264)", "MKV (H.265)", "MOV", "AVI",
            "MP3", "FLAC (Hi-Res)", "WAV", "OGG", "M4A"
        ]))
        group_config.add(self.format_row)

        self.hz_row = Adw.ComboRow(title="Sample Rate")
        self.hz_row.set_model(Gtk.StringList.new(["Original", "44100 Hz", "48000 Hz", "96000 Hz"]))
        group_config.add(self.hz_row)

        # RECUPERADO: Selector de Bitrate Real
        self.bitrate_row = Adw.ComboRow(title="Calidad / Bitrate (kbps)")
        self.bitrate_row.set_model(Gtk.StringList.new(["320k (Ultra)", "256k (Alta)", "192k (Estándar)", "128k (Media)", "112k (Baja)"]))
        group_config.add(self.bitrate_row)

        # --- LISTA CON SCROLL ---
        list_frame = Gtk.Frame(label="Cola de Procesamiento")
        content_box.append(list_frame)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_min_content_height(220)
        scrolled.set_vexpand(True)

        self.list_box = Gtk.ListBox()
        self.list_box.add_css_class("boxed-list")
        scrolled.set_child(self.list_box)
        list_frame.set_child(scrolled)

        self.progress_bar = Gtk.ProgressBar(show_text=True)
        content_box.append(self.progress_bar)

        action_box = Gtk.Box(spacing=10)
        self.btn_convert = Gtk.Button(label="🔥 Iniciar", hexpand=True)
        self.btn_convert.add_css_class("iniciar")
        self.btn_convert.connect("clicked", self.start_conversion)

        self.btn_stop = Gtk.Button(label="Detener", sensitive=False)
        self.btn_stop.add_css_class("destructive-action")
        self.btn_stop.connect("clicked", self.stop_conversion)

        action_box.append(self.btn_convert); action_box.append(self.btn_stop)
        content_box.append(action_box)

    def on_add_clicked(self, btn):
        dialog = Gtk.FileDialog.new()
        dialog.open_multiple(self, None, self.on_files_selected)

    def on_files_selected(self, dialog, result):
        try:
            files = dialog.open_multiple_finish(result)
            for i in range(files.get_n_items()):
                path = files.get_item(i).get_path()
                if path not in self.files_data:
                    self.files_data.append(path)
                    row = Adw.ActionRow(title=os.path.basename(path))
                    row.add_prefix(Gtk.Image.new_from_icon_name("media-record-symbolic"))
                    self.list_box.append(row)
        except: pass

    def on_clear_clicked(self, btn):
        while child := self.list_box.get_first_child(): self.list_box.remove(child)
        self.files_data = []
        self.progress_bar.set_fraction(0); self.progress_bar.set_text("")

    def start_conversion(self, btn):
        if not self.files_data: return
        self.toggle_ui(False)
        threading.Thread(target=self.run_ffmpeg, daemon=True).start()

    def stop_conversion(self, btn):
        self.is_running = False
        if self.current_process: self.current_process.terminate()
        self.toggle_ui(True)

    def run_ffmpeg(self):
        self.is_running = True
        exts = [".mp4", ".mkv", ".mov", ".avi", ".mp3", ".flac", ".wav", ".ogg", ".m4a"]
        hz_map = [None, "44100", "48000", "96000"]
        # Mapeo de Bitrate KBPS
        bitrate_map = ["320k", "256k", "192k", "128k", "112k"]
        # Mapeo de CRF para video (proporcional al bitrate elegido)
        crf_map = ["17", "20", "23", "28", "32"]

        sel_format = exts[self.format_row.get_selected()]
        sel_hz = hz_map[self.hz_row.get_selected()]
        sel_bitrate = bitrate_map[self.bitrate_row.get_selected()]
        sel_crf = crf_map[self.bitrate_row.get_selected()]

        out_dir = os.path.join(os.path.dirname(self.files_data[0]), "Convertidos")
        os.makedirs(out_dir, exist_ok=True)

        for i, file_path in enumerate(self.files_data):
            if not self.is_running: break
            GLib.idle_add(
                self.update_progress,
                i / len(self.files_data),
                f"Procesando archivo {i+1}/{len(self.files_data)}..."
            )

            try:
                probe = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], capture_output=True, text=True)
                total_duration = float(probe.stdout.strip()) if probe.stdout.strip() else 1.0
            except: total_duration = 1.0

            filename = os.path.splitext(os.path.basename(file_path))[0]
            out_path = os.path.join(out_dir, f"{filename}{sel_format}")

            cmd = ['ffmpeg', '-y', '-i', file_path]
            if sel_hz: cmd += ['-ar', sel_hz]

            if sel_format in [".mp3", ".flac", ".wav", ".ogg", ".m4a"]:
                cmd += [
                # Streams
                '-map', '0:a',
                '-map', '0:v?',
                '-map_metadata', '0',

                # Audio encoding
                '-c:a', 'libmp3lame' if sel_format == '.mp3' else 'copy',
                '-b:a', sel_bitrate,

                # Cover (carátula)
                '-c:v', 'copy',
                '-disposition:v', 'attached_pic',

                # ID3 tags
                '-id3v2_version', '3',
                '-write_id3v1', '1'
            ]

            else:
                # COMANDO VIDEO PREMIUM (Threads 0 para tu Core 2 Duo)
                codec = "libx265" if sel_format == ".mkv" else "libx264"
                cmd += ['-c:v', codec, '-crf', sel_crf, '-preset', 'medium', '-threads', '0', '-c:a', 'aac', '-b:a', '192k']

            cmd += ['-progress', 'pipe:1', '-nostats', out_path]
            self.current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')

            while True:
                line = self.current_process.stdout.readline()
                if not line:
                    break

                # Progreso real (solo cuando ffmpeg lo emite)
                if "out_time_ms" in line:
                    try:
                        time_ms = int(line.split('=')[1].strip())
                        progress_val = min((time_ms / 1_000_000) / total_duration, 1.0)
                        total_p = (i / len(self.files_data)) + (progress_val / len(self.files_data))
                        GLib.idle_add(
                            self.update_progress,
                            total_p,
                            f"Archivo {i+1}/{len(self.files_data)} - {int(progress_val * 100)}%"
                        )
                    except:
                        pass
            self.current_process.wait()
            GLib.idle_add(
                self.update_progress,
                (i + 1) / len(self.files_data),
                f"Archivo {i+1}/{len(self.files_data)} - 100%"
            )

        self.is_running = False
        GLib.idle_add(self.finish_ui)

    def update_progress(self, fraction, text):
        self.progress_bar.set_fraction(fraction)
        self.progress_bar.set_text(text)

    def finish_ui(self):
        self.toggle_ui(True)
        dialog = Adw.MessageDialog(transient_for=self, heading="¡Conversión Completada!", body="Tus archivos están en 'Convertidos'.")
        dialog.add_response("ok", "Excelente"); dialog.present()

    def toggle_ui(self, s):
        self.btn_convert.set_sensitive(s); self.btn_add.set_sensitive(s)
        self.btn_clear.set_sensitive(s); self.btn_stop.set_sensitive(not s)

class ConverterApp(Adw.Application):
    def __init__(self): super().__init__(application_id='com.tavo.converter_v199')
    GLib.set_prgname('multimedia-converter')

    def do_activate(self):
        win = ConverterWindow(application=self); win.present()

if __name__ == "__main__":
    app = ConverterApp(); app.run(sys.argv)
