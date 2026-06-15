# 🔗 Integração com Course Chapter — Pesquisa Automática

## 🎯 Objetivo

Após o aluno **completar o último capítulo de um curso**, ele é automaticamente redirecionado para responder a **pesquisa de satisfação**.

---

## 📊 Fluxo Completo

```
1. Aluno acessa Course (LMS)
   ↓
2. Lê capítulos sequencialmente
   ↓
3. Chega no ÚLTIMO capítulo
   ↓
4. Sistema detecta conclusão
   ↓
5. Modal aparece: "Parabéns! Responda pesquisa?"
   ↓
6. Aluno clica em "Ir para Pesquisa"
   ↓
7. Redireciona para formulário bonito de satisfação
   ↓
8. Aluno responde 4 perguntas (1-5)
   ↓
9. Submete pesquisa
   ↓
10. Feedback salvo no banco de dados ✅
```

---

## 🔧 Como Funciona

### 1️⃣ Detecção de Último Capítulo

```python
# Em course_chapter_integration.py
def is_last_chapter(course, chapter):
    """Verifica se é o último capítulo"""
    chapters = frappe.get_list("Course Chapter", filters={"course": course})
    return chapters[-1] == chapter
```

### 2️⃣ Redirecionamento Automático

```javascript
// Em course_chapter_redirect.js
frappe.call({
    method: "after_chapter_completion",
    args: {course: course, course_chapter: chapter},
    callback: function(r) {
        if (r.message.status === "redirect_survey") {
            show_survey_prompt(r.message);
        }
    }
});
```

### 3️⃣ Formulário Web Customizado

- **Arquivo**: `course_satisfaction_form.html`
- **Localização**: `/app/course-satisfaction-form?course=COURSE-ID&course_chapter=CHAPTER-ID`
- **Interface**: Botões coloridos para ratings (1-5)
- **Responsivo**: Funciona em desktop, tablet e mobile

---

## 📄 Componentes Criados

| Arquivo | Função |
|---------|--------|
| `course_satisfaction_form.html` | Formulário web customizado |
| `course_chapter_integration.py` | Lógica de integração + APIs |
| `course_chapter_redirect.js` | Detecção e redirecionamento |
| `course_satisfaction.css` | Estilos visuais |
| `course_satisfaction.json` | Campo `course_chapter` adicionado |

---

## 🚀 Como Usar

### Para Alunos

```
1. Acesse seu Course no LMS
2. Leia todos os capítulos
3. No último capítulo, você verá:
   ✨ Modal: "Parabéns! Pesquisa de Satisfação?"
4. Clique em "Ir para Pesquisa"
5. Responda as 4 perguntas
6. Clique "Submeter"
7. Pronto! ✅
```

### Para Desenvolvedores

#### Verificar se pesquisa foi respondida
```python
from lms_course_survey.satisfacao.course_chapter_integration import check_survey_completed

completed = check_survey_completed('user@example.com', 'COURSE-001')
# Retorna: True/False
```

#### Gerar URL de pesquisa
```python
from lms_course_survey.satisfacao.course_chapter_integration import get_satisfaction_survey_url

url = get_satisfaction_survey_url('COURSE-001', 'CHAPTER-005')
# Retorna: /app/course-satisfaction-form?course=COURSE-001&course_chapter=CHAPTER-005
```

#### Redirecionar manualmente
```javascript
// No navegador
redirect_to_satisfaction_survey('COURSE-001', 'CHAPTER-005');
```

#### Verificar status da pesquisa
```javascript
// No navegador
check_satisfaction_status('COURSE-001', function(r) {
    console.log(r.message.status); // 'completed' ou 'pending'
});
```

---

## 📋 APIs Disponíveis

### `after_chapter_completion(course, course_chapter)`

**Descrição**: Verifica se é último capítulo e retorna URL de redirecionamento

**Parâmetros**:
- `course` (string): Nome do Course
- `course_chapter` (string): Nome do Chapter

**Retorno**:
```json
{
  "status": "redirect_survey",
  "message": {
    "indicator": "green",
    "title": "Parabéns! 🎉",
    "description": "Você completou o último capítulo...",
    "action": {
      "label": "Responder Pesquisa",
      "url": "/app/course-satisfaction-form?..."
    }
  },
  "survey_url": "/app/course-satisfaction-form?..."
}
```

**Exemplo**:
```javascript
frappe.call({
    method: 'lms_course_survey.satisfacao.course_chapter_integration.after_chapter_completion',
    args: {
        course: 'MAT-2026-001',
        course_chapter: 'MAT-2026-001-CP-005'
    },
    callback: function(r) {
        console.log(r.message);
    }
});
```

---

### `get_course_satisfaction_status(course)`

**Descrição**: Retorna status de pesquisa respondida

**Parâmetros**:
- `course` (string): Nome do Course

**Retorno**:
```json
{
  "status": "completed",
  "message": "Pesquisa respondida",
  "survey_name": "SAT-062326-00001",
  "survey_date": "2026-06-23 14:30:00"
}
```

ou

```json
{
  "status": "pending",
  "message": "Pesquisa não respondida"
}
```

---

## 🎨 Personalização do Formulário

### Alterar cores dos botões

Edite `public/css/course_satisfaction.css`:

```css
.rating-btn.rating-5.active {
    background: #28a745; /* Verde */
    color: white;
    border-color: #28a745;
}
```

### Adicionar campo customizado

Edite `satisfacao/doctype/course_satisfaction/course_satisfaction.json`:

```json
{
  "fieldname": "seu_campo",
  "fieldtype": "Text",
  "label": "Seu Rótulo"
}
```

### Alterar texto/labels

Edite `templates/pages/course_satisfaction_form.html`:

```html
<h5 class="fw-bold mb-3">
    Sua pergunta aqui?
</h5>
```

---

## 🔒 Segurança

✅ **Autenticação**
- Apenas usuários logados podem acessar
- Pesquisa vinculada ao usuário logado

✅ **Validação**
- Todos os 4 itens obrigatórios
- Valores restritos (1-5)

✅ **Prevenção de múltiplas respostas**
- Sistema detecta se aluno já respondeu
- Impede duplicação de dados

---

## 🧪 Testes

### Teste Local

```bash
# 1. Criar Course com 5 Chapters
bench --site seu_site console

import frappe

# Criar course
course = frappe.new_doc('Course')
course.course_name = 'Teste Integração'
course.insert()

# Criar chapters
for i in range(1, 6):
    chapter = frappe.new_doc('Course Chapter')
    chapter.course = course.name
    chapter.chapter_number = i
    chapter.title = f'Capítulo {i}'
    chapter.insert()

# 2. Simular conclusão do último capítulo
from lms_course_survey.satisfacao.course_chapter_integration import is_last_chapter

last_chapter = chapter.name
is_last = is_last_chapter(course.name, last_chapter)
print(f"É último capítulo? {is_last}")  # True

# 3. Gerar URL
from lms_course_survey.satisfacao.course_chapter_integration import get_satisfaction_survey_url

url = get_satisfaction_survey_url(course.name, last_chapter)
print(f"URL: {url}")

# 4. Acessar no navegador
# http://seu_site/app/course-satisfaction-form?course=COURSE-ID&course_chapter=CHAPTER-ID
```

### Teste do Redirecionamento

```javascript
// No console do navegador
redirect_to_satisfaction_survey('COURSE-ID', 'CHAPTER-ID');

// Verificar status
check_satisfaction_status('COURSE-ID', function(r) {
    console.log('Status:', r.message.status);
});
```

---

## 📊 Monitorar Respostas

### Dashboard em tempo real

```
1. Vá para: /app/query-report/Satisfaction%20Dashboard
2. Filtre por course específico
3. Veja estatísticas em tempo real
```

### Via API

```python
from lms_course_survey.satisfacao.api import get_course_satisfaction_summary

summary = frappe.call({
    'method': 'lms_course_survey.satisfacao.api.get_course_satisfaction_summary',
    'args': {'course': 'COURSE-001'}
})
```

---

## 🚨 Troubleshooting

| Problema | Solução |
|----------|---------|
| Modal não aparece | Verificar se `course_chapter_redirect.js` está carregado |
| Redirecionamento não funciona | Confirmar que é o último capítulo |
| Formulário não carrega | Limpar cache: `bench clear-cache` |
| Dados não salvam | Verificar permissões do usuário |
| CSS não aplica | Limpar cache do navegador (Ctrl+Shift+Delete) |

---

## 📈 Métricas

Acompanhe:
- **Taxa de conclusão**: % de alunos que responderam
- **Tempo médio**: Quanto levam para responder
- **Nota média**: Satisfação geral (meta: >4.0)
- **Feedback qualitativo**: Comentários úteis

---

## 🔧 Customizações Avançadas

### 1. Bloquear acesso ao curso até pesquisa

```python
# Em satisfacao/course_chapter_integration.py
def validate_survey_before_certificate(doc, method=None):
    """Hook: bloqueia certificado até pesquisa"""
    if doc.doctype == 'Certification':
        student = doc.student
        course = doc.course
        
        if not check_survey_completed(student, course):
            frappe.throw("Complete a pesquisa antes de gerar certificado")

# Registrar no hooks.py
doc_events = {
    'Certification': {
        'validate': 'satisfacao.course_chapter_integration.validate_survey_before_certificate'
    }
}
```

### 2. Enviar email após pesquisa

```python
def send_thank_you_email(doc, method=None):
    """Envia email agradecendo por responder"""
    if doc.doctype == 'Course Satisfaction' and doc.docstatus == 1:
        frappe.sendmail(
            recipients=[doc.student],
            subject="Obrigado por responder a pesquisa!",
            message="Sua opinião nos ajuda a melhorar..."
        )
```

### 3. Integração com n8n/Zapier

Webhook automático:
```
Quando: Course Satisfaction é criada
Então: Enviar para Google Sheets / Slack / Teams
```

---

## 📞 Suporte

Documentação relacionada:
- `SATISFACAO.md` — Manual técnico
- `INSTALL.md` — Instalação
- `API_REFERENCE.md` — Todas as APIs

---

**Versão**: 1.0  
**Data**: 2026-06-15  
**Status**: ✅ Pronto para produção
