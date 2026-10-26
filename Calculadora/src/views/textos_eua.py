"""Textos que mudam quando o país é EUA: unidades americanas e exemplos com números de lá.

O txt() do comum.py procura aqui primeiro quando o país é EUA. O que não estiver aqui
vem do TEXTOS normal, então o Brasil continua igual.

Nos próximos passos, os textos das abas adaptadas (CMU, Romex, PEX...) e das abas novas
(montantes, drywall) também entram aqui.

Os exemplos usam ponto como decimal, porque nos EUA o separador é o ponto.
"""

TEXTOS_EUA = {
    "pt": {
        # --- Brocas e Baldrame ---
        "hint_prof": "Profundidade média em ft (ex: 10)",
        "hint_diam": "Diâmetro em in (ex: 12)",
        "hint_esp_estribo": "Espaçamento dos estribos em in (ex: 8)",
        "hint_mo": "Mão de obra por ft (opcional, ex: 8.00)",
        "hint_comprimento": "Comprimento total em ft (ex: 40)",
        "hint_largura": "Largura da viga em in (ex: 8)",
        "hint_altura": "Altura da viga em in (ex: 12)",
        "ajuda_brocas": "Informe a quantidade de brocas, o diâmetro (ex.: 12 in) e a profundidade média de cada uma. Se quiser, inclua a armadura. O app estima o concreto e o ferro necessários.\n\nOs estribos só entram se você informar as barras. Para não incluir estribos, deixe o espaçamento em branco.",
        # --- Paredes e Reboco ---
        "hint_area_parede": "Área bruta das paredes em sq ft (ex: 320)",
        "hint_vaos": "Portas e janelas em sq ft (opcional, ex: 50)",
        "hint_junta": "Espessura da junta em in (opcional, ex: 3/8)",
        "hint_area_reboco": "Área a rebocar em sq ft (ex: 320)",
        "hint_esp_reboco": "Espessura do reboco em in (ex: 3/4)",
        # --- Laje e Telhado ---
        "hint_area_laje": "Área da laje em sq ft (ex: 540)",
        "hint_capa_laje": "Capa de concreto em in (opcional, ex: 1 1/2)",
        "hint_esp_laje": "Espessura total da laje em in (ex: 4)",
        "hint_area_telhado": "Área do telhado em planta, em sq ft (ex: 860)",
        "hint_cumeeira": "Cumeeira em ft (opcional, ex: 30)",
        "ajuda_telhado": "Informe a área do telhado e o tipo de telha. Se quiser, inclua a inclinação, a cumeeira e o madeiramento.\n\nA área é a da planta (vista de cima, com os beirais). O app corrige pela inclinação.\n\nCumeeira é a linha do alto do telhado, onde as duas águas se encontram. Informe o comprimento dela em ft (no telhado de quatro águas, some também as quinas inclinadas). Telhado de uma água não tem cumeeira.",
        # --- Elétrica e Hidráulica (bitolas e diâmetros americanos entram no passo 2) ---
        "hint_conduite": "Conduíte em ft (opcional, ex: 500)",
        "hint_fio": "Fio {b} mm² em ft (opcional)",
        "hint_tubo_fria": "Água fria 25 mm, em ft",
        "hint_tubo_quente": "Água quente 22 mm, em ft",
        "hint_tubo_esg40": "Esgoto 40 mm, em ft",
        "hint_tubo_esg100": "Esgoto 100 mm, em ft",
        # --- Contrapiso, Piso, Azulejo e Rejunte ---
        "hint_area_contrapiso": "Área do contrapiso em sq ft (ex: 430)",
        "hint_esp_contrapiso": "Espessura média em in (ex: 2)",
        "hint_area_piso": "Área do piso em sq ft (ex: 430)",
        "hint_area_azulejo": "Área de parede a revestir em sq ft (ex: 320)",
        "hint_larg_peca": "Largura da peça em in (ex: 12)",
        "hint_alt_peca": "Altura da peça em in (ex: 12)",
        "hint_m2_caixa": "sq ft por caixa (opcional, ex: 15)",
        "hint_rodape": "Rodapé em ft (opcional, ex: 65)",
        "dica_area_contrapiso": "Usar a área do Contrapiso: {area} sq ft",
        "ajuda_piso": "Informe a área e o tamanho da peça (ex.: 12x12 in). Se quiser, inclua os sq ft por caixa, o tipo de argamassa e o rodapé. O app estima as caixas e os sacos de argamassa.",
        "ajuda_azulejo": "Informe a área de parede a revestir e o tamanho da peça. Desconte portas e janelas e, se quiser, informe os sq ft por caixa e o tipo de argamassa (AC-III para áreas molhadas).",
        "hint_area_rejunte": "Área a rejuntar em sq ft (ex: 430)",
        "hint_junta_mm": "Largura da junta em in (ex: 1/8)",
        "hint_esp_peca": "Espessura da peça em in (opcional, ex: 5/16)",
        "dica_rejunte_piso": "Dica: no Piso você usou {area} sq ft, peça {peca} in",
        "dica_rejunte_azulejo": "Dica: no Azulejo você usou {area} sq ft, peça {peca} in",
        "ajuda_rejunte": "Informe a área, o tamanho da peça e a largura da junta. Se você já preencheu Piso ou Azulejo, os dados deles aparecem como dica no topo da aba. A espessura da peça é opcional (padrão 5/16 in). O app estima os kg de rejunte e quantas latinhas de 1 kg e 2 kg comprar.",
        # --- Pintura ---
        "hint_area_parede_pint": "Área de parede em sq ft (ex: 1000)",
        "hint_area_teto_pint": "Área de teto em sq ft (ex: 430)",
        "hint_rendimento": "Rendimento em sq ft/gal (opcional, ex: 400)",
        "ajuda_pintura": "Informe a área de parede, a área de teto e o número de demãos. O rendimento da tinta já vem preenchido. Se quiser, inclua selador, massa corrida e fundo preparador.\n\nPode preencher só a parede ou só o teto. O rendimento é quantos sq ft 1 galão de tinta pinta em uma demão (veja na lata).\n\nMassa corrida é para áreas internas secas; massa acrílica, para áreas externas ou úmidas.",
        # --- Esquadrias ---
        "hint_larg_esquadria": "Largura do vão em in (ex: 36)",
        "hint_alt_esquadria": "Altura do vão em in (ex: 80)",
        # --- Legenda das siglas (só em português; aparece no fim do "?") ---
        "legenda_unidades": "Siglas: ft = pés · in = polegadas · sq ft = pés quadrados · cu yd = jardas cúbicas · lb = libras · gal = galões",
    },
    "en": {
        # --- Drilled shafts and grade beam ---
        "hint_prof": "Average depth, ft (ex: 10)",
        "hint_diam": "Diameter, in (ex: 12)",
        "hint_esp_estribo": "Stirrup spacing, in (ex: 8)",
        "hint_mo": "Labor cost per ft (optional, ex: 8.00)",
        "hint_comprimento": "Total length, ft (ex: 40)",
        "hint_largura": "Beam width, in (ex: 8)",
        "hint_altura": "Beam height, in (ex: 12)",
        "ajuda_brocas": "Enter the number of piles, the diameter (e.g. 12 in) and the average depth of each one. If you like, add the rebar. The app estimates the concrete and steel needed.\n\nStirrups are only included if you enter the bars. To leave stirrups out, keep the spacing empty.",
        # --- Walls and plaster ---
        "hint_area_parede": "Gross wall area, sq ft (ex: 320)",
        "hint_vaos": "Doors and windows, sq ft (optional, ex: 50)",
        "hint_junta": "Joint thickness, in (optional, ex: 3/8)",
        "hint_area_reboco": "Area to plaster, sq ft (ex: 320)",
        "hint_esp_reboco": "Plaster thickness, in (ex: 3/4)",
        # --- Slab and roof ---
        "hint_area_laje": "Slab area, sq ft (ex: 540)",
        "hint_capa_laje": "Topping thickness, in (optional, ex: 1 1/2)",
        "hint_esp_laje": "Total slab thickness, in (ex: 4)",
        "hint_area_telhado": "Roof plan area, sq ft (ex: 860)",
        "hint_cumeeira": "Ridge, ft (optional, ex: 30)",
        "ajuda_telhado": "Enter the roof area and the tile type. If you like, add the slope, ridge and timber framing.\n\nThe area is the plan area (seen from above, including eaves). The app adjusts it for the slope.\n\nThe ridge is the top line of the roof, where the two slopes meet. Enter its length in ft (on a hip roof, also add the sloped hips). A single-slope roof has no ridge.",
        # --- Electrical and plumbing (US wire gauges and pipe sizes come in step 2) ---
        "hint_conduite": "Conduit, ft (optional, ex: 500)",
        "hint_fio": "Wire {b} mm², ft (optional)",
        "hint_tubo_fria": "Cold water 25 mm, ft",
        "hint_tubo_quente": "Hot water 22 mm, ft",
        "hint_tubo_esg40": "Drain 40 mm, ft",
        "hint_tubo_esg100": "Drain 100 mm, ft",
        # --- Subfloor, floor, wall tile and grout ---
        "hint_area_contrapiso": "Subfloor area, sq ft (ex: 430)",
        "hint_esp_contrapiso": "Average thickness, in (ex: 2)",
        "hint_area_piso": "Floor area, sq ft (ex: 430)",
        "hint_area_azulejo": "Wall area to tile, sq ft (ex: 320)",
        "hint_larg_peca": "Tile width, in (ex: 12)",
        "hint_alt_peca": "Tile height, in (ex: 12)",
        "hint_m2_caixa": "sq ft per box (optional, ex: 15)",
        "hint_rodape": "Baseboard, ft (optional, ex: 65)",
        "dica_area_contrapiso": "Use the Subfloor area: {area} sq ft",
        "ajuda_piso": "Enter the area and the tile size (e.g. 12x12 in). If you like, add the sq ft per box, the adhesive type and the baseboard. The app estimates boxes and bags of tile adhesive.",
        "ajuda_azulejo": "Enter the wall area to tile and the tile size. Deduct doors and windows and, if you like, enter the sq ft per box and the adhesive type (AC-III for wet areas).",
        "hint_area_rejunte": "Area to grout, sq ft (ex: 430)",
        "hint_junta_mm": "Joint width, in (ex: 1/8)",
        "hint_esp_peca": "Tile thickness, in (optional, ex: 5/16)",
        "dica_rejunte_piso": "Tip: in Floor you used {area} sq ft, tile {peca} in",
        "dica_rejunte_azulejo": "Tip: in Wall Tile you used {area} sq ft, tile {peca} in",
        "ajuda_rejunte": "Enter the area, the tile size and the joint width. If you already filled in Floor or Wall Tile, their data appears as a tip at the top of the tab. Tile thickness is optional (default 5/16 in). The app estimates the kg of grout and how many 1 kg and 2 kg tubs to buy.",
        # --- Painting ---
        "hint_area_parede_pint": "Wall area, sq ft (ex: 1000)",
        "hint_area_teto_pint": "Ceiling area, sq ft (ex: 430)",
        "hint_rendimento": "Coverage, sq ft/gal (optional, ex: 400)",
        "ajuda_pintura": "Enter the wall area, ceiling area and number of coats. Paint coverage is already filled in. If you like, add sealer, wall putty and primer.\n\nYou can fill in only walls or only ceiling. Coverage is how many sq ft 1 gallon of paint covers in one coat (see the can).\n\nWall putty is for dry indoor areas; acrylic putty, for outdoor or damp areas.",
        # --- Doors and windows ---
        "hint_larg_esquadria": "Opening width, in (ex: 36)",
        "hint_alt_esquadria": "Opening height, in (ex: 80)",
    },
}