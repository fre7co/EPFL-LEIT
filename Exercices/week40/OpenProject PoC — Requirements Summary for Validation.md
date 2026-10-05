# OpenProject PoC — Requirements Summary for Validation

Oct 2, 2026 · @Anton Tkachuk

## Purpose

This page consolidates everything STI-IT stakeholders said about a project tracking tool, so that we agree on one list of requirements before evaluating OpenProject against it.

**Please review and confirm by ****0****9****.10****:** check that your input is captured correctly, correct anything wrong, and tick your name in the confirmation table at the end. Comments directly on the page are welcome.

This PoC covers STI-IT only. It does not decide licensing or an org-wide rollout; it feeds that decision.

## Problem and current situation

STI-IT has no shared tool for project work and non-incident tasks, which leads to miscommunication and no real task management.

**Main client:** the STI-IT group. The instance must be reachable only from the EPFL network / VPN.

**Authentication:** EPFL users log in with their Microsoft account (Entra ID).

**Today's tools and their limits:**

- **ServiceNow** — used EPFL-wide for incidents and standard requests (ITIL). Its Agile module is not flexible enough for STI-IT project work.
- **Microsoft Planner** — immediately available and integrated with M365, with checklists and comments. But it cannot be extended, integrates poorly outside Microsoft, and keeps each project isolated.
- **GitLab** — works well for the dev team thanks to code integration, but the Community edition is limited for other teams.
- **Text files** — used for tracking that fits nowhere else.

**What we need to track:**

- Projects per team (Support, Infra, Dev) and cross-team projects (e.g. network segmentation).
- Recurring, scheduled tasks: certificate renewals, licenses, routine admin operations.
- Lifecycles of assets and resources: serial numbers, EPFL tags, loaned computers, service accounts, accreditations.
- Changes and regular non-incident tickets.

**Team structure:** keep it as simple as possible, with a rather flat permission scheme.

## Consolidated requirements

Twenty requirements came up. The last column was checked against the OpenProject pricing page and docs (version 17.9, October 2026); details are in "Free vs paid: verified answers" below.

| ID | Requirement | Raised by | OpenProject Community |
| --- | --- | --- | --- |
| R1 | Custom fields: single-line, multi-line, integer, date, user, single-select list (serial number, EPFL tag, IP/host, related SNOW ticket) | Wiki, email, call 10-02 | Yes |
| R2 | Multi-select custom fields; group-type field | Wiki | Multi-select lists: Community. Hierarchy fields: Basic plan |
| R3 | REST API to query, create, modify and transition work packages | Wiki, email, call 10-02 | Yes |
| R4 | Login with the EPFL Microsoft account (Entra ID), no extra password; LDAP/AD also mentioned | Wiki, email | Entra ID login = SSO (OIDC/SAML): Professional plan. LDAP login: Community |
| R5 | LDAP group sync, nested groups | Wiki | Premium plan only; nested groups not supported |
| R6 | Recurring / scheduled tasks (certificates, licenses, routine operations) | Call 10-02, wiki | Not available (open feature request) |
| R7 | Reminders before key dates (expiry, renewal) | Wiki, call 10-02 | Community (date alerts for upcoming/overdue) |
| R8 | Issue types, parent/child hierarchy, epics | Wiki | Yes |
| R9 | Link issues, also across projects | Wiki, call 10-02 | Yes (relations) |
| R10 | Merge duplicate tasks | Call 10-02 | No merge, "duplicates" relation only |
| R11 | Kanban boards, also across several projects | Wiki | Community (all board types); cross-project boards to test |
| R12 | Views of my issues across all projects | Wiki, call 10-02 | Yes (global work package list) |
| R13 | Permissions per project; read access to other teams' progress | Wiki, call 10-02 | Yes (project roles) |
| R14 | Issue-level permissions | Wiki | Sharing a work package with internal users: Community. External users: Professional plan |
| R15 | Automations: status/transition-based actions, webhooks | Wiki | Webhooks + workflows: Community. Custom action buttons: Basic plan |
| R16 | Integrations: GitLab, ServiceNow, BookStack | Wiki | GitLab/GitHub: Community. ServiceNow/BookStack: no built-in integration |
| R17 | Saved queries, keyword search, reports, dashboards | Wiki | Community (project overview dashboard, My page, full-text search) |
| R18 | Bulk edit of many tasks, including custom fields | Call 10-02, call 09-25 | Bulk edit yes; custom fields not editable in bulk |
| R19 | Project templates | Wiki | Yes |
| R20 | Access only from EPFL network / VPN | Call 10-02 | Deployment topic, not a feature |

## User stories

The stories below combine the wiki's role-based list with what came up in the calls; they will be used as PoC test scenarios.

**Standard user**

- As a user, I want to create an issue from a board, choose its type and leave it loosely defined, so that I can capture work quickly and complete it later.
- As a user, I want to edit fields, status, priority and assignee, add the issue to an epic and link it to other issues, so that the work stays organised.
- As a user, I want to move issues across a board and have the status follow, so that the board always reflects reality.
- As a user, I want to see all issues assigned to me across projects, so that I know what to do next.
- As a user, I want to run saved queries and keyword searches across projects, so that I find information fast.
- As a team member, I want to see the progress of other teams' tasks, so that we stop miscommunicating.
- As a team member, I want to link related tasks across projects, so that cross-team work stays connected.

**Infra / support team member**

- As an infra team member, I want a task created automatically before a certificate or license expires, so that renewals are never missed.
- As a sysadmin, I want to track assets (e.g. all Synology systems) as work packages with serial number and EPFL tag fields, so that we stop using scattered text files.
- As a sysadmin, I want a script to update those work packages from epnet.epfl.ch through the API, so that the inventory stays current without manual work.

**Project manager**

- As a project manager, I want to create projects from a standard template, so that all projects share the same configuration.
- As a project manager, I want to bulk-modify issues, so that I can manage large numbers of tasks.
- As a project manager, I want to define which issues a board shows and create several boards per project, so that each context has its own view.
- As a project manager, I want to set standard dashboards and reports for a project, so that progress is visible at a glance.

**Platform admin**

- As an admin, I want to configure issue types, statuses, workflows, custom fields and permissions centrally, so that projects stay consistent.
- As an admin, I want to see where types, workflows and saved queries are used, so that changes don't break other projects.
- As an admin, I want to delete issues in exceptional cases, so that mistakes can be cleaned up.

**Automation ("dreamer")**

- As a team, we want status changes to trigger webhooks to external systems, so that other tools react automatically.
- As a team, we want issues to be created automatically for resources and their lifecycle (service accounts, groups, accreditations, loaned devices), so that administrative routines are tracked end to end.

## Findings so far

The 2026-09-25 call and first tests in a Docker instance (Community edition, no LDAP) confirmed most core features, with a few limits.

**From the 2026-09-25 call**

- Portfolio view can track several projects (Premium plan).
- Baseline shows recent changes on work packages.
- Sprints are available; swimlanes are not yet available.
- Statuses can be excluded from a backlog.
- Project members can be moved; workspace type variants exist.
- Work packages can be shared with individuals as an exception.
- Meetings: agenda items can hold work packages created from them.
- Task creation from emails works but needs specific text and is not recommended.
- Bulk edit cannot change custom fields.
- A follow-up call is to be organised.

**From testing**

- "Issue" is called "Work package" in OpenProject.
- Custom field "list" is available in Community, including multi-select. The wiki note saying "list is premium" should be corrected; only Hierarchy and Weighted item list fields are paid.
- Migrating from numerical to project identifiers cannot set IDs in bulk, but each ID can be changed afterwards. Identifiers are limited to 10 characters (e.g. STI\_IT\_SPT).

## Free vs paid: verified answers

Most of what STI-IT asked for is in the free Community edition. The main paid items are custom action buttons (Basic), SSO (Professional) and LDAP group sync (Premium); recurring work packages exist in no plan.

| Question | Answer | Plan needed |
| --- | --- | --- |
| Is a "list" custom field premium? | No. Text, long text, integer, float, date, boolean, list, user, version and link fields are free; list, user and version can be multi-select | Community |
| Hierarchy (multi-level) custom fields? | Available | Basic |
| Add custom fields to a type's form? | Sections and related-work-package tables are paid; plain add/remove of fields in Community to be tested in the PoC | To test |
| Reminders for upcoming / overdue tasks? | Yes, date alerts in notifications | Community |
| Recurring work packages? | Not available; long-standing feature request | None |
| Custom workflows per type and role? | Yes | Community |
| Buttons that change several fields at once? | Custom actions | Basic |
| Webhooks? | Yes: projects, work packages, comments, time entries, attachments; signed with a secret | Community |
| REST API? | Yes | Community |
| Boards: status (Kanban), assignee, version, subproject, parent-child | All available | Community |
| Swimlanes? | Not yet available | None |
| Baseline comparison? | Against yesterday only; any date needs Basic | Community / Basic |
| Display relations in the work package table? | Moved to Community in 17.8 | Community |
| LDAP login? | Yes | Community |
| LDAP group sync? | Yes, but nested groups are not supported | Premium |
| SSO (SAML, OIDC, CAS, Kerberos), needed for Microsoft Entra ID login? | Yes | Professional |
| SCIM provisioning? | Yes | Corporate |
| GitLab / GitHub integration? | Yes | Community |
| ServiceNow / BookStack integration? | No built-in integration | None |
| Share a work package with specific users? | Internal users: free. External users: paid | Community / Professional |
| Project templates, project overview dashboard, My page | Yes | Community |
| Team planner | Available | Basic |
| Portfolio management | Available | Premium |
| Antivirus scanning of attachments | ClamAV | Corporate |

**Pricing (on-premises, per user per month):** Basic €5.95 and Professional €10.95 with a minimum of 25 users, Premium €15.95 with a minimum of 100 users, Corporate on request from 250 users. OpenProject offers special rates for educational institutions. A free 14-day Enterprise trial key can be applied to a self-hosted Community instance and falls back to Community afterwards.

## Open questions

These need an answer from the team or verification in the PoC:

- [ ] Does "merge tasks" mean real merging, or is a "duplicates" link enough?
- [ ] Does "change management" need a formal approval workflow, or a dedicated work package type?
- [ ] Which custom fields are needed exactly, per team?
- [ ] Do we need issue-level permissions, or are project roles enough?
- [ ] Which ServiceNow and BookStack integrations matter (link only, or sync)?
- [ ] What do sub-projects and project attributes bring compared to separate projects?
- [ ] Can admin rights be delegated per sub-entity?
- [ ] How granular are queries and what search syntax is available?
- [ ] What is the update cadence, security patching and maintenance effort?
- [ ] What does moving to a paid plan imply (migration, cost, minimum users)?

## Confirmation

| Name | Role | Confirmed | Comments |
| --- | --- | --- | --- |
| Alan Garner | Stakeholder |  |  |
| Olli Salo | Stakeholder |  |  |
| David Desscan | Stakeholder |  |  |
| Dries Verachtert | Stakeholder |  |  |
| Juan Convers | Supervision |  |  |
| Andrii Babarytskyi | Supervision |  |  |

## Sources

Checked on 2026-10-02 against OpenProject 17.9.

- [OpenProject pricing and feature comparison](https://www.openproject.org/pricing/)
- [Custom fields (docs)](https://www.openproject.org/docs/system-admin-guide/custom-fields/)
- [Work package form configuration (docs)](https://www.openproject.org/docs/system-admin-guide/manage-work-packages/work-package-types/form-configuration/)
- [LDAP group synchronization (docs)](https://www.openproject.org/docs/system-admin-guide/authentication/ldap-connections/ldap-group-synchronization/)
- [API and webhooks (docs)](https://OpenProject.org/docs/system-admin-guide/api-and-webhooks)
- [Recurring tasks feature request (community forum)](https://community.openproject.org/projects/OP/forums/6/topics/19271)
- [OpenProject 17.8 release notes](https://github.com/opf/openproject/releases/tag/v17.8.0)
