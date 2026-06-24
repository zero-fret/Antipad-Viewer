# Name: Zero Fret
Phone: Unknown | Email: zerofret0@outlook.com | Location: Unknown
## Education
Anonymous Institution of Computer Science (AICS) | Computer Science
## Core Courses: 
C++ Programming 92.5 | Data Structures 92 | TOEFL 107  

## GitHub 
https://github.com/zero-fret/
## Applying to:
Computer Science
## Technical Stack
Python, C++, PyTorch, Ultralytics YOLO, LLM API Application Development, Data Synthesis & Augmentation, Prompt engineering
## CS Projects
### Antipad Viewer – Resume Screening Tool | Personal Project
Created a Python LLM API tool that uses Deepseek to evaluate resumes and label watered-down claims based on a predefined set of criteria. The tool sends resume text to the API, receives a structured assessment, and generates an HTML report with labels (💧/🚩/✅). Tested on 25 resume examples (5 real and 20 synthetic). Tool's evaluations match human judgment.  
Cost：~$0.01/resume  
Open-sourced：https://github.com/zero-fret/Antipad-Viewer/

### Computer Vision System for Aircraft Competition (Detect rotating targets and numbers written on them)
For rotating targets: Built a Python pipline to generate synthetic training data for aircraft-based OBB detection task. Pastes rotated and scaled target images onto background scenes and automatically creates oriented bounding box labels. Implemented 8 data augmentation techniques, including a function that cuts and rotates real targets to serve as texture-correct-logic-wrong hard false negatives. Trained a YOLOv11n-OBB model on synthetic data and achieved 0 FP & >70% confidence on real on 200 FPS of competition footage. Model converges 2x faster than real data without augmentation. For this task, sacrafice partially blocked real target for nearly no false positive  
For numbers: YOLO11n-CLS with 100 classes (00-99), trained on synthetic data
The system detects the target with YOLO11n-OBB, then reads the number with YOLO11n-CLS (used as OCR).  
Open sourced: https://github.com/zero-fret/YOLO_OBB_Data_Synthesizer
### NoobTorch
Created a set of tutorials for learning PyTorch and deep learning, with a roadmap from basic MNIST classification to YOLO object detection. The materials are designed for beginners and aim to explain complex topics in simple language.  
open sourced: https://github.com/zero-fret/NoobTorch
## Other Projects (Brief)
### KiHCA Harmonic Calculator :
Developed a GUI software for KiCad/Ngspice to calculate harmonic components and THD using least squares, reducing simulation cycles and saving 70% simulation time compared to KiCad's built in FFT. Already used in an actual HiFi amplifier project.
open sourced: https://github.com/zero-fret/KiHCA-Harmonic-Analyzer-for-SPICE-Simulation  
### Resistor Value Matching Tool :
Built a Python GUI application that suggests standard resistor combinations (series, parallel or single resistor) to approximate a desired non-standard resistance value, supporting E24 and E96 resistor series.  
Open sourced: https://github.com/zero-fret/Resistor-Value-Matcher  

