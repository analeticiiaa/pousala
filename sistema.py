import unicodedata #questao dos acentos e letras maiusculas 
from datetime import datetime #identificacao passado/futuro
from abc import ABC, abstractmethod #criar classe abst
from banco import BancoDeDados #classe do banco.py


def remover_acentos(texto):
    if not texto: return "" #se estiver vazio retorna vazio
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('utf-8').lower() #separa lestras dos acentos, ignora os acentos,  volta ao texto normal e coloca tudo em minusculo
    #remove acentos e transforma em minusculo
class Usuario(ABC): #criando uma classe abstrata ABC(abst base class), classe abstrata nao pode ser usada diretamente
    def __init__(self, nome, email, senha): #toda classe que herdar usuario vai ter nome, email,senha
        self.nome = nome; 
        self.email = email; 
        self._senha = senha #protegido
    @abstractmethod #nao tem implementacao aqui, obriga as subclasses implementarem
    def mostrar_painel(self): pass #polimorfismos, cada usuario criado tera seu mostrar painel

class Hospede(Usuario): #heranca, classe filha, herda tudo de usuario
    def __init__(self, nome, email, senha): 
        super().__init__(nome, email, senha) #chamou o construtor pai p criar esses atributos
        self.__reservas = [] #encapsulamento, so a propria classe pode acessar diretamente, cria uma lista privada
    def fazer_reserva(self, propriedade, data_inicio, data_fim): #inicializar um metodo
        reserva = Reserva(self, propriedade, data_inicio, data_fim) #cria um objeto reserva, self = hosp atual, liga o hosp a propriedade e as datas
        self.__reservas.append(reserva); #encapsulamento, adiciona a reserva na lista privada do hospede
        propriedade.adicionar_reserva(reserva); #adiciona a reserva em propriedade 
        return reserva 
    def mostrar_painel(self): return f"Painel do Hóspede: {self.nome}" #polimorfismo, tbm exite o painel p anfitriaro, Mesmo nome, comportamento diferente

class Anfitriao(Usuario): #heranca, classe filha, herda tudo de usuario
    def __init__(self, nome, email, senha): 
        super().__init__(nome, email, senha) #chamou o construtor pai p criar esses atributos
        self.__propriedades = [] #encapsulamento, cria uma lista privada fazia q so o hosp acessa
    @property #transforma um metodo em um atributo
    def propriedades(self): 
        return self.__propriedades.copy() #encapsulamento, devolve uma copia da lista de imóveis que o anfitrião possui, p n alterar a original
    def anunciar_propriedade(self, propriedade): 
        self.__propriedades.append(propriedade) #permite adicionar propriedades a lista de imoveis
    def mostrar_painel(self): 
        return f"Painel do Anfitrião: {self.nome}" #polimorfismo, 
   

class Propriedade: #modela o lugar q pode ser alugado
    def __init__(self, nome, localizacao, capacidade, preco, anfitriao): #construtor
        self.nome = nome; 
        self.localizacao = localizacao; 
        self.capacidade = capacidade; 
        self.preco = preco; 
        self.anfitriao = anfitriao
        self.__reservas = []; #encapsulamento, listas privadas
        self.__avaliacoes = []
    @property #transforma um metodo em um atributo
    def reservas(self):  #encapsulamento, devolve uma copia da lista de imóveis que o anfitrião possui, p n alterar a original
        return self.__reservas.copy()
    def adicionar_reserva(self, reserva): 
        self.__reservas.append(reserva)
    @property
    def avaliacoes(self): 
        return self.__avaliacoes.copy()
    def adicionar_avaliacao(self, av): 
        self.__avaliacoes.append(av)
    @property
    def media_notas(self): #calcular media avaliacoes
        if not self.__avaliacoes: 
            return "Novo" #se nao tem avaliacao retorna novo
        return round(sum(av['nota'] for av in self.__avaliacoes) / len(self.__avaliacoes), 1)
    def esta_disponivel(self, d_in, d_out): #verifica se esta livre p aqueles dias
        start = datetime.strptime(d_in, '%Y-%m-%d'); #transforma texto em data real
        end = datetime.strptime(d_out, '%Y-%m-%d') 
        for res in self.__reservas: #verificar conflito com cada reserva já feita
            r_s = datetime.strptime(res.data_inicio, '%Y-%m-%d'); 
            r_e = datetime.strptime(res.data_fim, '%Y-%m-%d')
            if not (end <= r_s or start >= r_e): 
                return False #end <= r_s verifica se o fim da viagem nova nao for antes da antiga comecar ou inicio da viagem nova nao for depois q a antiga acabar
        return True

class Reserva:
    def __init__(self, hospede, propriedade, d_in, d_out): #recebe os objetos hospede e propriedade
        self.hospede = hospede; 
        self.propriedade = propriedade; 
        self.data_inicio = d_in; 
        self.data_fim = d_out; 
        self.__status = "ativa"
    @property
    def status(self): return self.__status #encapsulamento, devolve se a reserva esta ativa ou concluida, @property p ser so leitura e n conseguir alterar p cancelado por fora

class Sistema: #responsavel por app.py, regras do negocio e o banco de dados
    def __init__(self): #construtor
        self.db = BancoDeDados();  #conecta com o banco de dados
        self.__propriedades = []; #cria uma lista privada e vazia p guardar as propriedades na memoria
        self.carregar_dados_do_banco() #carrega tudo q ja existe no BD

    def carregar_dados_do_banco(self):
        self.__propriedades.clear()  #evita duplicacao ao recarregar
        for p in self.db.buscar_propriedades(): #p eh uma linha no banco de dados
            self.__propriedades.append(Propriedade(p[1], p[2], p[3], p[4], Anfitriao("Dono", str(p[5]).strip().lower(), "")))
            #p1 = nome, p2=localizacao, p3= capacidade, p4=preco, anfitriao
        for r in self.db.buscar_reservas(): #percorre as reservas
            for prop in self.__propriedades: #percorre as propriedades
                #encontrar qual propriedade corresponde a reserva
                if prop.nome.strip().lower() == str(r[1]).strip().lower():
                    prop.adicionar_reserva(Reserva(Hospede("Hóspede", str(r[2]).strip().lower(), ""), prop, r[3], r[4]))
        for av in self.db.buscar_avaliacoes():
            for prop in self.__propriedades:
                if prop.nome.strip().lower() == str(av[1]).strip().lower():
                    prop.adicionar_avaliacao({"hospede": av[2], "nota": av[3], "comentario": av[4]})

    @property
    def propriedades(self): #transforma um metodo em um atributo
        return self.__propriedades

    def cadastrar_hospede(self, n, e, s): 
        if self.db.salvar_usuario(n, e, s, "hospede"): #salva no BD nome, email,senha, tipo de usu.:hosp
            return Hospede(n, e, s)
        return None #falhou

    def cadastrar_anfitriao(self, n, e, s):
        if self.db.salvar_usuario(n, e, s, "anfitriao"): #salva no BD nome, email,senha, tipo de usu.:anfitriao
            return Anfitriao(n, e, s)
        return None

    def anunciar_propriedade(self, anf, n, l, c, preco):
        if self.db.salvar_propriedade(n, l, c, preco, anf.email):  #salva no BD
            p = Propriedade(n, l, c, preco, anf); #cria um objeto
            self.__propriedades.append(p); #guarda no sistema
            return p 
        return None

    def registrar_reserva(self, h, p, d_in, d_out): #recebe o hospedde, propriedade e as datas
        res = h.fazer_reserva(p, d_in, d_out) #manda p hospede fazer a reserva
        self.db.salvar_reserva(p.nome, h.email, d_in, d_out, res.status);  #dps q o hospede cria a reserva eh mandada para o bd
        return res 
    
    
    def buscar(self, loc, cap, d_in, d_out): #filtra as propriedades 
        loc_limpa = remover_acentos(loc) 
        return [p for p in self.__propriedades if remover_acentos(p.localizacao) == loc_limpa and p.capacidade >= cap and p.esta_disponivel(d_in, d_out)] #passa pela lista de propriedade p ve se esta habilitada p aquele hosp(data e capacidade)

    def fazer_login(self, e, s): 
        for u in self.db.buscar_todos_usuarios(): #percorrer usuarios do banco
            if str(u[2]).strip().lower() == str(e).strip().lower() and u[3] == s: return {"nome": u[1], "email": u[2], "tipo": u[4]}
        return None

    def enviar_mensagem(self, prop, rem, dest, texto): #envia a mensagem p BD
        self.db.salvar_mensagem(prop, rem, dest, texto)
    def obter_mensagens(self, prop, h_e, a_e):
        return [{'remetente': m[2], 'texto': m[4]} 
                for m in self.db.buscar_mensagens() 
                if m[1] == prop and ((m[2] == h_e and m[3] == a_e) or (m[2] == a_e and m[3] == h_e))]
    
    def obter_chats_usuario(self, email): #retorna todas as conversas do usuar.
        e = str(email).strip().lower(); chats = set()
        for m in self.db.buscar_mensagens():
            if m[2] == e: chats.add((m[1], m[3]))
            elif m[3] == e: chats.add((m[1], m[2]))
        return list(chats)

    def registrar_duvida(self, prop, perg, resp):  #salva duvida no BD
        self.db.salvar_duvida(prop, perg, resp)
    def obter_duvidas(self, prop): #retorna todas as perguntas e resposta desse imovel
        return self.db.buscar_duvidas(prop)

    def obter_favoritos_usuario(self, email):
        e = str(email).strip().lower(); 
        favs = [f[2] 
                for f in self.db.buscar_favoritos() 
                if f[1] == e]
        return [p for p in self.__propriedades if p.nome in favs]

    def toggle_favorito(self, email, prop): #clicar em favoritar
        e = str(email).strip().lower()
        if any(f[1] == e and f[2] == prop for f in self.db.buscar_favoritos()): self.db.remover_favorito(e, prop)
        else: self.db.adicionar_favorito(e, prop)