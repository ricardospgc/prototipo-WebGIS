import pandas as pd
import geopandas as gpd
from shapely import wkt

def preprocessar_adicionar_lat_lon(caminho_input_csv, caminho_output_geojson):
    """
    Utilizado para preprocessar os dados do .csv para json
    Adicionar os campos latitude e longitude facilita muito
    """
    df = pd.read_csv(caminho_input_csv, sep=';')
    df['geometry'] = df['GEOMETRIA'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:31983")
    
    # versão WGS84 apenas para extrair as coordenadas decimais
    gdf_wgs84 = gdf.to_crs(epsg=4326)
    
    # Cria os novos campos
    gdf['latitude'] = gdf_wgs84.geometry.y
    gdf['longitude'] = gdf_wgs84.geometry.x
    
    # Salva o arquivo (agora com as colunas lat/lon nas propriedades)
    gdf.to_file(caminho_output_geojson, driver="GeoJSON")
    
    return gdf