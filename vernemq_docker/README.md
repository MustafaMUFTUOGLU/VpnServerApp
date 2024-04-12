Step-by-step instruction

1. Generate public and private RSA keypair for CA:
openssl genrsa -out vernemq_ca.key 2048

2. Create CA certificate:
openssl req -new -x509 -days 3650 -key vernemq_ca.key -out vernemq_ca.crt

3. Create VerneMQ keypair:
openssl genrsa -out vernemq.key 2048

4. Create certificate request from CA:
openssl req -new -out vernemq.csr -key vernemq.key

5. Verify and sign the certificate request: create cert.cnf, edit values (names, DNS and IPs) and run command:
---------------------------------------------
[ req ]
default_bits       = 2048
default_md         = sha512
default_keyfile    = vernemq.key
prompt             = no
encrypt_key        = no
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
countryName                 = RU
stateOrProvinceName         = Moscow
localityName               = Moscow
organizationName           = Ivy Knob
commonName                 = ivyknob.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1   = localhost
DNS.2   = mqtt.ivyknob.com
IP.1 = 127.0.0.1
IP.2 = 192.168.0.10
IP.2 = 1.1.1.1
---------------------------------------------
openssl x509 -req -in vernemq.csr -CA vernemq_ca.crt -CAkey vernemq_ca.key -CAcreateserial -extensions req_ext -extfile cert.cnf -out vernemq.crt -days 3650

To check if values of alternative names are generated valid use:
openssl x509 -text -noout -in vernemq.crt -certopt no_subject,no_header,no_version,no_serial,no_signame,no_validity,no_issuer,no_pubkey,no_sigdump,no_aux
6. Copy vernemq.crt, vernemq.key, vernemq_ca.crt to the folder with certificates:

7. Add listener in the vernemq.conf file:

listener.ssl.cafile = /etc/vernemq/vernemq_ca.crt
listener.ssl.certfile = /etc/vernemq/vernemq.crt
listener.ssl.keyfile = /etc/vernemq/vernemq.key

listener.ssl.default = 0.0.0.0:8883

8. In the client use vernemq_ca.crt or vernemq.crt file to verify identity of the MQTT broker.

To test broker to work over ssl use these mosqutto CLI commands:

Subscribe to the topic:
mosquitto_sub -h localhost -p 8883 --cafile ./vernemq_ca.crt -t "test/test" -d

Send message to the topic:
mosquitto_pub -h localhost -p 8883 -t test/test -m "test" -d --cafile ./vernemq_ca.crt