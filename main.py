from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import requests

moradores = [
    {
        'id': 1,
        'nome': 'Gabriel',
        'cep': '06162-220',
        'nome_rua': 'Rua Campo Grande',
        "bairro": "Padroeira",
        "localidade": "Osasco",
        'numero': 644
    }
]

app = Flask(__name__)
api = Api(app)


class Morador(Resource):
    def post(self):
        cep = request.json['cep']
        envio_cep = requests.get('https://viacep.com.br/ws/{}/json'.format(cep))

        dados_endereco = envio_cep.json()
        novo_morador = {
            'id': moradores[-1]['id'] + 1,
            'nome': request.json['nome'],
            'cep': dados_endereco['cep'],
            'nome_rua': dados_endereco['logradouro'],
            "bairro": dados_endereco['bairro'],
            "localidade": dados_endereco['localidade'],
            'numero': request.json['numero']
        }
        moradores.append(novo_morador)
        return jsonify({'mensagem': 'Morador cadastrado com sucesso'})

    def get(self):
        return jsonify(moradores)


class MoradorById(Resource):
    def get(self, id):
        for morador in moradores:
            if int(morador['id']) == int(id):
                return morador
        return jsonify({'mensagem': 'Morador não encontrado'})

    def put(self, id):
        cep = request.json['cep']

        envio_cep = requests.get('https://viacep.com.br/ws/{}/json'.format(cep))
        dados_cep = envio_cep.json()

        for morador in moradores:
            if int(morador['id'] == int(id)):
                morador['nome'] = request.json['nome']
                morador['cep'] = request.json['cep']
                morador['nome_rua'] = dados_cep['logradouro']
                morador['bairro'] = dados_cep['bairro']
                morador['localidade'] = dados_cep['localidade']
                morador['numero'] = request.json['numero']
                return jsonify({'mensagem': 'Morador alterado com sucesso'})
        return jsonify({'mensagem': 'Morador não encontrado'})

    def delete(self, id):
        for morador in moradores:
            if int(morador['id']) == int(id):
                moradores.remove(morador)
                return jsonify({'mensagem': 'Morador deletado com sucesso'})
        return jsonify({'mensagem': 'Morador não encontrado'})


api.add_resource(Morador, "/morador")
api.add_resource(MoradorById, "/morador/<id>")
app.run()
