import subprocess
import os
import logging

#Logger Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Downloader.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class SpotifyDownloader:
    def __init__(self, output_dir="downloads"):
        """
        Starting downloader and ensuring that the output directory exists
        """

        self.output_dir = output_dir
        self._setup_environment()



    def _setup_environment(self):
        """
        Creating Downloads directory if it doesnt already exist
        """

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logging.info(f"[SETUP] Directory {self.output_dir} created successfully.")



    def download_track(self, url: str) -> bool:
        """
        Execute spotdl command using subprocess to download the music or playlist.
        Return True if the download was successful or False, otherwise.
        """

        logging.info(f"\n[INFO] Starting the processing of: {url}")

        command =  [
            "spotdl",
            url,
            "--output",
            f"{self.output_dir}/{{artist}} - {{title}}"
        ]

        try:
            #Subprocess.run stop the script until the process finish.
            subprocess.run(command, check=True)
            logging.info(f"\n[SUCCESS] Downloaded Succesfully.")
            return True
        
        except subprocess.CalledProcessError as e:
            logging.error(f"\n[ERROR] Error processing download. Details: {e}")
            return False
        

    def download_from_file(self, filepath: str):
        """
        Read a textfile containing many urls per line, and process them all.
        """

        if not os.path.exists(filepath):
            logging.error(f"[ERROR] {filepath} not found. ")
            return
        
        logging.info(f"[INFO] Reading URL's from: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as file:
            urls = [line.strip() for line in file if line.strip()]

        if not urls:
            logging.warning(f"[WARNING] {filepath} is empty.")
            return
        
        logging.info(f"[INFO] total number of URLs found: {len(urls)}")

        for index, url in enumerate(urls, start=1):
            logging.info(f"[INFO] Processing item {index} of {len(urls)}")
            self.download_track(url)

        logging.info("[INFO] Processing Finished.")
        
if __name__ == "__main__":
    bot = SpotifyDownloader()

    while True:
        print("\n" + "="*30)
        print("🎵 SPOTIFY DOWNLOADER 🎵")
        print("="*30)
        print("1 - Insert an URL manually")
        print("2 - Read URLs from 'urls.txt'")
        print("0 - Exit program")
        print("="*30)

        escolha = input("Choose an option: ")

        if escolha == '1':
            url_teste = input("\nPaste the Spotify URL (Song or Playlist): ")

            if url_teste:
                bot.download_track(url_teste)

        elif escolha == '2':
            bot.download_from_file("urls.txt")

        elif escolha == '0':
            logging.info("[SYSTEM INFO] Exiting...")
            break

        else:
            logging.info("\nOpção inválida. Digite 0, 1 ou 2.")