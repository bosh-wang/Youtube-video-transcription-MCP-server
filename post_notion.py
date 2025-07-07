from mcp.server.fastmcp import FastMCP
from notion_client import Client as NotionClient
from dotenv import load_dotenv
import os

# Initialize FastMCP server
mcp = FastMCP("transcribe")

@mcp.tool()
def post_to_notion(title: str, url: str, summary: str) -> str:
    """Upload summarized articles to Notion page and return the published Notion page url.
    
    Agrs:
        title: Summary titile.
        url: Video url.
        summary: Summary.
    """
    load_dotenv()
    client = NotionClient(auth=os.getenv("NOTION_TOKEN"))
    page_id = os.getenv("NOTION_PAGE_ID")
    try:
        client.blocks.children.append(
            block_id=page_id,
            children=[
                {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"type": "text", "text": {"content": title}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"URL: {url}"}}]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": summary}}]}}
            ]
        )
        return "https://scratched-fluorine-d9c.notion.site/Video-Transcription-21c2f714a55480a1aecbdc42b759c3cc?source=copy_link"
    except Exception as e:
        return e
    
    
if __name__ == "__main__":
    mcp.run(transport='stdio')