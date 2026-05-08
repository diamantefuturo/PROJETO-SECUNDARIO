"""
=============================================================
  MÓDULO 1 - CONTROLE DE ACESSO
  Arquivo: usuarios.py
  Descrição: CRUD completo de usuários do sistema ShopControl
  Projeto: PROJETOFINAL_4TIERAI_CNAK
=============================================================
"""

import json
import os
import uuid
from datetime import datetime

# ─────────────────────────────────────────
#  CAMINHO DO BANCO DE DADOS JSON
# ─────────────────────────────────────────
# Ajustado para buscar a pasta 'dados' no mesmo diretório se o arquivo estiver na raiz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "dados", "usuarios.json")


# ─────────────────────────────────────────
#  CONSTANTES / OPÇÕES VÁLIDAS
# ─────────────────────────────────────────

PERFIS_USUARIO = [
    "visitante",          # pessoa comum que visita o shopping
    "funcionario_loja",   # trabalha em uma loja específica
    "dono_loja",          # proprietário/locatário da loja
    "funcionario_shopping", # trabalha para o shopping em si
    "seguranca",          # equipe de segurança
    "administrador",      # admin do sistema
]

FAIXAS_ETARIAS = [
    "crianca",      # 0–12
    "adolescente",  # 13–17
    "jovem",        # 18–24
    "adulto",       # 25–59
    "idoso",        # 60+
]

STATUS_USUARIO = [
    "ativo",
    "inativo",
    "bloqueado",
    "pendente",
]

SHOPPINGS = [
    "Shopping Norte",
    "Shopping Sul",
    "Shopping Leste",
    "Shopping Oeste",
]

GENEROS = ["masculino", "feminino", "nao_informado"]


# ─────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────

def _carregar_dados():
    """Lê o arquivo JSON e retorna o dicionário de dados."""
    if not os.path.exists(ARQUIVO_JSON):
        return {"metadados": _metadados_inicial(), "usuarios": []}
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_dados(dados: dict):
    """Salva o dicionário de dados no arquivo JSON."""
    os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)
    dados["metadados"]["ultima_atualizacao"] = datetime.now().isoformat()
    dados["metadados"]["total_usuarios"] = len(dados["usuarios"])
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _metadados_inicial():
    return {
        "criado_em": datetime.now().isoformat(),
        "total_usuarios": 0,
        "versao": "1.0",
        "ultima_atualizacao": datetime.now().isoformat(),
    }


def _gerar_id():
    return uuid.uuid4().hex[:8].upper()


def _calcular_faixa_etaria(idade: int) -> str:
    if idade <= 12:
        return "crianca"
    elif idade <= 17:
        return "adolescente"
    elif idade <= 24:
        return "jovem"
    elif idade <= 59:
        return "adulto"
    else:
        return "idoso"


def _cpf_existe(cpf: str, dados: dict, ignorar_id: str = None) -> bool:
    """Verifica se o CPF já está cadastrado (ignora o próprio usuário ao atualizar)."""
    for u in dados["usuarios"]:
        if u["cpf"] == cpf and u["id"] != ignorar_id:
            return True
    return False


# ─────────────────────────────────────────
#  C R U D
# ─────────────────────────────────────────

def criar_usuario(
    nome: str,
    cpf: str,
    email: str,
    senha: str,
    perfil: str,
    idade: int,
    genero: str,
    shopping_principal: str,
    outros_shoppings: list = None,
    loja: str = None,
    telefone: str = None,
    observacoes: str = None,
) -> dict:
    """
    Cria um novo usuário e salva no JSON.
    Retorna o usuário criado ou levanta ValueError em caso de erro.
    """
    # Validações
    if perfil not in PERFIS_USUARIO:
        raise ValueError(f"Perfil inválido. Escolha: {PERFIS_USUARIO}")
    if genero not in GENEROS:
        raise ValueError(f"Gênero inválido. Escolha: {GENEROS}")
    if shopping_principal not in SHOPPINGS:
        raise ValueError(f"Shopping inválido. Escolha: {SHOPPINGS}")
    if not (0 < idade < 120):
        raise ValueError("Idade inválida.")

    dados = _carregar_dados()

    if _cpf_existe(cpf, dados):
        raise ValueError(f"CPF {cpf} já cadastrado no sistema.")

    usuario = {
        "id": _gerar_id(),
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha_hash": senha,           # Em produção: usar bcrypt/hashlib
        "perfil": perfil,
        "idade": idade,
        "faixa_etaria": _calcular_faixa_etaria(idade),
        "genero": genero,
        "shopping_principal": shopping_principal,
        "outros_shoppings": outros_shoppings or [],
        "loja": loja,                  # Preenchido se for funcionário/dono de loja
        "telefone": telefone,
        "observacoes": observacoes,
        "status": "ativo",
        "data_cadastro": datetime.now().isoformat(),
        "ultimo_acesso": None,
        "visitas": [],                 # Histórico de visitas (preenchido pelo monitoramento)
        "comportamento": {             # Preenchido pela IA de câmeras futuramente
            "lojas_frequentadas": [],
            "horarios_preferidos": [],
            "tempo_medio_visita_min": 0,
        },
    }

    dados["usuarios"].append(usuario)
    _salvar_dados(dados)
    print(f"✅ Usuário '{nome}' cadastrado com ID {usuario['id']}.")
    return usuario


def listar_usuarios(
    filtro_perfil: str = None,
    filtro_status: str = None,
    filtro_shopping: str = None,
    filtro_faixa: str = None,
) -> list:
    """
    Retorna lista de usuários com filtros opcionais.
    Todos os filtros são opcionais — sem filtro retorna todos.
    """
    dados = _carregar_dados()
    usuarios = dados["usuarios"]

    if filtro_perfil:
        usuarios = [u for u in usuarios if u["perfil"] == filtro_perfil]
    if filtro_status:
        usuarios = [u for u in usuarios if u["status"] == filtro_status]
    if filtro_shopping:
        usuarios = [u for u in usuarios if u["shopping_principal"] == filtro_shopping]
    if filtro_faixa:
        usuarios = [u for u in usuarios if u["faixa_etaria"] == filtro_faixa]

    return usuarios


def buscar_usuario(identificador: str) -> dict | None:
    """
    Busca um usuário por ID, CPF ou e-mail.
    Retorna o usuário ou None se não encontrado.
    """
    dados = _carregar_dados()
    for u in dados["usuarios"]:
        if u["id"] == identificador.upper() or \
           u["cpf"] == identificador or \
           u["email"].lower() == identificador.lower():
            return u
    return None


def atualizar_usuario(id_usuario: str, **campos) -> dict:
    """
    Atualiza campos de um usuário existente.
    Uso: atualizar_usuario("A1B2C3D4", nome="Novo Nome", status="bloqueado")
    """
    dados = _carregar_dados()
    for i, u in enumerate(dados["usuarios"]):
        if u["id"] == id_usuario.upper():
            # Campos protegidos que não podem ser alterados por aqui
            campos_protegidos = {"id", "cpf", "data_cadastro", "visitas"}
            for campo, valor in campos.items():
                if campo in campos_protegidos:
                    print(f"⚠️  Campo '{campo}' não pode ser alterado diretamente.")
                    continue
                if campo == "idade":
                    dados["usuarios"][i]["faixa_etaria"] = _calcular_faixa_etaria(valor)
                if campo == "status" and valor not in STATUS_USUARIO:
                    raise ValueError(f"Status inválido. Escolha: {STATUS_USUARIO}")
                dados["usuarios"][i][campo] = valor

            _salvar_dados(dados)
            print(f"✅ Usuário {id_usuario} atualizado.")
            return dados["usuarios"][i]

    raise ValueError(f"Usuário com ID '{id_usuario}' não encontrado.")


def deletar_usuario(id_usuario: str) -> bool:
    """
    Remove um usuário pelo ID.
    Retorna True se removido, False se não encontrado.
    """
    dados = _carregar_dados()
    antes = len(dados["usuarios"])
    dados["usuarios"] = [u for u in dados["usuarios"] if u["id"] != id_usuario.upper()]
    if len(dados["usuarios"]) < antes:
        _salvar_dados(dados)
        print(f"🗑️  Usuário {id_usuario} removido.")
        return True
    print(f"❌ Usuário {id_usuario} não encontrado.")
    return False


def registrar_visita(id_usuario: str, shopping: str, local_dentro: str = None):
    """
    Registra uma visita do usuário (chamado pelo módulo de monitoramento).
    """
    dados = _carregar_dados()
    for i, u in enumerate(dados["usuarios"]):
        if u["id"] == id_usuario.upper():
            visita = {
                "data_hora": datetime.now().isoformat(),
                "shopping": shopping,
                "local": local_dentro,
            }
            dados["usuarios"][i]["visitas"].append(visita)
            dados["usuarios"][i]["ultimo_acesso"] = datetime.now().isoformat()
            _salvar_dados(dados)
            return
    raise ValueError(f"Usuário {id_usuario} não encontrado.")


def obter_estatisticas() -> dict:
    """Retorna um resumo estatístico dos usuários cadastrados."""
    usuarios = listar_usuarios()
    if not usuarios:
        return {}

    stats = {
        "total": len(usuarios),
        "por_status": {},
        "por_perfil": {},
        "por_faixa_etaria": {},
        "por_shopping": {},
        "por_genero": {},
    }

    for u in usuarios:
        for campo, chave in [
            ("status", "por_status"),
            ("perfil", "por_perfil"),
            ("faixa_etaria", "por_faixa_etaria"),
            ("shopping_principal", "por_shopping"),
            ("genero", "por_genero"),
        ]:
            val = u.get(campo, "desconhecido")
            stats[chave][val] = stats[chave].get(val, 0) + 1

    return stats


# ─────────────────────────────────────────
#  MENU INTERATIVO (TERMINAL)
# ─────────────────────────────────────────

def menu():
    """Menu interativo para testar o CRUD no terminal."""
    while True:
        print("\n" + "═" * 50)
        print("   SHOPCONTROL — Gerenciamento de Usuários")
        print("═" * 50)
        print("  1. Cadastrar novo usuário")
        print("  2. Listar todos os usuários")
        print("  3. Buscar usuário (ID / CPF / e-mail)")
        print("  4. Atualizar usuário")
        print("  5. Deletar usuário")
        print("  6. Ver estatísticas")
        print("  0. Sair")
        print("═" * 50)
        opcao = input("  Escolha: ").strip()

        if opcao == "1":
            print("\n── Cadastrar Usuário ──")
            nome     = input("Nome completo: ")
            cpf      = input("CPF (somente números): ")
            email    = input("E-mail: ")
            senha    = input("Senha: ")
            print(f"Perfis: {PERFIS_USUARIO}")
            perfil   = input("Perfil: ")
            idade    = int(input("Idade: "))
            print(f"Gênero: {GENEROS}")
            genero   = input("Gênero: ")
            print(f"Shoppings: {SHOPPINGS}")
            shopping = input("Shopping principal: ")
            loja     = input("Loja (deixe em branco se não aplicável): ") or None
            try:
                u = criar_usuario(nome, cpf, email, senha, perfil, idade, genero, shopping, loja=loja)
                print(f"\n✅ Cadastrado! ID: {u['id']}")
            except ValueError as e:
                print(f"\n❌ Erro: {e}")

        elif opcao == "2":
            print("\n── Lista de Usuários ──")
            usuarios = listar_usuarios()
            if not usuarios:
                print("Nenhum usuário cadastrado.")
            for u in usuarios:
                print(f"  [{u['id']}] {u['nome']} | {u['perfil']} | {u['faixa_etaria']} | {u['status']} | {u['shopping_principal']}")

        elif opcao == "3":
            termo = input("\nDigite ID, CPF ou e-mail: ")
            u = buscar_usuario(termo)
            if u:
                print(json.dumps(u, ensure_ascii=False, indent=2))
            else:
                print("❌ Usuário não encontrado.")

        elif opcao == "4":
            id_u = input("\nID do usuário: ").strip().upper()
            print("Campos editáveis: nome, email, perfil, status, shopping_principal, loja, telefone, observacoes")
            campo = input("Campo a editar: ").strip()
            valor = input("Novo valor: ").strip()
            try:
                atualizar_usuario(id_u, **{campo: valor})
            except ValueError as e:
                print(f"❌ Erro: {e}")

        elif opcao == "5":
            id_u = input("\nID do usuário a deletar: ").strip().upper()
            confirma = input(f"Confirma deletar {id_u}? (s/n): ")
            if confirma.lower() == "s":
                deletar_usuario(id_u)

        elif opcao == "6":
            stats = obter_estatisticas()
            print("\n── Estatísticas ──")
            print(json.dumps(stats, ensure_ascii=False, indent=2))

        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
