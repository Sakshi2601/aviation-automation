import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(summary: dict, dataframe=None, out_path=None):
    """Generate a simple PDF report containing the summary and a small table.

    summary: dictionary returned by process_data.load_and_process_data
    dataframe: optional pandas DataFrame (will include first 20 rows in table)
    out_path: path to write PDF
    """
    base = os.path.dirname(__file__)
    if not out_path:
        out_path = os.path.join(base, "reports", "output_report.pdf")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    doc = SimpleDocTemplate(out_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Automated Flights Report", styles["Title"]))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("Summary", styles["Heading2"]))
    for k, v in summary.items():
        if k in ("top_origins", "top_carriers", "sample_rows"):
            # skip large structured fields for now
            continue
        story.append(Paragraph(f"<b>{k.replace('_', ' ').title()}:</b> {v}", styles["Normal"]))

    story.append(Spacer(1, 12))

    # add top origins and carriers if present
    if summary.get("top_origins"):
        story.append(Paragraph("Top Origins:", styles["Heading3"]))
        for origin, count in summary["top_origins"].items():
            story.append(Paragraph(f"{origin}: {count}", styles["Normal"]))

    if summary.get("top_carriers"):
        story.append(Paragraph("Top Carriers:", styles["Heading3"]))
        for carrier, count in summary["top_carriers"].items():
            story.append(Paragraph(f"{carrier}: {count}", styles["Normal"]))

    story.append(Spacer(1, 12))

    # Small table (first 20 rows)
    if dataframe is not None:
        story.append(Paragraph("Sample Flights", styles["Heading2"]))
        # limit columns to a handful
        cols = list(dataframe.columns[:6])
        rows = [cols]
        for idx, row in dataframe.head(20).iterrows():
            rows.append([str(row.get(c, "")) for c in cols])

        t = Table(rows, hAlign="LEFT")
        t.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ]))
        story.append(t)

    doc.build(story)
    return out_path


if __name__ == "__main__":
    # quick smoke test
    from process_data import load_and_process_data
    s, df = load_and_process_data()
    p = generate_pdf(s, df)
    print("Wrote:", p)