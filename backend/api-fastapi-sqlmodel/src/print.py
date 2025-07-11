from weasyprint import HTML

def printTable(title, heading, text, header, data):
    html = f'<!DOCTYPE html>\n<html>\n<head>\n<title>{title}</title>\n</head>\n<body>\n'
    html += f'<h1>{heading}</h1>'
    html += f'<p>{text}</p>'
    html += "<table border='1'>\n"
    html += "<tr>\n"
    for item in header:
        html += f"<th>{item}</th>\n"
    html += "</tr>\n"

    for row in data:
        html += "<tr>\n"
        for item in row:
            html += f"<td>{item}</td>\n"
        html += "</tr>\n"

    html += "</table>\n</body>\n</html>"
    htmldoc = HTML(string=html, base_url="")
    return htmldoc.write_pdf()
