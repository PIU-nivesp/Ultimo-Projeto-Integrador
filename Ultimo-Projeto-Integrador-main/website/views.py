from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Medicamento, Paciente, Movimentacao
import json

# 1. Renderiza a página HTML
def home(request):
    return render(request, 'index.html')

# 2. APIs de Listagem
def api_medicamentos(request):
    medicamentos = list(Medicamento.objects.all().values())
    return JsonResponse(medicamentos, safe=False)

def api_pacientes(request):
    pacientes = list(Paciente.objects.all().values())
    return JsonResponse(pacientes, safe=False)

# 3. APIs de Cadastro e Movimentação
@csrf_exempt
def api_novo_medicamento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        med = Medicamento.objects.create(
            nome=data.get('nome'),
            dosagem=data.get('dosagem'),
            quantidade=data.get('quantidade', 0),
            estoque_critico=data.get('estoque_critico', 10)
        )
        return JsonResponse({'status': 'sucesso', 'id': med.id})

@csrf_exempt
def api_novo_paciente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pac = Paciente.objects.create(
            nome=data.get('nome'),
            documento=data.get('documento'),
            endereco=data.get('endereco', ''),
            telefone=data.get('telefone', '')
        )
        return JsonResponse({'status': 'sucesso', 'id': pac.id})

@csrf_exempt
def api_update_estoque(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        med_id = data.get('medicamento_id')
        qtd = int(data.get('quantidade', 0))
        tipo = data.get('tipo')
        pac_id = data.get('paciente_id')
        
        try:
            medicamento = Medicamento.objects.get(id=med_id)
            if tipo == 'entrada':
                medicamento.quantidade += qtd
            elif tipo == 'saida':
                medicamento.quantidade -= qtd
            medicamento.save()
            
            # Registrar a movimentação com os novos campos
            paciente = Paciente.objects.get(id=pac_id) if pac_id else None
            
            Movimentacao.objects.create(
                medicamento=medicamento,
                paciente=paciente,
                quantidade=qtd,
                tipo=tipo,
                crm=data.get('crm'),
                nome_medico=data.get('nome_medico'),
                endereco_saida=data.get('endereco'),
                telefone_saida=data.get('telefone')
            )
            
            return JsonResponse({'status': 'sucesso', 'nova_quantidade': medicamento.quantidade})
        except Exception as e:
            return JsonResponse({'status': 'erro', 'message': str(e)}, status=400)