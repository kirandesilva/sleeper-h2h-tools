"""
Functions for delivering head-to-head information to Discord
"""

from pathlib import Path

from discord_webhook import DiscordWebhook, DiscordEmbed
from requests import Response

def send_text(webhook_url: str, content: str) -> Response:

    """
    Sends a string over a Discord webhook request

    PARAMETERS
    ----------
    webhook_url : str
        string of the webhook URL

    content : str
        string content to publish to the specified webhook URL

    RETURNS
    -------
    response : Response
        a requests Response object
    """

    webhook = DiscordWebhook(url=webhook_url, content=content)
    response = webhook.execute()

    return response

def send_image(webhook_url: str, content_path: str) -> Response:

    """
    Sends an image over a Discord webhook request

    PARAMETERS
    ----------
    webhook_url : str
        string of the webhook URL

    content_path : str
        string path of image to publish to the specified webhook URL

    RETURNS
    -------
    response : Response
        a requests Response object
    """

    webhook = DiscordWebhook(url=webhook_url)
    filename = Path(content_path).name

    with open(content_path, "rb") as img:
        webhook.add_file(file=img.read(), filename=filename)

    embed = DiscordEmbed(url=webhook_url, title="A new H2H board has been generated!")
    embed.set_image(url=f"attachment://{filename}")
    webhook.add_embed(embed)
    response = webhook.execute()

    return response
