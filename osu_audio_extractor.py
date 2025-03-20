import os
import zipfile
import shutil
import argparse
import sys


def extract_audio_from_osz(osz_file_path, output_dir):
    """
    Extrae el archivo de audio de un archivo .osz de OSU

    Args:
        osz_file_path (str): Ruta al archivo .osz
        output_dir (str): Directorio donde se guardará el archivo de audio extraído

    Returns:
        bool: True si la extracción fue exitosa, False en caso contrario
    """
    try:
        # Obtener el nombre del archivo sin extensión para usarlo como nombre de la canción
        file_name = os.path.basename(osz_file_path)
        song_name = os.path.splitext(file_name)[0]

        # Abrir el archivo .osz como un archivo zip
        with zipfile.ZipFile(osz_file_path, "r") as osz_zip:
            # Listar todos los archivos dentro del .osz
            file_list = osz_zip.namelist()

            # Buscar archivos de audio comunes en los beatmaps de OSU
            audio_extensions = [".mp3"]
            audio_files = []

            for file in file_list:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in audio_extensions:
                    audio_files.append(file)

            if not audio_files:
                print(f"No se encontraron archivos de audio en {file_name}")
                return False

            # Extraer cada archivo de audio encontrado
            for audio_file in audio_files:
                # Extraer el archivo de audio
                osz_zip.extract(audio_file, output_dir)

                # Ruta completa al archivo extraído
                extracted_file = os.path.join(output_dir, audio_file)

                # Nuevo nombre para el archivo (nombre del beatmap + extensión original)
                new_file_name = f"{song_name}{os.path.splitext(audio_file)[1]}"
                new_file_path = os.path.join(output_dir, new_file_name)

                # Renombrar y mover el archivo a la raíz del directorio de salida
                if os.path.dirname(extracted_file) != output_dir:
                    # Si el archivo está en una subcarpeta, moverlo a la raíz
                    if os.path.exists(new_file_path):
                        os.remove(new_file_path)  # Eliminar si ya existe
                    shutil.move(extracted_file, new_file_path)
                    # Eliminar carpetas vacías
                    parent_dir = os.path.dirname(extracted_file)
                    while parent_dir != output_dir:
                        if not os.listdir(parent_dir):
                            os.rmdir(parent_dir)
                        parent_dir = os.path.dirname(parent_dir)
                elif extracted_file != new_file_path:
                    # Si el archivo ya está en la raíz pero con otro nombre
                    if os.path.exists(new_file_path):
                        os.remove(new_file_path)  # Eliminar si ya existe
                    os.rename(extracted_file, new_file_path)

                print(f"Archivo extraído: {new_file_name}")

            return True
    except Exception as e:
        print(f"Error al procesar {osz_file_path}: {str(e)}")
        return False


def process_folder(input_folder, output_folder):
    """
    Procesa todos los archivos .osz en una carpeta

    Args:
        input_folder (str): Carpeta que contiene los archivos .osz
        output_folder (str): Carpeta donde se guardarán los archivos de audio extraídos
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Contar archivos procesados
    total_files = 0
    successful_extractions = 0

    # Buscar todos los archivos .osz en la carpeta de entrada
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".osz"):
                total_files += 1
                file_path = os.path.join(root, file)
                print(f"Procesando: {file}")
                if extract_audio_from_osz(file_path, output_folder):
                    successful_extractions += 1

    # Mostrar resumen
    print(f"\nResumen:")
    print(f"Total de archivos .osz encontrados: {total_files}")
    print(f"Extracciones exitosas: {successful_extractions}")


def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description="Extractor de audio de archivos .osz de OSU"
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Carpeta con archivos .osz (por defecto: 'input')",
        default="input",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Carpeta para audios extraídos (por defecto: 'output')",
        default="output",
    )

    # Parsear argumentos
    args = parser.parse_args()

    # Verificar y crear carpetas si no existen
    if not os.path.exists(args.input):
        os.makedirs(args.input, exist_ok=True)
        os.makedirs(args.output, exist_ok=True)
        print("\nPrimera ejecución detectada. Se han creado:\n")
        print(f"[INPUT]  {os.path.abspath(args.input)}")
        print(f"[OUTPUT] {os.path.abspath(args.output)}")
        print("\nColoca tus archivos .osz en la carpeta INPUT y vuelve a ejecutar.")
        sys.exit(0)

    # Asegurar que la carpeta de salida existe
    if not os.path.exists(args.output):
        os.makedirs(args.output, exist_ok=True)

    # Procesar la carpeta
    process_folder(args.input, args.output)


if __name__ == "__main__":
    main()
