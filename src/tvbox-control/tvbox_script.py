import serial
import time
import datetime
import tvbox_config as Config
import keyboard

# Classe responsável pela comunicação com o Arduino
class Connection():
    
    class device: None

    def __init__(self, vid, pid):
        self.device.vid = vid
        self.device.pid = pid
        self.device.id = vid + ":" + pid
        self.device.port = None
        self.device.desc = None
        self.serial = None

    # Scanea os dispositivos disponíveis
    def scan(self):
        import serial.tools.list_ports

        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if self.device.id in hwid:
                self.device.port = port
                self.device.desc = desc
                return
        
        # Não encontrou o dispositivo
        self.device.port = None
        self.device.desc = None
    
    # Inicia a comunicação com o dispositivo
    def begin(self):
        try:
            self.serial = serial.Serial(
                self.device.port, Config.CON_BAUD_RATE, serial.EIGHTBITS, 
                serial.PARITY_NONE, serial.STOPBITS_ONE, Config.CON_SERIAL_READ_TIMEOUT
            )
            print ("> Info: Comunicação iniciada com '{}' a {}bps".format(self.device.port, Config.CON_BAUD_RATE))
            return True
        except:
            print("> Erro: Comunicação serial não inicializada")
            self.serial = None
            return False

    # Loop até receber uma mensagem completa
    def receive(self, timeout = Config.CON_RECEIVE_TIMEOUT):
        try:
            if self.serial == None:
                print ("> Erro: A comunicação serial não está ativa")
                raise

            time_init = datetime.datetime.now()
            date_timeout = datetime.timedelta(seconds=timeout)            
            message = ""

            while True:
                byte = self.serial.read()
                
                if byte == Config.CON_END_BYTE:
                    return message
                else:
                    message = message + byte.decode(Config.CON_ENCODE_DECODE)

                if timeout > -1 and (datetime.datetime.now() - time_init) > date_timeout:
                    print("> Erro: Timeout ao receber a mensagem")
                    raise
                
        # Erro para o timeout        
        except Exception:
            return None

    # Envia uma mensagem ao arduino
    def send(self, msg):
        self.serial.write(msg.encode(Config.CON_ENCODE_DECODE))
        self.serial.write(Config.CON_END_BYTE)

    # Executar o comando de ping
    def ping(self):
        attempt = Config.CON_PING_ATTEMPT

        while attempt:
            print("   > Info: Executando PING-PONG ({})".format(attempt))            
            attempt = attempt - 1
            
            self.send("PING")
            
            print("   ", end="")
            if self.receive(Config.CON_PING_TIMEOUT) != None:
                print("> Info: PING-PONG completado com sucesso!")
                return True

        print("   > Erro: Não foi possível completar o PING-PONG")
        return False
        

# Classe responsável pelo controle do sistema
class Controller():

    time_last_key = datetime.datetime.now() 
    
    def __init__(self):
        self.conn = Connection(Config.DEVICE_VID, Config.DEVICE_PID)

    # Executa em loop de 500ms até conectar-se com sucesso e executar um ping-pong
    def connect(self):
        import time

        print_header = True

        while True:
            try:
                if print_header:
                    print ("> Info: Localizando o arduino...")

                self.conn.scan()

                print("   ", end="")
                if self.conn.device.port == None:
                    print("\b\b\b", end="")
                    print_header = False                    
                else:
                    print("> Info: Arduino encontrado em '{}'".format(self.conn.device.port))
                    
                    print("> Info: Iniciando a comunicação...")
                    print("   ", end="")
                    if self.conn.begin():
                        print("> Info: Testando a conexão...")

                        if self.conn.ping():
                            return
                        else:
                            print("")
                            print_header = True
                    else:
                        print("> Info: O baud rate está configurado corretamente?")
                        print("")
                        print_header = True
            except:
                print("> Erro: Não foi possível conectar-se ao Arduino")
                print("")
                print_header = True

            time.sleep(0.5)

    # Executa um comando
    def irHandle(self, command):
        if command in Config.CTL_KEY_MAP:

            # Envita que os comando sejam executados rapidamente
            if datetime.datetime.now() - self.time_last_key > datetime.timedelta(seconds=Config.CTL_KEY_DELAY):
                self.time_last_key = datetime.datetime.now()
            else:
                print ("> Info: Comando não pode ser executado ainda")
                return

            try:
                keyboard.press_and_release(Config.CTL_KEY_MAP[command])
                print("> Info: Tecla pressionada: '{}'".format(Config.CTL_KEY_MAP[command]))
            except ImportError:
                print("> Erro: Não foi possível carregar as dependências. O script está rodando como root?")
            except:
                print("> Erro: Não foi possível pressionar a tecla mapeada")
        else:
            print("> Info: Tecla não mapeada")

    # Executa em loop respondendo aos comandos
    def run(self):        
        self.connect() # Conectar ao arduino

        while True:
            print("> Info: Aguardando um comando...")
            command = self.conn.receive(-1) # Fica parado aqui até receber uma mensagem do arduino

            if command != None: # Algum comando válido foi recebido?
                print("   > Info: Comando recebido: {}".format(command))

                if command.startswith(Config.CTL_IR_PRE): # Comando contém a flag do IR?
                    print("   ", end="")
                    self.irHandle(command.replace(Config.CTL_IR_PRE, ""))
                else:
                    print("   > Info: Não é um comando via IRemote")
            else:
                print("> Erro: Não foi possível receber uma mensagem")
                print()
                self.connect() # reconectar ao Arduino


# Executar...
Controller().run()
    