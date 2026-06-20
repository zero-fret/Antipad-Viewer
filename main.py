# ---- Antipad Viewer ----
import os, re, json
from pathlib import Path
from openai import OpenAI
from jinja2 import Template

# ------------------------- USER CONFIG -------------------------
API_KEY = os.environ.get("API_KEY", "key")
BASE_URL =  "https://api.deepseek.com"
# BASE_URL ="http://localhost:8000/v1"
MODEL = "deepseek-v4-flash"
THINKING_ENABLED = True
REASONING_EFFORT = "high"
TEMPERATURE = 0.1
BATCH_INPUT_DIR = "RESUME"
BATCH_OUTPUT_DIR = "RESUME_ANTIPAD"
SYSTEM_PROMPT_FILE = "prompt.txt"
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
    
    # Base params - remove temperature when thinking is enabled
    params = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        "stream": False,
    }
    
    if THINKING_ENABLED:
        # According to DeepSeek docs:
        # 1. Don't set temperature (not supported in thinking mode)
        # 2. Use reasoning_effort to control intensity ("high" or "max")
        # 3. Use nested thinking parameter in extra_body
        params["reasoning_effort"] = "high"  # NOT "low" - low/map get mapped to high anyway
        params["extra_body"] = {"thinking": {"type": "enabled"}}
        # Remove temperature since it's ignored in thinking mode
    else:
        params["temperature"] = TEMPERATURE
    
    resp = client.chat.completions.create(**params)
    # Extract reasoning_content if present (some DeepSeek models use this field)
    reasoning = None
    if hasattr(resp.choices[0].message, "reasoning_content"):
        reasoning = resp.choices[0].message.reasoning_content
        print(f"Reasoning content found: {len(reasoning)} chars")
    
    # Parse the main content: it contains a plain text thinking block followed by JSON
    content = resp.choices[0].message.content
    # The thinking block is everything before the first '{' that starts a JSON object
    thinking = ""
    json_part = content
    # Look for the start of a JSON object
    first_brace = content.find('{')
    if first_brace != -1:
        thinking = content[:first_brace].strip()
        json_part = content[first_brace:]
    else:
        # If no JSON object found, use entire content as thinking and raise error
        thinking = content
        raise ValueError("Model output did not contain valid JSON after thinking block")
    
    # Parse JSON
    try:
        data = json.loads(json_part)
    except json.JSONDecodeError as e:
        # Try to extract just the JSON part more strictly
        json_match = re.search(r'\{.*\}', json_part, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse JSON: {e}\nRaw content: {content}")
        else:
            raise ValueError(f"Failed to parse JSON: {e}\nRaw content: {content}")
    
    # If reasoning_content was provided by the API, add it to the thinking output
    if reasoning:
        thinking = f"// API reasoning_content //\n{reasoning}\n\n// User-visible thinking //\n{thinking}"
    
    return data, thinking

def build_html(data: dict, thinking_comment: str) -> str:
    """
    Render HTML report. Insert thinking_comment as an HTML comment at the very top.
    """
    # Remove any old reasoningLog from data (if present due to legacy)
    data.pop("reasoningLog", None)
    # Add the thinking comment to data so template can insert it if desired
    data["thinkingComment"] = thinking_comment
    template = Template(HTML_TEMPLATE)
    return template.render(**data)

def process_cv(input_file: str, output_file: str = None):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Not found: {input_file}")
    print(f"Extracting: {input_file}")
    text = extract_text(input_file)
    print(f"Calling {MODEL}...")
    data, thinking = call_model(text)
    name = data.get("basicInfo", {}).get("name", "Unknown")
    confidence = data.get("verdict", {}).get("confidence", 0.5)
    print(f"Name: {name}, Confidence: {confidence:.2f}")
    # Build HTML 
    html = build_html(data, thinking)
    # Wrap thinking block in HTML comment at the very beginning
    html_comment = f"<!--\nTHINKING BLOCK (auto-inserted by main.py):\n{thinking}\n-->\n"
    html = html_comment + html

    if output_file is None:
        output_file = str(Path(input_file).parent / f"{Path(input_file).stem}_annotated.html")
    Path(output_file).write_text(html, encoding="utf-8")
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
