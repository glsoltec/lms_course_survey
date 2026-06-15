# 🚀 Guia de Instalação — Pesquisa de Satisfação

## Pré-requisitos

- ERPNext v16
- Bench CLI instalado
- Acesso de Administrator

## Instalação Rápida

### 1️⃣ Sincronizar DocTypes

```bash
cd $BENCH_PATH

# Entrar no site
bench --site seu_site.local execute frappe.utils.fixtures.sync_doctypes
```

Ou via interface:

```bash
# No seu bench
bench --site seu_site.local console

# Dentro do console Python:
>>> import frappe
>>> from frappe.utils.fixtures import sync_doctypes
>>> sync_doctypes('lms_course_survey')
```

### 2️⃣ Executar Migrate

```bash
bench --site seu_site.local migrate
```

### 3️⃣ Limpar Cache

```bash
bench --site seu_site.local clear-cache
```

### 4️⃣ Reiniciar Bench (Desenvolvimento)

```bash
# Parar bench
bench stop

# Iniciar novamente
bench start
```

---

## ✔️ Validação

### Verificar se DocTypes foram criados

```bash
bench --site seu_site.local console
```

```python
import frappe

# Verificar DocTypes
frappe.get_doc('DocType', 'Course Satisfaction')
frappe.get_doc('DocType', 'Satisfaction Item')

# Listar campos
doc = frappe.get_doc('DocType', 'Course Satisfaction')
for field in doc.fields:
    print(f"{field.fieldname}: {field.fieldtype}")
```

### Testar Criação de Pesquisa

```python
import frappe

doc = frappe.new_doc('Course Satisfaction')
doc.student = 'test_user@example.com'
doc.course = 'Test Course'
doc.append('satisfaction_items', {
    'item_name': 'Treinamento',
    'rating': '5 - Ótimo'
})

doc.insert()
print(f"Pesquisa criada: {doc.name}")
```

---

## 🎯 Uso Imediato

### Acessar via Interface Web

1. Acesse: `http://seu_site.local/app/course-satisfaction`
2. Clique em "+ Novo"
3. Preencha aluno e curso
4. Avalie os 4 itens
5. Submeta

### Ver Relatório

1. Acesse: `http://seu_site.local/app/query-report/Satisfaction%20Dashboard`
2. Visualize gráficos e estatísticas

---

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| DocType não aparece | `bench migrate` + `bench clear-cache` |
| Erro ao submeter pesquisa | Verifique validação Python em `course_satisfaction.py` |
| Relatório vazio | Certifique-se de que existe pelo menos uma pesquisa com `docstatus=1` |
| Permissões negadas | Verifique role do usuário (Admin/User/Teacher) |

---

## 📝 Próximos Passos Opcionais

### 1. Criar Trigger para Avisar Alunos
```python
# Adicionar em satisfacao/api.py
def send_survey_reminder(course):
    # Email para alunos do curso
    pass
```

### 2. Integrar com Avaliação (Exam/Assessment)
```python
# Adicionar campo em Course Satisfaction:
# - exam_name (Link → Exam)
# Validação: bloquear submissão de exam até pesquisa ser feita
```

### 3. Exportar Dados para Excel
```python
# Adicionar em satisfacao/api.py
def export_satisfaction_excel(course, start_date, end_date):
    pass
```

---

## 📞 Suporte

Documentação completa: `SATISFACAO.md`

---

**Última atualização**: 2026-06-15
