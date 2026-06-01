# Integración de servicios externos — protocolo de "paso 0" (bootstrap)

> Capa de proceso. Cuando el proyecto necesita integrar un servicio externo "caro" —no de dinero, sino
> laborioso y propenso a errores (pagos, auth, email, base de datos, storage, SMS, etc.)—, ANTES de
> escribir una línea de código de la integración, descubre si el servicio publica tooling oficial para
> Claude Code y, con confirmación humana, instálalo. Es el patrón repetible que ahorra horas.

Lee este archivo entero antes de ejecutar. Aplícalo a cualquier servicio (Stripe, Supabase, Resend,
Twilio, Auth0, Clerk, PayPal, Shopify...). Stripe es solo el ejemplo resuelto al final.

## Modelo mental: las vías complementarias

No compiten, se usan juntas:

| Vía | Qué es | Cuándo actúa |
|---|---|---|
| **Skill / Docs** | Conocimiento en texto (agent skill, plugin de docs, `.md`/`llms.txt`) | Diseño y codificación |
| **MCP** | Conexión en vivo a tu cuenta vía herramientas | Desarrollo (acciones reales + buscar doc) |
| **API / SDK** | La librería del servicio en tu código | Producción (lo que ejecuta tu app desplegada) |
| **Plugin** | Empaquetado oficial que trae varias de las anteriores de golpe | Setup |

Clave que confunde a todos: **MCP y API pueden "hacer lo mismo" pero en momentos y sitios distintos.**
El MCP lo ejecutas tú una vez durante el setup; la API la ejecuta tu app, sin ti, en cada operación real.
El MCP nunca está en producción; la API nunca te ayuda a explorar tu cuenta mientras programas.

## Las 3 reglas de oro (no las violes nunca)

**Regla 1 — Condicional, nunca asumas.** No todos los servicios tienen plugin oficial de Claude Code.
Unos tienen MCP pero no plugin; otros solo docs en `llms.txt`; otros nada. Stripe es la excepción
redonda, no la norma. Descubre primero qué existe e instala solo lo que exista. Nunca lances un
`install` a ciegas. Si no hay nada oficial, aplica el fallback y dilo claramente.

**Regla 2 — Confirmación humana, no instalación silenciosa.** (a) Los CLI cambian: verifica la sintaxis
vigente en la doc oficial antes de proponer un comando; no la des por memorizada. (b) Hay pasos que
siguen siendo del humano: OAuth inicial del MCP, sacar claves, configurar webhooks y revelar secretos,
completar onboarding. Propón plan numerado y espera OK antes de ejecutar nada.

**Regla 3 — Genérico, con el servicio como ejemplo.** El valor es el patrón ("para cualquier integración
laboriosa, busca el tooling oficial primero"), no una receta clavada a un servicio. El ejemplo de Stripe
es plantilla mental, no literal.

## Protocolo

1. **Identifica servicio y alcance** (¿pagos? ¿auth? ¿qué parte?) y el **runtime** (Node vs Edge/Workers
   vs serverless — cambia trampas como la verificación de firmas de webhook).
2. **Descubre qué tooling oficial existe** (NO asumas — Regla 1). Para cada uno marca EXISTE/NO/NO SÉ:
   plugin oficial · MCP server (remoto/local) · agent skills oficiales · docs para agentes
   (`llms.txt` o truco `.md`) · SDK/API. Compruébalo en la doc oficial del servicio ("build with AI" /
   "MCP" / "for agents" / "LLMs"), en el registro de plugins/MCP, o con el registry de conectores del
   usuario. Si no confirmas el nombre/comando, dilo y pide el enlace o ve al fallback.
3. **Clasifica** lo encontrado en las vías y explica qué aporta cada una.
4. **Propón el plan numerado y espera OK** (Regla 2), advirtiendo que verificarás la sintaxis del CLI.
5. **Instala lo que exista**, paso a paso. Si un comando falla, no improvises variantes: verifica en la
   doc oficial y reintenta.
6. **Fallbacks si NO hay tooling oficial** (el primero posible): solo docs vía `llms.txt`/`.md` (lectura,
   sin claves) → MCP community de confianza con aprobación → solo SDK + doc oficial a mano. Documenta que
   no había recurso oficial.
7. **Reparte el trabajo y cierra:** qué hará el MCP por el usuario y qué seguirá haciendo a mano en el
   dashboard. Para el alcance real del MCP, una vez conectado pídele: *"lista las herramientas que tienes
   disponibles de [servicio]"* — esa es la foto fiable, no una suposición.

## Seguridad (mínimos para cualquier servicio)

- **Sandbox/test primero.** No toques producción hasta que el usuario lo pida (claves y secretos de test ≠ live).
- **OAuth > secret key** para el MCP. Si hace falta clave, *restringida* y en variables de entorno; nunca en el repo.
- **Confirmación humana** para acciones irreversibles o que muevan dinero/datos reales.
- Cuidado con **prompt injection** si hay varios MCPs conectados a la vez.
- Los métodos `.md`/`llms.txt` no requieren clave: lo más seguro para solo leer documentación.

## Encaje en Canon

- Lo dispara el `CLAUDE.md` (§14): cuando una tarea del `PROJECT_PLAN.md` toca una integración externa,
  Claude Code sigue este protocolo ANTES de codear.
- El PRD (P9) identifica *qué* integraciones hacen falta; este protocolo resuelve el *cómo prepararlas*.
- Si el usuario tiene un playbook propio de errores de un servicio, úsalo para las trampas; pero cuando la
  doc oficial y el playbook discrepen en detalles de API, **manda la doc oficial**.

---

## Ejemplo resuelto: Stripe (plantilla mental, verifica sintaxis vigente)

Stripe es el caso redondo: plugin + MCP + agent skills + docs `.md`. Los comandos cambian; verifícalos en
docs.stripe.com/building-with-ai y docs.stripe.com/mcp antes de ejecutar.

| Recurso | Vía | Instalación (verifica vigencia) |
|---|---|---|
| Plugin oficial | Skill/Plugin | `claude plugin install stripe@claude-plugins-official` |
| Agent skills (stripe-best-practices) | Skill | `npx skills add https://docs.stripe.com --yes` |
| MCP server (remoto) | MCP | `claude mcp add --transport http stripe https://mcp.stripe.com/` |
| MCP server (local) | MCP | `npx -y @stripe/mcp@latest --api-key=rk_...` |
| Truco `.md` / `llms.txt` | Docs | Añadir `.md` a cualquier URL de docs.stripe.com (sin auth) |

Instalación con OAuth: `claude plugin install ...` → `npx skills add ...` → `claude mcp add ...` →
`claude /mcp` (autenticar). Empieza en TEST/sandbox.

**El MCP SÍ hace:** crear productos/precios, payment links, cupones, facturas; listar/actualizar/cancelar
suscripciones; reembolsos; balance, clientes, disputes; `search_stripe_documentation`.
**Sigues a mano:** claves (`sk_`,`pk_`), endpoint de webhook + `whsec_`, activar/configurar Connect,
OAuth inicial del MCP.

### Playbook de trampas (cicatrices que el tooling oficial no tiene)

| Síntoma | Causa | Solución |
|---|---|---|
| "Invalid webhook secret format" | `sk_test_` en `STRIPE_WEBHOOK_SECRET` | Usar `whsec_...` |
| "No signatures found matching…" | Body parseado antes de verificar (Edge) | Raw body + `constructEventAsync` + Web Crypto |
| "Waiting for events" | App privada/local → 403/404 | Hacerla pública; en local `stripe listen` |
| "Error al crear Checkout" | Se usó `prod_...` | Usar `price_...` |
| Créditos concedidos dos veces | Evento procesado más de una vez | Idempotencia por `event.id` |
| Acceso sin pago real | Se fió de la redirección del frontend | Fuente de verdad = DB vía webhook |
| (Connect) vendedor no puede cobrar | Onboarding incompleto | Escuchar `account.updated`; esperar `charges_enabled` |
| (Connect) no llegan eventos | Endpoint scope "Your account" | Endpoint scope "Connected accounts" (`connect: true`) |

Verificación de webhook en Edge (patrón correcto): `Stripe.createFetchHttpClient()` +
`Stripe.createSubtleCryptoProvider()` + `await request.text()` (RAW) +
`stripe.webhooks.constructEventAsync(rawBody, sig, whsec, undefined, webCrypto)`. Desde stripe-node
v11.10.0+ no hace falta `node_compat` en `wrangler.toml`.

Enlaces: docs.stripe.com/building-with-ai · /mcp · /webhooks · /connect/charges · github.com/stripe/ai
