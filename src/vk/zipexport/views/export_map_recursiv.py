from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.interfaces import IContentish
import shutil
import os

export_basedir = "c:\\map\\export"
export_file = os.path.join(export_basedir,"export_data.txt")
file_basedir = "c:\\map\\export\\files"
i = 1
types_to_export = ["Folder", "Image", "File", "Page", "News Item", "Link",
                    "PMFolder", "PM", "Wiki Ordner", "Wiki-Artikel"]


# Aufteilung in mehrere Teile wg. MemoryError
def export_part1(self):
    pathlist = [
    'Plone/info/pruefung',
    'Plone/info/rechtsgrundlagen'
    ]
    export_part(self,pathlist)
    print "Export beendet"

def export_part2(self):
    pathlist = [
    'Plone/info/organisation'
    ]
    export_part(self,pathlist)
    print "Export beendet"

def export_part3(self):
    pathlist = [
    'Plone/info/finanzkontrolle-vor-ort',
    'Plone/info/medien'
    ]
    export_part(self,pathlist)
    print "Export beendet"

def export_part4(self):
    pathlist = [
    'Plone/info/interessenvertretung',
    'Plone/info/hilfe',
    'Plone/info/linksammlung'
    ]
    export_part(self,pathlist)
    print "Export beendet"

def export_part5(self):
    pathlist = [
    'Plone/info/projekgruppe-intranet',
    'Plone/info/prufungsbilanz',
    'Plone/info/ergebnisbericht',
    'Plone/info/ag-controlling',
    'Plone/info/fink-redaktion',
    'Plone/info/gesundheitsvorsorge',
    'Plone/info/hpr',
    'Plone/info/oepr-rh',
    'Plone/info/vorstand-vereinigung',
    'Plone/info/pg-design',
    'Plone/info/rh-fis',
    'Plone/bilderpool',
    'Plone/finko-wiki',
    ]
    export_part(self,pathlist)
    print "Export beendet"


# Aufteilung wg. MemoryError
def export_part(self,pathlist):
    portal_url = getToolByName(self, "portal_url")
    portal = portal_url.getPortalObject()

    # mit welcher Nummer geht es weiter
    global i
    i = getNextNumberFromExportFile()

    # Oeffne Exportdatei
    global target
    target = open(export_file,'a')

    for path in pathlist:
        element = portal.restrictedTraverse(path)
        export_branch(element)

    target.close()
    print "Export beendet"


def export_branch(element):
    if element.Type() in types_to_export:
        global i
        print i
        print element.Title()
        print element.Type()
        export_content(element, i)
        i = i + 1
        # alle Kindelemente ermitteln
        if IFolderish.providedBy(element):
            for id, child in element.contentItems():
                export_branch(child)

def export_content(element,i):
    data_dict = getMetadata(element)
    # lfd Nummer hinzufuegen
    data_dict.update({'nr': i})
    # typspezifische Inhalte hinzufuegen
    # und ggf. Datei ablegen
    data_dict.update(getTypeSpecificData(element ,i))
    # Datensatz in in Datei schreiben
    global target
    target.write(str(data_dict)+"\n")



# Hilfsmethode zum Ermitteln der Metadaten
# return a dictionary with metadata for content object
def getMetadata(obj):
    workflowTool = getToolByName(obj, 'portal_workflow')

    # eine Liste der Workflow-Objekte
    # print workflowTool.getWorkflowsFor(object)

    # ein Tuple mit Workflow-Namen
    chain = workflowTool.getChainFor(obj)
    #print chain
    #print type(chain)

    review_history = []
    wfid = ""
    # folgendes geht nur wenn ein workflow zugeordnet ist
    if chain != ():
        wfid = chain[0]
        # print history
        if wfid != "finko_geschlossen":
            review_history = workflowTool.getInfoFor(obj, 'review_history')
        #print review_history
        # print status
        #print  workflowTool.getStatusOf(chain[0], object)
    metadata = {
                   'id': obj.getId(),
                   'title': obj.Title(),
                   'description': obj.Description(),
                   'type': obj.Type(),
                   'path': obj.absolute_url_path(),
                   'creator': obj.Creator(),
                   'created': str(obj.created()),
                   'modified': str(obj.modified()),
                   'expirationDate': str(obj.getExpirationDate()),
                   'effectiveDate': str(obj.getEffectiveDate()),
                   'contributors': obj.Contributors(),
                   'creators': obj.Creators(),
                   'subject': obj.Subject(),
                   'local_roles': obj.get_local_roles(),
                   #'uuid': IUUID(object,None),
                   'wfid': wfid,
                   'review_history': str(review_history),
                   'excludeFromNav': obj.getExcludeFromNav(),
                   'owner_tuple': obj.getOwnerTuple()
               }
    return metadata

# Hilfsmethode fuer die Datenfelder der einzelnen Datantypen
def getTypeSpecificData(obj,nr):
    elementtype = obj.Type()
    print elementtype
    data_dict = {}
    if elementtype == "Folder":
        data_dict = getFolderData(obj)
    if elementtype == "Image":
        data_dict = getImageData(obj,nr)
    if elementtype == "File":
        data_dict = getFileData(obj,nr)
    if elementtype == "Page":
        data_dict = getPageData(obj)
    if elementtype == "News Item":
        data_dict = getNewsData(obj,nr)
    if elementtype == "Link":
        data_dict = getLinkData(obj)
    if elementtype == "PM":
        data_dict = getPMData(obj,nr)
    if elementtype == "Wiki-Artikel":
            data_dict = getWikiPageData(obj)
    return data_dict

def getFolderData(obj):
    # falls es eine placeful workflow-richtlinie gibt, diese speichern

    placefulWorkflowTool = getToolByName(obj, "portal_placeful_workflow")
    config = placefulWorkflowTool.getWorkflowPolicyConfig(obj)
    policyBelowId = ""
    policyInId = ""
    if config:
      policyBelowId = config.getPolicyBelowId()
      policyInId = config.getPolicyInId()

    # Darstellung des Ordners
    layout = obj.getLayout()

    # Artikel aus dem Ordner
    defaultpage = obj.getDefaultPage()


    data_dict = {
        'policyBelowId':  policyBelowId,
        'policyInId': policyInId,
        'layout': layout,
        'defaultpage': defaultpage,
    }

    return data_dict

def getImageData(obj,nr):
    # Dictionary mit Metadaten anlegen
    data_dict = {
             'nr': nr,
             'filename': obj.getFilename(),
             }
    # Datei speichern
    imagedata = obj.getImage()
    createFile( filename ="file_"+str(nr), data = str(imagedata.data))
    return data_dict

def getFileData(obj,nr):
    # Dictionary mit Metadaten anlegen
    data_dict =  {
             'nr': nr,
             'filename': obj.getFilename(),
             }
    # Datei speichern
    attachment = obj.getFile()
    createFile( filename ="file_"+str(nr), data = str(attachment.data))
    return data_dict


def getPageData(obj):
    # Dictionary mit Metadaten anlegen
    data_dict = {
             'text': obj.getText(),
             'rawtext': obj.getRawText(),
             }
    return data_dict

def getNewsData(obj,nr):
    # Dictionary mit Metadaten anlegen
    data_dict = {
             'nr': nr,
             'text': obj.getText(),
             'rawtext': obj.getRawText(),
             'imageCaption': obj.getImageCaption()
             }
    # Datei speichern
    image = obj.getImage()

    if type(image) is str:
          print image
    else:
        createFile( filename ="file_"+str(nr), data = str(image.data))
    return data_dict


def getLinkData(obj):
    # Dictionary mit Metadaten anlegen
    data_dict = {
             'remoteUrl': obj.getRemoteUrl()
             }
    return data_dict


def getPMData(obj,nr):
    # Dictionary mit Metadaten anlegen
    data_dict = {
             'nr': nr,
             'aktenzeichen': obj.getAktenzeichen(),
             'vertraulich': obj.getVertraulich(),
             'ansprechpartner': obj.getAnsprechpartner(),
             'pmDate': str(obj.getPmDate()),
             'filename': obj.getPmFile().filename
             }
    # Datei speichern
    pmfile = obj.getPmFile()

    if pmfile.filename:
        createFile( filename ="file_"+str(nr), data = str(pmfile))
    return data_dict


def getWikiPageData(obj):
    # Dictionary mit Metadaten anlegen
    data_dict = {
             'text': obj.getText(),
             'rawtext': obj.getRawText(),
             }
    return data_dict


# Hilfsmethode zum Erzeugen der Einzeldateien
def createFile(filename, data):
    if not os.path.exists(file_basedir):
      os.makedirs(file_basedir)
    destfilepath = os.path.join(file_basedir, filename)
    f = open(destfilepath,'wb')
    f.write(data)
    f.close()


# wenn bereits eine Exportdatei existiert, ermittle die Nummer der letzten Zeile
def getNextNumberFromExportFile():
    i = 1
    if os.path.isfile(export_file):
        # welche Nummer hat letzte Zeile
        target = open(export_file,'r')
        lastline = target.readlines()[-1]
        lastdict = eval(lastline)
        i = lastdict['nr']+1
        target.close()
        print "i"
    return i
