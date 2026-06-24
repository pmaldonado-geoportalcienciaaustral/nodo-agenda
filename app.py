import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64

# Configuración de la página
st.set_page_config(page_title="Agenda de Actividades", layout="wide")

# Directorio del script para rutas absolutas seguras
dir_actual = os.path.dirname(os.path.abspath(__file__))
ruta_logo_unico = os.path.join(dir_actual, "logo LNS1.png")

# Función auxiliar modificada para evitar pantallas negras por culpa de rutas en Linux
def obtener_base64_imagen(ruta_imagen):
    try:
        if os.path.exists(ruta_imagen):
            with open(ruta_imagen, "rb") as image_file:
                return f"data:image/png;base64,{base64.b64encode(image_file.read()).decode()}"
    except Exception:
        return "" # Si falla, devuelve vacío y evita que la app se quede en negro
    return ""

logo_b64 = obtener_base64_imagen(ruta_logo_unico)

# ==========================================
# CONEXIÓN A LIBRERÍA DE ICONOS DE LÍNEA Y CSS
# ==========================================
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/remixicon@4.2.0/fonts/remixicon.css" rel="stylesheet"/>
    
    <style>
    /* Cambiar el color de fondo general del Modo Claro */
    .stAppViewContainer, .stApp, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #f0f4f8 !important;
    }
    
    /* Mantener fondo oscuro por defecto de Streamlit si está activo */
    @media (prefers-color-scheme: dark) {
        .stAppViewContainer, .stApp, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: transparent !important;
        }
    }

    /* Título de la Aplicación */
    .main-title {
        color: var(--text-color) !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    
    /* Estructura del contenedor para el Logo Único + Título */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
        padding-top: 10px;
    }
    
    .unique-logo {
        max-width: 38px; 
        height: auto;
    }
    
    /* Estilos globales para los títulos de sección con icono de línea integrado */
    .section-title {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 15px;
        margin-top: 5px;
    }
    .section-title i {
        font-size: 1.5rem;
        color: #ee750a; 
        font-weight: normal;
    }
    
    /* FUENTE DE FILTROS Y CORRECCIÓN DE PUNTERO (Barra Lateral) */
    .stSidebar [data-testid="stWidgetLabel"] p,
    .stSidebar label,
    div[data-testid="stSidebar"] h2,
    div[data-testid="stSidebar"] h3 {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"],
    div[data-testid="stSelectbox"] svg,
    .stSidebar select,
    .stSidebar option,
    div[data-testid="stCheckbox"] label {
        cursor: pointer !important;
    }
    
    /* CONTENEDORES DE MÉTRICAS EN HTML PURO */
    .custom-metric-box {
        background-color: #253b50 !important; 
        border: 2px solid #afd5ca !important;
        padding: 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05) !important;
        text-align: left !important;
    }
    .custom-metric-label {
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        margin-bottom: 8px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .custom-metric-value {
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        color: #ee750a !important;
        line-height: 1 !important;
    }
    
    /* ESTILO DE LAS TARJETAS DE LA AGENDA (FONDO #253b50) */
    .agenda-card {
        background-color: #253b50 !important; 
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #ee750a !important;
        border-top: 1px solid rgba(255,255,255,0.05) !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
        border-bottom: 1px solid rgba(255,255,255,0.05) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s ease;
    }
    
    .agenda-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.15);
    }
    
    .agenda-card h4, .agenda-card p, .agenda-card strong, .agenda-card i {
        color: #ffffff !important;
    }
    
    .agenda-card i {
        font-size: 1.1rem;
        vertical-align: -2px;
        margin-right: 6px;
        opacity: 0.8;
    }

    .region-tag {
        background-color: #afd5ca !important;
        color: #253b50 !important;
        padding: 3px 10px !important;
        border-radius: 4px !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        display: inline-block !important;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    .region-tag i {
        color: #253b50 !important;
        font-size: 0.85rem;
        margin-right: 4px;
    }

    /* DISEÑO DE MENÚ DE BOTONES HORIZONTALES PARA LOS MESES */
    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
    }
    
    div[data-testid="stRadio"] label {
        background-color: #253b50 !important;
        border: 1px solid #253b50 !important;
        padding: 6px 14px !important;
        border-radius: 6px !important;
        cursor: pointer !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-testid="stRadio"] label p {
        color: #ffffff !important;
        font-size: 0.95rem !important;
    }
    
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #afd5ca !important;
        border-color: #afd5ca !important;
    }
    
    div[data-testid="stRadio"] label:has(input:checked) p {
        color: #253b50 !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }

    button, a {
        cursor: pointer !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# SECCIÓN DE ENCABEZADO CON LOGO ÚNICO UNIVERSAL
# ==========================================
if logo_b64:
    st.markdown(
        f"""
        <div class="header-container">
            <img class="unique-logo" src="{logo_b64}" width="45" alt="Logo Laboratorio Natural Subantártico" />
            <h1 class="main-title">Agenda de Actividades Laboratorio Natural Subantártico</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    if os.path.exists("logo LNS1.png"):
        st.markdown(
            f"""
            <div class="header-container">
                <img class="unique-logo" src="data:image/png;base64,{base64.b64encode(open("logo LNS1.png", "rb").read()).decode()}" width="45" alt="Logo" />
                <h1 class="main-title">Agenda de Actividades Laboratorio Natural Subantártico</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown('<h1 class="main-title">Agenda de Actividades Laboratorio Natural Subantártico</h1>', unsafe_allow_html=True)


# Diccionario para meses
MESES_ESPANOL = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# ==========================================
# FUNCIÓN PARA CARGAR DATOS DESDE GOOGLE DRIVE
# ==========================================
@st.cache_data(ttl=600)
def cargar_datos():
    URL_DRIVE = "https://docs.google.com/spreadsheets/d/1XKF_eRwNKnqSWMNT9mdO0fv13EfezHak/export?format=xlsx"
    df = pd.read_excel(URL_DRIVE)
    
    COL_ACTIVIDAD = 'Actividad'  
    COL_FECHA = 'Fecha_Final'    
    COL_HORA = 'Hora'            
    
    df[COL_FECHA] = df[COL_FECHA].fillna(pd.Timestamp.now().strftime('%Y-%m-%d'))
    
    if pd.api.types.is_datetime64_any_dtype(df[COL_FECHA]):
        df[COL_FECHA] = df[COL_FECHA].dt.strftime('%Y-%m-%d')
    else:
        df[COL_FECHA] = df[COL_FECHA].astype(str)
    
    df[COL_HORA] = df[COL_HORA].fillna('09:00:00').astype(str).str.strip()
    
    fecha_completa_texto = df[COL_FECHA] + " " + df[COL_HORA]
    
    df['Fecha_Inicio'] = pd.to_datetime(fecha_completa_texto, errors='coerce', utc=True)
    df['Fecha_Inicio'] = df['Fecha_Inicio'].fillna(pd.to_datetime(df[COL_FECHA], errors='coerce', utc=True))
    df['Fecha_Inicio'] = df['Fecha_Inicio'].dt.tz_localize(None)
    
    df = df.dropna(subset=['Fecha_Inicio'])
    df[COL_ACTIVIDAD] = df[COL_ACTIVIDAD].fillna("Actividad sin nombre").astype(str)
    df['Fecha_Fin'] = df['Fecha_Inicio'] + pd.to_timedelta(1, unit='h')
    
    df['N asistentes'] = pd.to_numeric(df['N asistentes'], errors='coerce').fillna(0).astype(int)
    
    df['Anio'] = df['Fecha_Inicio'].dt.year
    df['Mes_Num'] = df['Fecha_Inicio'].dt.month
    
    if 'Organización' in df.columns:
        df['Organización'] = df['Organización'].astype(str).str.strip()

    # 🔥 NORMALIZACIÓN Y SEGURO PARA EL NUEVO CAMPO DESDE GOOGLE DRIVE
    if 'Link inscripción' in df.columns:
        df['Link inscripción'] = df['Link inscripción'].fillna('').astype(str).str.strip()
    else:
        df['Link inscripción'] = ''
    
    df = df.rename(columns={COL_ACTIVIDAD: 'Actividad'})
    return df

try:
    df_original = cargar_datos()
    
    df_original['Región'] = df_original['Región'].fillna('No especificada').astype(str)
    df_original['Descripción'] = df_original['Descripción'].fillna('').astype(str)

    # BARRA LATERAL: ICONO DE LUPA EN FILTROS
    st.sidebar.markdown('<div class="section-title"><i class="ri-search-line"></i> Búsqueda</div>', unsafe_allow_html=True)
    
    lista_regiones = ["Todas"] + sorted(list(df_original['Región'].unique()))
    region_seleccionada = st.sidebar.selectbox("Filtrar por región:", lista_regiones)
    
    descripciones_limpias = [d for d in df_original['Descripción'].unique() if d.strip() != '']
    lista_descripciones = ["Todas"] + sorted(descripciones_limpias)
    descripcion_seleccionada = st.sidebar.selectbox("Filtrar por tipo de actividad:", lista_descripciones)

    # Filtro: Casilla de verificación de la organización del Nodo
    filtrar_por_nodo = st.sidebar.checkbox("Actividad organizada por Nodo Subantártico", value=False)

    # APLICAR FILTROS AL DATAFRAME
    df_filtrado = df_original.copy()
    
    if region_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Región'] == region_seleccionada]
    if descripcion_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Descripción'] == descripcion_seleccionada]
        
    if filtrar_por_nodo:
        if 'Organización' in df_filtrado.columns:
            df_filtrado = df_filtrado[
                (df_filtrado['Organización'].notna()) & 
                (df_filtrado['Organización'] != '') & 
                (df_filtrado['Organización'].str.lower() != 'nan')
            ]

    # PANEL: ICONO DE GRÁFICO EN RESUMEN
    st.markdown('<div class="section-title"><i class="ri-bar-chart-box-line"></i> Resumen 2026</div>', unsafe_allow_html=True)
    
    total_actividades = len(df_filtrado)
    total_asistentes = int(df_filtrado['N asistentes'].sum())
    promedio_asistentes = int(total_asistentes / total_actividades) if total_actividades > 0 else 0
    
    col_met1, col_met2, col_met3 = st.columns(3)
    with col_met1:
        st.markdown(f'<div class="custom-metric-box"><div class="custom-metric-label">Total Actividades</div><div class="custom-metric-value">{total_actividades} eventos</div></div>', unsafe_allow_html=True)
    with col_met2:
        st.markdown(f'<div class="custom-metric-box"><div class="custom-metric-label">Total Asistentes</div><div class="custom-metric-value">{total_asistentes} personas</div></div>', unsafe_allow_html=True)
    with col_met3:
        st.markdown(f'<div class="custom-metric-box"><div class="custom-metric-label">Promedio Asistencia</div><div class="custom-metric-value">{promedio_asistentes} por evento</div></div>', unsafe_allow_html=True)
        
    st.markdown("---")

    # DISEÑO DISTRIBUIDO (PANEL DE ACTIVIDADES DETALLADAS Y PRÓXIMOS)
    col_agenda_principal, col_eventos = st.columns([2.5, 1])
    
    with col_agenda_principal:
        st.markdown('<div class="section-title"><i class="ri-calendar-todo-line"></i> Cronograma</div>', unsafe_allow_html=True)
        
        df_cronograma = df_filtrado.sort_values(by=['Anio', 'Mes_Num', 'Fecha_Inicio'])
        
        if not df_cronograma.empty:
            df_cronograma['Id_Mes'] = df_cronograma['Anio'].astype(str) + "-" + df_cronograma['Mes_Num'].astype(str).str.zfill(2)
            meses_disponibles = sorted(list(df_cronograma['Id_Mes'].unique()))
            
            etiquetas_meses = []
            for m in meses_disponibles:
                anio, mes_num = m.split("-")
                mes_txt = MESES_ESPANOL.get(int(mes_num), "Mes")
                etiquetas_meses.append(f"{mes_txt} {anio}")
            
            fecha_hoy = datetime.now()
            id_mes_hoy = f"{fecha_hoy.year}-{str(fecha_hoy.month).zfill(2)}"
            
            index_defecto = 0
            if id_mes_hoy in meses_disponibles:
                index_defecto = meses_disponibles.index(id_mes_hoy)
            else:
                futuros = [m for m in meses_disponibles if m >= id_mes_hoy]
                if futuros:
                    index_defecto = meses_disponibles.index(futuros[0])
            
            mes_seleccionado_texto = st.radio(
                label="Seleccione el mes:",
                options=etiquetas_meses,
                index=index_defecto,
                label_visibility="collapsed"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
            posicion_seleccionada = etiquetas_meses.index(mes_seleccionado_texto)
            id_mes_activo = meses_disponibles[posicion_seleccionada]
            
            df_mes_especifico = df_cronograma[df_cronograma['Id_Mes'] == id_mes_activo]
            
            for idx, fila in df_mes_especifico.iterrows():
                f_inicio = pd.to_datetime(fila['Fecha_Inicio']).strftime('%d/%m/%Y a las %H:%M')
                asistentes_valor = fila['N asistentes']
                asistentes_texto = f"{asistentes_valor} personas" if asistentes_valor > 0 else "Sin datos / Por confirmar"
                
                st.markdown(
                    f"""
                    <div class="agenda-card">
                        <span class="region-tag"><i class="ri-map-pin-line"></i> {fila.get('Región', 'General')}</span>
                        <h4 style="margin-top: 10px; margin-bottom: 10px; font-weight: 700; letter-spacing: -0.3px;">{fila['Actividad']}</h4>
                        <p style="margin: 4px 0; font-size: 0.95rem; opacity: 0.95;"><i class="ri-time-line"></i> <strong>Horario:</strong> {f_inicio} hrs.</p>
                        <p style="margin: 4px 0; font-size: 0.95rem; opacity: 0.95;"><i class="ri-shield-line"></i> <strong>Tipo de actividad:</strong> {fila['Descripción'] if fila['Descripción'] else 'Sin especificar'}</p>
                        <p style="margin: 4px 0; font-size: 0.95rem; opacity: 0.95;"><i class="ri-team-line"></i> <strong>Asistentes estimados:</strong> {asistentes_texto}</p>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # ==========================================
                # BOTONES DE ACCIÓN CON ICONOGRAFÍA MINIMALISTA DE LÍNEA
                # ==========================================
                link_zoom = str(fila.get('Link reunión', ''))
                url_invitacion = str(fila.get('URL', ''))
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    if link_zoom and link_zoom.lower() != 'nan' and link_zoom.strip() != '':
                        st.markdown(f'<a href="{link_zoom}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:10px; border-radius:8px; border:none; background-color:var(--primary-color, #22a7e0); color:white; font-weight:600; cursor:pointer;"><i class="ri-video-line" style="margin-right:6px;"></i>Entrar a Reunión</button></a>', unsafe_allow_html=True)
                    else:
                        st.button("✖ Sin Enlace Reunión", disabled=True, use_container_width=True, key=f"z_{idx}")
                with col_btn2:
                    if url_invitacion and url_invitacion.lower() != 'nan' and url_invitacion.strip() != '':
                        st.markdown(f'<a href="{url_invitacion}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:10px; border-radius:8px; border:none; background-color:var(--primary-color, #22a7e0); color:white; font-weight:600; cursor:pointer;"><i class="ri-external-link-line" style="margin-right:6px;"></i>Enlace Invitación</button></a>', unsafe_allow_html=True)
                    else:
                        st.button("✖ Sin Invitación", disabled=True, use_container_width=True, key=f"i_{idx}")
                
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("No hay actividades registradas que coincidan con los filtros seleccionados.")

    # ==========================================
    # SECCIÓN DE PROXIMOS EVENTOS CON SU FILTRADO DE CASILLA ACTIVO
    # ==========================================
    with col_eventos:
        st.sidebar.markdown("<br>", unsafe_allow_html=True) 
        st.markdown('<div class="section-title"><i class="ri-notification-badge-line"></i> Próximos eventos</div>', unsafe_allow_html=True)
        
        hoy = datetime.now().date()
        proximos = df_filtrado[pd.to_datetime(df_filtrado['Fecha_Inicio']).dt.date >= hoy]
        proximos = proximos.sort_values(by='Fecha_Inicio').head(5)
        
        if not proximos.empty:
            for idx_prox, fila in proximos.iterrows():
                fecha_str = pd.to_datetime(fila['Fecha_Inicio']).strftime('%d %b, %H:%M')
                
                # Obtención segura del enlace para el renderizado dinámico
                link_inscripcion = str(fila.get('Link inscripción', ''))
                
                # HTML Base de la tarjeta de próximos eventos
                st.markdown(
                    f"""
                    <div style="background-color: #253b50; padding: 14px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ee750a; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
                        <strong style="color: #ffffff; font-size: 0.95rem; display: block; margin-bottom: 4px;">{fila['Actividad']}</strong>
                        <span style="color: #ffffff; opacity: 0.8; font-size: 0.85rem; display: block;"><i class="ri-map-pin-5-line" style="color:#afd5ca; margin-right:4px;"></i>{fila.get('Lugar', 'No indicado')}</span>
                        <span style="color: #afd5ca; font-weight: 700; font-size: 0.85rem; display: block; margin-top: 2px;"><i class="ri-calendar-line" style="color:#afd5ca; margin-right:4px;"></i>{fecha_str}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
# Renderizado del botón "Inscribirse aquí" condicionado a la presencia del dato
                if link_inscripcion and link_inscripcion.lower() != 'nan' and link_inscripcion.strip() != '':
                    st.markdown(
                        f"""
                        <a href="{link_inscripcion}" target="_blank" style="text-decoration:none;">
                            <button style="width:100%; padding:10px; margin-top:-6px; margin-bottom:15px; border-radius:8px; border:none; background-color:#22a7e0; color:white; font-size:0.9rem; font-weight:600; cursor:pointer; transition: all 0.2s ease;">
                                <i class="ri-edit-box-line" style="margin-right:6px; vertical-align:-1px;"></i>Inscribirse aquí
                            </button>
                        </a>
                        """, 
                        unsafe_allow_html=True
                    )
        else:
            st.write("No hay eventos futuros próximos.")

except Exception as e:
    st.error(f"Error en la aplicación: {e}")