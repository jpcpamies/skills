# FRAMEWORK_DEV.md
## Development Framework for Fullstack Web Apps — Método CANON

> Reusable, stack-agnostic framework for fullstack web apps. Default stack: React 18 (Vite) + TypeScript strict +
> Tailwind + shadcn/ui on the frontend; backend/DB one of Convex · Express+Supabase · Hono+Turso; auth Clerk or
> Supabase; routing Wouter; payments Stripe (or none). Adapt phase details to the stack defined in the PRD/CLAUDE.md.
>
> **Alignment with CANON (read this):**
> - The visual system is NOT invented during development. `DESIGN.md` (Google Stitch format) is the **single source of
>   truth** for visuals, generated upfront by CANON. Phase 4 APPLIES it; it does not create it.
> - **Impeccable** is the quality engine. Install it in Phase 0, never run `teach`/`init` (PRODUCT.md + DESIGN.md already
>   exist), and weave its commands into the build (shape/craft, critique/polish, audit/harden, detect, live).
> - "Non-slop": every visual change avoids AI-slop tells and runs an Impeccable pass before closing.

---

## CORE PHILOSOPHY

- **Atomic Development**: One phase = One specific objective
- **Mandatory Validation**: No advancement without confirmation
- **Progressive Complexity**: Build foundation first, add features incrementally
- **Mobile First**: Design for mobile, enhance for desktop
- **Static First**: UI with mock data before any integrations
- **Backend Before Frontend Logic**: Database and API ready before wiring to UI
- **Design-Driven (North Star)**: apply DESIGN.md; refine with Impeccable; never improvise the aesthetic

---

## THE GOLDEN ORDER

```
0. BOOTSTRAP (Scaffold + deps + install Impeccable + verify PRODUCT.md/DESIGN.md present → SKIP teach)
        |
1. PROJECT SETUP (Initialize + dependencies + environment + folder structure)
        |
2. DATABASE STRUCTURE (Schema + types + migrations + access rules/RLS)
        |
3. UI FOUNDATION (Static component shells with mock data)
        |
4. DESIGN SYSTEM (APPLY DESIGN.md → CSS theme + component library; refine with Impeccable)
        |
5. BACKEND API (Routes/functions + queries + validation)
        |
6. FRONTEND-BACKEND CONNECTIONS (Wire UI to real data)
        |
7. AUTHENTICATION (Auth flows + protected routes)
        |
8. CORE FEATURES (One at a time, by PRD priority; shape→craft per feature)
        |
9. PAYMENTS (After features work)
        |
10. POLISH (Responsive, SEO, perf, errors; Impeccable polish/audit/harden)
        |
11. DEPLOYMENT (CI/CD, env config, production testing)
```

---

## PHASE DETAILS

### PHASE 0: BOOTSTRAP
**Objective**: Prepare the project and the quality tooling before building.

**Tasks**:
1. Scaffold the project skeleton for the stack defined in CLAUDE.md (root, package.json, base config).
2. Install Impeccable: `npx impeccable skills install` (auto-detects Claude Code; latest). Update with `npx impeccable skills update`.
3. Verify `PRODUCT.md` and `DESIGN.md` are present (root or `/docs/`). They exist (CANON generated them) → **DO NOT run `/impeccable teach` or `/impeccable init`**.
4. (Optional) Refresh `docs/FRAMEWORK_DEV.md` to the latest version from the CANON framework repo.

**Deliverables**:
- [ ] Project root initialized
- [ ] `/impeccable` available in the harness
- [ ] PRODUCT.md + DESIGN.md resolved by Impeccable's loader

---

### PHASE 1: PROJECT SETUP
**Objective**: Initialize project with all dependencies configured.

**Tasks**:
1. Initialize project structure (per stack: client/server/shared, or src/+convex/, etc.)
2. Install frontend dependencies (React, Vite, TypeScript, Tailwind, shadcn/ui)
3. Install backend/DB dependencies (per stack)
4. Configure backend/DB connection
5. Configure environment variables (.env.example)
6. Set up dev scripts (dev, build, typecheck, db sync)
7. Create folder structure matching the PRD

**Deliverables**:
- [ ] `npm run dev` starts the app
- [ ] Backend/DB connection verified
- [ ] No TypeScript errors

---

### PHASE 2: DATABASE STRUCTURE
**Objective**: Design and implement the data layer.

**Tasks**:
1. Define schemas for all tables/collections
2. Create shared types/interfaces
3. Run initial migration / schema sync
4. Configure access rules (RLS, or auth-scoped queries)
5. Verify schema matches PRD specs

**Rules**:
- All prices in cents (integer, not float)
- UUID (or platform id) for primary keys
- Timestamps on all tables
- Access rules must be tested (no cross-user leakage)

**Deliverables**:
- [ ] All tables/collections created
- [ ] Access rules active and tested
- [ ] Shared types match schema

---

### PHASE 3: UI FOUNDATION
**Objective**: Create basic component shells (placeholder).

**Tasks**:
1. Create page layouts (Home, Dashboard, Admin…)
2. Create navigation components
3. Create card/list shells (placeholder)
4. Create modal/sheet shells

**Rules**:
- NO real data yet — structure ONLY
- Minimal layout; full visual styling comes in Phase 4 from DESIGN.md
- Each component typed (interfaces for props), default export
- For any net-new screen, prefer `/impeccable shape` to plan before coding

**Deliverables**:
- [ ] All pages render without errors
- [ ] Navigation works between routes
- [ ] No TypeScript errors

---

### PHASE 4: DESIGN SYSTEM
**Objective**: Apply the existing visual identity (DESIGN.md) consistently. DO NOT invent it.

**Tasks**:
1. Translate DESIGN.md tokens → CSS variables / Tailwind theme (`@theme`), OKLCH, tinted neutrals (never #000/#fff)
2. Build/configure the UI component library (buttons, inputs, badges, cards) aligned to the tokens
3. Set up typography scales per DESIGN.md (Two-Voice: distinctive display + refined body; never Inter-for-everything)
4. Apply theme (light/dark) ONLY as DESIGN.md specifies — not by default
5. Verify responsive breakpoints
6. Run `/impeccable document` once tokens exist to reconcile DESIGN.md with real code; refine with `/impeccable typeset`, `colorize`, `layout`

**Deliverables**:
- [ ] Components render with DESIGN.md tokens (no hardcoded hex, no slate-* direct)
- [ ] Typography hierarchy matches DESIGN.md
- [ ] `npx impeccable detect` passes on styled screens

---

### PHASE 5: BACKEND API
**Objective**: Create all API endpoints / backend functions.

**Tasks**:
1. CRUD for primary resources
2. CRUD for secondary resources
3. Purchase/access routes
4. Admin-only middleware / authorization
5. Input validation (Zod / `v.*` validators)
6. Error handling

**Rules**:
- Proper HTTP status codes / consistent response shape
- Input validation on all writes
- Auth checks on every protected operation

**Deliverables**:
- [ ] All endpoints testable
- [ ] Proper error responses
- [ ] Admin/protected routes secured

---

### PHASE 6: FRONTEND-BACKEND CONNECTIONS
**Objective**: Wire UI to real data.

**Tasks**:
1. Set up data client / hooks (TanStack Query or platform-native)
2. Replace mock data with real calls
3. Loading and error states
4. End-to-end data flow test

**Rules**:
- ONE component connection at a time
- Loading skeleton for every fetch
- Error boundary for failed requests

**Deliverables**:
- [ ] Pages show real data
- [ ] Loading states visible
- [ ] Errors handled gracefully

---

### PHASE 7: AUTHENTICATION
**Objective**: User auth and protected routes.

**Tasks**:
1. Implement auth (login/register) per stack (Clerk / Supabase Auth)
2. Auth modal/page
3. Protected route middleware
4. Session persistence
5. Admin role detection

**Rules**:
- Auth persists across refresh
- Protected routes redirect to login
- Admin detection via env var or dedicated table

**Deliverables**:
- [ ] Login/register working
- [ ] Protected routes functional
- [ ] Admin access verified

---

### PHASE 8: CORE FEATURES
**Objective**: Business logic, one feature at a time (PRD priority order).

**Rules**:
- ONE feature per task cycle; test independently before the next
- Follow PRD specs exactly
- For visual work: `/impeccable shape` → `/impeccable craft`; iterate with `/impeccable live`
- Before closing a visual feature: `/impeccable critique` + `/impeccable polish`

**Deliverables**:
- [ ] Each feature works as specified
- [ ] No regressions
- [ ] Impeccable pass reported on visual features

---

### PHASE 9: PAYMENTS
**Objective**: Integrate payments (if applicable) after features work.

**Tasks**:
1. Configure provider (keys, products, prices)
2. Checkout session creation
3. Webhook endpoint with signature validation
4. Purchase records on success
5. Idempotency (no duplicate purchases)
6. Test full flow in test mode

**Rules**:
- Payments ALWAYS after features work
- Validate webhook signature; handle duplicate/failed events

**Deliverables**:
- [ ] Test purchase completes
- [ ] Purchase record created
- [ ] Webhook handles all events

---

### PHASE 10: POLISH
**Objective**: Final optimizations and quality.

**Tasks**:
1. Responsive testing (375 / 768 / 1024 / 1280)
2. SEO meta tags
3. Performance (`/impeccable optimize`)
4. Error boundaries
5. Accessibility review (WCAG AA per PRODUCT.md)
6. Final visual pass: `/impeccable audit` → `/impeccable harden` → `/impeccable polish`; `npx impeccable detect` clean

**Deliverables**:
- [ ] Responsive on all breakpoints
- [ ] No console errors
- [ ] Impeccable detect clean; Lighthouse acceptable

---

### PHASE 11: DEPLOYMENT
**Objective**: Deploy to production.

**Tasks**:
1. Production environment variables
2. Build and test production bundle
3. CI/CD (GitHub → host); optional `npx impeccable detect` in CI
4. Custom domain (if applicable)
5. Smoke test production
6. Monitor post-deploy

**Deliverables**:
- [ ] Production build runs
- [ ] Auto-deploy working
- [ ] Production verified

---

## CRITICAL RULES

```
NEVER skip validation of any phase
NEVER work on multiple features at once
NEVER add payments before features work
NEVER add frontend logic before backend is ready
NEVER use `any` in TypeScript
NEVER invent the visual system — DESIGN.md is the source of truth
NEVER ship AI-slop tells (Inter-for-everything, side-stripe borders, nested cards,
       gradient text, gray-on-color, purple/cyan gradients, bounce easing, em-dash spam)

ALWAYS: Mobile First
ALWAYS: One Task Per Iteration
ALWAYS: Validate Before Advancing
ALWAYS: Backend API before frontend wiring
ALWAYS: Apply DESIGN.md; run an Impeccable pass on visual changes
```

---

## WHEN TO ADD NEW PHASES

If the human requests a feature not covered: (1) identify which phase it fits; (2) if none, create a new phase AFTER
the current ones; (3) break it into atomic tasks; (4) add it to PROJECT_PLAN.md; (5) respect the Golden Order.
Future expansions re-enter the build loop with the same Impeccable discipline.

---

*Método CANON · Framework reutilizable y alineado · stack-agnostic · v2.0*
