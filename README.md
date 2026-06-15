# 📊 Pesquisa de Satisfação para LMS - ERPNext v16

> Sistema completo de pesquisas de satisfação integrado ao LMS (Learning Management System) do ERPNext v16 com suporte a múltiplas fases, modal automático após conclusão de cursos e mecanismos de reforço para garantir adesão dos alunos.

---

## 📋 Informações do Projeto

| Campo | Valor |
|-------|-------|
| **Nome** | LMS Course Survey |
| **Título Português** | Pesquisa de Satisfação para Cursos |
| **Autor** | GL SOLTEC |
| **Email** | ti@glsoltec.com.br |
| **Licença** | MIT |
| **Versão ERPNext** | 16 |
| **Status** | ✅ Pronto para Produção |
| **Data de Lançamento** | 2026-06-15 |

---

## ✨ Funcionalidades

### 🎯 **Fase 1: Pesquisa Core**
- ✅ 4 perguntas padrão (Treinamento, Instrutor, Conteúdo, Satisfação Geral)
- ✅ Escala de avaliação 1-5
- ✅ Feedback textual opcional
- ✅ Autopreenchimento de data
- ✅ Validação automática

### 📱 **Fase 2: Modal Automático**
- ✅ Detecção automática do último capítulo do curso
- ✅ Modal elegante ao final da última aula
- ✅ Botões "Responder Agora" e "Responder Depois"
- ✅ Redirecionamento automático para pesquisa
- ✅ Design responsivo com animações

### 🛡️ **Fase 3: Mecanismos de Reforço**
- ✅ **Bloqueio de Certificado**: Impede geração sem responder
- ✅ **Lembretes Automáticos**: Emails diários para pendentes
- ✅ **Widget Dashboard**: Visualiza pesquisas pendentes
- ✅ **Relatórios**: Acompanhamento de compliance

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
- Scheduler ativo para jobs automáticos

---

## 🚀 Instalação

### Pré-requisitos
Certifique-se de ter um ambiente Frappe/ERPNext v16 configurado com bench.

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

### 1. Ativar Scheduler (Necessário para Lembretes)

```bash
# Verificar status
bench scheduler-status

# Se parado, iniciar
bench start-scheduler
```

### 2. Configurar Email (Para Lembretes Automáticos)

No ERPNext:
1. Acesse **Setup → Email Account**
2. Configure sua conta SMTP
3. Teste a conexão

### 3. Configuração de Permissões

As permissões são gerenciadas automaticamente por:
- **Estudantes**: Podem responder suas próprias pesquisas
- **Instrutores**: Podem visualizar resultados dos seus cursos
- **Administradores**: Acesso total

---

## 📖 Como Usar

### Para Alunos

#### Respondendo a Pesquisa

1. **Após finalizar o último capítulo** → Modal automático aparece
2. **Clique em "Responder Agora"** → Abrir formulário
3. **Preencha as 4 questões** → Escala 1-5
4. **Adicione feedback (opcional)** → Campo de texto
5. **Clique em "Submeter"** → Pesquisa salva

#### Visualizar Pesquisas Pendentes

1. Acesse **Dashboard pessoal**
2. Veja widget **"Pesquisas Pendentes"**
3. Clique em curso para responder

### Para Gestores/Instrutores

#### Acessar Resultados

1. Vá para **Pesquisa de Satisfação**
2. Filtre por Curso ou Período
3. Visualize relatórios e estatísticas

#### Monitorar Compliance

1. Acesse **Relatório de Pesquisas Pendentes**
2. Veja alunos que ainda não responderam
3. Envie lembretes manualmente se necessário

---

## 📁 Estrutura do Projeto

```
lms_course_survey/
├── lms_course_survey/
│   ├── __init__.py
│   ├── hooks.py                              # Configurações e hooks
│   ├── modules.txt                           # Definição de módulos
│   ├── templates/
│   │   └── pages/
│   │       └── course_satisfaction_form.html # Formulário web
│   └── public/
│       ├── js/
│       │   ├── course_satisfaction.js        # Lógica form desk
│       │   └── course_chapter_redirect.js    # Modal automático
│       └── css/
│           └── course_satisfaction.css       # Estilos
│
├── satisfacao/                                # Módulo principal
│   ├── __init__.py
│   ├── api.py                                # APIs REST
│   ├── dashboard.py                          # Dashboard data
│   ├── certificate_validation.py             # Bloqueio certificado
│   ├── survey_reminders.py                   # Lembretes automáticos
│   ├── pending_surveys_widget.py             # Widget dashboard
│   ├── course_chapter_integration.py         # Integração capítulos
│   ├── doctype/
│   │   ├── course_satisfaction/              # DocType principal
│   │   │   ├── course_satisfaction.json
│   │   │   └── course_satisfaction.py
│   │   └── satisfaction_item/                # Child table
│   │       ├── satisfaction_item.json
│   │       └── satisfaction_item.py
│   ├── report/
│   │   └── satisfaction_dashboard/
│   │       └── satisfaction_dashboard.py     # Query Report
│   └── tests/
│       └── test_course_satisfaction.py       # Testes unitários
│
├── docs/                                      # Documentação
│   ├── INSTALL.md                            # Guia de instalação
│   ├── NON_COMPLIANCE_SOLUTIONS.md            # Mecanismos de reforço
│   ├── COURSE_CHAPTER_INTEGRATION.md         # Integração capítulos
│   └── DEPLOYMENT_CHECKLIST.md               # Checklist deploy
│
├── README.md                                  # Este arquivo
├── LICENSE                                    # MIT License
└── .gitignore
```

---

## 🔗 Documentação Completa

| Documento | Descrição |
|-----------|-----------|
| **[INSTALL.md](docs/INSTALL.md)** | Guia detalhado de instalação e troubleshooting |
| **[NON_COMPLIANCE_SOLUTIONS.md](docs/NON_COMPLIANCE_SOLUTIONS.md)** | 3 soluções para garantir respostas (bloqueio, lembretes, dashboard) |
| **[COURSE_CHAPTER_INTEGRATION.md](docs/COURSE_CHAPTER_INTEGRATION.md)** | Como a modal automática funciona e APIs |
| **[DEPLOYMENT_CHECKLIST.md](docs/DEPLOYMENT_CHECKLIST.md)** | Checklist antes de ir para produção |
| **[SATISFACAO.md](docs/SATISFACAO.md)** | Documentação técnica dos DocTypes |

---

## 🧪 Testando a Aplicação

### Teste Manual da Pesquisa

```bash
# 1. Acesse o desk do ERPNext
# 2. Vá para: Pesquisa de Satisfação → Novo
# 3. Preencha:
#    - Aluno: escolha um usuário
#    - Curso: escolha um curso LMS
#    - Itens: 4 perguntas padrão (auto-preenchidas)
# 4. Clique Submeter
```

### Teste do Modal Automático

```bash
# 1. Crie um curso com múltiplos capítulos
# 2. Aluno acessa último capítulo
# 3. Modal deve aparecer automaticamente
# 4. Botões "Responder Agora" e "Depois" funcionam
```

### Teste de Lembretes

```bash
# Via console Frappe:
from lms_course_survey.satisfacao.survey_reminders import send_survey_reminders
send_survey_reminders()

# Verificar logs:
tail -f /home/frappe/frappe-bench/logs/schedule.log
```

---

## 🐛 Troubleshooting

### Erro: "No module named 'lms_course_survey.satisfação'"

**Solução**: O arquivo `modules.txt` contém caracteres especiais. Corrija para `Satisfacao` sem til.

```bash
# Em modules.txt linha 2:
# Altere: Satisfação
# Para: Satisfacao
```

### Modal não aparece após último capítulo

**Verificar**:
1. JavaScript `course_chapter_redirect.js` está carregado no console
2. `app_include_js` em `hooks.py` contém `course_chapter_redirect.js`
3. Cache limpo: `bench clear-cache`

### Emails de lembrete não são enviados

**Verificar**:
1. Scheduler está rodando: `bench scheduler-status`
2. Email account está configurado em Setup → Email Account
3. Logs: `tail -f logs/schedule.log`

### Bloqueio de certificado não funciona

**Verificar**:
1. `doc_events` em `hooks.py` contém hook para `Course Completion Certificate`
2. `certificate_validation.py` está no caminho correto
3. Migrate foi executado: `bench migrate`

---

## 🔐 Segurança

### Boas Práticas Implementadas

✅ **Validação de Dados**: Todos os campos validados server-side  
✅ **Permissões**: Whitelisted methods, sem acesso anônimo  
✅ **CSRF Protection**: Frappe padrão habilitado  
✅ **SQL Injection Prevention**: ORM Frappe previne injeções  
✅ **XSS Prevention**: Sanitização automática de HTML  

### Recomendações para Produção

1. **Backup regular** do banco de dados
2. **Monitorar logs** para atividades suspeitas
3. **Atualizar** regularmente Frappe/ERPNext
4. **SSL/TLS** em produção (obrigatório)
5. **GDPR Compliance**: Pesquisas contêm dados pessoais

---

## 📊 Estatísticas & Métricas

### Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/method/lms_course_survey.api.get_satisfaction_stats` | Stats gerais |
| GET | `/api/method/lms_course_survey.api.get_course_satisfaction_summary` | Resumo curso |
| GET | `/api/method/lms_course_survey.satisfacao.pending_surveys_widget.get_pending_surveys_data` | Pesquisas pendentes |
| POST | `/api/method/lms_course_survey.api.create_default_satisfaction_items` | Criar itens padrão |

---

## 📝 Licença

MIT License - Veja arquivo [LICENSE](LICENSE) para detalhes completos.

Basicamente: use livremente, modificar, distribuir, inclusive comercialmente. 
Apenas mencione a autoria original (GL SOLTEC).

---

## 📧 Suporte & Contribuição

### Reportar Bugs

1. Abra uma [Issue no GitHub](https://github.com/glsoltec/lms_course_survey/issues)
2. Descreva o problema com detalhes
3. Inclua logs e screenshots se possível

### Contribuir

```bash
# 1. Fork o repositório
# 2. Crie sua branch: git checkout -b feature/nova-funcionalidade
# 3. Commit mudanças: git commit -am 'Add feature'
# 4. Push: git push origin feature/nova-funcionalidade
# 5. Abra Pull Request
```

### Requisitos para Contribuição

- Python 3.10+
- Frappe/ERPNext v16
- Pre-commit hooks instalados
- Código seguindo PEP 8

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
| 1.0 | 2026-06-15 | 🎉 Release inicial com todas as 3 fases |

---

## 📚 Referências

- [ERPNext Documentation](https://docs.erpnext.com)
- [Frappe Framework](https://frappe.io)
- [Bench Documentation](https://frappeframework.com/docs/user/en/guides/deployment)
- [LMS Module](https://docs.erpnext.com/docs/user/manual/en/modules/learning)

---

## ⚖️ Aviso Legal

Este software é fornecido "como está", sem garantias de nenhum tipo. 
Para informações detalhadas, consulte a licença MIT incluída no repositório.

---

**Versão do README**: 1.0  
**Última atualização**: 2026-06-15  
**Status**: ✅ Pronto para Produção
