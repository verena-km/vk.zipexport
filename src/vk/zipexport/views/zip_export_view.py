# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
import zipfile
from pathlib import Path
import yaml
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
              fun = (IExportAdapter(obj).get_fun())
              #metadata = print(IExportAdapter(obj).get_metata())

              # Schreib Metadaten in eine yaml-Datei, die nach der id benannt ist.
              print(vars(obj))
              #metadata = yaml.dump(vars(obj))
              #zip_file.writestr(f'{relative_path}/{obj.id}.yml', metadata)
              zip_file.writestr(f'{relative_path}/{obj.id}.meta', fun)
              if obj.isPrincipiaFolderish:
                  # Wenn es sich um ein Verzeichnis handelt, rufe die Funktion rekursiv auf
                  self._add_folder_to_zip(obj, zip_file)
              else:
                  # Wenn es sich um eine Datei handelt, füge sie dem Zipfile hinzu

                  if obj.portal_type == "File":
                    filename = obj.file.filename
                    file_data = obj.file.data
                    zip_file.writestr(f'{relative_path}/{filename}', file_data)

    def __call__(self):
      self.export_content_as_zip()




