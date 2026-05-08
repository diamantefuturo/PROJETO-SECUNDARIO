"""
=============================================================
  MÓDULO 1 - CONTROLE DE ACESSO
  Arquivo: __init__.py
  Torna a pasta 'Controle de Acesso' um pacote Python.
=============================================================
"""

from .usuarios import (
    criar_usuario,
    listar_usuarios,
    buscar_usuario,
    atualizar_usuario,
    deletar_usuario,
    registrar_visita,
    obter_estatisticas,
)

from .modulos_sistema import (
    criar_modulo,
    listar_modulos,
    buscar_modulo,
    atualizar_modulo,
    deletar_modulo,
    verificar_acesso,
    inicializar_modulos_padrao,
)

from .ambientes import (
    criar_ambiente,
    listar_ambientes,
    buscar_ambiente,
    atualizar_ambiente,
    deletar_ambiente,
    adicionar_loja_ao_ambiente,
    atualizar_monitoramento,
    obter_estatisticas_ambientes,
    inicializar_ambientes_padrao,
)
