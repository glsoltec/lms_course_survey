# 📋 Course Feedback - ERPNext v16 LMS

> Sistema de feedback para cursos LMS no ERPNext v16, com avaliação estruturada por opções textuais (Péssimo/Ruim/Regular/Bom/Ótimo), integração com certificados e dashboard de estatísticas.

---

## 📋 Informações do Projeto

| Campo | Valor |
|-------|-------|
| **Nome** | LMS Course Feedback |
| **Título Português** | Feedback de Cursos |
| **Autor** | GL SOLTEC |
| **Email** | ti@glsoltec.com.br |
| **Licença** | MIT |
| **Versão ERPNext** | 16.x |
| **Status** | ✅ Pronto para Produção |
| **Data de Lançamento** | 2026-06-16 |

---

## ✨ Funcionalidades

### 🎯 **Sistema de Feedback Estruturado**
- ✅ 4 perguntas obrigatórias com opções textuais
  - Como você avalia a clareza nas explicações e o domínio técnico do instrutor?
  - Como você avalia a relevância e utilidade prática do material?
  - Como você avalia a organização geral, plataforma e carga horária?
  - Qual é sua avaliação geral sobre a experiência?
- ✅ Opções: Péssimo, Ruim, Regular, Bom, Ótimo
- ✅ Campo de sugestões e comentários (opcional)
- ✅ Auto-registro do aluno logado (auditoria)

### 📊 **Dashboard com Estatísticas**
- ✅ Total de feedbacks nos últimos 30 dias
- ✅ Avaliação geral média
- ✅ Gráfico comparativo por categoria (Instrutor, Conteúdo, Curso, Geral)
- ✅ Indicadores de desempenho com cores

### 🔐 **Segurança e Compliance**
- ✅ **Bloqueio de Certificado**: Impede geração sem feedback respondido
- ✅ Auditoria automática (quem respondeu, quando)
- ✅ Apenas usuários logados podem responder
- ✅ Role-based permissions (Student, Manager, Admin)

---

## 📦 Requisitos

### Sistema
- **ERPNext**: v16.x
- **Frappe Framework**: v16.x
- **Python**: 3.10+
- **Node.js**: 18+
- **Banco de Dados**: MariaDB 10.6+ ou MySQL 8.0+

### Permissões
- Acesso a bench CLI
- Permissões de administrador para instalar apps

---

## 🚀 Instalação

### Passo 1: Clone o Repositório

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app lms_course_survey https://github.com/glsoltec/lms_course_survey.git --branch version-16
```

### Passo 2: Instale a App

```bash
bench install-app lms_course_survey --site seu_site
```

### Passo 3: Execute Migrações

```bash
bench --site seu_site migrate
```

### Passo 4: Limpe o Cache

```bash
bench --site seu_site clear-cache
```

### Verificação

```bash
bench --site seu_site list-apps
# Você deve ver "lms_course_survey" na lista
```

---

## ⚙️ Configuração

### 1. Permissões de Função

As permissões são configuradas automaticamente:

**Student (Aluno)**
- ✅ Criar feedback
- ✅ Responder (Submit)
- ❌ Editar após envio
- ❌ Visualizar relatórios

**System Manager / Education Manager**
- ✅ Visualizar todos os feedbacks
- ✅ Gerar relatórios
- ✅ Exportar dados

### 2. Bloquear Certificado sem Feedback

O bloqueio é automático. Quando aluno tenta gerar certificado:

```
Se feedback não respondido:
  ❌ Gera erro: "Feedback Obrigatório"
  → Exibe link para responder feedback
  
Se feedback respondido:
  ✅ Permite gerar certificado normalmente
```

---

## 📖 Como Usar

### Para Alunos

#### Respondendo ao Feedback

1. Acesse: **Menu → Feedback de Cursos → Novo**
2. Ou acesse via link direto: `/app/course-feedback?course=seu_curso`
3. **Preencha os campos:**
   - Curso Avaliado (obrigatório)
   - 4 perguntas com opções Péssimo/Ruim/Regular/Bom/Ótimo
   - Comentários (opcional)
4. **Clique em "Submeter"**
5. Feedback salvo com auditoria (aluno, data, hora)

#### Ao Tentar Gerar Certificado

1. Se feedback **pendente** → Erro com link para responder
2. Se feedback **respondido** → Certificado gerado normalmente

### Para Gestores

#### Acessar Resultados

1. Vá para **Feedback de Cursos**
2. Visualize dashboard com estatísticas
3. Filtre por curso, data, aluno
4. Exporte dados para análise

#### Ver Estatísticas

- Dashboard mostra gráfico comparativo
- Médias por categoria (Instrutor, Conteúdo, etc)
- Total de feedbacks nos últimos 30 dias

---

## 📁 Estrutura do Projeto

```
lms_course_survey/
├── lms_course_survey/
│   ├── __init__.py
│   ├── hooks.py                           # Configurações principais
│   ├── modules.txt                        # Definição de módulos
│   └── public/
│       └── js/
│           └── course_satisfaction.js     # Scripts da form
│
├── satisfacao/                             # Módulo principal
│   ├── __init__.py
│   ├── api.py                             # APIs REST (se necessário)
│   ├── dashboard.py                       # Dashboard statistics
│   ├── certificate_validation.py          # Bloqueio de certificado
│   ├── api/
│   │   └── permission.py                  # Controle de permissões
│   ├── doctype/
│   │   └── course_feedback/
│   │       ├── __init__.py
│   │       ├── course_feedback.json       # Definição do DocType
│   │       ├── course_feedback.py         # Lógica Python
│   │       └── course_feedback.js         # Scripts da form
│   └── tests/
│       └── test_course_feedback.py        # Testes unitários
│
├── README.md                              # Este arquivo
├── LICENSE                                 # MIT License
└── .gitignore
```

---

## 🔗 Estrutura de Dados

### DocType: Course Feedback

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-----------|-----------|
| `student` | Link (User) | Sim | Preenchido automaticamente |
| `course` | Link (LMS Course) | Sim | Curso avaliado |
| `instructor_rating` | Select | Sim | Instrutor: Péssimo/Ruim/Regular/Bom/Ótimo |
| `content_rating` | Select | Sim | Conteúdo: Péssimo/Ruim/Regular/Bom/Ótimo |
| `course_rating` | Select | Sim | Curso: Péssimo/Ruim/Regular/Bom/Ótimo |
| `overall_rating` | Select | Sim | Geral: Péssimo/Ruim/Regular/Bom/Ótimo |
| `feedback_comments` | Small Text | Não | Sugestões e comentários |
| `submitted_date` | Datetime | Sim | Data/hora de envio (auto) |

---

## 🧪 Testando a Aplicação

### Teste Manual

```bash
# 1. Acesse o desk do ERPNext
# 2. Vá para: Feedback de Cursos → Novo
# 3. Preencha:
#    - Curso: escolha um curso LMS
#    - Ratings: selecione opções para cada pergunta
#    - Comentários: opcional
# 4. Clique Submeter
```

### Teste de Bloqueio de Certificado

```bash
# 1. Tente gerar certificado para aluno que NÃO respondeu feedback
# 2. Deve exibir erro: "Feedback Obrigatório"
# 3. Responda o feedback
# 4. Tente novamente → deve funcionar
```

### Teste de Dashboard

```bash
# 1. Acesse Feedback de Cursos
# 2. Dashboard deve mostrar:
#    - Cards com total e média
#    - Gráfico com comparativo
# 3. Dados devem estar corretos
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'lms_course_survey.satisfacao'"

**Verificar**:
- `modules.txt` contém `Satisfacao` (sem til)
- Não use caracteres especiais em nomes de módulos Python

### DocType não aparece

**Verificar**:
1. Migração executada: `bench migrate`
2. Cache limpo: `bench clear-cache`
3. Permissions configuradas: Role Permissions Manager

### Bloqueio de certificado não funciona

**Verificar**:
1. Hook configurado em `hooks.py` → `doc_events`
2. Caminho correto: `certificate_validation.validate_certificate_needs_feedback`
3. Migrate foi executado

### Dados não aparecem no dashboard

**Verificar**:
1. Feedbacks foram submetidos (docstatus = 1)
2. Data está dentro dos últimos 30 dias
3. Cache limpo: `bench clear-cache`

---

## 🔐 Segurança

### Boas Práticas Implementadas

✅ **Validação de Dados**: Server-side validation  
✅ **Permissões**: Role-based, whitelist de métodos  
✅ **Auditoria**: Track changes habilitado  
✅ **Imutabilidade**: Submittable (não pode editar após envio)  
✅ **Usuário**: Auto-registrado via `frappe.session.user`

### Recomendações para Produção

1. **Backup regular** do banco de dados
2. **Monitorar logs** para atividades anormais
3. **Atualizar** regularmente Frappe/ERPNext
4. **SSL/TLS** em produção (obrigatório)

---

## 📊 APIs REST Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/method/lms_course_survey.satisfacao.certificate_validation.get_feedback_completion_status` | Status do feedback |
| GET | `/api/method/lms_course_survey.satisfacao.certificate_validation.get_pending_feedbacks` | Feedbacks pendentes |

---

## 📊 Relatórios e Exportação

### Via Desk

1. Vá para **Feedback de Cursos**
2. Clique em **Menu** → **Report Builder**
3. Filtre por período, curso, aluno
4. Exporte para CSV/Excel

### Via API

```python
# Python/console Frappe
from lms_course_survey.satisfacao.doctype.course_feedback.course_feedback import CourseFeedback

stats = CourseFeedback.get_feedback_stats(course="seu_curso")
print(stats)
# Retorna: {
#   "total_feedbacks": 10,
#   "instructor_avg": 4.2,
#   "content_avg": 3.8,
#   "course_avg": 4.0,
#   "overall_avg": 4.0
# }
```

---

## 📝 Licença

MIT License - Veja arquivo [LICENSE](LICENSE) para detalhes.

Resumidamente: use livremente, modifique, distribua. Mencione a autoria original (GL SOLTEC).

---

## 📧 Suporte & Contribuição

### Reportar Bugs

1. Abra uma [Issue no GitHub](https://github.com/glsoltec/lms_course_survey/issues)
2. Descreva o problema com detalhes
3. Inclua logs se possível

### Contribuir

```bash
# 1. Fork o repositório
# 2. Crie sua branch: git checkout -b feature/sua-feature
# 3. Commit: git commit -am 'Add feature'
# 4. Push: git push origin feature/sua-feature
# 5. Abra Pull Request
```

---

## 🤝 Contato

**GL SOLTEC**
- 📧 Email: ti@glsoltec.com.br
- 🌐 Website: [glsoltec.com.br](https://www.glsoltec.com.br)
- 🐙 GitHub: [@glsoltec](https://github.com/glsoltec)

---

## 🗓️ Histórico de Versões

| Versão | Data | Notas |
|--------|------|-------|
| 2.0 | 2026-06-16 | Refactoring: Course Feedback com opções textuais |
| 1.0 | 2026-06-15 | Release inicial com Course Satisfaction (descontinuado) |

---

## 📚 Referências

- [ERPNext Documentation](https://docs.erpnext.com)
- [Frappe Framework](https://frappe.io)
- [DocType Documentation](https://docs.erpnext.com/docs/user/manual/en/customize-erpnext/custom-field)

---

**Versão do README**: 2.0  
**Última atualização**: 2026-06-16  
**Status**: ✅ Pronto para Produção
