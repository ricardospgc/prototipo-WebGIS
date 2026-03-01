import folium
from branca.element import Template, MacroElement

# Deixa a interface mais funcional e bonita
def otimizar_interface(fmap):
    template = """
    {% macro script(this, kwargs) %}
    var style = document.createElement('style');
    style.innerHTML = `
        .leaflet-control-layers-expanded {
            max-height: 250px !important;
            overflow-y: auto !important;
            width: 200px !important;
        }
        .toggle-btn {
            width: 100%;
            margin-bottom: 8px;
            background: #28a745;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
            font-weight: bold;
        }
    `;
    document.head.appendChild(style);

    var container = document.querySelector('.leaflet-control-layers-list');
    var btn = document.createElement('button');
    btn.innerHTML = 'Alternar Equipamentos';
    btn.className = 'toggle-btn';
    
    btn.onclick = function() {
        // Seleciona todos os itens do menu
        var overlays = container.querySelectorAll('.leaflet-control-layers-overlays label');
        
        // Verifica se algum item (que não seja o limite fixo) está marcado
        var anyChecked = Array.from(overlays).some(label => {
            var isFixed = label.innerText.includes('Limite') || label.innerText.includes('Fixo');
            var input = label.querySelector('input');
            return !isFixed && input.checked;
        });

        overlays.forEach(label => {
            var text = label.innerText;
            var input = label.querySelector('input');
            
            // Lógica: Se for o Limite, NÃO clica. 
            // Para os outros, clica para igualar o estado (todos on ou todos off)
            if (!text.includes('Limite') && !text.includes('Fixo')) {
                if (anyChecked && input.checked) {
                    input.click();
                } else if (!anyChecked && !input.checked) {
                    input.click();
                }
            }
        });
    };
    container.prepend(btn);
    {% endmacro %}
    """
    macro = MacroElement()
    macro._template = Template(template)
    fmap.add_child(macro)
    return fmap

# Dicionário com os tipos de equipamentos e os estilos do marcador
def obter_estilo_por_tipo():
    """
    Retorna um dicionário de mapeamento para ícones e cores dos marcadores
    """
    return {
        'CAMPO DE FUTEBOL':        {'cor': 'lightgreen',  'icon': 'soccer-ball', 'prefix': 'fa','sufix': 'o'},
        'CAMPO DE FUTEBOL SOCIETY':{'cor': 'darkgreen', 'icon': 'soccer-ball', 'prefix': 'fa','sufix': 'o'},
        'QUADRA DE FUTSAL':        {'cor': 'green', 'icon': 'soccer-ball', 'prefix': 'fa','sufix': 'o'},
        'QUADRA DE VÔLEI':         {'cor': 'lightblue', 'icon': 'hand-paper', 'prefix': 'fa', 'sufix': 'o'},
        'QUADRA POLIESPORTIVA':    {'cor': 'blue',   'icon': 'trophy',        'prefix': 'fa'},
        'ACADEMIA A CÉU ABERTO':   {'cor': 'red',    'icon': 'heartbeat',     'prefix': 'fa'},
        'PISTA DE SKATE':          {'cor': 'orange', 'icon': 'road',          'prefix': 'fa'},
        'GINÁSIO':                 {'cor': 'purple', 'icon': 'building',      'prefix': 'fa'},
        'QUADRA DE PETECA':        {'cor': 'beige', 'icon': 'rocket',      'prefix': 'fa'},
        'QUADRA RECREATIVA':       {'cor': 'lightred', 'icon': 'bolt',      'prefix': 'fa'},
        
        'PADRAO':                  {'cor': 'gray',   'icon': 'info-sign',     'prefix': 'glyphicon'}
    }

# Alternar entre camadas do OpenStreetMap e satélite
def configurar_camadas_base(fmap):
    folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(fmap)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Satélite (Esri)', overlay=False
    ).add_to(fmap)
    return fmap

# Criação dos marcadores
def criar_marcador_esportivo(row, estilos):
    """
    Usa o dicionário de estilos para montar o marcador.
    """
    tipo = str(row['TIPO']).upper()
    
    # Busca o estilo ou usa o PADRAO se não encontrar
    estilo = estilos.get(tipo, estilos['PADRAO'])

    return folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=folium.Popup(f"<b>{row['NOME']}</b><br>Tipo: {row['TIPO']}", max_width=300),
        icon=folium.Icon(color=estilo['cor'], icon=estilo['icon'], prefix=estilo['prefix'])
    )