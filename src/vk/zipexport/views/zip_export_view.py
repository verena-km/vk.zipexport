# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
import zipfile
from pathlib import Path
from vk.zipexport.interfaces import IExportAdapter


class ZipExportView(BrowserView):
    def export_content_as_zip(self):

        # Erhalte das aktuelle Verzeichnis
        current_folder = self.context
        self.start_path = Path(current_folder.absolute_url_path()).parent

        # Erstelle eine Zip-Datei und füge die Inhalte des Verzeichnisses hinzu
        zip_filename = f'{current_folder.id}.zip'
        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            self._add_folder_to_zip(current_folder, zip_file)

        # Sende die generierte Zip-Datei an den Benutzer
        self.request.response.setHeader('Content-Type', 'application/zip')
        self.request.response.setHeader('Content-Disposition', f'attachment; filename="{zip_filename}"')
        with open(zip_filename, 'rb') as zip_file:
          self.request.response.write(zip_file.read())


    def _add_folder_to_zip(self, folder, zip_file):
          # Füge den aktuellen Ordner dem Zipfile hinzu
          folder_path = Path(folder.absolute_url_path())
          relative_path = folder_path.relative_to(self.start_path)
          zip_file.writestr(str(relative_path) +'/', '')

          # Füge die Inhalte des Ordners dem Zipfile hinzu
          for obj in folder.contentValues():

              # Hole den zu zippenden Content für den Inhaltstyp (Liste aus Dicts mit filename / content)
              content_for_zip = IExportAdapter(obj).get_content_for_zip()

              # Schreibe den Content in die Zipdatei
              for element in content_for_zip:
                  zip_file.writestr(f'{relative_path}/{element["filename"]}', element["content"])

              if obj.isPrincipiaFolderish:
                  # Wenn es sich um ein Verzeichnis handelt, rufe die Funktion rekursiv auf
                  self._add_folder_to_zip(obj, zip_file)

    def __call__(self):
      self.export_content_as_zip()




