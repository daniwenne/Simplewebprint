#http://nagyak.eastron.hu/doc/system-config-printer-libs-1.2.4/pycups-1.9.51/html/
import web
import os
import cups
urls = ('/', 'Upload',\
'/concluido', 'Concluido')

class Upload:
    def GET(self):
        return """<html><head><meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Serviço de Impressão</title>
      <style type = "text/css">
         .myclass {
            background-color: #aaa;
            padding: 10px;
         }
      </style>
   </head>

   <body>
      <p class = "myclass">Enviar Trabalho de Impressão</p>
   </body>
<p style="margin:10px">Selecione aqui um arquivo para impressão. Formatos aceitos: pdf, docx, doc, odt, jpeg e png.</p>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" style="margin:10px" name="myfile" accept=".pdf,.docx,.doc,.odt,.jpg,.png" "/>
<br/>
<input type="submit" style="margin:10px" value="Enviar"/>
</form>
</body>
</html>"""

    def POST(self):
        pdfpath='/tmp/tmpprintfile.pdf'
        x = web.input(myfile={})
        filename=x['myfile'].filename
        filetype=filename.split('.')[-1]
        filepath='/tmp/tmpprintfile.'+filetype
        if os.path.exists(filepath):
            os.system('rm "'+filepath+'"')
        fout = open(filepath,'wb')
        fout.write(x['myfile'].file.read())
        fout.close()
        if filetype!='pdf':
            if os.path.exists(pdfpath):
                os.system('rm "'+pdfpath+'"')
            os.system('libreoffice --headless --convert-to pdf "{}" --outdir /tmp/'.format(filepath))
            os.system('rm "'+filepath+'"')
        conn = cups.Connection()
        conn.printFile(conn.getDefault(),'/tmp/tmpprintfile.pdf',filename, {})
        os.system('rm "'+pdfpath+'"')
        raise web.seeother('/concluido')

class Concluido:
    def GET(self):
        return """<html><head><meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Serviço de Impressão</title>
      <style type = "text/css">
         .myclass {
            background-color: #aaa;
            padding: 10px;
         }
      </style>
   </head>

   <body>
      <p class = "myclass">Enviar Trabalho de Impressão</p>
   </body>
<p style="margin:5px">Trabalho de impressão enviado com sucesso</p>
<a style="margin:5px" href="/">Enviar outro trabalho</a>
</html>"""
if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
