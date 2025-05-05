from fpdf import FPDF

def generate_pdf_statement(account_number: str) -> str:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Statement for {account_number}", ln=True)
    pdf.cell(200, 10, txt="[Mock Transactions List]", ln=True)
    filename = f"statement_{account_number}.pdf"
    pdf.output(filename)
    return filename