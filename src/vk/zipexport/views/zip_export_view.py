# -*- coding: utf-8 -*-

# from vk.zipexport import _
from io import BytesIO
from pathlib import Path
from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from plone import api
from vk.zipexport.interfaces import IExportAdapter
import zipfile


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IZipExportView(Interface):
    """Marker Interface for IExtendedZipExportView"""


@implementer(IZipExportView)
class ZipExportView(BrowserView):

    def export_content_as_zip(self, meta = True):

        # Erhalte das aktuelle Verzeichnis
        current_folder = self.context
        self.start_path = Path(current_folder.absolute_url_path()).parent

        # Erstelle eine Zip-Datei und füge die Inhalte des Verzeichnisses hinzu
        zip_filename = f"{current_folder.id}.zip"
        zip_buffer = BytesIO()

        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            self._add_folder_to_zip(current_folder, zip_file, meta = meta)

        # Sende die generierte Zip-Datei an den Benutzer
        self.request.response.setHeader("Content-Type", "application/zip")
        self.request.response.setHeader(
            "Content-Disposition", f'attachment; filename="{zip_filename}"'
        )
        zip_buffer.seek(0)
        self.request.response.write(zip_buffer.read())

    def _add_folder_to_zip(self, folder, zip_file, meta = True):
        # Füge den aktuellen Ordner dem Zipfile hinzu
        folder_path = Path(folder.absolute_url_path())
        relative_path = folder_path.relative_to(self.start_path)
        zip_file.writestr(str(relative_path) + "/", "")

        # Füge die Inhalte des Ordners dem Zipfile hinzu
        for obj in folder.contentValues():

            #print(obj.id)
            # Hole den zu zippenden Content für den Inhaltstyp (Liste aus Dicts mit filename / content)
            content_for_zip = IExportAdapter(obj).get_content_for_zip(meta)

            # Schreibe den Content in die Zipdatei
            for element in content_for_zip:
                # date_time is six field tuple (1980, 1, 1, 0, 0, 0) of int
                date_time = tuple(map(int,element['timestamp'].parts()[:6]))
                filename = f'{relative_path}/{element["filename"]}'

#                if filename in (zip_file.namelist()):
#                    print("file is already in zip")

                info = zipfile.ZipInfo(filename=filename, date_time = date_time)
                zip_file.writestr(info, element["content"])

            if obj.isPrincipiaFolderish:
                # Wenn es sich um ein Verzeichnis handelt, rufe die Funktion rekursiv auf
                self._add_folder_to_zip(obj, zip_file, meta)




    def __call__(self):

        self.submitted = False
        form = self.request.form

        if "Submit" in form:
            self.submitted = True
            self.modus = form["modus"]
            if self.modus == "content": # export only content
                self.export_content_as_zip(meta = False)
            else: # export with metadata
                self.export_content_as_zip(meta = True)

        else:
            return self.index()

