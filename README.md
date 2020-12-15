# surl

# Configuracion aplicacion:
Para levantar la app, se necesita configurar una variable de entorno con el URI de MONGODB.
Por ejemplo:
Replica set "surl":
export MONGO_URI="mongodb://USUARIO:PASSWORD@mongodb1,mongodb2,mongodb3/NOMBREBASE?replicaSet=surl&readPreference=secondaryPreferred"

Modo local:
export MONGO_URI="mongodb://USUARIO:PASSWORD@localhost:27017/NOMBREBASE"

Acortador url

# Uso:
Crear url corta:

POST json https://surl.todok8s.com/crear
Header Content-Type application/json

Ejemplo:
{"url_larga": "https://google.com"}

Usar URL corta:

GET https://surl.todok8s.com/XXYYZZ

Borrar URL corta:

DELETE https://surl.todok8s.com/borrar/XXYYZZ

# Infraestructura:

Consta de una VPC, con dos subredes y sus respectivos security groups.
Tiene configurado un Load Balancer y Cloudfront para cache.

Las dos subredes estan dos AZ diferentes en California.(En esta region hay solo dos AZ)

Se configuro un ECS con una imagen docker de la app. Que tiene como parametros la conexion URI a Mongodb, y ademas se parametriza los hosts de Mongo.

Se genero un replica set de Mongo, con 3 miembros, y un arbiter.
1 es primario y los otros dos nodos son secundarios.