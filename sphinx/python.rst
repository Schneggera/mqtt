Publishing der Heizungslimits mittels Python
=================================================

Grundlagen
----------

Zum publishen der aktuellen Temperatur wurde eine einfach Konsolenanwendung in
Python mit dem Paho Client implementiert.

In der Anwendung kann man dann einen Wert zwischen -50 und +50 eingeben welcher
dann per MQTT auf ein festgelgtes Topic gepublished wird.

Implementierung
---------------

Das Paho Modul kann einfach mit `pip install paho-mqtt` installiert werden und
anschließend in seinem Code importiert werdern. Um eine Verbindung aufzubauen
erstellt man sich eine Instanz mit `client = paho.Client()` und kann sich dann
anschließend mit `client.connect()` zum server verbinden. Anschließend kann man
man sich dann bestimmte callbacks festlegen.

.. code-block:: bash

    client.on_publish = _on_publish
    client.on_connect = _on_connect

Konfiguration
^^^^^^^^^^^^^

.. code-block:: bash

    HOST = "test.mosquitto.org"
    CLIENTID = "mqttPaho"
    TOPIC = "/$_fluzzy$$cadabra/Nö/Temperatur";
    MIN_VALUE = -50
    MAX_VALUE = 50

Anwendung
---------

Zum Starten der Anwendung navigiert man in der Kommandozeile zur main.py und
führt `python main.py` aus. 

.. code-block:: bash

    python main.py
    Enter new temperature between -50 and 50:

Anschließend kann man eine neue Temperatur eingeben und mit Enter abschicken und
wird dann benachritigt wenn die Nachricht abgeschickt wurde.

.. code-block:: bash

    Enter new temperature between -50 and 50:
    10
    Temperature published!

Bei einem falschem Wert wird der User benachrichtigt das der Wert ungültig ist.

.. code-block:: bash

    Enter new temperature between -50 and 50:
    100
    Not a valid temparature! Has to be a value between -50 and 50
    Enter new temperature between -50 and 50: