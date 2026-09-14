# Change Request

**This is the front door. To change anything governed — stack, architecture,
principles, constraints, vision, product-level design intent, or the
committed development line in `backlog.md` (adding/removing an Epic/Story,
or materially changing one) — write it here and nowhere else.**

This file is not a decision log and not a pull request. It is a formal request
for architectural or development-line review. The agent may read it, analyze
it, and draft a proposal, but it does not modify the governed context, ADRs,
or `backlog.md`'s structure directly.

Overwrite the block below each time. This file is a desk, not an archive — the
history lives in `cdad/adr/` for architecture and in `backlog.md` itself for
the development line.

---

## CDAD Request

```text
Change: <what needs to change in the design, system architecture, or development line>
Reason: <why this change is needed>
Trigger: <what event caused the request: bug, cost, limit, requirement, review, etc.>
Scope: <what is included and what is intentionally out of scope>
Impact: <systems, modules, teams, dependencies, adoption cost, migration implications>
Risk: <technical, operational, delivery, and adoption risk>
Priority: <critical / high / medium / low>
```

### Example

```text
Change: Introduce OAuth2-based authentication with multi-tenant SSO support.
Reason: The current system depends on local credentials and does not scale for clients with centralized identity policies.
Trigger: New business requirement and a security audit.
Scope: Changes the authentication flow, the session layer, and provider configuration; does not modify internal domain business logic.
Impact: Affects access services, session management, environment configuration, and the onboarding experience.
Risk: High, due to compatibility with existing users, integration with external providers, and possible migration failures.
Priority: High
```

---

## How to use this

1. Fill in the request block above with the architectural or development-line
   intent.
2. Tell your agent: *"process the change request"*.
3. The agent reads this file and the relevant governed context (or
   `backlog.md`, for a development-line request), then writes a full
   proposal to `cdad/proposals/`.
4. Review the proposal. Reject it, request changes, or approve it.
5. On approval: an architecture/context change gets an ADR and the exact
   stack map delta, which you apply. A development-line change is applied
   directly to `backlog.md` — it does not get an ADR unless it also touches
   governed context.

If you are only asking a question ("is this even possible?", "what would this
cost us?"), ask in chat instead. This file is for changes you intend to make.

Routine Story status updates in `backlog.md` (moving a Story through
`Ready` → `In Progress` → `Done` as work actually happens) do not belong
here either — that is routine implementation, not a change request. This
file is for adding, removing, or materially changing what the backlog
commits to, the same bar as an architectural change.

## What does not belong here

Implementation work. Bugs, feature requests, refactors inside existing
boundaries, and anything under `src/` never belongs here — that is L3 and can be
handled directly in implementation. Routine backlog status updates don't
belong here either, for the same reason.

If you find yourself filling this in for routine work, the constraints in
`cdad/context/` are written too broadly. Narrow them.
