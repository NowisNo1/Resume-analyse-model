import comtypes.client
from docx2pdf import convert

app_doc = None
app_ppt = None
doc = None

def cvt2pdf(path, fmt, output_path):
    global app_doc, app_ppt, doc
    if app_doc is None:
        app_doc = comtypes.client.CreateObject('Word.Application')
    if app_ppt is not None:
        app_ppt = comtypes.client.CreateObject('PowerPoint.Application')
    try:
        if fmt == 'doc':
            # app = comtypes.client.CreateObject('Word.Application')
            doc = app_doc.Documents.Open(path)
            doc.SaveAs(output_path, FileFormat=17)
            doc.Close()
            # app.Quit()
            return output_path
        elif fmt == 'ppt':
            # app = comtypes.client.CreateObject('PowerPoint.Application')
            doc = app_ppt.Presentations.Open(path)
            doc.SaveAs(output_path, FileFormat=32)
            doc.Close()
            # app.Quit()
            return output_path
        else:
            return ''
    except BaseException as e:
        if app_doc is not None:
            app_doc.Quit()
        if app_ppt is not None:
            app_ppt.Quit()
        print(e)
        return ''


