import streamlit as st
import os
from datetime import datetime, time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuración de la página para móviles y PC
st.set_page_config(page_title="Max Car Apto - Contratos", layout="centered")

# Archivo persistente para folios en el servidor web
ARCHIVO_FOLIO = "ultimo_folio_num.txt"

def inicializar_folio():
    if os.path.exists(ARCHIVO_FOLIO):
        try:
            with open(ARCHIVO_FOLIO, "r") as f:
                return int(f.read().strip())
        except:
            return 1
    return 1

def guardar_ultimo_folio(folio):
    with open(ARCHIVO_FOLIO, "w") as f:
        f.write(str(folio))

# Inicializar estados de la aplicación
if "num_folio_actual" not in st.session_state:
    st.session_state.num_folio_actual = inicializar_folio()

# Colores Corporativos
COLOR_AZUL_MARINO = "#0D47A1"
COLOR_DORADO = "#C5A059"

# --- ENCABEZADO DE LA APLICACIÓN WEB ---
st.markdown(
    f"""
    <div style="background-color:{COLOR_AZUL_MARINO}; padding:15px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h1 style="color:white; margin:0; font-size:24px;">MAX CAR APTO</h1>
        <p style="color:#FFCDD2; margin:5px 0 0 0; font-size:14px;">Panel de Control de Contratos Móvil</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Control de Folio en la parte superior
col_fol1, col_fol2, col_fol3 = st.columns([1, 2, 1])
with col_fol1:
    if st.button("◀ Folio"):
        if st.session_state.num_folio_actual > 1:
            st.session_state.num_folio_actual -= 1
with col_fol2:
    folio_str = f"{st.session_state.num_folio_actual:04d}"
    st.markdown(f"<h3 style='text-align:center; color:red; margin:0;'>Folio No. {folio_str}</h3>", unsafe_allow_html=True)
with col_fol3:
    if st.button("Folio ▶"):
        st.session_state.num_folio_actual += 1

# ==========================================
# SECCIÓN 1: DATOS GENERALES
# ==========================================
with st.expander("📝 1. Datos Generales", expanded=True):
    entry_arrendador_nom = st.text_input("Nombre/Razón Social Arrendador:", value="AMADO RAMOS PUERTO")
    entry_arrendador_tel = st.text_input("Tel Celular Arrendador:", value="9998 471413")
    entry_nombre = st.text_input("Nombre Cliente / Arrendatario:")
    
    col1, col2 = st.columns(2)
    with col1:
        entry_licencia = st.text_input("Licencia No.:")
    with col2:
        cal_venc_lic = st.date_input("Vencimiento Lic. Titular:")
        
    entry_domicilio = st.text_input("Domicilio/Hotel/Airbnb:")
    
    col3, col4 = st.columns(2)
    with col3:
        entry_rfc = st.text_input("RFC Arrendatario:")
    with col4:
        entry_email = st.text_input("Correo Electrónico:")
        
    col5, col6 = st.columns(2)
    with col5:
        entry_tel1 = st.text_input("Teléfono 1:")
    with col6:
        entry_tel2 = st.text_input("Teléfono 2:")

    st.markdown("---")
    st.caption("Conductores Adicionales")
    c1_col1, c1_col2, c1_col3 = st.columns([2, 1, 1])
    with c1_col1: entry_cond1 = st.text_input("Conductor Adicional 1:")
    with c1_col2: entry_lic_cond1 = st.text_input("Licencia Adic 1:")
    with c1_col3: cal_venc_cond1 = st.date_input("Vencimiento Adic 1:")

    c2_col1, c2_col2, c2_col3 = st.columns([2, 1, 1])
    with c2_col1: entry_cond2 = st.text_input("Conductor Adicional 2:")
    with c2_col2: entry_lic_cond2 = st.text_input("Licencia Adic 2:")
    with c2_col3: cal_venc_cond2 = st.date_input("Vencimiento Adic 2:")

    st.markdown("---")
    entry_lugar = st.text_input("Lugar de Entrega:")
    entry_lugar_dev = st.text_input("Lugar Devolución:")
    
    combo_formato_tiempo = st.selectbox("Formato Renta:", ["Por ciclo de 24 Horas", "Por Día Calendario (Diario)"])
    
    col_fech1, col_fech2 = st.columns(2)
    with col_fech1:
        cal_salida = st.date_input("Fecha Salida:")
        hora_salida = st.time_input("Hora Salida:", time(12, 0))
    with col_fech2:
        cal_devolucion = st.date_input("Fecha Devolución:")
        hora_dev = st.time_input("Hora Devolución:", time(12, 0))

    entry_fac_a = st.text_input("Facturar a:")
    entry_fac_rfc = st.text_input("RFC Factura:")

# ==========================================
# SECCIÓN 2: VEHÍCULO E INVENTARIO
# ==========================================
with st.expander("🚗 2. Vehículo e Inventario"):
    col_v1, col_v2 = st.columns(2)
    with col_v1: entry_marca = st.text_input("Marca:")
    with col_v2: entry_modelo = st.text_input("Modelo:")
    
    col_v3, col_v4 = st.columns(2)
    with col_v3: entry_placas = st.text_input("Placas:")
    with col_v4: entry_km_salida = st.text_input("Km Salida:")

    st.markdown("#### Unidad de Repuesto")
    combo_repuesto_sn = st.selectbox("¿Activar Unidad de Repuesto?:", ["no", "si"])
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        entry_marca = st.text_input("Marca Rep.:")
        entry_modelo = st.text_input("Modelo Rep.:")
    with col_r2:
        entry_placas = st.text_input("Placas Rep.:")
        entry_rep_km = st.text_input("Km Salida Rep.:")

    col_am, col_ac = st.columns(2)
    with col_am: entry_asp_mecanicos = st.text_input("Aspectos Mecánicos:", value="Excelentes")
    with col_ac: entry_asp_carroceria = st.text_input("Aspectos Carrocería:", value="Excelentes")
    
    combo_aceite = st.selectbox("Niveles de Aceite:", ["Lleno", "Vacío"])
    entry_documentacion = st.text_input("Documentación entregada:", value="TARJETA DE CIRCULACION")

    st.markdown("#### Tablero de Nivel de Gasolina")
    gas_opciones = ["Vacío", "Reserva", "1/4 Tanque", "1/2 Tanque", "3/4 Tanque", "4/4 (Full)"]
    gas_sel = st.select_slider("Selecciona nivel:", options=gas_opciones, value="4/4 (Full)")

    st.markdown("#### Inventario (Desmarca el que no tenga)")
    inv_items = ["Espejos", "Asientos", "Faros delanteros", "Luz de faro trasero", "Direccionales", "Cubiertas completas", "Molduras completas", "Tapón de gasolina", "Claxon", "Batería", "Llaves"]
    inv_resultados = {}
    
    col_inv1, col_inv2 = st.columns(2)
    for idx, item in enumerate(inv_items):
        with col_inv1 if idx % 2 == 0 else col_inv2:
            inv_resultados[item] = st.checkbox(item, value=True)
            
    entry_obs = st.text_input("Observaciones del Inventario:")

# ==========================================
# SECCIÓN 3: COBERTURAS Y SEGURO
# ==========================================
with st.expander("🛡️ 3. Coberturas y Seguro"):
    entry_aseguradora = st.text_input("Compañía Aseguradora:", value="ANA SEGUROS -- CHUBB")
    entry_poliza = st.text_input("Póliza Número:")
    entry_tipo_cobertura = st.text_input("Tipo de Cobertura Global:")
    
    entry_tpl = st.text_input("TPL Responsabilidad Civil:")
    entry_cdw = st.text_input("CDW Colisión (% Deducible):")
    entry_pai = st.text_input("PAI Gastos Médicos Ocupantes:")
    entry_dp = st.text_input("DP Cobertura Amplia (Deducible):")
    entry_tp = st.text_input("TP Robo Total (% Deducible):")

# ==========================================
# SECCIÓN 4: COSTOS Y GARANTÍAS
# ==========================================
with st.expander("💰 4. Costos y Garantías"):
    # --- CÁLCULO DE TIEMPOS AUTOMÁTICO EXACTO ---
    dt_inicio = datetime.combine(cal_salida, hora_salida)
    dt_fin = datetime.combine(cal_devolucion, hora_dev)
    
    if "24 Horas" in combo_formato_tiempo:
        diferencia = dt_fin - dt_inicio
        total_horas = diferencia.total_seconds() / 3600.0
        dias_calc = int(total_horas // 24)
        horas_restantes = total_horas % 24
        if horas_restantes > 0.25:
            hrs_ex_enteras = int(horas_restantes)
            if horas_restantes - hrs_ex_enteras > 0.25:
                hrs_ex_enteras += 1
        else:
            hrs_ex_enteras = 0
        if dias_calc == 0 and total_horas > 0:
            dias_calc = 1
            hrs_ex_enteras = 0
    else:
        dias_calc = (cal_devolucion - cal_salida).days + 1
        if dias_calc < 1: dias_calc = 1
        hrs_ex_enteras = 0

    col_c1, col_c2 = st.columns(2)
    with col_c1: dias = st.number_input("Días Vigencia Contrato:", value=int(dias_calc))
    with col_c2: tarifa = st.number_input("Tarifa por Día ($):", value=0.0, step=50.0)
    
    col_c3, col_c4 = st.columns(2)
    with col_c3: h_extra_calculadas = st.number_input("Horas Extra Calculadas:", value=int(hrs_ex_enteras), disabled=True)
    with col_c4: h_extra = st.number_input("Costo Total Extra ($):", value=0.0)
        
    col_c5, col_c6 = st.columns(2)
    with col_c5: delivery = st.number_input("Delivery / Traslado ($):", value=0.0)
    with col_c6: fuera_h = st.number_input("Fuera Horario ($):", value=0.0)

    col_c7, col_c8 = st.columns(2)
    with col_c7: iva_porcentaje = st.number_input("IVA (%):", value=0.0)
    with col_c8: af_porcentaje = st.number_input("A.F. Impuesto Aero (%):", value=0.0)

    col_c9, col_c10 = st.columns(2)
    with col_c9: silla_dia = st.number_input("Silla Bebé por día ($):", value=0.0)
    with col_c10: c_adic_dia = st.number_input("Cond. Adicional por día ($):", value=0.0)

    col_c11, col_c12 = st.columns(2)
    with col_c11: drop = st.number_input("Drop-Off ($):", value=0.0)
    with col_c12: upgrade = st.number_input("Up-Grade ($):", value=0.0)

    st.markdown("#### Anticipo / Reserva")
    col_ant1, col_ant2 = st.columns(2)
    with col_ant1: anticipo = st.number_input("Monto Anticipo ($):", value=0.0)
    with col_ant2: combo_metodo_anticipo = st.selectbox("Método Anticipo:", ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia", "Link MP", "Otro"])

    st.markdown("#### Depósito de Garantía")
    col_gar1, col_gar2 = st.columns(2)
    with col_gar1: deposito = st.number_input("Monto Garantía ($):", value=0.0)
    with col_gar2: combo_metodo_garantia = st.selectbox("Método Dejado:", ["Tarjeta de Crédito", "Efectivo", "Tarjeta de Débito", "Transferencia", "Voucher firmado", "Otro"])

    st.markdown("#### Distribución de Formas de Pago (Renta)")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1: p_efectivo = st.number_input("Efectivo $:", value=0.0)
    with col_p2: p_tarjeta = st.number_input("Tarjeta $:", value=0.0)
    with col_p3: p_transf = st.number_input("Transferencia $:", value=0.0)
    
    col_p4, col_p5 = st.columns(2)
    with col_p4: p_linkmp = st.number_input("Link MP $:", value=0.0)
    with col_p5: p_otros = st.number_input("Otros $:", value=0.0)

    # --- LÓGICA MATEMÁTICA EXACTA ORIGINAL ---
    silla = silla_dia * dias
    c_adic = c_adic_dia * dias
    subtotal = (dias * tarifa) + h_extra + delivery + fuera_h + silla + c_adic + drop + upgrade
    iva = subtotal * (iva_porcentaje / 100)
    af = subtotal * (af_porcentaje / 100)
    
    total_global_antes_anticipo = subtotal + iva + af
    total_final_neto = total_global_antes_anticipo - anticipo

    st.markdown(f"### NETO A PAGAR: **${total_final_neto:,.2f} MXN**")

# ==========================================
# PROCESAMIENTO Y CONFIGURACIÓN DEL PDF
# ==========================================
def fabricar_pdf():
    nombre_archivo = f"Contrato_{folio_str}.pdf"
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter, rightMargin=14, leftMargin=14, topMargin=6, bottomMargin=6)
    story = []
    styles = getSampleStyleSheet()
    
    style_titulo = ParagraphStyle('Tit', parent=styles['Heading1'], fontSize=19, alignment=1, textColor=colors.HexColor(COLOR_DORADO), leading=21)
    style_sub = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=7.2, alignment=1, textColor=colors.dimgray, leading=9.5)
    style_sec = ParagraphStyle('Sec', parent=styles['Heading2'], fontSize=8.5, leading=11, textColor=colors.white, backColor=colors.HexColor(COLOR_DORADO), spaceBefore=2, spaceAfter=2, leftIndent=4)
    style_txt = ParagraphStyle('Txt', parent=styles['Normal'], fontSize=8, leading=10.2)
    style_legal = ParagraphStyle('Leg', parent=styles['Normal'], fontSize=6.2, leading=8.2, alignment=4)
    style_alerta_final = ParagraphStyle('AlertaFinal', parent=styles['Normal'], fontSize=7, leading=9, textColor=colors.red, alignment=1, spaceBefore=1, spaceAfter=1)
    style_folio_rojo = ParagraphStyle('FolioRojo', parent=styles['Normal'], fontSize=12, leading=13, textColor=colors.red, alignment=2)
    style_contrato_centrado = ParagraphStyle('CentredContrato', parent=styles['Normal'], fontSize=12.5, leading=15, alignment=1, fontName="Helvetica-Bold", spaceBefore=3, spaceAfter=2)

    # Encabezado estructurado en el documento
    info_empresa = [
        Paragraph("<b>MAX CAR APTO</b>", style_titulo),
        Paragraph("Calle 21 #333 entre 26 y 28 Col. Manuel Crescencio Rejón, Mérida, Yucatán.", style_sub),
        Paragraph("Tels. 9998 471413 / 9992 070213 / 9995 863100 / 9994 454645 | Correo: contacto-reservas@maxcarsrental.com", style_sub)
    ]
    folio_p = Paragraph(f"<b>Folio No.<br/><font size=14>{folio_str}</font></b>", style_folio_rojo)
    
    # Manejo adaptativo del logotipo corporativo
    if os.path.exists("logo.jpg"):
        img_logo = RLImage("logo.jpg", width=80, height=60)
        header_data = [[img_logo, info_empresa, folio_p]]
    else:
        header_data = [["[Logo]", info_empresa, folio_p]]
    
    t_header = Table(header_data, colWidths=[80, 420, 80])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), 
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT')
    ]))
    story.append(t_header)
    
    story.append(Paragraph("CONTRATO DE ARRENDAMIENTO DE VEHÍCULOS / RENTAL AGREEMENT", style_contrato_centrado))

    # --- TABLA: DATOS ARRENDADOR ---
    story.append(Paragraph("<b>DATOS DEL ARRENDADOR</b>", style_sec))
    t_arr = Table([[Paragraph(f"<b>Nombre o razón social:</b> {entry_arrendador_nom}", style_txt), Paragraph(f"<b>Teléfono Celular / Phone:</b> {entry_arrendador_tel}", style_txt)]], colWidths=[290, 290])
    t_arr.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    story.append(t_arr)

    # --- TABLA: DATOS CLIENTE ---
    story.append(Paragraph("<b>DATOS DEL ARRENDATARIO / CLIENTE</b>", style_sec))
    venc_titular = cal_venc_lic.strftime('%d/%m/%Y')
    lic_c1_str = f"{entry_lic_cond1} (Venc: {cal_venc_cond1.strftime('%d/%m/%Y')})" if entry_lic_cond1 else "N/A"
    lic_c2_str = f"{entry_lic_cond2} (Venc: {cal_venc_cond2.strftime('%d/%m/%Y')})" if entry_lic_cond2 else "N/A"
    
    tabla_g = [
        [Paragraph(f"<b>Arrendatario / Renter:</b> {entry_nombre}", style_txt), Paragraph(f"<b>Licencia No:</b> {entry_licencia} (Venc: {venc_titular})", style_txt)],
        [Paragraph(f"<b>Domicilio / Address:</b> {entry_domicilio}", style_txt), Paragraph(f"<b>RFC:</b> {entry_rfc}", style_txt)],
        [Paragraph(f"<b>Teléfonos:</b> {entry_tel1} / {entry_tel2}", style_txt), Paragraph(f"<b>Correo / Email:</b> {entry_email}", style_txt)],
        [Paragraph(f"<b>Conductor Adicional 1:</b> {entry_cond1 or 'N/A'}", style_txt), Paragraph(f"<b>Lic / Venc Adic 1:</b> {lic_c1_str}", style_txt)],
        [Paragraph(f"<b>Conductor Adicional 2:</b> {entry_cond2 or 'N/A'}", style_txt), Paragraph(f"<b>Lic / Venc Adic 2:</b> {lic_c2_str}", style_txt)]
    ]
    t_g = Table(tabla_g, colWidths=[290, 290]); t_g.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    story.append(t_g)

    # --- TABLA: ENTREGAS Y TIEMPOS ---
    story.append(Paragraph("<b>LUGAR DE ENTREGA Y RECEPCION DEL VEHICULO</b>", style_sec))
    f_salida_str = f"{cal_salida.strftime('%d/%m/%Y')} {hora_salida.strftime('%H:%M')} hrs"
    f_dev_str = f"{cal_devolucion.strftime('%d/%m/%Y')} {hora_dev.strftime('%H:%M')} hrs"
    
    tabla_l = [
        [Paragraph(f"<b>Lugar de Entrega:</b> {entry_lugar}", style_txt), Paragraph(f"<b>Lugar Devolución:</b> {entry_lugar_dev}", style_txt)],
        [Paragraph(f"<b>Fecha/Hora Salida:</b> {f_salida_str}", style_txt), Paragraph(f"<b>Fecha/Hora Devolución:</b> {f_dev_str}", style_txt)],
        [Paragraph(f"<b>Vigencia Contrato:</b> {dias} días", style_txt), Paragraph(f"<b>Horas Extra:</b> {h_extra_calculadas} hrs", style_txt)],
        [Paragraph(f"<b>Facturar a:</b> {entry_fac_a}", style_txt), Paragraph(f"<b>RFC Facturación:</b> {entry_fac_rfc}", style_txt)]
    ]
    t_l = Table(tabla_l, colWidths=[290, 290]); t_l.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    story.append(t_l)

    # --- TABLA: CARACTERÍSTICAS E INVENTARIO ---
    story.append(Paragraph("<b>CARACTERISTICAS DEL VEHICULO</b>", style_sec))
    datos_auto_html = (
        f"<b>Marca / Modelo:</b> {entry_marca} / {entry_modelo}<br/>"
        f"<b>Placas:</b> {entry_placas} &nbsp;|&nbsp; <b>Km Salida:</b> {entry_km_salida} km<br/>"
        f"<b>Nivel Gasolina:</b> {gas_sel}<br/>"
        f"<b>Mecánicos / Carrocería:</b> {entry_asp_mecanicos} / {entry_asp_carroceria}<br/>"
        f"<b>Niveles Aceite:</b> {combo_aceite} &nbsp;|&nbsp; <b>Docs:</b> {entry_documentacion}"
    )
    if combo_repuesto_sn == "si":
        datos_auto_html += (
            f"<br/><font color='blue'><b>[UNIDAD DE REPUESTO ACTIVA]</b><br/>"
            f"<b>Marca / Modelo Rep:</b> {entry_rep_marca} / {entry_rep_modelo}<br/>"
            f"<b>Placas Rep:</b> {entry_rep_placas} &nbsp;|&nbsp; <b>Km Rep:</b> {entry_rep_km} km</font>"
        )
    
    inv_col1, inv_col2 = [], []
    for idx, (k, v) in enumerate(inv_resultados.items()):
        chk = "✓" if v else "X"
        item_p = Paragraph(f"• {k}: <b>[{chk}]</b>", style_txt)
        if idx % 2 == 0: inv_col1.append(item_p)
        else: inv_col2.append(item_p)
        
    t_inv_interna = Table([[inv_col1, inv_col2]], colWidths=[130, 130])
    t_inv_interna.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'), ('PADDING',(0,0),(-1,-1),0)]))

    t_maestra_v = Table([[Paragraph(datos_auto_html, style_txt), t_inv_interna]], colWidths=[310, 270])
    t_maestra_v.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LINEBEFORE', (1,0), (1,0), 0.5, colors.HexColor(COLOR_DORADO)), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
    story.append(t_maestra_v)
    if entry_obs:
        story.append(Paragraph(f"<b>Observaciones de Inventario:</b> {entry_obs}", style_txt))

    # --- TABLA: SEGUROS ---
    story.append(Paragraph("<b>PÓLIZA DE SEGURO Y COBERTURAS</b>", style_sec))
    tabla_cob = [
        [Paragraph(f"<b>Aseguradora:</b> {entry_aseguradora}", style_txt), Paragraph(f"<b>Póliza No:</b> {entry_poliza}", style_txt)],
        [Paragraph(f"<b>Tipo Cobertura:</b> {entry_tipo_cobertura}", style_txt), Paragraph(f"<b>TPL Resp. Civil:</b> {entry_tpl}", style_txt)],
        [Paragraph(f"<b>CDW Colisión:</b> {entry_cdw}", style_txt), Paragraph(f"<b>PAI Gastos Médicos:</b> {entry_pai}", style_txt)],
        [Paragraph(f"<b>DP Cobertura Amplia:</b> {entry_dp}", style_txt), Paragraph(f"<b>TP Robo Total:</b> {entry_tp}", style_txt)]
    ]
    t_cob = Table(tabla_cob, colWidths=[290, 290]); t_cob.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    story.append(t_cob)

    # --- TABLA: COSTOS ---
    story.append(Paragraph("<b>COSTOS TOTALES DEL ARRENDAMIENTO Y GARANTÍAS</b>", style_sec))
    tabla_c = [
        [Paragraph(f"<b>Tarifa Base por Día:</b> ${tarifa} M.N.", style_txt), Paragraph(f"<b>Garantía Dejada:</b> ${deposito} M.N. ({combo_metodo_garantia})", style_txt)],
        [Paragraph(f"<b>Delivery:</b> ${delivery} &nbsp;|&nbsp; <b>Costo Extras:</b> ${h_extra}", style_txt), Paragraph(f"<b>Anticipo Reserva:</b> ${anticipo} M.N. ({combo_metodo_anticipo})", style_txt)],
        [Paragraph(f"<b>Silla Bebé:</b> ${silla} &nbsp;|&nbsp; <b>Cond Adic:</b> ${c_adic}", style_txt), Paragraph(f"<b>Drop-Off / Up-Grade:</b> ${drop} / ${upgrade}", style_txt)]
    ]
    t_c = Table(tabla_c, colWidths=[290, 290]); t_c.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    story.append(t_c)

    pago_detalles = f"<b>Efec:</b> ${p_efectivo} | <b>Tarj:</b> ${p_tarjeta}<br/><b>Trans:</b> ${p_transf} | <b>MP:</b> ${p_linkmp}"
    tabla_totales = [
        [Paragraph(pago_detalles, style_txt), Paragraph(f"<b>TOTAL GLOBAL RENTA:</b> ${total_global_antes_anticipo:.2f} MXN<br/><b>NETO A PAGAR:</b> <font color='#0D47A1'><b>${total_final_neto:.2f} MXN</b></font>", style_txt)]
    ]
    t_tot = Table(tabla_totales, colWidths=[240, 340])
    t_tot.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'), ('BACKGROUND',(1,0),(1,0),colors.HexColor("#E3F2FD")), ('BOX',(1,0),(1,0),1,colors.HexColor(COLOR_DORADO)), ('PADDING',(0,0),(-1,-1),3)]))
    story.append(t_tot)

    # --- CLÁUSULAS ---
    nuevas_clausulas = (
        "• <b>EL SEGURO SOLO CUBRE YUCATAN, CAMPECHE Y QUINTANA ROO. INSURANCE ONLY COVERS YUCATAN, CAMPECHE Y QUINTANA ROO.</b><br/>"
        "• Este vehiculo no esta autorisado a salir dela Republica Méxicana.<br/>"
        "• Si pasadas las 24 horas de la fecha y hora de la promesa de regreso de este vehículo, el ARRENDADOR no ha sido notificado de la intención de prorrogar el contrato por parte del arrendatario, se procederá por los medios legales en contra del mismo y hasta recuperar la propiedad.<br/>"
        "• EL ARRENDATARIO es responsable por el pago de infracciones y retiro o perdida de placas o documentos de circulación.<br/><br/>"
        "<b>PAGARÉ / PROMISSORY NOTE:</b> Por este pagaré me(nos) obligo(amos) a pagar incondicionalmente a la vista y a la orden de "
        "____________________________________________________, en cualquier parte que se requiera la cantidad de "
        "$_____________________________________________________"
    )
    t_clausulas_box = Table([[Paragraph(nuevas_clausulas, style_legal)]], colWidths=[580])
    t_clausulas_box.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1.2, colors.HexColor(COLOR_DORADO)), ('PADDING', (0,0), (-1,-1), 5), ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
    story.append(Paragraph("<br/>", style_txt))
    story.append(t_clausulas_box)
    story.append(Paragraph("<b>NINGUNA COBERTURA INCLUYE EL ROBO PARCIAL / PARTIAL THEFT IS NOT INCLUDED IN ANY COVERAGE</b>", style_alerta_final))

    # --- BLOQUE DE FIRMAS ---
    cond1_nom = entry_cond1 or "N/A"
    cond2_nom = entry_cond2 or "N/A"
    tabla_firmas = [[
        Paragraph("<b>ARRENDATARIO / CLIENTE</b><br/><br/><br/><br/>___________________________<br/>Firma y Huella Digital", style_txt),
        Paragraph(f"<b>CONDUCTOR ADICIONAL 1</b><br/><br/><br/><br/>___________________________<br/>{cond1_nom}<br/>Acepto Obligaciones", style_txt),
        Paragraph(f"<b>CONDUCTOR ADICIONAL 2</b><br/><br/><br/><br/>___________________________<br/>{cond2_nom}<br/>Acepto Obligaciones", style_txt)
    ]]
    t_firmas = Table(tabla_firmas, colWidths=[193, 193, 194])
    t_firmas.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'), ('VALIGN',(0,0),(-1,-1),'TOP'), ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    story.append(t_firmas)

    doc.build(story)
    return nombre_archivo

# --- BOTÓN DE GENERACIÓN Y DESCARGA DIRECTA MULTIPLATAFORMA ---
st.markdown("---")
if st.button("📄 ACCIONAR GENERADOR DE CONTRATO", use_container_width=True, type="primary"):
    if not entry_nombre:
        st.error("Por favor, ingresa al menos el Nombre del Cliente.")
    else:
        nombre_pdf = fabricar_pdf()
        
        # Aumentar y salvar el consecutivo
        st.session_state.num_folio_actual += 1
        guardar_ultimo_folio(st.session_state.num_folio_actual)
        
        st.success(f"¡Contrato procesado exitosamente bajo el Folio {folio_str}!")
        
        # Permite la descarga directa en cualquier Navegador, Celular o Tablet
        with open(nombre_pdf, "rb") as file:
            st.download_button(
                label="📥 Descargar Contrato PDF en Dispositivo",
                data=file,
                file_name=nombre_pdf,
                mime="application/pdf",
                use_container_width=True
            )