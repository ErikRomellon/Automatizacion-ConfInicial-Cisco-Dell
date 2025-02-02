#Programa realizado por Erik Jesús Romellón Lorenzana

#getpass para ocultar contraseña en modo ventana terminal (no funciona en ejecucion desde pycharm)
from getpass import getpass
import paramiko,re
from time import gmtime, strftime, sleep

#Conexion por ssh
global ip
global usuario
global password
vlans=[]
global vlans_str
comillas='"'

ip = input("Ingrese la IP del dispositivo: ")
usuario = input("Ingrese nombre de usuario: ")
password = input("Ingrese el password: ")
#password = getpass("Ingrese el password: ")
print("Conectando al switch por SSH")
sleep(1)
cliente = paramiko.SSHClient()
cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cliente.connect(hostname=ip,port=22, username=usuario, password=password)
devices_access = cliente.invoke_shell()
print("Conectado!!!\n\n")

#####################################
devices_access.send("enable\n")
sleep(1)
devices_access.send(password+"\n")
sleep(1)
devices_access.send("configure\n")
sleep(1)
hn=input("Ingresa el hostname: ")
devices_access.send("hostname "+hn+"\n")
anio=strftime("%Y", gmtime())
sleep(1)
devices_access.send("username admin password Dell"+anio+" privilege 15\n")
sleep(1)
devices_access.send("username manager password password"+anio+" privilege 1\n")
sleep(1)
devices_access.send("username telecom password password"+anio+" privilege 1\n")
sleep(1)
devices_access.send("enable password password"+anio+"\n")
sleep(1)
print("--------------------------------------------------------------------------")


#Creacion de lista de vlans
numVlans = input("Ingresa el numero total de vlans: ")
numVlans = int(numVlans)

for i in range(numVlans):
    vi = input(f"Ingresa numero de vlan { i +1}: ")
    vi = int(vi)
    vlans.append(vi)
    vi = str(vi)
    vlans_str = str(vlans)[1:-1]
vlans_str = re.sub(r"\s+", "", vlans_str)
print("--------------------------------------------------------------------------")

#Nombre de vlans y database
devices_access.send("vlan database "+vlans_str+"\n")
sleep(1)
for i in vlans:
    i = str(i)
    name = input("Ingresa nombre de la vlan "+i+": ")
    devices_access.send("vlan "+i+"\n")
    sleep(1)
    devices_access.send("name "+name+"\n")
    sleep(1)
    devices_access.send("exit\n")
print("--------------------------------------------------------------------------")

        
#Asignaccion de puertos         
print("   Configuracion de puertos :D   ")
while True:
    try:
        datos = input("Cuantos puertos de datos son?: ")
        datos = int(datos)
        camaras = input("Cuantos puertos de camaras son?: ")
        camaras = int(camaras)
        aps = input("Cuantos puertos de aps son?: ")
        aps = int(aps)
        trunks = input("Cuantos puertos troncales son?: ")
        trunks = int(trunks)
    except ValueError:
        print("\nERROR, INTROUCE UNICAMENTE VALORES NUMERICOS")
        print("***********************************************\n")
    else:
        break

sum=datos+camaras+aps+trunks
sum=str(sum)
print("Se van a configurar "+sum+" puertos")
#Asignacion puertos de datos
if(datos>1):
    ranA=input("Define el rango de los puertos de datos Ej.(gi1/0/1-15): ")
    vlnDatos=input("Define la vlan de datos: ")
    vlnVoip=input("Define la vlan de Voip: ")
    devices_access.send("interface range "+ranA+"\n")
    sleep(1)
    devices_access.send("storm-control broadcast\n")
    sleep(1)
    devices_access.send("storm-control multicast\n")
    sleep(1)
    devices_access.send("switchport security max 6\n")
    sleep(1)
    devices_access.send("switchport security mode max-addresses\n")
    sleep(1)
    devices_access.send("switchport security discard-shutdown\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("spanning-tree portfast\n")
    sleep(1)
    devices_access.send("switchport mode general\n")
    sleep(1)
    devices_access.send("switchport general allowed vlan add "+vlnVoip+" tagged\n")
    sleep(1)
    devices_access.send("switchport general allowed vlan add "+vlnDatos+" untagged\n")
    sleep(1)
    devices_access.send("switchport general pvid "+vlnVoip+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
elif(datos==1):
    puerto=input("Define el puerto de datos Ej. (gi1/0/5): ")
    vlnDatos=input("Define la vlan de datos: ")
    vlnVoip=input("Define la vlan de Voip: ")
    devices_access.send("interface "+puerto+"\n")
    sleep(1)
    devices_access.send("storm-control broadcast level 5\n")
    sleep(1)
    devices_access.send("storm-control multicast level 5\n")
    sleep(1)
    devices_access.send("switchport security max 6\n")
    sleep(1)
    devices_access.send("switchport security mode max-addresses\n")
    sleep(1)
    devices_access.send("switchport security discard-shutdown\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("spanning-tree portfast\n")
    sleep(1)
    devices_access.send("switchport mode general\n")
    sleep(1)
    devices_access.send("switchport general allowed vlan add "+vlnVoip+" tagged\n")
    sleep(1)
    devices_access.send("switchport general allowed vlan add "+vlnDatos+" untagged\n")
    sleep(1)
    devices_access.send("switchport general pvid "+vlnDatos+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
    
#Asignacion puertos de camaras
if(camaras>1):
    ranA=input("Define el rango de los puertos de camaras Ej.(gi1/0/16-22): ")
    vlnCams=input("Define la vlan de camaras: ")
    devices_access.send("interface range "+ranA+"\n")
    sleep(1)
    devices_access.send("storm-control broadcast\n")
    sleep(1)
    devices_access.send("storm-control multicast\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("switchport mode access\n")
    sleep(1)
    devices_access.send("switchport access vlan "+vlnCams+"\n")
    sleep(1)
    devices_access.send("switchport security max 1\n")
    sleep(1)
    devices_access.send("switchport security mode max-addresses\n")
    sleep(1)
    devices_access.send("switchport security discard-shutdown\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
elif(camaras==1):
    puerto=input("Define el puerto de camaras Ej. (gi1/0/5): ")
    vlnCams=input("Define la vlan de camaras: ")
    devices_access.send("interface "+puerto+"\n")
    sleep(1)
    devices_access.send("storm-control broadcast level 5\n")
    sleep(1)
    devices_access.send("storm-control multicast level 5\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("switchport mode access\n")
    sleep(1)
    devices_access.send("switchport access vlan "+vlnCams+"\n")
    sleep(1)
    devices_access.send("port security max 1\n")
    sleep(1)
    devices_access.send("port security mode max-addresses\n")
    sleep(1)
    devices_access.send("port security discard-shutdown\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
 
#Asignacion puertos de accessPoint
if(aps>1):
    ranA=input("Define el rango de los puertos de APs Ej.(gi1/0/22-43): ")
    vlnSiu=[]
    devices_access.send("interface range "+ranA+"\n")
    sleep(1)
    devices_access.send("storm-control broadcast level 30\n")
    sleep(1)
    devices_access.send("storm-control multicast level 30\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("spanning-tree portfast\n")
    sleep(1)
    devices_access.send("switchport mode general\n")
    sleep(1)
    numSiu=input("Define numero total de vlans para los aps sin incluir la de administracion de aps: ")
    numSiu=int(numSiu)
    for i in range(numSiu):
        siu = input(f"Ingresa numero de vlan {i + 1}: ")
        siu = int(siu)
        vlnSiu.append(siu)
        siu = str(siu)
        siu_str = str(vlnSiu)[1:-1]
    devices_access.send("switchport general allowed vlan add "+siu_str+" tagged\n")
    vlnAdmAps=input("Define la vlan de adm de aps: ")
    devices_access.send("switchport general allowed vlan add "+vlnAdmAps+" untagged\n")
    sleep(1)
    devices_access.send("switchport general pvid "+vlnAdmAps+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
elif(aps==1):
    puerto=input("Define el puerto de APs Ej. (gi1/0/5): ")
    vlnSiu=[]
    devices_access.send("interface "+puerto+"\n")
    sleep(1)
    devices_access.send("storm-control broadcast level 30\n")
    sleep(1)
    devices_access.send("storm-control multicast level 30\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("spanning-tree portfast\n")
    sleep(1)
    devices_access.send("switchport mode general\n")
    sleep(1)
    numSiu=input("Define numero total de vlans para los aps")
    numSiu=int(numSiu)
    for i in range(numSiu):
        siu = input(f"Ingresa numero de vlan {i + 1}: ")
        siu = int(siu)
        vlnSiu.append(siu)
        siu = str(siu)
        siu_str = str(vlnSiu)[1:-1]
    devices_access.send("switchport general allowed vlan add "+siu_str+" tagged\n")
    sleep(1)
    vlnAdmAps=input("Define la vlan de adm de aps: ")
    devices_access.send("switchport general allowed vlan add "+vlnAdmAps+" untagged\n")
    sleep(1)
    devices_access.send("switchport general pvid "+vlnAdmAps+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
   
#Configuracion puertos troncales
if(trunks>1):
    ranA=input("Define el rango de los puertos troncales Ej.(gi1/0/44-48): ")
    devices_access.send("interface range "+ranA+"\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("no spanning-tree portfast\n")
    sleep(1)
    devices_access.send("switchport mode trunk\n")
    sleep(1)
    devices_access.send("switchport trunk allowed vlan add "+vlans_str+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
    print("--------------------------------------------------------------------------")  
    te=input("Puertos troncales tenGiga? si/no: " )
    te=te.upper()
    if(te=="SI"):
        ranA=input("Define el rango de los puertos troncales Ej.(te1/0/1-4): ")
        devices_access.send("interface range "+ranA+"\n")
        sleep(1)
        devices_access.send("spanning-tree disable\n")
        sleep(1)
        devices_access.send("no spanning-tree portfast\n")
        sleep(1)
        devices_access.send("switchport mode trunk\n")
        sleep(1)
        devices_access.send("switchport trunk allowed vlan add "+vlans_str+"\n")
        sleep(1)
        devices_access.send("exit\n")
        sleep(1)
        print("--------------------------------------------------------------------------")  
elif(trunks==1):
    puerto=input("Define el puerto troncal Ej. (gi1/0/5): ")
    devices_access.send("interface "+puerto+"\n")
    sleep(1)
    devices_access.send("spanning-tree disable\n")
    sleep(1)
    devices_access.send("no spanning-tree portfast\n")
    sleep(1)
    devices_access.send("switchport mode trunk\n")
    sleep(1)
    devices_access.send("switchport trunk allowed vlan add "+vlans_str+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)

#Comunidades
devices_access.send("snmp-server view CommunityView system included\n")
sleep(1)
devices_access.send("snmp-server view CommunityView interfaces included\n")
sleep(1)
devices_access.send("snmp-server view CommunityView snmp included\n")
sleep(1)
devices_access.send("snmp-server view M0n|Tmx%9u# system included\n")
sleep(1)
devices_access.send("snmp-server view M0n|Tmx%9u# interfaces included\n")
sleep(1)
devices_access.send("snmp-server view M0n|Tmx%9u# snmp included\n")
sleep(1)
devices_access.send("snmp-server community M0n|Tmx%9u# ro view CommunityView\n")
sleep(1)
devices_access.send("snmp-server community &R1$UAdY=Tw8! rw view CommunityView\n")
sleep(1)
#Cambiar ip
devices_access.send("snmp-server host ip.ip.ip.ip traps version 2 M0n|Tmx%9u#\n")
sleep(1)
#Cambiar ip
devices_access.send("snmp-server host ip.ip.ip.ip traps version 2 M0n|Tmx%9u#\n")
sleep(1)
devices_access.send("snmp-server group C@tI-ADm0n v3 priv read CommunityView write M0n|Tmx%9u#\n")
sleep(1)
devices_access.send("snmp-server group SoporT3leC0m v3 auth read M0n|Tmx%9u#\n")
sleep(1)
devices_access.send("snmp-server contact NOC-RIUADY_9237428\n")
sleep(1)
lugar=input("Ingresa dependecia (DER,FCA,CAC, etc.): ")
lugar_uper=lugar.upper()
lugar_full=comillas+lugar_uper+comillas
devices_access.send("snmp-server location "+lugar_full+"\n")
sleep(1)
devices_access.send("snmp-server enable traps snmp authentication\n")
sleep(1)
devices_access.send("clock timezone MEX -6\n")
sleep(1)
devices_access.send("clock source sntp\n")
sleep(1)
devices_access.send("sntp unicast client enable\n")
sleep(1)
#Cambiar ip
devices_access.send("sntp server ip.ip.ip.ip\n")
sleep(1)
#Cambiar ip
devices_access.send("sntp server ip.ip.ip.ip\n")
sleep(1)
print("--------------------------------------------------------------------------")


#Servicios
devices_access.send("crypto key generate dsa\n")
sleep(10)
devices_access.send("crypto key generate rsa\n")
sleep(10)
devices_access.send("ip ssh server\n")
sleep(1)
devices_access.send("crypto certificate 1 generate\n")
sleep(1)
devices_access.send("key-generate\n")
sleep(10)
devices_access.send("end\n")
sleep(1)
devices_access.send("configure\n")
sleep(1)
devices_access.send("no lldp med all\n")
sleep(1)
devices_access.send("no ip http server\n")
sleep(1)
devices_access.send("no ip http secure-server\n")
sleep(1)

print("Configuracion finalizada con exito :D")
print("--------------------------------------------------------------------------")

devices_access.send("end\n")
sleep(1)
devices_access.send("wr\n")
sleep(8)
devices_access.send("y")
sleep(5)
devices_access.send("y")
devices_access.send("\n")
output = devices_access.recv(32767).decode("utf-8")
print("\nConfiguracion aplicada: ")
print(output)
sleep(1)
cerrar = input("Presiona enter para cerrar el programa")
j=5
while (j>0):
    j=str(j)
    print("Cerrando en "+j)
    sleep(1)
    j=int(j)
    j=j-1
cliente.close()