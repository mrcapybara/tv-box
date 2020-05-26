# Arduino
DEVICE_VID = "1A86"
DEVICE_PID = "7523"

# Comunicação
CON_BAUD_RATE = 9600
CON_END_BYTE = b'\n'
CON_ENCODE_DECODE = "utf-8"
CON_PING_TIMEOUT = 5  # in seconds (0 = no timeout; -1 = forever timeout)
CON_PING_ATTEMPT = 3
CON_RECEIVE_TIMEOUT = 1 # in seconds (0 = no timeout; -1 = forever timeout)
CON_SERIAL_READ_TIMEOUT = CON_RECEIVE_TIMEOUT

# Controle
CTL_IR_PRE = "IR_"   # Flag para verificar se o comando é do leitor

CTL_KEY_DELAY = 0.25 # Delay entre o press. das teclas (em segundos)

CTL_KEY_MAP = {
    # Chave no Modo SKY
	"2FD28D7"  : "", # TV VIDEO
	"39767224" : "", # TELA TV   
	"6D8867D7" : "s", # ON        
	"692D04A0" : "s", # OFF       
	"427EBE9F" : "", # GUIA      
	"9D65B0BC" : "", # (QUADRADO)
	"AB4D94A9" : "", # LISTA     
	"34498102" : "esc", # SAIR      
	"F24119FE" : "up", # SETA CIMA 
	"C53794B4" : "left", # SETA ESQ  
	"75A956A7" : "enter", # CONFIRMA  
	"BC9DF06"  : "right", # SETA DIR  
	"B489062B" : "down", # SETA BAIX 
	"BB9BDEE7" : "", # (RETORNO) 
	"76CF1379" : "", # MENU      
	"F640360"  : "", # ?INFO     
	"C332FABB" : "", # (VERMELHO)
	"8C0B38A3" : "", # (VERDE)   
	"2591C110" : "", # (AMARELO) 
	"506AE98B" : "", # (AZUL)    
	"2FD58A7"  : "+", # VOL + 
	"2FD7887"  : "-", # VOL -  
	"2FD08F7"  : "F8", # (MUTE) 
	"5BFBFDE9" : "", # RET CH    
	"165412B7" : "", # CH +      
	"5815B090" : "", # CH -      
	"C9767F76" : "1", # 1         
	"C8155AB1" : "2", # 2         
	"B6996DAE" : "3", # 3         
	"969AE844" : "4", # 4         
	"4AAFAC67" : "5", # 5         
	"9C2A936C" : "6", # 6         
	"833ED333" : "7", # 7         
	"55F2B93"  : "8", # 8         
	"DE78B0D0" : "9", # 9         
	"BDE97C12" : "", # DASH      
	"F32F72D7" : "0", # 0         
	"3F23F43"  : "", # i                     
}