from django.db import models

class Medicamento(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Medicamento")
    dosagem = models.CharField(max_length=50, verbose_name="Dosagem")
    quantidade = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")
    # Usamos snake_case para bater com o que configuramos na View e no Index
    estoque_critico = models.IntegerField(default=10, verbose_name="Nível de Alerta")

    def __str__(self):
        return f"{self.nome} ({self.dosagem})"

    class Meta:
        verbose_name = "Medicamento"
        verbose_name_plural = "Medicamentos"

class Paciente(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    documento = models.CharField(max_length=20, unique=True, verbose_name="CPF ou Prontuário")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone de Contato")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

class Movimentacao(models.Model):
    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída (Baixa)'),
    )
    
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name="movimentacoes")
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True, blank=True, related_name="movimentacoes")
    quantidade = models.IntegerField()
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    data = models.DateTimeField(auto_now_add=True)
    
    # Campos específicos para a Baixa (Saída)
    crm = models.CharField(max_length=20, blank=True, null=True, verbose_name="CRM do Médico")
    nome_medico = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do Médico")
    endereco_saida = models.TextField(blank=True, null=True, verbose_name="Endereço (na Baixa)")
    telefone_saida = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone (na Baixa)")

    def __str__(self):
        return f"{self.tipo} - {self.medicamento.nome} ({self.quantidade})"

    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"