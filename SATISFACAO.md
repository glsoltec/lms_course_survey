# Módulo de Pesquisa de Satisfação de Cursos

## 🎯 Objetivo

Implementar uma pesquisa de satisfação para alunos realizarem **antes ou após avaliações**, coletando feedback sobre:
- Treinamento
- Instrutor
- Conteúdo
- Satisfação Geral

## 📊 Estrutura

### DocTypes Criados

#### 1. **Course Satisfaction** (Principal)
- **Descrição**: Documento principal que contém a pesquisa completa
- **Campos**:
  - `student`: Link para usuário/aluno (obrigatório)
  - `course`: Link para curso (obrigatório)
  - `instructor`: Link para instrutor (automático)
  - `survey_date`: Data/hora da pesquisa (automática)
  - `satisfaction_items`: Tabela com 4 itens de avaliação
  - `general_feedback`: Campo de texto para comentários adicionais

#### 2. **Satisfaction Item** (Child Table)
- **Descrição**: Cada item individual de avaliação
- **Campos**:
  - `item_name`: Nome do item (Treinamento/Instrutor/Conteúdo/Satisfação Geral)
  - `item_label`: Descrição legível
  - `rating`: Nota de 1-5 (Péssimo → Ótimo)

### Escala de Avaliação

```
1 - Péssimo
2 - Ruim
3 - Regular
4 - Bom
5 - Ótimo
```

---

## 🚀 Como Usar

### 1. Criar uma Pesquisa

```
1. Acesse: Awesome Bar > Course Satisfaction
2. Clique em "+ Novo"
3. Preencha:
   - Aluno (obrigatório)
   - Curso (obrigatório)
4. Os 4 itens aparecerão automaticamente
5. Avalie cada item com uma nota de 1-5
6. (Opcional) Adicione comentários gerais
7. Clique em "Salvar" e depois "Submeter"
```

### 2. Ver Dashboard de Resultados

```
1. Acesse: Awesome Bar > Satisfaction Dashboard
2. (Opcional) Filtre por:
   - Curso específico
   - Período (De/Até)
3. Visualize:
   - Total de pesquisas respondidas
   - Nota média por item
   - Distribuição de notas (1-5)
   - Percentual de satisfeitos (notas 4-5)
```

### 3. Acessar Dashboard do DocType

```
1. Vá para: Course Satisfaction (List View)
2. Clique em um registro
3. Na aba "Dashboard" visualize:
   - Cards com métricas principais
   - Gráfico de satisfação por item
```

---

## 🔧 APIs Disponíveis

### 1. `get_satisfaction_stats(course=None, start_date=None, end_date=None)`
```python
# Exemplo: Obter estatísticas de um curso
import frappe
from lms_course_survey.satisfacao.api import get_satisfaction_stats

stats = frappe.call({
    'method': 'lms_course_survey.satisfacao.api.get_satisfaction_stats',
    'args': {
        'course': 'Course-001',
        'start_date': '2026-01-01',
        'end_date': '2026-06-30'
    },
    'callback': function(r) {
        console.log(r.message);
    }
});
```

**Retorno**:
```json
{
  "total_surveys": 45,
  "average_rating": 4.2,
  "by_item": {
    "Treinamento": {
      "average": 4.1,
      "count": 45,
      "distribution": {1: 2, 2: 3, 3: 5, 4: 15, 5: 20}
    },
    "Instrutor": {
      "average": 4.3,
      "count": 45,
      "distribution": {1: 1, 2: 2, 3: 4, 4: 18, 5: 20}
    },
    ...
  }
}
```

### 2. `create_default_satisfaction_items(satisfaction_doc)`
```python
# Cria automaticamente os 4 itens padrão
frappe.call({
    'method': 'lms_course_survey.satisfacao.api.create_default_satisfaction_items',
    'args': {'satisfaction_doc': 'SAT-060126-00001'}
});
```

### 3. `get_course_satisfaction_summary(course)`
```python
# Resumo rápido de satisfação de um curso
frappe.call({
    'method': 'lms_course_survey.satisfacao.api.get_course_satisfaction_summary',
    'args': {'course': 'Course-001'},
    'callback': function(r) {
        console.log(r.message);
    }
});
```

---

## 📈 Relatórios

### Satisfaction Dashboard
- **Tipo**: Query Report
- **Localização**: Awesome Bar > Satisfaction Dashboard
- **Colunas**:
  - Item de Avaliação
  - Total de Respostas
  - Nota Média
  - Distribuição por Nota (1-5)
  - % de Satisfeitos (4-5)

**Filtros**:
- Curso (opcional)
- Data Início (opcional)
- Data Fim (opcional)

---

## 🔐 Permissões

### Por Padrão

| Grupo | Permissões |
|-------|-----------|
| Administrator | Criar, Ler, Escrever, Deletar, Submeter, Relatórios |
| User | Criar, Ler, Escrever, Submeter (próprias pesquisas) |
| Teacher/Instructor | Ler, Relatórios |

---

## 🛠️ Customizações Possíveis

### 1. Alterar Itens de Avaliação

Edite a lista em:
- `lms_course_survey/satisfacao/doctype/satisfaction_item/satisfaction_item.json` (campo `options` em `rating`)
- `lms_course_survey/satisfacao/api.py` (função `create_default_satisfaction_items`)

### 2. Adicionar Mais Perguntas

1. Edite `Course Satisfaction` JSON
2. Adicione novos Child Tables (se necessário)
3. Atualize validações em `.py`

### 3. Integrar com Avaliações

Adicione em `Course Satisfaction` DocType:
```python
def before_submit(self):
    # Marcar avaliação como pesquisa completada
    if self.course:
        frappe.db.set_value('Evaluation', self.course, 
            'satisfaction_completed', 1)
```

---

## 📝 Exemplo de Fluxo Completo

```
1. Aluno acessa Sistema
   ↓
2. Antes de Prova/Avaliação:
   - Sistema redireciona para Course Satisfaction
   ↓
3. Aluno responde 4 perguntas:
   - Treinamento: nota
   - Instrutor: nota
   - Conteúdo: nota
   - Satisfação Geral: nota
   ↓
4. Aluno adiciona feedback (opcional)
   ↓
5. Aluno clica "Submeter"
   ↓
6. Sistema registra pesquisa
   ↓
7. Professor/Gestor visualiza:
   - Dashboard em tempo real
   - Relatório agregado
   - Tendências por curso
```

---

## 🧪 Executando Testes

```bash
# Entrar no bench
cd $BENCH_PATH

# Rodar testes do módulo
bench --site seu_site.local run-tests lms_course_survey.satisfacao.tests.test_course_satisfaction

# Ou testes específicos
bench --site seu_site.local run-tests lms_course_survey.satisfacao.tests.test_course_satisfaction.TestCourseSatisfaction.test_create_course_satisfaction
```

---

## 🚨 Troubleshooting

### Problema: DocTypes não aparecem no Awesome Bar
**Solução**:
```bash
# Fazer migrate dos doctypes
bench --site seu_site.local bench --site seu_site.local execute frappe.client.make_doc \
    doctype='DocType' \
    name='Course Satisfaction'
```

### Problema: Relatório retorna erro
**Solução**:
```bash
# Limpar cache
bench --site seu_site.local clear-cache

# Recarregar página
```

### Problema: Validação de 4 itens falha
**Solução**:
- Verifique se os 4 items foram adicionados com exatamente:
  - `Treinamento`
  - `Instrutor`
  - `Conteúdo`
  - `Satisfação Geral`

---

## 📦 Arquivos Criados

```
lms_course_survey/
├── lms_course_survey/
│   ├── satisfacao/
│   │   ├── doctype/
│   │   │   ├── course_satisfaction/
│   │   │   │   ├── course_satisfaction.json
│   │   │   │   ├── course_satisfaction.py
│   │   │   │   └── __init__.py
│   │   │   ├── satisfaction_item/
│   │   │   │   ├── satisfaction_item.json
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── report/
│   │   │   ├── satisfaction_dashboard/
│   │   │   │   ├── satisfaction_dashboard.py
│   │   │   │   ├── satisfaction_dashboard.json
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── tests/
│   │   │   ├── test_course_satisfaction.py
│   │   │   └── __init__.py
│   │   ├── api.py
│   │   ├── dashboard.py
│   │   └── __init__.py
│   ├── api/
│   │   ├── permission.py
│   │   └── __init__.py
│   ├── modules.txt ✏️ Atualizado
│   └── hooks.py ✏️ Atualizado
└── SATISFACAO.md (este arquivo)
```

---

## 🤝 Suporte

Para dúvidas ou problemas:
1. Verifique os logs: `bench --site seu_site.local logs`
2. Teste via console: `frappe.call({'method': '...'})`
3. Consulte a documentação oficial: https://frappeframework.com/docs/v16

---

**Versão**: 1.0  
**Data**: 2026-06-15  
**Autor**: GL SOLTEC  
**Licença**: MIT
