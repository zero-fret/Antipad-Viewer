# ---- Antipad Viewer ----
import os, re, json, html
from pathlib import Path
from openai import OpenAI
from jinja2 import Template
from markupsafe import Markup

# ------------------------- USER CONFIG -------------------------
# Read API key from key.txt file
key_file = Path(__file__).parent / "key.txt"
if key_file.exists():
    API_KEY = key_file.read_text(encoding="utf-8").strip()
else:
    API_KEY = os.environ.get("API_KEY", "")  # fallback to environment variable

BASE_URL = "https://api.deepseek.com"
# BASE_URL = "http://localhost:8000/v1"
MODEL = "deepseek-v4-flash"
THINKING_ENABLED = True
REASONING_EFFORT = "high"
TEMPERATURE = 0.1
BATCH_INPUT_DIR = "INPUT"
BATCH_OUTPUT_DIR = "OUTPUT"
SYSTEM_PROMPT_FILE = "prompt.md"
# ----------------------------------------------------------------

script_dir = Path(__file__).parent
SYSTEM_PROMPT = (script_dir / SYSTEM_PROMPT_FILE).read_text(encoding="utf-8")
HTML_TEMPLATE = (script_dir / "template.html").read_text(encoding="utf-8")

def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        import fitz
        doc = fitz.open(file_path)
        t = '\n'.join(page.get_text() for page in doc)
        doc.close()
        return t
    elif ext == '.docx':
        from docx import Document
        return '\n'.join(p.text for p in Document(file_path).paragraphs)
    elif ext in ('.txt', '.md'):
        return Path(file_path).read_text(encoding='utf-8')
    else:
        raise ValueError(f'Unsupported format: {ext}')

def call_model(text: str):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    user_msg = f"Resume text:\n\n{text}\n\nIMPORTANT: output exactly as instructed."

    params = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "stream": False,
    }

    if THINKING_ENABLED:
        params["reasoning_effort"] = "high"
        params["extra_body"] = {"thinking": {"type": "enabled"}}
    else:
        params["temperature"] = TEMPERATURE

    resp = client.chat.completions.create(**params)

    # The new prompt outputs only JSON (with a "reasoning" field inside)
    content = resp.choices[0].message.content

    # Try to parse the entire response as JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        # Fallback: extract anything that looks like a JSON object
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse JSON: {e}\nRaw content: {content}")
        else:
            raise ValueError(f"Failed to parse JSON: {e}\nRaw content: {content}")

    # Ensure the reasoning field exists (some models may not return it)
    if "reasoning" not in data:
        data["reasoning"] = "No reasoning provided by the model."

    return data

def build_html(data: dict) -> str:
    """
    Render HTML report. Process originalText fields to replace <💧...>, <🚩...>, and <🔘...>
    with highlighted spans. Also inject the reasoning as an HTML comment.
    """
    # Remove any leftover "reasoningLog" if present (old version)
    data.pop("reasoningLog", None)

    # Process each experience's original text to highlight markers
    for exp in data.get('experiences', []):
        if 'originalText' in exp:
            raw = exp['originalText']
            result_parts = []
            last_pos = 0
            # Match any of the three markers: 💧 🚩 🔘
            pattern = r'(&lt;|<)([💧🚩🔘])(.*?)(&gt;|>)'

            for match in re.finditer(pattern, raw):
                result_parts.append(html.escape(raw[last_pos:match.start()]))
                marker = match.group(2)  # 💧 🚩 🔘
                content = match.group(3)
                if marker == '💧':
                    result_parts.append(f'<span style="background-color: #b3d9ff;">{html.escape(content)}</span>')
                elif marker == '🚩':
                    result_parts.append(f'<span style="background-color: #ffb3b3;">{html.escape(content)}</span>')
                elif marker == '🔘':
                    result_parts.append(f'<span style="background-color: #d3d3d3;">{html.escape(content)}</span>')
                last_pos = match.end()
            result_parts.append(html.escape(raw[last_pos:]))
            exp['originalText'] = Markup(''.join(result_parts))

    # Get reasoning for comment injection
    reasoning = data.get("reasoning", "")

    # Render the template with all data including reasoning
    template = Template(HTML_TEMPLATE)
    html_content = template.render(**data)

    # Prepend reasoning as HTML comment at the very top
    comment = f"<!--\nREASONING:\n{reasoning}\n-->\n"
    return comment + html_content

def process_cv(input_file: str, output_file: str = None):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Not found: {input_file}")
    print(f"Extracting: {input_file}")
    text = extract_text(input_file)
    print(f"Calling {MODEL}...")
    data = call_model(text)
    name = data.get("basicInfo", {}).get("name", "Unknown")
    confidence = data.get("verdict", {}).get("confidence", 0.5)
    print(f"Name: {name}, Confidence: {confidence:.2f}")

    html_content = build_html(data)

    if output_file is None:
        output_file = str(Path(input_file).parent / f"{Path(input_file).stem}_annotated.html")
    Path(output_file).write_text(html_content, encoding="utf-8")
    print(f"Saved: {output_file}")
    return output_file, name, confidence

def batch_process():
    input_dir = script_dir / BATCH_INPUT_DIR
    output_dir = script_dir / BATCH_OUTPUT_DIR
    if not input_dir.exists():
        print(f"Input folder not found: {input_dir}")
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    files = [f for f in input_dir.iterdir() if f.suffix.lower() in {'.pdf','.docx','.txt','.md'}]
    if not files:
        print("No supported files found.")
        return
    print(f"Processing {len(files)} file(s)...")
    for fp in files:
        try:
            tmp = output_dir / f"_tmp_{fp.stem}.html"
            _, name, conf = process_cv(str(fp), str(tmp))
            safe = re.sub(r'[\\/*?:"<>|]', '', name).strip()
            final = output_dir / f"{conf:.2f}_{safe}.html"
            if final.exists():
                final = output_dir / f"{conf:.2f}_{safe}_1.html"
            os.rename(tmp, final)
            print(f"  -> {final.name}")
        except Exception as e:
            print(f"Error on {fp.name}: {e}")

if __name__ == "__main__":
    batch_process()