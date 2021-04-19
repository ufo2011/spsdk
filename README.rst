.. doctree::

    docs/spsdk.rst
    examples/README.md
    spsdk/apps/README.md

============
i.Mx RT 1050
============

To run examples using i.MX RT 1050 you need to download a flashloader:
- Go to: `RT 1050 MCU Flashloader <https://www.nxp.com/webapp/sps/download/license.jsp?colCode=IMX-RT1050-FLASHLOADER>`_
- Review the license agreement, download and unzip the package
- Convert the elf file into bin (For this operation you need to have MCUXpresso IDE, IAR or Keil)
- Run 
  
.. code:: bash

    python tools\flashloader_converter.py --elf-path <path/to/flashloader.elf> --ide-type <mcux | iar | keil> --ide-path <path/to/IDE/install/folder

============
Dependencies
============

The core dependencies are included in `requirements.txt <requirements.txt>`_. 

The dependencies for the development and testing are included in `requirements-develop.txt <requirements-develop.txt>`_.
