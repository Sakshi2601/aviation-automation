import os
from process_data import load_and_process_data
from generate_report import generate_pdf
from send_email import send_report_via_gmail


def run_pipeline(csv_path=None, out_pdf=None, email_cfg=None):
    # load & process
    summary, df = load_and_process_data(csv_path)

    # generate report
    pdf_path = generate_pdf(summary, dataframe=df, out_path=out_pdf)
    print("Report written to:", pdf_path)

    # send email if config provided
    if email_cfg:
        sender = email_cfg.get("sender")
        recipient = email_cfg.get("recipient")
        subject = email_cfg.get("subject", "Automated Flight Report")
        body = email_cfg.get("body", "Attached is the automated flight report.")
        creds_path = email_cfg.get("credentials_path")
        res = send_report_via_gmail(sender, recipient, subject, body, pdf_path, credentials_path=creds_path)
        print("Email sent:", res)

    return summary, pdf_path


if __name__ == "__main__":
    base = os.path.dirname(__file__)
    default_csv = os.path.join(base, "data", "input.csv")
    # fallback if file named flights.csv was provided
    fallback_csv = os.path.join(base, "data", "flights.csv")
    csv_to_use = default_csv if os.path.exists(default_csv) else (fallback_csv if os.path.exists(fallback_csv) else None)

    # Example: if you want to test send, populate email_cfg accordingly
    email_cfg = None

    run_pipeline(csv_to_use, out_pdf=os.path.join(base, "reports", "output_report.pdf"), email_cfg=email_cfg)