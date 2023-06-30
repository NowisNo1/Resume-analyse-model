import comtypes.client
from docx2pdf import convert

def cvt2pdf(path, fmt, output_path):
    global app, doc
    try:
        if fmt == 'doc':
            app = comtypes.client.CreateObject('Word.Application')
            doc = app.Documents.Open(path)
            doc.SaveAs(output_path, FileFormat=17)
            doc.Close()
            app.Quit()
            return output_path
        elif fmt == 'ppt':
            app = comtypes.client.CreateObject('PowerPoint.Application')
            doc = app.Presentations.Open(path)
            doc.SaveAs(output_path, FileFormat=32)
            doc.Close()
            app.Quit()
            return output_path
        else:
            return ''
    except BaseException as e:
        doc.Close()
        app.Quit()
        print(e)
        return ''


