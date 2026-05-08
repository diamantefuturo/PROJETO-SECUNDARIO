"""
=============================================================
  MÓDULO 1 - CONTROLE DE ACESSO
  Arquivo: modulos_sistema.py
  Descrição: CRUD de módulos do sistema ShopControl
             Define quais módulos existem e quem tem acesso
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
ARQUIVO_JSON = os.path.join(BASE_DIR, "dados", "modulos_sistema.json")


# ─────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────

PERFIS_COM_ACESSO = [
    "visitante",
    "funcionario_loja",
    "dono_loja",
    "funcionario_shopping",
    "seguranca",
    "administrador",
]

STATUS_MODULO = ["ativo", "inativo", "em_manutencao"]

# Módulos padrão do sistema (serão criados na inicialização)
MODULOS_PADRAO = [
    {
        "nome": "Controle de Acesso",
        "codigo": "MOD_ACESSO",
        "descricao": "Gerenciamento de usuários, perfis e permissões do sistema.",
        "icone": "🔐",
        "perfis_autorizados": ["administrador"],
    },
    {
        "nome": "Gerenciamento de Equipamentos",
        "codigo": "MOD_EQUIP",
        "descricao": "Cadastro e distribuição de câmeras, sensores e outros equipamentos.",
        "icone": "📷",
        "perfis_autorizados": ["administrador", "funcionario_shopping"],
    },
    {
        "nome": "Monitoramento de Ambientes",
        "codigo": "MOD_MONITOR",
        "descricao": "Monitoramento em tempo real de prédios e estacionamentos via câmeras e IA.",
        "icone": "🏢",
        "perfis_autorizados": ["administrador", "funcionario_shopping", "seguranca"],
    },
    {
        "nome": "Auditoria",
        "codigo": "MOD_AUDIT",
        "descricao": "Registros de eventos, logs e relatórios de auditoria do sistema.",
        "icone": "📋",
        "perfis_autorizados": ["administrador", "funcionario_shopping"],
    },
    {
        "nome": "Análise e Mapa de Calor",
        "codigo": "MOD_CALOR",
        "descricao": "Geração de mapas de calor e análise de fluxo de pessoas nos shoppings.",
        "icone": "🔥",
        "perfis_autorizados": ["administrador", "dono_loja", "funcionario_shopping"],
    },
    {
        "nome": "Controle de Estacionamento",
        "codigo": "MOD_ESTAC",
        "descricao": "Monitoramento de vagas, leitura de placas e controle de entrada/saída de veículos.",
        "icone": "🚗",
        "perfis_autorizados": ["administrador", "funcionario_shopping", "seguranca"],
    },
    {
        "nome": "Perfis de Visitantes",
        "codigo": "MOD_PERFIL",
        "descricao": "Visualização de perfis comportamentais e preferências dos visitantes.",
        "icone": "👤",
        "perfis_autorizados": ["administrador", "dono_loja", "funcionario_shopping"],
    },
    {
        "nome": "Dashboard",
        "codigo": "MOD_DASH",
        "descricao": "Painel principal com visão geral e métricas em tempo real.",
        "icone": "📊",
        "perfis_autorizados": ["administrador", "dono_loja", "funcionario_shopping", "seguranca"],
    },
]


# ─────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────

def _carregar_dados() -> dict:
    if not os.path.exists(ARQUIVO_JSON):
        return {"metadados": _metadados_inicial(), "modulos": []}
    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_dados(dados: dict):
    os.makedirs(os.path.dirname(ARQUIVO_JSON), exist_ok=True)
    dados["metadados"]["ultima_atualizacao"] = datetime.now().isoformat()
    dados["metadados"]["total_modulos"] = len(dados["modulos"])
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def _metadados_inicial() -> dict:
    return {
        "criado_em": datetime.now().isoformat(),
        "total_modulos": 0,
        "versao": "1.0",
        "ultima_atualizacao": datetime.now().isoformat(),
    }


def _gerar_id() -> str:
    return uuid.uuid4().hex[:8].upper()


def _codigo_existe(codigo: str, dados: dict, ignorar_id: str = None) -> bool:
    for m in dados["modulos"]:
        if m["codigo"] == codigo.upper() and m["id"] != ignorar_id:
            return True
    return False


# ─────────────────────────────────────────
#  C R U D
# ─────────────────────────────────────────

def criar_modulo(
    nome: str,
    codigo: str,
    descricao: str,
    perfis_autorizados: list,
    icone: str = "📦",
    dependencias: list = None,
) -> dict:
    """
    Cadastra um novo módulo do sistema.
    perfis_autorizados: lista de perfis que podem acessar este módulo.
    dependencias: lista de códigos de outros módulos necessários.
    """
    codigo = codigo.upper()

    # Validações
    for p in perfis_autorizados:
        if p not in PERFIS_COM_ACESSO:
            raise ValueError(f"Perfil inválido: '{p}'. Opções: {PERFIS_COM_ACESSO}")

    dados = _carregar_dados()

    if _codigo_existe(codigo, dados):
        raise ValueError(f"Código '{codigo}' já cadastrado.")

    modulo = {
        "id": _gerar_id(),
        "nome": nome,
        "codigo": codigo,
        "descricao": descricao,
        "icone": icone,
        "perfis_autorizados": perfis_autorizados,
        "dependencias": dependencias or [],     # outros módulos necessários
        "status": "ativo",
        "data_criacao": datetime.now().isoformat(),
        "ultima_atualizacao": datetime.now().isoformat(),
        "versao_modulo": "1.0",
        "configuracoes": {},                    # configurações específicas do módulo
    }

    dados["modulos"].append(modulo)
    _salvar_dados(dados)
    print(f"✅ Módulo '{nome}' criado com código {codigo}.")
    return modulo


def listar_modulos(
    filtro_status: str = None,
    filtro_perfil: str = None,
) -> list:
    """
    Lista módulos com filtros opcionais.
    filtro_perfil: retorna só os módulos acessíveis por aquele perfil.
    """
    dados = _carregar_dados()
    modulos = dados["modulos"]

    if filtro_status:
        modulos = [m for m in modulos if m["status"] == filtro_status]
    if filtro_perfil:
        modulos = [m for m in modulos if filtro_perfil in m["perfis_autorizados"]]

    return modulos


def buscar_modulo(identificador: str) -> dict | None:
    """Busca por ID ou código do módulo."""
    dados = _carregar_dados()
    for m in dados["modulos"]:
        if m["id"] == identificador.upper() or m["codigo"] == identificador.upper():
            return m
    return None


def atualizar_modulo(id_modulo: str, **campos) -> dict:
    """Atualiza campos de um módulo existente."""
    dados = _carregar_dados()
    for i, m in enumerate(dados["modulos"]):
        if m["id"] == id_modulo.upper():
            campos_protegidos = {"id", "data_criacao"}
            for campo, valor in campos.items():
                if campo in campos_protegidos:
                    continue
                if campo == "status" and valor not in STATUS_MODULO:
                    raise ValueError(f"Status inválido. Opções: {STATUS_MODULO}")
                dados["modulos"][i][campo] = valor
            dados["modulos"][i]["ultima_atualizacao"] = datetime.now().isoformat()
            _salvar_dados(dados)
            print(f"✅ Módulo {id_modulo} atualizado.")
            return dados["modulos"][i]
    raise ValueError(f"Módulo '{id_modulo}' não encontrado.")


def deletar_modulo(id_modulo: str) -> bool:
    """Remove um módulo pelo ID."""
    dados = _carregar_dados()
    antes = len(dados["modulos"])
    dados["modulos"] = [m for m in dados["modulos"] if m["id"] != id_modulo.upper()]
    if len(dados["modulos"]) < antes:
        _salvar_dados(dados)
        print(f"🗑️  Módulo {id_modulo} removido.")
        return True
    print(f"❌ Módulo {id_modulo} não encontrado.")
    return False


def verificar_acesso(codigo_modulo: str, perfil_usuario: str) -> bool:
    """
    Verifica se um perfil de usuário tem acesso a determinado módulo.
    Usado pelo sistema de login para controlar o que cada usuário vê.
    """
    modulo = buscar_modulo(codigo_modulo)
    if not modulo:
        return False
    if modulo["status"] != "ativo":
        return False
    return perfil_usuario in modulo["perfis_autorizados"]


def inicializar_modulos_padrao():
    """
    Cria os módulos padrão do sistema se ainda não existirem.
    Chamado uma vez na primeira execução do sistema.
    """
    dados = _carregar_dados()
    existentes = {m["codigo"] for m in dados["modulos"]}
    criados = 0
    for m in MODULOS_PADRAO:
        if m["codigo"] not in existentes:
            criar_modulo(
                nome=m["nome"],
                codigo=m["codigo"],
                descricao=m["descricao"],
                perfis_autorizados=m["perfis_autorizados"],
                icone=m["icone"],
            )
            criados += 1
    if criados:
        print(f"\n✅ {criados} módulos padrão inicializados.")
    else:
        print("ℹ️  Módulos padrão já existem.")


# ─────────────────────────────────────────
#  MENU INTERATIVO
# ─────────────────────────────────────────

def menu():
    while True:
        print("\n" + "═" * 50)
        print("   SHOPCONTROL — Gerenciamento de Módulos")
        print("═" * 50)
        print("  1. Criar módulo")
        print("  2. Listar módulos")
        print("  3. Buscar módulo (ID ou código)")
        print("  4. Atualizar módulo")
        print("  5. Deletar módulo")
        print("  6. Verificar acesso de perfil")
        print("  7. Inicializar módulos padrão do sistema")
        print("  0. Sair")
        print("═" * 50)
        opcao = input("  Escolha: ").strip()

        if opcao == "1":
            nome    = input("Nome do módulo: ")
            codigo  = input("Código (ex: MOD_MAPA): ")
            desc    = input("Descrição: ")
            print(f"Perfis: {PERFIS_COM_ACESSO}")
            perfis  = input("Perfis autorizados (separados por vírgula): ").split(",")
            perfis  = [p.strip() for p in perfis]
            try:
                criar_modulo(nome, codigo, desc, perfis)
            except ValueError as e:
                print(f"❌ {e}")

        elif opcao == "2":
            modulos = listar_modulos()
            for m in modulos:
                print(f"  {m['icone']} [{m['codigo']}] {m['nome']} | {m['status']} | perfis: {m['perfis_autorizados']}")

        elif opcao == "3":
            termo = input("ID ou código: ").strip()
            m = buscar_modulo(termo)
            print(json.dumps(m, ensure_ascii=False, indent=2) if m else "❌ Não encontrado.")

        elif opcao == "4":
            id_m   = input("ID do módulo: ").strip().upper()
            campo  = input("Campo a editar: ").strip()
            valor  = input("Novo valor: ").strip()
            try:
                atualizar_modulo(id_m, **{campo: valor})
            except ValueError as e:
                print(f"❌ {e}")

        elif opcao == "5":
            id_m = input("ID do módulo a deletar: ").strip().upper()
            if input(f"Confirma deletar {id_m}? (s/n): ").lower() == "s":
                deletar_modulo(id_m)

        elif opcao == "6":
            codigo = input("Código do módulo: ").strip().upper()
            perfil = input("Perfil do usuário: ").strip()
            ok = verificar_acesso(codigo, perfil)
            print(f"{'✅ Acesso PERMITIDO' if ok else '❌ Acesso NEGADO'}")

        elif opcao == "7":
            inicializar_modulos_padrao()

        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
