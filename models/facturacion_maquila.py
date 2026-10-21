import pandas as pd 
from models.connection import init_connection

def get_factura_maquila():
    engine = init_connection()
    query = """

    SELECT 
        T0.DocDate,
        DATEPART(ISO_WEEK,(T0.DocDate)) as Num_sem,
        T0.TransNum,
        T0.BASE_REF,
        CASE 
            WHEN T0.ItemCode LIKE '0135PT%' THEN 'AVON FULL SERVICE'
            WHEN T0.ItemCode LIKE '0128PT%' THEN 'COLGATE FULL SERVICE'
            WHEN T0.ItemCode LIKE '03PT%' THEN 'ARMESSO'
            WHEN T0.ItemCode LIKE '58PT%' THEN 'AZUL K'
            WHEN T0.ItemCode LIKE '37PT%' THEN 'BELCORP'
            WHEN T0.ItemCode LIKE '28PT%' THEN 'COLGATE'
            WHEN T0.ItemCode LIKE '88PT%CRY' THEN 'CROYDON'
            WHEN T0.ItemCode LIKE '88PT%' THEN 'KDX'
            WHEN T0.ItemCode LIKE '39PT%' THEN 'PROCAPS'
            WHEN T0.ItemCode LIKE '54PT%' THEN 'UNILEVER'
            WHEN T0.ItemCode LIKE '63PT%' THEN 'COMERCIALIZADORA MEXICO AMERICANA'
            WHEN T0.ItemCode LIKE '64PT%' THEN 'SCALPI ECUADOR'
            WHEN T0.ItemCode LIKE '66PT%' THEN 'SUD SCRUD'
            WHEN T0.ItemCode LIKE '35PT%' THEN 'AVON PARTIAL SERVICE'
            WHEN T0.ItemCode LIKE '0138PT%' OR T0.ItemCode LIKE '38PT%' THEN 'ALICORP'
            WHEN T0.ItemCode LIKE '0152PT%' THEN 'GENOMMA'
            WHEN T0.ItemCode LIKE '0167PT%' THEN 'V-SHAPES'
            WHEN T0.ItemCode LIKE '20PT%' AND T0.Dscription LIKE '%SKINO%' THEN 'JERONIMO MARTINS SKINO'
            WHEN T0.ItemCode LIKE '20PT%' AND T0.Dscription NOT LIKE '%SKINO%' THEN 'JERONIMO HOME CARE'
            WHEN T0.ItemCode LIKE '05PT%' THEN 'GELTECK'
            WHEN T0.ItemCode LIKE '34PT%' OR T0.ItemCode LIKE '45PT%' THEN 'OTROS'
            WHEN T0.ItemCode LIKE '42PT%' THEN 'POLAR'
            WHEN T0.ItemCode LIKE '43PT%' THEN 'SCANDINAVIA'
            WHEN T0.ItemCode LIKE '47PT%' THEN 'BIOTECNIK'
            WHEN T0.ItemCode LIKE '51PT%' THEN 'HENKEL'
            WHEN T0.ItemCode LIKE '55PT%' THEN 'FACTORES Y MERCADEO'
            WHEN T0.ItemCode LIKE '57PT%' THEN 'TECNOQUIMICAS'
            WHEN T0.ItemCode LIKE '60PT%' THEN 'SHULTZ'
            WHEN T0.ItemCode LIKE '61PT%' THEN 'DROCARAS'
            WHEN T0.ItemCode LIKE '62PT%' THEN 'ARMESSO PANAMA'
            WHEN T0.ItemCode LIKE '65PT%' THEN 'PULPAPIES'
            WHEN T0.ItemCode LIKE '0131ST%' THEN 'SC JOHNSON'
            WHEN T0.ItemCode LIKE '0119PT%' THEN 'IND. BISONTE'
            WHEN T0.ItemCode LIKE '0103PT%' THEN 'ARMESSO'
            WHEN T0.ItemCode LIKE '0175PT%' THEN 'CINE COLOMBIA'
            WHEN T0.ItemCode LIKE '12PT%' THEN 'MILAGROS'
            ELSE 'OTROS / NO ASIGNADO'
        END AS Cliente, 
        T0.ItemCode,
        T0.Dscription,
        T0.InQty, 
        T0.Price, 
        T0.InQty * T0.Price AS Valor_ingresado,
        T1.InvntryUom
    FROM OINM T0
    LEFT JOIN OITM T1 ON T1.ItemCode = T0.ItemCode
    WHERE T0.DocDate BETWEEN '20260101' AND '20261231' -- Filtro de fecha optimizado
    AND T0.TransType = 59                            -- Entradas de mercancía
    AND (
        -- Regla 1: Todo lo que tenga PT (excepto 0131PT) debe ser del almacén INSPEC
        (T0.ItemCode LIKE '%PT%' AND T0.ItemCode NOT LIKE '0131PT%' AND T0.Warehouse = 'INSPEC')
        
        OR 
        
        -- Regla 2: Lo que empiece por 0131ST debe ser del almacén ENVASE
        (T0.ItemCode LIKE '0131ST%' AND T0.Warehouse = 'ENVASE')
    );
    
    """
    return pd.read_sql(query,engine)