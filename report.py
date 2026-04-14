from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import numpy as np

def generate_report(reps, angles):
    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    avg_angle = np.mean(angles) if angles else 0
    max_angle = np.max(angles) if angles else 0
    min_angle = np.min(angles) if angles else 0

   
    if reps > 15:
        score = 9
        feedback = "Excellent Performance"
    elif reps > 8:
        score = 7
        feedback = "Good Performance"
    else:
        score = 5
        feedback = "Needs Improvement"

    content.append(Paragraph("Sports Performance Report", styles['Title']))
    content.append(Paragraph(f"Total Reps: {reps}", styles['Normal']))
    content.append(Paragraph(f"Average Angle: {avg_angle:.2f}", styles['Normal']))
    content.append(Paragraph(f"Max Angle: {max_angle:.2f}", styles['Normal']))
    content.append(Paragraph(f"Min Angle: {min_angle:.2f}", styles['Normal']))
    content.append(Paragraph(f"Performance Score: {score}/10", styles['Normal']))
    content.append(Paragraph(f"Feedback: {feedback}", styles['Normal']))

    doc.build(content)