import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def fetch_scp_page(scp_number):
    scp_id = f'scp-{scp_number:03d}'
    url = f'https://scp-wiki.wikidot.com/{scp_id}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch {scp_id}")
        return None, None, None

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', {'id': 'page-content'})

    if not content_div:
        print(f"No content found for {scp_id}")
        return None, None, None

    # Extract title
    title_tag = soup.find('div', {'id': 'page-title'})
    title = title_tag.text.strip() if title_tag else scp_id.upper()

    # Extract object class if mentioned
    raw_text = content_div.get_text().lower()
    object_class = "Unknown"
    for line in raw_text.splitlines():
        if "object class" in line:
            object_class = line.split(":")[-1].strip().capitalize()
            break

    return scp_id.upper(), object_class, md(str(content_div))

def save_to_markdown(scp_id, object_class, markdown_content):
    # Create the vault folder
    os.makedirs("scp-vault", exist_ok=True)
    file_path = os.path.join("scp-vault", f"{scp_id}.md")

    markdown_output = f"""# {scp_id}

**Object Class:** {object_class}

---

{markdown_content}

---

[Source](https://scp-wiki.wikidot.com/{scp_id.lower()})
"""

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(markdown_output)

    print(f"Saved: {file_path}")

# Run the prototype for SCP-001
scp_id, object_class, markdown_content = fetch_scp_page(1)

if markdown_content:
    save_to_markdown(scp_id, object_class, markdown_content)
