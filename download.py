import os
import subprocess

def download_subtitles_from_playlist(playlist_url, language='ja', output_dir='subtitles'):
    os.makedirs(output_dir, exist_ok=True)
    command = [
        'yt-dlp',
        '--write-sub',
        '--write-auto-sub',
        '--sub-lang', 'ja*',   # <-- match all Japanese variants
        '--sub-format', 'vtt/srt',
        '--convert-subs', 'srt',
        '--skip-download',
        '--output', os.path.join(output_dir, '%(title)s.%(ext)s').replace(".ja", ""),
        playlist_url
    ]


    try:
        subprocess.run(command, check=True)
        print("✅ Subtitles downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Error during download:", e)

if __name__ == '__main__':
    playlist_url = input("Enter YouTube playlist URL: ").strip()
    download_subtitles_from_playlist(playlist_url)
