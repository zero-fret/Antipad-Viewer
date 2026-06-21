# 💧 Antipad Viewer - CV Analysis Software
Analyze **resumes**, flag potentially **inflated** or **suspicious** experiences, generate technical interview questions and output HTML reports. 
- Designed for admission officers and HR managers
- **Enhance but DOES NOT REPLACE technical interview**

## Core Features:
- Extract text from PDF/DOCX/TXT files
- Call LLM to analyze each experience according to rules in prompt.txt
- Mark experiences as: ✅ Substantive / 💧 Watered-Down / 🚩 Suspicious with analysis
- Output confidence score (0–1)
- Generate clean, table-based HTML reports

### Known Limitations:
- Does NOT verify facts (e.g., grades, whether papers are actually published)
- Does NOT support scanned image-based PDFs (no OCR)
- Relies on strict LLM output formatting; parsing may fail if format is incorrect
- Confidence score is the model's subjective judgment, not a hard admission prediction

### Output Example:
```
0.05_Alan Water.html -- inflated CV with fabricated claims
0.05_Edward Van Halen.html -- absurdity test, guitarist applying to CS  
0.75_Spidey (Yichi Zhang).html -- real candidate's CV. https://github.com/spidey-zyc
0.85_Zero Fret.html -- real candidate's CV. https://github.com/zero-fret/
```

## Manual
### Dependencies:
- Python 3.8+
- openai
- python-docx
- pymupdf

### Installation:
pip install openai python-docx pymupdf

### Configuration:
1. Place prompt.txt in the same directory as main.py
2. Set environment variable API_KEY, or replace it inside main.py
3. Optional: Modify MODEL / BASE_URL / THINKING_ENABLED

### Quick Start (single resume):
python -c "from main import process_cv; process_cv('resume.pdf')"

### Batch processing:
Place resumes into ./RESUME/ directory, then run:
python main.py

### Output:
./RESUME_ANTIPAD/<confidence>_<name>.html

License:
GPL v3.0

Contact / Issues:
GitHub Issues or email zerofret0@outlook.com
