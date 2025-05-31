# to generate private key
openssl genrsa -out jwt-private.pem 2048

# to extract the public key
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

<br>

the keys were stored here in application/certs