from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas

from utils.calculations import completion_percentage


def weekly_report(disciplines, tasks) -> bytes:
    output = BytesIO()
    canvas = Canvas(output, pagesize=A4)
    width, height = A4
    y = height - 54
    canvas.setTitle("Relatorio semanal EduTrack AI")
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(48, y, "EduTrack AI - Relatorio semanal")
    y -= 30
    canvas.setFont("Helvetica", 11)
    pending = 0 if tasks.empty else int((~tasks["completed"].astype(bool)).sum())
    for line in (f"Disciplinas: {len(disciplines)}", f"Tarefas: {len(tasks)}", f"Pendentes: {pending}", f"Progresso: {completion_percentage(tasks):.1f}%"):
        canvas.drawString(48, y, line); y -= 18
    y -= 10
    canvas.setFont("Helvetica-Bold", 12); canvas.drawString(48, y, "Tarefas"); y -= 20
    canvas.setFont("Helvetica", 9)
    if tasks.empty:
        canvas.drawString(48, y, "Nenhuma tarefa disponivel.")
    else:
        for row in tasks.to_dict("records"):
            if y < 54:
                canvas.showPage(); y = height - 54; canvas.setFont("Helvetica", 9)
            status = "Concluida" if row.get("completed") else "Pendente"
            text = f"[{status}] {row.get('title', '')} - {row.get('discipline', 'Sem disciplina')}"
            canvas.drawString(48, y, text[:100]); y -= 15
    canvas.save()
    return output.getvalue()

