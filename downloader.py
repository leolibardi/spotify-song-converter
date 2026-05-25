import subprocess
import os

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
            print(f"[SETUP] Directory {self.output_dir} created successfully.")



    def download_track(self, url: str) -> bool:
        """
        Execute spotdl command using subprocess to download the music or playlist.
        Return True if the download was successful or False, otherwise.
        """

        print(f"\n[INFO] Starting the processing of: {url}")

        command =  [
            "spotdl",
            url,
            "--output",
            f"{self.output_dir}/{{artist}} - {{title}}"
        ]

        try:
            #Subprocess.run stop the script until the process finish.
            subprocess.run(command, check=True)
            print(f"\n[SUCCESS] Downloaded Succesfully.")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Error processing download. Details: {e}")
            return False
        
if __name__ == "__main__":
    bot = SpotifyDownloader()

    url_test = input("Insert Spotify URL to test: ")
    
    if url_test:
        bot.download_track(url_test)

