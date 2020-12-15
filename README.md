# surl



Acortador url

Uso:
Crear url corta:

POST json https://surl.todok8s.com/crear
Header Content-Type application/json

Ejemplo:
{"url_larga": "https://google.com"}

Usar URL corta:

GET https://surl.todok8s.com/XXYYZZ

Borrar URL corta:

DELETE https://surl.todok8s.com/borrar/XXYYZZ
