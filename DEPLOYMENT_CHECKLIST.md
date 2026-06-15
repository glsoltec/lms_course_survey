# ✅ Checklist de Deployment — Pesquisa de Satisfação

## 🎯 Antes de Deploy

### Ambiente Local (Dev)
```
☐ Git está atualizado
☐ Todos os arquivos do módulo satisfacao/ foram criados
☐ modules.txt contém "Satisfação"
☐ hooks.py foi atualizado
☐ Sem conflitos de merge
```

### Testes Locais
```
☐ bench migrate executado
☐ bench clear-cache executado
☐ Nenhum erro no console
☐ DocTypes aparecem no Awesome Bar
☐ Formulário Course Satisfaction abre
☐ 4 itens adicionados automaticamente
☐ Validação funciona (teste submeter sem rating)
☐ Relatório abre e mostra dados
```

---

## 🚀 Passo a Passo — Deploy em Produção

### 1️⃣ Backup (CRÍTICO!)

```bash
# Banco de dados
mysqldump -u root -p erpnext_site > backup_$(date +%Y%m%d).sql

# Arquivos
tar -czf /backups/erpnext_$(date +%Y%m%d).tar.gz /home/frappe/frappe-bench/apps/lms_course_survey
```

### 2️⃣ Push no GitHub

```bash
cd /path/to/lms_course_survey

# Adicionar todos os arquivos novos
git add .

# Commit com mensagem descritiva
git commit -m "feat: Módulo de pesquisa de satisfação com 4 itens fixos

- DocType Course Satisfaction com validações
- Child Table Satisfaction Item (1-5 scale)
- Query Report com dashboard
- API com 3 funções principais
- Frontend interativo
- Testes unitários
- Documentação completa"

# Push
git push origin main
```

### 3️⃣ Atualizar em Produção

```bash
cd /home/frappe/frappe-bench

# Pull últimas mudanças
bench get-app lms_course_survey

# ou se já está instalado
cd apps/lms_course_survey && git pull

# Executar migration
bench --site seu_site.local migrate

# Limpar cache
bench --site seu_site.local clear-cache

# Reiniciar workers (se houver)
bench restart
```

### 4️⃣ Validação Pós-Deploy

```bash
# Verificar se DocTypes foram criados
bench --site seu_site.local console
```

```python
import frappe

# Teste 1: DocTypes existem
doc1 = frappe.get_doc('DocType', 'Course Satisfaction')
doc2 = frappe.get_doc('DocType', 'Satisfaction Item')
print("✅ DocTypes existem")

# Teste 2: Criar pesquisa teste
from lms_course_survey.satisfacao.api import create_default_satisfaction_items

test_doc = frappe.new_doc('Course Satisfaction')
test_doc.student = 'test@example.com'
test_doc.course = 'TEST-001'
test_doc.insert()

create_default_satisfaction_items(test_doc.name)
print(f"✅ Pesquisa teste criada: {test_doc.name}")

# Teste 3: Relatório funciona
from frappe.desk.query_report import run
result = run('Satisfaction Dashboard', filters={})
print(f"✅ Relatório retorna dados: {result}")

# Teste 4: Permissões OK
perms = frappe.get_doc('DocType', 'Course Satisfaction').permissions
print(f"✅ Permissões configuradas: {len(perms)} roles")
```

---

## 🔍 Validação em Produção

### Acessar via Web

```
1. Vá para: https://seu_site.com/app/course-satisfaction
2. Clique "+ Novo"
3. Preencha formulário
4. Submeta
5. Verifique se foi salvo

Dashboard:
1. Vá para: https://seu_site.com/app/query-report/Satisfaction%20Dashboard
2. Filtre por curso/data
3. Verifique gráficos
```

### Logs de Erro

```bash
# Se houver erros
bench --site seu_site.local logs

# Ver últimas 100 linhas
tail -100 /home/frappe/frappe-bench/logs/error.log
```

---

## 📋 Checklist de Deploy

### Pré-Deploy
```
☐ Backup do banco feito
☐ Backup dos arquivos feito
☐ Comunicado time sobre manutenção
☐ Branch pronto em Git
☐ Sem merges pendentes
☐ Testes locais passaram
```

### Deploy
```
☐ git pull executado
☐ bench migrate executado sem erros
☐ bench clear-cache executado
☐ Workers reiniciados (se aplicável)
```

### Pós-Deploy
```
☐ Website acessível
☐ DocTypes aparecem no Awesome Bar
☐ Formulário abre sem erros
☐ Relatório funciona
☐ Permissões corretas
☐ Logs sem erros críticos
```

### Comunicação
```
☐ Time informado que deploy concluído
☐ Tutorial enviado para usuários
☐ Hotline ativada para suporte
☐ Documentação disponível
```

---

## 🆘 Rollback (Se necessário)

```bash
# Desfazer última versão
cd /home/frappe/frappe-bench/apps/lms_course_survey
git revert HEAD

# Ou voltar para commit anterior
git reset --hard <commit-hash>

# Re-aplicar migrate
bench --site seu_site.local migrate

# Restaurar banco se necessário
mysql -u root -p erpnext_site < backup_YYYYMMDD.sql
```

---

## 📞 Suporte Pós-Lançamento

### Usuários Finais
1. **Tutorial**: Compartilhar `SATISFACAO.md`
2. **Vídeo**: Gravar demo de como usar
3. **Email**: Avisar alunos sobre nova funcionalidade
4. **FAQ**: Documento com perguntas comuns

### Time Técnica
1. **Docs**: Disponibilizar `SATISFACAO.md` + `INSTALL.md`
2. **Testes**: Executar testes unitários regularmente
3. **Monitoramento**: Observar performance do relatório
4. **Updates**: Manter módulo atualizado com ERPNext

---

## 🎯 KPIs de Sucesso

```
✅ Taxa de Adoção: % alunos respondendo pesquisa
✅ Tempo Médio: Quanto leva para responder (meta: <5min)
✅ Nota Média: Média geral de satisfação (meta: >4.0)
✅ Feedback Qualitativo: Comentários recebidos
✅ Sistema Performance: Tempo de resposta do relatório
```

---

## 📊 Métricas a Acompanhar

```python
# Script para monitorar
import frappe
from frappe.utils import getdate
from datetime import timedelta

# Últimos 7 dias
start_date = frappe.utils.add_days(getdate(), -7)

total = frappe.db.count(
    'Course Satisfaction',
    filters={'docstatus': 1, 'survey_date': ['>', start_date]}
)

avg_rating = frappe.db.get_value(
    'Course Satisfaction',
    filters={'docstatus': 1, 'survey_date': ['>', start_date]},
    fieldname='AVG(average_rating)'
)

print(f"Última semana:")
print(f"- Total pesquisas: {total}")
print(f"- Nota média: {avg_rating}")
```

---

## 🔐 Checklist de Segurança

```
☐ Permissões revisadas
☐ SQL injection validado (Frappe ORM protege)
☐ XSS validado (Frappe sanitiza)
☐ CSRF tokens ativados
☐ Dados sensíveis mascarados em relatórios
☐ Backup testado e verificado
☐ Rate limiting considerado para API
```

---

## 📅 Plano de Manutenção

```
Semanal:
  ☐ Verificar relatório de satisfação
  ☐ Observar comentários negativos
  ☐ Validar performance

Mensal:
  ☐ Análise de tendências
  ☐ Relatório para gestor
  ☐ Backup completo

Trimestral:
  ☐ Revisão de mudanças necessárias
  ☐ Planejamento de melhorias
  ☐ Atualização de documentação
```

---

## ✨ Go Live Sequence

```
T-24h: Backup + Comunicação
T-0h:  Deploy + Testes
T+1h:  Validação com usuários
T+4h:  Primeiro relatório
T+1d:  Check de qualidade
T+1w:  Análise de adoption
```

---

**Status**: ✅ Pronto para Deploy  
**Versão**: 1.0  
**Data**: 2026-06-15
