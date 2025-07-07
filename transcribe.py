from mcp.server.fastmcp import FastMCP
import yt_dlp
import os
from datetime import datetime
import whisper
from notion_client import Client as NotionClient
from dotenv import load_dotenv

# Initialize FastMCP server
mcp = FastMCP("transcribe")

@mcp.tool()
def transcribe(url: str) -> str:
    """Download video and transcribe audio to text.
    
    Args:
        url: Youtube video url.
    """
    folder = os.path.abspath(datetime.today().strftime("%Y-%m-%d"))
    os.makedirs(f"/home/eclab/projects/bosh/pytube/{folder}", exist_ok=True)
    ydl_opts = {
        'outtmpl': f'/home/eclab/projects/bosh/pytube/{folder}/%(upload_date)s - %(title)s.%(ext)s',
        'format': 'mp4/bestvideo+bestaudio',
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        path = ydl.prepare_filename(info).replace('.webm', '.mp4').replace('.mkv', '.mp4')

    # print(f"🎧 Transcribing {os.path.basename(path)}...")
    model = whisper.load_model("base")
    result = model.transcribe(path, verbose=False)
    # print("\n--- Transcribed Text ---\n")
    # print(result['text'])
    return result['text']

    
if __name__ == "__main__":
    # transcribe("https://www.youtube.com/watch?v=t9pRS1Mvy6c")
    mcp.run(transport='stdio')