.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.


============
vk.zipexport
============

A Plone add-on with which users can export content as a zip file

Features
--------

This add-on adds an "Export as zip"-Action to folderish content types. Each object in the folder will be saved in the zip file.
Metadata is saved in a text file for each content item (suffix .meta). File and Image objects are saved as files.



This add-on is meant for end users which want to archive their content, for example before deleting or restructuring content.
It is not possible to import the exported content.

Missing features

- Workflow states are currently not saved as metata.
- Links, Events and Collections are currently not exported

Usage
--------

Klick on  "Export as zip"-Action to generate and download a zip file


Translations
------------

TODO


Installation
------------


TODO: put on PyPI or in collective

(((

Install vk.zipexport by adding it to your buildout::

    [buildout]

    ...

    eggs =
        vk.zipexport


and then running ``bin/buildout``

)))

Authors
-------

Provided by awesome people ;)


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/verena-km/vk.zipexport/issues
- Source Code: https://github.com/verena-km/vk.zipexport


Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
-------

The project is licensed under the GPLv2.
