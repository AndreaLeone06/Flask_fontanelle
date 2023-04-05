from flask import Flask, render_template, request, Response
app = Flask(__name__)

import geopandas as gpd

gdfQuar = gpd.read_file('/workspace/Flask_fontanelle/ds964_nil_wm.zip')
gdfFont = gpd.read_file('/workspace/Flask_fontanelle/Fontanelle.zip')

@app.route('/', methods=['GET'])
def quartieri():
    list = gdfQuar.NIL.to_list()
    return render_template('home.html', lista=list)

@app.route('/quartieri', methods=['GET'])
def mappa():
    return render_template('url_elencoReg.html', nomi=gdfRegioni['DEN_REG'].to_list(), codici=gdfRegioni['COD_REG'].to_list())

@app.route('/mappa', methods=['GET'])
def mappa_quartiere():
    quartiere_selezionato = request.args.get('quartiere')
    gdfQuartiere = gdfQuar[gdfQuar['NIL'] == quartiere_selezionato]
    gdfFontanelle_quartiere = gpd.sjoin(gdfFont, gdfQuartiere, op='within')
    return render_template('mappa_quartiere.html', quartiere=quartiere_selezionato, gdfFontanelle=gdfFontanelle_quartiere.to_json())

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)