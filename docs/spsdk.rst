.. SPSDK links definition block

.. NXP Devices location

.. _LPC55S6x_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpc5500-cortex-m33/high-efficiency-arm-cortex-m33-based-microcontroller-family:LPC55S6x
.. _LPC55S2x_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpc5500-cortex-m33/lpc552x-s2x-mainstream-arm-cortex-m33-based-microcontroller-family:LPC552x-S2x
.. _LPC55S1x_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpc5500-cortex-m33/lpc551x-s1x-baseline-arm-cortex-m33-based-microcontroller-family:LPC551X-S1X
.. _LPC55S0x_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpc5500-cortex-m33/lpc550x-s0x-baseline-arm-cortex-m33-based-microcontroller-family:LPC550x
.. _RT1060_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1060-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1060
.. _RT1050_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1050-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1050
.. _RT1020_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1020-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1020
.. _RT1010_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt1010-crossover-mcu-with-arm-cortex-m7-core:i.MX-RT1010
.. _RT600_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt600-crossover-mcu-with-arm-cortex-m33-and-dsp-cores:i.MX-RT600 
.. _RT500_link: https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/i-mx-rt-crossover-mcus/i-mx-rt500-crossover-mcu-with-arm-cortex-m33-core:i.MX-RT500

.. Project location

.. _github_loc: https://github.com/NXPmicro/spsdk
.. _pypi_loc: https://pypi.org/project/spsdk/
.. _rdd_loc: https://spsdk.readthedocs.io

.. Start of SPSDK document

============
Introduction
============

**Secure Provisioning SDK (SPSDK)** enables connection and communication with target devices for purposes of secure provisioning and programming. Delivered as python library with command-line applications for direct utilization.

.. figure:: _static/images/SPSDK-Architecture.png
    :align: center
    :scale: 50 %

    SPSDK Simple Diagram

Project source code could be found at those locations:

- `GitHub <github_loc_>`__
- `PyPi <pypi_loc_>`__

=================
Supported Devices
=================
    
- LPC55 `S6x <LPC55S6x_link_>`_ / `S2x <LPC55S2x_link_>`_ / `S1x <LPC55S1x_link_>`_ / `S0x <LPC55S0x_link_>`_
- i.MX RT `1060 <RT1060_link_>`_ / `1050 <RT1050_link_>`_ / `1020 <RT1020_link_>`_ / `1010 <RT1010_link_>`_
- i.MX RT `600 <RT600_link_>`_ / `500 <RT500_link_>`_
    
==============
Supported OSes
==============
    
- Windows 10, 64bit
- Ubuntu 16.04 or above, 64bit
- Mac OS 10.13 or above, x64
    
====================
Supported Enviroment
====================
        
SPSDK is tested on Python 3.6+ interpreter, old version 2.x is not supported.

============
Installation
============

- Make sure to have `Python <https://www.python.org>`_ installed
- Create a virtual environment (``venv``, ``pipenv``, etc.)

----
PyPi
----

.. code:: bash

    pip install spsdk

------
GitHub
------

.. code:: bash

    $ pip install -U https://github.com/NXPmicro/spsdk/archive/master.zip

---------------------
From sources - GitHub
---------------------

.. code:: bash

    $ git clone https://github.com/NXPmicro/spsdk.git
    $ cd spsdk
    $ pip install -r requirements-develop.txt
    $ pip install -U -e .


.. note::

    In **Windows OS** you need to install `Microsoft Visual C++ Build Tools <https://www.scivision.dev/python-windows-visual-c-14-required/>`_
 
.. note::
 
    In case of problems during instalation, please make sure that you have the latest pip version.
    You can upgrade pip using this command: 
    
    .. code:: bash

        pip install --upgrade pip

 
 