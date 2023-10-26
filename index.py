import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

url = "https://dadosabertos.aneel.gov.br/api/3/action/datastore_search_sql"

sql_query = """
    SELECT DISTINCT "SigAgente", "DscSubGrupo", "DscModalidadeTarifaria", "VlrTUSD",
    "VlrTE", "NomPostoTarifario", "DscUnidadeTerciaria", "DscREH","DatInicioVigencia", "DatFimVigencia", "DscDetalhe"
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
    # Função para corrigir a codificação dos campos
    for key, value in record.items():
        if isinstance(value, str):
            try:
                record[key] = value.encode('latin-1').decode('utf-8')
            except:
                pass  # Ignore erros de codificação

    return record


@app.route('/distribuidorasInfo')
def get_data():
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        records = data["result"]["records"]

        # Corrija a codificação dos campos em cada registro
        fixed_records = [fix_encoding(record) for record in records]
        # print(fixed_records)
        # Use jsonify com o argumento 'indent' para formatar o JSON e defina Content-Type como UTF-8
        return jsonify(fixed_records), 200, {'Content-Type': 'application/json; charset=utf-8'}

    else:
        return jsonify({"error": "Erro na requisição", "status_code": response.status_code})


@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == '__main__':
    app.run()
