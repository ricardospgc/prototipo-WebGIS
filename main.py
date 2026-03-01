import src.visualizacao as vis
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, LocateControl

def main():
    # Carga dos dados
    gdf_eqpEsportivo = gpd.read_file("data/eqpEsportivo_bh.json")
    gdf_BH = gpd.read_file("data/capitaL_Belo_Horizonte.json")

    # Inicialização do mapa
    fmap = folium.Map(location=[gdf_eqpEsportivo['latitude'].median(), 
                               gdf_eqpEsportivo['longitude'].median()], 
                      zoom_start=12, tiles=None)
    
    vis.configurar_camadas_base(fmap)
    estilos = vis.obter_estilo_por_tipo()
    
    # Clusterização por Categoria
    for tipo in gdf_eqpEsportivo['TIPO'].unique():
        grupo = folium.FeatureGroup(name=tipo).add_to(fmap)
        
        cluster = MarkerCluster(name=tipo, overlay=True, control=False).add_to(grupo)
        
        df_filtrado = gdf_eqpEsportivo[gdf_eqpEsportivo['TIPO'] == tipo]
        for _, row in df_filtrado.iterrows():
            vis.criar_marcador_esportivo(row, estilos).add_to(cluster)

    # Localização do dispositivo
    LocateControl(
        keepCurrentZoomLevel=True,
        showPopup=True,
        strings={"title": "Mostrar minha localização", "popup": "Você está aqui"},
        flyTo=True,
        cacheLocation=True
    ).add_to(fmap)

    # Perímetro Urbano | Fica depois para ficar na camada superior
    folium.GeoJson(gdf_BH, name="Limite Municipal", 
                   style_function=lambda x: {'color':'blue', 'fillOpacity':0}).add_to(fmap)

    # MENU DROPDOWN
    # collapsed=True faz o menu virar um ícone pequeno que expande ao clicar
    folium.LayerControl(collapsed=True).add_to(fmap)

    # Interface Mobile e Botão Toggle
    vis.otimizar_interface_mobile(fmap)

    # Salvamento do mapa
    fmap.save('maps/mapa_equipamento_esportivo_bh.html')

if __name__ == "__main__":
    main()