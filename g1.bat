rem set AA=%CD%

pushd  C:\utils\openssl-3.3.2\x64\bin
openssl req -config openssl.cnf  -x509 -newkey rsa:4096 -nodes -sha256 -out server.crt -keyout server.key -days 3650 

rem cd %AA%

rem popd