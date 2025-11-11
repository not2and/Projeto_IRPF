import flet as ft

# regras 
DEPENDENT = 189.59
SIMPLIFIED = 528.00

# tabela de faixas (limite_superior, aliquota_percent, parcela_deduzir)
TABELA = [
    (1903.98, 0.0, 0.0),
    (2826.65, 7.5, 142.80),
    (3751.05, 15.0, 354.80),
    (4664.68, 22.5, 636.13),
    (float('inf'), 27.5, 869.36),
]

def achar_faixa(valor):
    for limite, aliq, parcela in TABELA:
        if valor <= limite:
            return aliq, parcela
    return 0.0, 0.0

def calcular(salario, dependentes, usar_simpl):
    try:
        s = float(str(salario).replace(',', '.'))
    except:
        s = 0.0
    try:
        d = int(dependentes)
    except:
        d = 0
    ded_depend = DEPENDENT * d
    ded = ded_depend
    if usar_simpl and SIMPLIFIED > ded_depend:
        ded = SIMPLIFIED
    base = s - ded
    if base < 0:
        base = 0.0
    aliq_percent, parcela = achar_faixa(base)
    if aliq_percent == 0.0:
        imposto = 0.0
    else:
        imposto_bruto = base * (aliq_percent/100)
        imposto = imposto_bruto - parcela
        if imposto < 0:
            imposto = 0.0
    liquido = s - imposto
    # resultados simples
    return {
        'salario': round(s,2),
        'desconto': round(ded,2),
        'base': round(base,2),
        'aliquota': aliq_percent,
        'parcela': round(parcela,2),
        'ir': round(imposto,2),
        'liquido': round(liquido,2),
    }

def main(page: ft.Page):
    page.title = "IRPF Calculadora"
    page.padding = 12
    page.window_width = 360
    page.window_height = 700

    salario = ft.TextField(label="Salário bruto (R$)", keyboard_type=ft.KeyboardType.NUMBER)
    dependentes = ft.TextField(label="Dependentes", keyboard_type=ft.KeyboardType.NUMBER)
    simpl = ft.Checkbox(label="Usar desconto simplificado (R$ 528,00)")
    resultado = ft.Column()

    def on_click(e):
        res = calcular(salario.value, dependentes.value, simpl.value)
        resultado.controls.clear()
        resultado.controls.append(ft.Text(f"Salário: R$ {res['salario']:.2f}"))
        resultado.controls.append(ft.Text(f"Desconto: R$ {res['desconto']:.2f}"))
        resultado.controls.append(ft.Text(f"Salário base: R$ {res['base']:.2f}"))
        if res['aliquota'] == 0.0:
            resultado.controls.append(ft.Text("Alíquota: Isento"))
        else:
            resultado.controls.append(ft.Text(f"Alíquota: {res['aliquota']:.1f}%"))
            resultado.controls.append(ft.Text(f"Parcela a deduzir: R$ {res['parcela']:.2f}"))
        resultado.controls.append(ft.Text(f"IR devido: R$ {res['ir']:.2f}"))
        resultado.controls.append(ft.Text(f"Salário líquido: R$ {res['liquido']:.2f}"))
        page.update()

    btn = ft.ElevatedButton(text="Calcular", on_click=on_click)
    page.add(ft.Column([ft.Text('Calculadora IRPF'), salario, dependentes, simpl, btn, ft.Divider(), resultado], spacing=8))

if __name__ == '__main__':
    ft.app(target=main)
