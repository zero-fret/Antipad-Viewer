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
Python, C++, PyTorch, Ultralytics YOLO, LLM API Application Development, Data Synthesis & Augmentation
## CS Projects
### Antipad Viewer – Resume Anti-Inflation Analysis System | Independent Project
To address the time-consuming and inconsistent nature of manual resume screening by admissions officers, developed an automated analysis pipeline based on Deepseek LLM: inputs a resume, outputs a structured report with per-item annotations ("substantive/inflated") and explainable justifications.
Through highly constrained prompt design ("presumption of water" principle + chain-of-work template) and JSON output optimization, achieved <4% inconsistency rate on mixed resume tests (>30% without thinking mode); cost per analysis ≈ $0.01.
Reduced manual screening time from 10 minutes to 30 seconds per resume (only requiring final confidence score and item summaries to review). Prompt compressed from 2000 tokens to 500 tokens with no performance loss.
### Computer Vision System for Aircraft Competition 
To address the difficulty of collecting real aerial data and high annotation costs, designed an automated data synthesis pipeline: pasting rotated/scaled targets onto open-source images, automatically generating YOLO-format OBB annotations, reducing marginal annotation cost per image to almost zero.
Implemented 8 data augmentation strategies (brightness perturbation, Gaussian blur, rotation-cutting to simulate occlusion, etc.) to simulate real interference and improve model generalization. Among these, false_target() chops up and rotates real targets to generate unlabeled distractors, forcing the model to learn "complete geometric structure" rather than "texture features," improving confidence and suppressing false positives.
Trained on YOLOv11n-OBB; achieved perfect detection (confidence >0.7) on real competition footage (16 targets × 200 frames). Under heavy data augmentation, mAP50 reached 0.95; model convergence speed improved 2x compared to training on manually annotated datasets (epochs to reach mAP50=0.8 reduced from 20 to 8).
### NoobTorch
Designed and built an introductory PyTorch deep learning course for beginners (NoobTorch). Through a series of hands-on tutorials progressing from basics to advanced topics (from MNIST handwritten digit recognition to YOLO object detection), it helps novices systematically master the PyTorch framework and classic models. The project demonstrates clear instructional design capabilities and solid code engineering skills.
## Other Projects (Brief)
### KiHCA Harmonic Calculator :
Developed a GUI software for KiCad/Ngspice to calculate harmonic components and THD using least squares, reducing simulation cycles and saving 70% simulation time. Already used in an actual HiFi amplifier project.
### Resistor Value Matching Tool :
Developed a cross-platform GUI application supporting E24/E96 series, achieving millisecond-level multi-target optimal resistance matching and error calculation.

