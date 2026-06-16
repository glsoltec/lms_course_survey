# 🚀 Quick Start - Course Feedback

Guia rápido para começar a usar o sistema de feedback.

---

## ✅ Pré-requisitos

- ERPNext v16 instalado
- App `lms_course_survey` instalada via `bench install-app lms_course_survey`
- Migração executada: `bench migrate`
- Cache limpo: `bench clear-cache`

---

## 📋 5 Minutos de Setup

### 1️⃣ Verificar Instalação

```bash
# Acessar console Frappe
bench --site seu_site console

# Verificar se DocType existe
frappe.db.exists("DocType", "Course Feedback")
# Deve retornar: 'Course Feedback'

# Sair
exit()
```

### 2️⃣ Testar Criação de Feedback

```
1. Acesse ERPNext
2. Menu → Feedback de Cursos → Novo
3. Preencha:
   - Curso: Selecione um curso LMS
   - Instructor Rating: Escolha uma opção
   - Content Rating: Escolha uma opção
   - Course Rating: Escolha uma opção
   - Overall Rating: Escolha uma opção
4. Clique "Submeter"
```

### 3️⃣ Testar Bloqueio de Certificado

```
1. Tente gerar certificado para aluno que NÃO respondeu feedback
2. Deve aparecer erro: "📋 Feedback Obrigatório"
3. Responda o feedback conforme passo 2
4. Tente novamente → deve funcionar
```

### 4️⃣ Visualizar Dashboard

```
1. Vá para Menu → Feedback de Cursos
2. Dashboard deve mostrar:
   ✅ Cards com métricas (total, média)
   ✅ Gráfico comparativo de ratings
```

---

## 🔗 URLs Úteis

| Funcionalidade | URL |
|---|---|
| Criar Feedback | `/app/course-feedback` |
| Feedback de Curso Específico | `/app/course-feedback?course=NOME_DO_CURSO` |
| Ver Todos os Feedbacks | `/app/course-feedback-list` |
| Dashboard | `/app/course-feedback` |

---

## 🎯 Fluxo de Uso

```
┌─────────────────────────────────────┐
│     Aluno Completa Curso            │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   Aluno Tenta Gerar Certificado     │
└──────────────┬──────────────────────┘
               ↓
        ┌──────────────┐
        │ Feedback     │
        │ respondido?  │
        └──────┬───────┘
         SIM ↓ NÃO
             │  └─────────────────────┐
             │                        ↓
             │         ┌──────────────────────────┐
             │         │ ❌ Erro: Feedback Pendente│
             │         │ → Exibe link para         │
             │         │   responder feedback      │
             │         └──────────────────────────┘
             │                        │
             │                        ↓
             │         ┌──────────────────────────┐
             │         │   Aluno Responde         │
             │         │   Feedback               │
             │         └──────────────────────────┘
             │                        │
             └────────────┬───────────┘
                          ↓
          ┌──────────────────────────┐
          │   ✅ Certificado Gerado   │
          └──────────────────────────┘
```

---

## 📊 Entendendo as Avaliações

### Opções de Rating

```
Péssimo  → Insatisfeito, não recomenda
Ruim     → Problemas significativos
Regular  → Atende minimamente
Bom      → Atende bem às expectativas
Ótimo    → Superou expectativas
```

### Dashboard

O dashboard mostra a **média das avaliações** em formato numérico (1-5):

```
Péssimo  = 1.0
Ruim     = 2.0
Regular  = 3.0
Bom      = 4.0
Ótimo    = 5.0
```

**Exemplo**: Se 2 alunos escolhem "Bom" e 1 escolhe "Ótimo":
```
Média = (4 + 4 + 5) / 3 = 4.33
```

---

## 🔍 Verificações de Troubleshooting

### Checklist

```bash
# 1. App instalada?
bench --site seu_site list-apps | grep lms_course_survey

# 2. DocType existe?
bench --site seu_site console
frappe.db.exists("DocType", "Course Feedback")
# Deve retornar: 'Course Feedback'

# 3. Permissões configuradas?
# Role Permissions Manager → Course Feedback
# Student: Create, Write, Submit
# System Manager: (all)

# 4. Hook configurado?
# Verificar em hooks.py: doc_events para Course Completion Certificate

# 5. Cache limpo?
bench --site seu_site clear-cache
```

---

## 💡 Dicas Importantes

### ✅ Boas Práticas

1. **Sempre fazer backup antes de migrar**
   ```bash
   bench --site seu_site backup
   ```

2. **Limpar cache após mudanças**
   ```bash
   bench --site seu_site clear-cache
   ```

3. **Criar feedback de teste**
   - Responda como aluno de teste
   - Verifique se bloqueio de certificado funciona

4. **Monitorar comentários**
   - Campo feedback_comments contém sugestões valiosas
   - Exportar para análise de melhoria contínua

### ❌ Evitar

- ❌ Editar feedback após submit (imutável por design)
- ❌ Deletar registros manualmente (afeta auditoria)
- ❌ Alterar permissões sem entender impacto

---

## 📞 Suporte Rápido

| Problema | Solução |
|---|---|
| Feedback não aparece após submit | Limpar cache: `bench clear-cache` |
| DocType não existe | Executar migrate: `bench migrate` |
| Aluno não consegue responder | Verificar role: Student deve ter Create permission |
| Certificado gerado sem feedback | Verificar hook em hooks.py |

---

## 🔗 Próximos Passos

1. ✅ Instalar app
2. ✅ Testar feedback (passo 2)
3. ✅ Testar bloqueio (passo 3)
4. ✅ Configurar permissões específicas se necessário
5. ✅ Treinar alunos/gestores
6. ✅ Acompanhar dados no dashboard

---

**Precisa de ajuda?** Consulte [README.md](README.md) para documentação completa.
