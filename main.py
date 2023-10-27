import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

url = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search_sql"

sql_query = """
    SELECT DISTINCT "SigAgente", "DscSubGrupo", "DscModalidadeTarifaria", "VlrTUSD",
    "VlrTE", "NomPostoTarifario", "DscUnidadeTerciaria", "DscREH", "DatInicioVigencia", "DatFimVigencia", "DscDetalhe"
    FROM "fcf2906c-7c32-4b9b-a637-054e7a5234f4"
    WHERE "DscBaseTarifaria" = 'Tarifa de Aplicação'
    AND CURRENT_DATE BETWEEN TO_DATE("DatInicioVigencia", 'YYYY-MM-DD')
    AND TO_DATE("DatFimVigencia", 'YYYY-MM-DD')
    AND ("DscModalidadeTarifaria" = 'Azul' OR "DscModalidadeTarifaria" = 'Verde')
    AND ("DscDetalhe" = 'Não se aplica')
    ORDER BY "SigAgente" ASC
"""

params = {"sql": sql_query}


def fix_encoding(record):
    for key, value in record.items():
        if isinstance(value, str):
            try:
                record[key] = value.encode('latin-1').decode('utf-8')
            except:
                pass
    return record


@app.route('/distribuidorasInfo')
def get_data():
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        records = data["result"]["records"]
        fixed_records = [fix_encoding(record) for record in records]
        return jsonify(fixed_records), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        return jsonify({"error": "Erro na requisição", "status_code": response.status_code})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
