import redis

# Conectarse a Redis (localmente)
client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Probar si Redis está funcionando
#client.set('temperatura', '24')
#print(client.get('temperatura').decode('utf-8'))
client.delete('temperatura')
client.delete('humedad')