..
    Warning: Do not edit this file. It is automatically generated from the
    software project's code and your changes will be overwritten.

    The tool to generate this file lives in openstack-doc-tools repository.

    Please make any changes needed in the code, then run the
    autogenerate-config-doc tool from the openstack-doc-tools repository, or
    ask for help on the documentation mailing list, IRC channel or meeting.

.. _ec2api-clients:

.. list-table:: Description of OpenStack Clients configuration options
   :header-rows: 1
   :class: config-ref-table

   * - Configuration option = Default value
     - Description

   * - **[DEFAULT]**
     -

   * - ``cinder_service_type`` = ``volumev3``

     - (String) Service type of Volume API, registered in Keystone catalog.

   * - ``ec2_timestamp_expiry`` = ``300``

     - (Integer) Time in seconds before ec2 timestamp expires

   * - ``keystone_ec2_tokens_url`` = ``http://localhost:5000/v3/ec2tokens``

     - (String) URL to authenticate token from ec2 request.

   * - ``nova_service_type`` = ``compute``

     - (String) Service type of Compute API, registered in Keystone catalog. Should be v2.1 with microversion support. If it is obsolete v2, a lot of useful EC2 compliant instance properties will be unavailable.