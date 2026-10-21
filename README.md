# Workspace Assistant

Integración modular y segura de **Google Workspace** para un agente autónomo:
Gmail, Calendar, Tasks, Drive, Docs, Sheets, Slides y Forms sobre una sola CLI,
con una capa de guardrails que decide qué se puede ejecutar sin preguntar.

```bash
python3 cli.py gmail list --query "from:banco" --max 5
python3 cli.py calendar list --max 10
python3 cli.py drive search --query "tesis"
python3 cli.py gmail send --to a@b.c --subject "Hola" --body "..." --confirmed
```

## Servicios

| Servicio | Operaciones |
|---|---|
| **Gmail** | perfil, listar, leer, buscar, borradores, enviar (con confirmación), papelera |
| **Calendar** | agenda, crear/editar eventos, `freebusy` |
| **Tasks** | listas, alta, edición, completar |
| **Drive** | listar, buscar, crear carpetas, mover a papelera (borrado definitivo bloqueado) |
| **Docs** | crear, leer, insertar texto |
| **Sheets** | crear, leer, agregar y actualizar rangos con límites |
| **Slides** | crear presentaciones, añadir diapositivas |
| **Forms** | metadatos del formulario y respuestas |

## Política de seguridad

La idea es que el agente pueda *leer* mucho y *escribir* poco, y que lo que
escribe quede auditado:

- **Bloqueo permanente** de operaciones destructivas o irreversibles: borrado
  definitivo en Drive, cambios de administración, Apps Script.
- **Confirmación explícita** (`confirmed=True`) para lo sensible: enviar correo,
  borrar, sobrescribir contenido.
- **Guardrails por operación**: cada llamada pasa por una tabla de riesgo
  (`workspace_assistant/guardrails.py`) que lanza `BlockedOperationError` o
  `ConfirmationRequiredError` antes de tocar la API.
- **Auditoría estructurada** en `audit.log`: operación, servicio, resultado y
  parámetros — nunca tokens, cabeceras de autorización ni cuerpos de correo.

## Estructura

```text
cli.py                     CLI de argparse con subcomandos por servicio
workspace_assistant/
  assistant.py             fachada que agrupa los servicios
  guardrails.py            tabla de riesgo + confirmaciones
  audit.py                 log estructurado sin secretos
  services/                un módulo por servicio de Google
tests/                     guardrails y lecturas en vivo
```

## Autenticación

Se espera un token OAuth de Google Workspace (scope de lectura/escritura según el
servicio) en el entorno o en el almacén de credenciales del runtime. Este
repositorio no incluye, y no debe incluir, credenciales: `tokens/`,
`*_token.json` y `client_secret*.json` están en `.gitignore`.

## Requisitos

Python 3.11+ y las librerías cliente de Google (`google-api-python-client`,
`google-auth-oauthlib`).

## Licencia

MIT — ver [LICENSE](LICENSE).
