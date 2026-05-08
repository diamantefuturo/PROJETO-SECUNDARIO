"""
=============================================================
  SHOPCONTROL — Inicializador do Sistema
  Arquivo: inicializar.py
  Descrição: Popula os 3 JSONs do Módulo 1 com dados reais
             de exemplo para demonstração e testes.
  
  ⚠️  Rode este arquivo UMA VEZ para preparar o sistema.
      Após isso, use os menus de cada módulo ou o dashboard.
=============================================================
"""

import sys
import os

# Garante que o Python encontra os módulos na pasta correta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime

# ── Importa as funções dos 3 módulos ────────────────────────
from usuarios           import criar_usuario
from modulos_sistema    import inicializar_modulos_padrao
from ambientes          import inicializar_ambientes_padrao, adicionar_loja_ao_ambiente, buscar_ambiente

print("=" * 60)
print("  SHOPCONTROL — Inicializando Módulo 1")
print("=" * 60)


# ─────────────────────────────────────────
#  1. MÓDULOS DO SISTEMA
# ─────────────────────────────────────────
print("\n📦 Criando módulos do sistema...")
inicializar_modulos_padrao()


# ─────────────────────────────────────────
#  2. AMBIENTES (PRÉDIOS / SETORES)
# ─────────────────────────────────────────
print("\n🏢 Criando ambientes dos 4 shoppings...")
inicializar_ambientes_padrao()

# Adiciona algumas lojas de exemplo nos ambientes
print("\n🏪 Adicionando lojas de exemplo...")
try:
    # Busca o corredor do Shopping Norte e adiciona lojas
    corredor = buscar_ambiente("Shopping Norte — Corredor Principal L1")
    if corredor:
        adicionar_loja_ao_ambiente(corredor["id"], "Renner",       "moda",        800.0)
        adicionar_loja_ao_ambiente(corredor["id"], "Riachuelo",    "moda",        750.0)
        adicionar_loja_ao_ambiente(corredor["id"], "Magazine Luiza","tecnologia",  600.0)
        adicionar_loja_ao_ambiente(corredor["id"], "Cacau Show",   "alimentação", 80.0)
except Exception as e:
    print(f"  ⚠️  {e}")


# ─────────────────────────────────────────
#  3. USUÁRIOS
# ─────────────────────────────────────────
print("\n👥 Criando usuários de exemplo...")

usuarios_exemplo = [
    # Administradores
    dict(nome="Ana Paula Silva",   cpf="11111111111", email="ana.admin@shopcontrol.com",
         senha="admin@2024",       perfil="administrador",        idade=34,
         genero="feminino",        shopping_principal="Shopping Norte",
         outros_shoppings=["Shopping Sul", "Shopping Leste", "Shopping Oeste"],
         observacoes="Administradora geral do sistema"),

    dict(nome="Ricardo Moura",     cpf="22222222222", email="ricardo.admin@shopcontrol.com",
         senha="admin@2024",       perfil="administrador",        idade=41,
         genero="masculino",       shopping_principal="Shopping Sul",
         outros_shoppings=["Shopping Norte"],
         observacoes="Administrador Shopping Sul e Norte"),

    # Funcionários do Shopping
    dict(nome="Carlos Lima",       cpf="33333333333", email="carlos.func@shopnorte.com",
         senha="func@2024",        perfil="funcionario_shopping", idade=28,
         genero="masculino",       shopping_principal="Shopping Norte",
         loja=None,
         observacoes="Supervisor de operações"),

    dict(nome="Fernanda Rocha",    cpf="44444444444", email="fernanda.func@shopsul.com",
         senha="func@2024",        perfil="funcionario_shopping", idade=32,
         genero="feminino",        shopping_principal="Shopping Sul",
         observacoes="Coordenadora de atendimento"),

    # Segurança
    dict(nome="Marcos Oliveira",   cpf="55555555555", email="marcos.seg@shopcontrol.com",
         senha="seg@2024",         perfil="seguranca",            idade=45,
         genero="masculino",       shopping_principal="Shopping Norte",
         outros_shoppings=["Shopping Leste"],
         observacoes="Chefe de segurança"),

    dict(nome="Patrícia Santos",   cpf="66666666666", email="patricia.seg@shopcontrol.com",
         senha="seg@2024",         perfil="seguranca",            idade=30,
         genero="feminino",        shopping_principal="Shopping Oeste",
         observacoes="Analista de monitoramento"),

    # Donos de loja
    dict(nome="João Ferreira",     cpf="77777777777", email="joao@renner.com.br",
         senha="loja@2024",        perfil="dono_loja",            idade=52,
         genero="masculino",       shopping_principal="Shopping Norte",
         loja="Renner",
         observacoes="Gerente/proprietário Renner Shopping Norte"),

    dict(nome="Mariana Costa",     cpf="88888888888", email="mariana@cacaushow.com.br",
         senha="loja@2024",        perfil="dono_loja",            idade=38,
         genero="feminino",        shopping_principal="Shopping Norte",
         loja="Cacau Show",
         observacoes="Franqueada Cacau Show"),

    # Funcionários de loja
    dict(nome="Lucas Pereira",     cpf="99999999901", email="lucas.func@renner.com",
         senha="func@2024",        perfil="funcionario_loja",     idade=22,
         genero="masculino",       shopping_principal="Shopping Norte",
         loja="Renner",
         observacoes="Vendedor Renner"),

    dict(nome="Isabela Mendes",    cpf="99999999902", email="isabela.func@magalu.com",
         senha="func@2024",        perfil="funcionario_loja",     idade=25,
         genero="feminino",        shopping_principal="Shopping Norte",
         loja="Magazine Luiza",
         observacoes="Vendedora Magazine Luiza"),

    # Visitantes — diferentes perfis etários
    dict(nome="Rafael Souza",      cpf="99999999903", email="rafael.s@gmail.com",
         senha="user@2024",        perfil="visitante",            idade=19,
         genero="masculino",       shopping_principal="Shopping Norte",
         outros_shoppings=["Shopping Sul"],
         observacoes="Frequentador assíduo — vai 3x por semana"),

    dict(nome="Beatriz Alves",     cpf="99999999904", email="beatriz.a@gmail.com",
         senha="user@2024",        perfil="visitante",            idade=16,
         genero="feminino",        shopping_principal="Shopping Leste",
         observacoes="Adolescente — frequenta fins de semana"),

    dict(nome="José Gonçalves",    cpf="99999999905", email="jose.g@gmail.com",
         senha="user@2024",        perfil="visitante",            idade=67,
         genero="masculino",       shopping_principal="Shopping Sul",
         observacoes="Idoso — frequenta pela manhã"),

    dict(nome="Camila Torres",     cpf="99999999906", email="camila.t@gmail.com",
         senha="user@2024",        perfil="visitante",            idade=35,
         genero="feminino",        shopping_principal="Shopping Oeste",
         outros_shoppings=["Shopping Norte"],
         observacoes="Adulta — foco em compras de moda"),

    dict(nome="Pedro Nascimento",  cpf="99999999907", email="pedro.n@gmail.com",
         senha="user@2024",        perfil="visitante",            idade=10,
         genero="masculino",       shopping_principal="Shopping Norte",
         observacoes="Criança — acompanhado dos pais"),
]

criados = 0
for u in usuarios_exemplo:
    try:
        criar_usuario(**u)
        criados += 1
    except ValueError as e:
        print(f"  ⚠️  {u['nome']}: {e}")

print(f"\n✅ {criados}/{len(usuarios_exemplo)} usuários criados.")


# ─────────────────────────────────────────
#  RESUMO FINAL
# ─────────────────────────────────────────
print("\n" + "=" * 60)
print("  ✅ Módulo 1 inicializado com sucesso!")
print("=" * 60)
print("\n📁 Arquivos JSON gerados em /dados/:")
print("   • usuarios.json         → 15 usuários")
print("   • modulos_sistema.json  → 8 módulos")
print("   • ambientes.json        → 12 ambientes + lojas")
print("\n▶️  Como usar:")
print('   python usuarios.py         → menu de usuários')
print('   python modulos_sistema.py  → menu de módulos')
print('   python ambientes.py        → menu de ambientes')
print("=" * 60)
