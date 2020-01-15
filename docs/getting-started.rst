Getting Started
===============

You need a Python version >= 2.7 and git.
Install the package via pip:

.. code-block:: bash

    pip install git+https://github.com/tomtom-international/openlr-python.git


The package comes with a simple CLI to convert base64 encoded binary data
into OpenLR XML format.

.. code-block:: bash

    python -m openlr CwRbWyNG9RpsCQCb/jsbtAT/6/+jK1lE

**Output:**

.. code-block:: xml

    <?xml version="1.0" ?>
    <OpenLR xmlns="http://www.openlr.org/openlr">
        <LocationID></LocationID>
        <XMLLocationReference>
            <LineLocationReference>
            <LocationReferencePoint>
                <Coordinates>
                    <Longitude>6.126819849014282</Longitude>
                    <Latitude>49.60851788520813</Latitude>
                </Coordinates>
                <LineAttributes>
                    <FRC>FRC3</FRC>
                    <FOW>MULTIPLE_CARRIAGEWAY</FOW>
                    <BEAR>141</BEAR>
                </LineAttributes>
                <PathAttributes>
                    <LFRCNP>FRC3</LFRCNP>
                    <DNP>557</DNP>
                </PathAttributes>
            </LocationReferencePoint>
            <LocationReferencePoint>
                <Coordinates>
                    <Longitude>6.128369849014282</Longitude>
                    <Latitude>49.60398788520813</Latitude>
                </Coordinates>
                <LineAttributes>
                    <FRC>FRC3</FRC>
                    <FOW>SINGLE_CARRIAGEWAY</FOW>
                    <BEAR>231</BEAR>
                </LineAttributes>
                <PathAttributes>
                    <LFRCNP>FRC5</LFRCNP>
                    <DNP>264</DNP>
                </PathAttributes>
            </LocationReferencePoint>
            <LastLocationReferencePoint>
                <Coordinates>
                    <Longitude>6.128159849014282</Longitude>
                    <Latitude>49.60305788520813</Latitude>
                </Coordinates>
                    <LineAttributes>
                    <FRC>FRC5</FRC>
                    <FOW>SINGLE_CARRIAGEWAY</FOW>
                    <BEAR>287</BEAR>
                </LineAttributes>
            </LastLocationReferencePoint>
            <Offsets>
                <PosOff>149</PosOff>
                <NegOff>0</NegOff>
            </Offsets>
            </LineLocationReference>
        </XMLLocationReference>
    </OpenLR>

The same example programmatically:

.. code-block:: python

    import openlr
    location = openlr.binary_decode("CwRbWyNG9RpsCQCb/jsbtAT/6/+jK1lE")
    print(location.points[0].lon)  # 6.126819849014282
    print(location.points[0].lat)  # 49.60851788520813


Defining a location object and converting it to XML and binary physical formats

.. code-block:: python

    import openlr
    location = openlr.GeoCoordinateLocation(
        openlr.Coordinates(52.495218, 13.461668)
    )
    print(openlr.binary_encode(location))  # IyVUdwmSoA==
    print(openlr.xml_encode_to_string(location))  # <?xml version="1.0" ?><OpenLR ...

Defining a LineLocation

.. code-block:: python

    from openlr import LineLocation, LocationReferencePoint, FRC, FOW

    location = LineLocation(
        [
            LocationReferencePoint(
                6.1268198, 49.6085178, FRC.FRC3, FOW.MULTIPLE_CARRIAGEWAY, 141, FRC.FRC3, 557,
            ),
            LocationReferencePoint(
                6.1283698, 49.6039878, FRC.FRC3, FOW.SINGLE_CARRIAGEWAY, 231, FRC.FRC5, 264
            ),
            LocationReferencePoint(
                6.1281598, 49.6030578, FRC.FRC5, FOW.SINGLE_CARRIAGEWAY, 287, FRC.FRC7, 0
            ),
        ],
        0.26757812,
        0,
    )
