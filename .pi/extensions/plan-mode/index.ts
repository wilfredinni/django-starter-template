/**
 * Plan Mode Extension — OpenCode-compatible plan mode for pi.
 *
 * Read-only exploration mode with subagent delegation, structured plan files,
 * clarifying question workflow, and phased execution tracking.
 *
 * Commands:
 *   /plan           — Toggle plan mode
 *   /plans          — List saved plans
 *   Ctrl+Alt+P      — Toggle plan mode
 *
 * Flags:
 *   --plan          — Start in plan mode
 *
 * Tools:
 *   plan_write      — Save a plan to .pi/plans/
 *   plan_read       — Read a saved plan
 *   plan_list       — List all saved plans
 */

import type { AgentMessage } from "@earendil-works/pi-agent-core";
import type {
  AssistantMessage,
  TextContent,
} from "@earendil-works/pi-ai";
import type {
  ExtensionAPI,
  ExtensionContext,
} from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { Key } from "@earendil-works/pi-tui";
import { PLAN_MODE_SYSTEM_PROMPT, EXECUTION_MODE_PROMPT } from "./prompts.ts";
import {
  createPlanFile,
  readPlanFile,
  listPlans,
  slugify,
  type PlanMetadata,
} from "./plan-files.ts";

// ── Tool Sets ──────────────────────────────────────────────────────────

/** Tools allowed in plan mode (read-only + plan management) */
const PLAN_MODE_TOOLS = [
  "read",
  "grep",
  "find",
  "ls",
  "bash",
  "subagent",
  "web_search",
  "fetch_content",
  "code_search",
  "get_search_content",
  "ctx_execute",
  "ctx_execute_file",
  "ctx_search",
  "ctx_batch_execute",
  "ctx_index",
  "ctx_fetch_and_index",
  "plan_write",
  "plan_read",
  "plan_list",
];

/** Tools restored when exiting plan mode */
const NORMAL_MODE_TOOLS = [
  ...PLAN_MODE_TOOLS,
  "edit",
  "write",
];

// ── Bash Safety ────────────────────────────────────────────────────────

const DESTRUCTIVE_PATTERNS = [
  /\brm\b/i,
  /\brmdir\b/i,
  /\bmv\b/i,
  /\bcp\b/i,
  /\bmkdir\b/i,
  /\btouch\b/i,
  /\bchmod\b/i,
  /\bchown\b/i,
  /\bchgrp\b/i,
  /\bln\s+-s\b/i,
  /\btee\b/i,
  /\btruncate\b/i,
  /\bdd\b/i,
  /\bshred\b/i,
  /\bsed\s+.*-i\b/i,
  /(^|[^<])>(?!>)/,
  />>/,
  /\bnpm\s+(install|uninstall|update|ci|link|publish)/i,
  /\byarn\s+(add|remove|install|publish)/i,
  /\bpip\s+(install|uninstall)/i,
  /\bapt(-get)?\s+(install|remove|purge|update|upgrade)/i,
  /\bbrew\s+(install|uninstall|upgrade)/i,
  /\bgit\s+(add|commit|push|pull|merge|rebase|reset|checkout|stash|cherry-pick|revert|tag|init|clone)/i,
  /\bsudo\b/i,
  /\bsu\b/i,
  /\bkill\b/i,
  /\bpkill\b/i,
  /\bkillall\b/i,
  /\breboot\b/i,
  /\bshutdown\b/i,
  /\bsystemctl\s+(start|stop|restart|enable|disable)/i,
  /\bservice\s+\S+\s+(start|stop|restart)/i,
  /\b(vim?|nano|emacs|code|subl)\b/i,
];

const SAFE_PATTERNS = [
  /^\s*cat\b/,
  /^\s*head\b/,
  /^\s*tail\b/,
  /^\s*less\b/,
  /^\s*more\b/,
  /^\s*grep\b/,
  /^\s*find\b/,
  /^\s*ls\b/,
  /^\s*pwd\b/,
  /^\s*echo\b/,
  /^\s*printf\b/,
  /^\s*wc\b/,
  /^\s*sort\b/,
  /^\s*uniq\b/,
  /^\s*diff\b/,
  /^\s*file\b/,
  /^\s*stat\b/,
  /^\s*du\b/,
  /^\s*df\b/,
  /^\s*tree\b/,
  /^\s*which\b/,
  /^\s*whereis\b/,
  /^\s*type\b/,
  /^\s*env\b/,
  /^\s*printenv\b/,
  /^\s*uname\b/,
  /^\s*whoami\b/,
  /^\s*id\b/,
  /^\s*date\b/,
  /^\s*cal\b/,
  /^\s*uptime\b/,
  /^\s*ps\b/,
  /^\s*top\b/,
  /^\s*htop\b/,
  /^\s*free\b/,
  /^\s*git\s+(status|log|diff|show|branch|remote|config\s+--get)/i,
  /^\s*git\s+ls-/i,
  /^\s*npm\s+(list|ls|view|info|search|outdated|audit)/i,
  /^\s*yarn\s+(list|info|why|audit)/i,
  /^\s*node\s+--version/i,
  /^\s*python\s+--version/i,
  /^\s*curl\s/i,
  /^\s*wget\s+-O\s*-/i,
  /^\s*jq\b/,
  /^\s*sed\s+-n/i,
  /^\s*awk\b/,
  /^\s*rg\b/,
  /^\s*fd\b/,
  /^\s*bat\b/,
  /^\s*eza\b/,
  /^\s*make\s+(test|test-cov|shell|logs)/i,
];

function isSafeCommand(command: string): boolean {
  const isDestructive = DESTRUCTIVE_PATTERNS.some((p) => p.test(command));
  const isSafe = SAFE_PATTERNS.some((p) => p.test(command));
  return !isDestructive && isSafe;
}

// ── Todo / Plan Step Tracking ──────────────────────────────────────────

interface TodoItem {
  step: number;
  text: string;
  completed: boolean;
}

function isAssistantMessage(
  m: AgentMessage,
): m is AssistantMessage {
  return m.role === "assistant" && Array.isArray(m.content);
}

function getTextContent(message: AssistantMessage): string {
  return message.content
    .filter((block): block is TextContent => block.type === "text")
    .map((block) => block.text)
    .join("\n");
}

function extractTodosFromPlan(message: string): TodoItem[] {
  const items: TodoItem[] = [];
  const headerMatch = message.match(/\*{0,2}Phase\s+\d+\*{0,2}[:*-]?\s*\n/i);
  if (!headerMatch) {
    // Fallback: look for "Plan:" header
    const planMatch = message.match(/\*{0,2}Plan:\*{0,2}\s*\n/i);
    if (!planMatch) return items;

    const planSection = message.slice(
      message.indexOf(planMatch[0]) + planMatch[0].length,
    );
    const numberedPattern = /^\s*(\d+)[.)]\s+\*{0,2}([^*\n]+)/gm;
    for (const match of planSection.matchAll(numberedPattern)) {
      const text = match[2].trim().replace(/\*{1,2}$/, "").trim();
      if (text.length > 3) {
        items.push({
          step: items.length + 1,
          text: text.length > 60 ? text.slice(0, 57) + "..." : text,
          completed: false,
        });
      }
    }
    return items;
  }

  // Extract phases from the plan
  const phasePattern =
    /(?:###?\s*)?\*{0,2}Phase\s+(\d+)\*{0,2}[:*-]?\s*([^\n]+)/gi;
  for (const match of message.matchAll(phasePattern)) {
    const num = parseInt(match[1], 10);
    const name = match[2].trim();
    if (name.length > 3) {
      items.push({
        step: num,
        text: name.length > 60 ? name.slice(0, 57) + "..." : name,
        completed: false,
      });
    }
  }

  // If no phases found, try numbered list under "Changes" or "Implementation"
  if (items.length === 0) {
    const changesMatch = message.match(
      /(?:###?\s*)?(?:Changes|Implementation|Approach)[:*]?\s*\n/i,
    );
    if (changesMatch) {
      const section = message.slice(
        message.indexOf(changesMatch[0]) + changesMatch[0].length,
      );
      const numPattern = /^\s*(\d+)[.)]\s+([^\n]+)/gm;
      for (const match of section.matchAll(numPattern)) {
        const text = match[2].trim();
        if (text.length > 3) {
          items.push({ step: items.length + 1, text, completed: false });
        }
      }
    }
  }

  return items;
}

function extractDoneSteps(text: string): number[] {
  const steps: number[] = [];
  for (const match of text.matchAll(/\[DONE:(\d+)\]/gi)) {
    const step = Number(match[1]);
    if (Number.isFinite(step)) steps.push(step);
  }
  return steps;
}

function markCompletedSteps(text: string, items: TodoItem[]): number {
  const done = extractDoneSteps(text);
  for (const step of done) {
    const item = items.find((t) => t.step === step);
    if (item) item.completed = true;
  }
  return done.length;
}

// ── Extension ──────────────────────────────────────────────────────────

export default function planModeExtension(pi: ExtensionAPI): void {
  // ── State ──────────────────────────────────────────────────────────
  let planModeEnabled = false;
  let executionMode = false;
  let todoItems: TodoItem[] = [];

  // ── CLI Flag ────────────────────────────────────────────────────────
  pi.registerFlag("plan", {
    description: "Start in plan mode (read-only exploration)",
    type: "boolean",
    default: false,
  });

  // ── UI Helpers ──────────────────────────────────────────────────────

  function updateUI(ctx: ExtensionContext): void {
    // Footer status
    if (executionMode && todoItems.length > 0) {
      const completed = todoItems.filter((t) => t.completed).length;
      ctx.ui.setStatus(
        "plan-mode",
        ctx.ui.theme.fg("accent", `📋 ${completed}/${todoItems.length}`),
      );
    } else if (planModeEnabled) {
      ctx.ui.setStatus(
        "plan-mode",
        ctx.ui.theme.fg("warning", "⏸ plan"),
      );
    } else {
      ctx.ui.setStatus("plan-mode", undefined);
    }

    // Widget showing plan progress
    if (executionMode && todoItems.length > 0) {
      const lines = todoItems.map((item) => {
        if (item.completed) {
          return (
            ctx.ui.theme.fg("success", "✓ ") +
            ctx.ui.theme.fg(
              "muted",
              ctx.ui.theme.strikethrough(item.text),
            )
          );
        }
        return (
          ctx.ui.theme.fg("muted", "○ ") +
          ctx.ui.theme.fg("accent", item.text)
        );
      });
      ctx.ui.setWidget("plan-todos", lines);
    } else if (planModeEnabled && todoItems.length > 0) {
      const lines = todoItems.map(
        (item) => `${ctx.ui.theme.fg("muted", "○ ")}${item.text}`,
      );
      ctx.ui.setWidget("plan-todos", [
        ctx.ui.theme.fg("warning", "── Plan Steps ──"),
        ...lines,
      ]);
    } else {
      ctx.ui.setWidget("plan-todos", undefined);
    }
  }

  function persistState(): void {
    pi.appendEntry("plan-mode-v2", {
      enabled: planModeEnabled,
      todos: todoItems,
      executing: executionMode,
    });
  }

  // ── Toggle ──────────────────────────────────────────────────────────

  function enterPlanMode(ctx: ExtensionContext): void {
    planModeEnabled = true;
    executionMode = false;
    pi.setActiveTools(PLAN_MODE_TOOLS);
    ctx.ui.notify(
      `Plan mode enabled — read-only. Tools: read, grep, find, ls, bash (safe), subagent, research, plan_write`,
      "info",
    );
    updateUI(ctx);
    persistState();
  }

  function exitPlanMode(ctx: ExtensionContext): void {
    planModeEnabled = false;
    executionMode = false;
    todoItems = [];
    pi.setActiveTools(NORMAL_MODE_TOOLS);
    ctx.ui.notify("Plan mode disabled — full access restored.", "info");
    updateUI(ctx);
    persistState();
  }

  function togglePlanMode(ctx: ExtensionContext): void {
    if (planModeEnabled) {
      exitPlanMode(ctx);
    } else {
      enterPlanMode(ctx);
    }
  }

  // ── Commands ────────────────────────────────────────────────────────

  pi.registerCommand("plan", {
    description: "Toggle plan mode (read-only exploration with structured planning)",
    handler: async (_args, ctx) => togglePlanMode(ctx),
  });

  pi.registerCommand("plans", {
    description: "List saved plans",
    handler: async (_args, ctx) => {
      const plans = listPlans(ctx.cwd);
      if (plans.length === 0) {
        ctx.ui.notify("No saved plans.", "info");
        return;
      }
      const list = plans
        .map(
          (p) =>
            `• ${p.filename} [${p.metadata.status}] — ${p.metadata.title}`,
        )
        .join("\n");
      ctx.ui.notify(`Saved Plans:\n${list}`, "info");
    },
  });

  // ── Shortcut ────────────────────────────────────────────────────────

  pi.registerShortcut(Key.ctrlAlt("p"), {
    description: "Toggle plan mode",
    handler: async (ctx) => togglePlanMode(ctx),
  });

  // ── Plan Management Tools ───────────────────────────────────────────

  pi.registerTool({
    name: "plan_write",
    label: "Write Plan",
    description:
      "Save an implementation plan to .pi/plans/. Use during plan mode to persist structured plans with phases, verification steps, and risks.",
    promptSnippet: "Save an implementation plan to .pi/plans/{filename}",
    promptGuidelines: [
      "Use plan_write to save structured plans during plan mode. Include phases, verification steps, risks, and pause points.",
    ],
    parameters: Type.Object({
      filename: Type.String({
        description: "Plan filename (e.g. 'add-rate-limiting' or 'feature-auth'). Auto-prefixed with date and .md extension.",
      }),
      title: Type.String({
        description: "Human-readable plan title",
      }),
      content: Type.String({
        description: "Full plan content in markdown. Include phases, verification, risks, and pause points.",
      }),
      type: Type.Optional(
        Type.String({
          description: "Plan type: feature, fix, refactor, or chore (default: feature)",
        }),
      ),
    }),
    async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
      try {
        const filename = slugify(params.filename);
        const metadata: PlanMetadata = {
          title: params.title,
          status: "draft",
          created: new Date().toISOString(),
          type: (params.type as PlanMetadata["type"]) ?? "feature",
        };
        const result = createPlanFile(ctx.cwd, filename, params.content, metadata);
        return {
          content: [
            {
              type: "text",
              text: `Plan saved: ${result.path}\n\nUse plan_read("${filename.replace(/^\d{4}-\d{2}-\d{2}-/, "")}") to review it later.`,
            },
          ],
          details: { path: result.path, filename },
        };
      } catch (err: unknown) {
        return {
          content: [
            {
              type: "text",
              text: `Failed to save plan: ${err instanceof Error ? err.message : String(err)}`,
            },
          ],
          details: {},
          isError: true,
        };
      }
    },
  });

  pi.registerTool({
    name: "plan_read",
    label: "Read Plan",
    description:
      "Read a saved plan from .pi/plans/. Use to review plans created earlier in this or previous sessions.",
    promptSnippet: "Read a plan from .pi/plans/{filename}",
    parameters: Type.Object({
      filename: Type.String({
        description: "Plan filename or partial name (e.g. 'add-rate-limiting', 'feature-auth')",
      }),
    }),
    async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
      try {
        const plan = readPlanFile(ctx.cwd, params.filename);
        if (!plan) {
          return {
            content: [
              {
                type: "text",
                text: `No plan found matching "${params.filename}". Use plan_list to see available plans.`,
              },
            ],
            details: {},
          };
        }
        return {
          content: [
            {
              type: "text",
              text: `# ${plan.metadata.title}\nStatus: ${plan.metadata.status} | Created: ${plan.metadata.created} | Type: ${plan.metadata.type}\n\n${plan.content}`,
            },
          ],
          details: { filename: plan.filename, metadata: plan.metadata },
        };
      } catch (err: unknown) {
        return {
          content: [
            {
              type: "text",
              text: `Failed to read plan: ${err instanceof Error ? err.message : String(err)}`,
            },
          ],
          details: {},
          isError: true,
        };
      }
    },
  });

  pi.registerTool({
    name: "plan_list",
    label: "List Plans",
    description:
      "List all saved plans in .pi/plans/. Shows filename, status, title, and creation date.",
    promptSnippet: "List all saved plans",
    parameters: Type.Object({
      status: Type.Optional(
        Type.String({
          description: "Filter by status: draft, approved, in_progress, or done",
        }),
      ),
    }),
    async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
      try {
        const plans = listPlans(
          ctx.cwd,
          params.status as PlanMetadata["status"] | undefined,
        );
        if (plans.length === 0) {
          return {
            content: [
              { type: "text", text: "No plans found." },
            ],
            details: { plans: [] },
          };
        }
        const list = plans
          .map(
            (p) =>
              `- **${p.filename}** [${p.metadata.status}] ${p.metadata.title} (${p.metadata.created.slice(0, 10)})`,
          )
          .join("\n");
        return {
          content: [
            { type: "text", text: `# Saved Plans\n\n${list}` },
          ],
          details: { plans: plans.map((p) => p.filename) },
        };
      } catch (err: unknown) {
        return {
          content: [
            {
              type: "text",
              text: `Failed to list plans: ${err instanceof Error ? err.message : String(err)}`,
            },
          ],
          details: {},
          isError: true,
        };
      }
    },
  });

  // ── Event: Block Dangerous Bash ─────────────────────────────────────

  pi.on("tool_call", async (event) => {
    if (!planModeEnabled || event.toolName !== "bash") return;

    const command = event.input.command as string;
    if (!isSafeCommand(command)) {
      return {
        block: true,
        reason:
          `Plan mode: destructive command blocked.\n` +
          `To run: exit plan mode first with /plan, then re-run.\n` +
          `Blocked: ${command.slice(0, 80)}`,
      };
    }
  });

  // ── Event: Inject System Prompts ────────────────────────────────────

  pi.on("before_agent_start", async () => {
    if (planModeEnabled) {
      return {
        message: {
          customType: "plan-mode-context",
          content: PLAN_MODE_SYSTEM_PROMPT,
          display: false,
        },
      };
    }

    if (executionMode && todoItems.length > 0) {
      const remaining = todoItems.filter((t) => !t.completed);
      const todoList = remaining
        .map((t) => `${t.step}. ${t.text}`)
        .join("\n");
      return {
        message: {
          customType: "plan-execution-context",
          content:
            EXECUTION_MODE_PROMPT +
            `\n\nRemaining steps:\n${todoList}`,
          display: false,
        },
      };
    }
  });

  // ── Event: Track [DONE:n] Markers ───────────────────────────────────

  pi.on("turn_end", async (event, ctx) => {
    if (!executionMode || todoItems.length === 0) return;
    if (!isAssistantMessage(event.message)) return;

    const text = getTextContent(event.message);
    if (markCompletedSteps(text, todoItems) > 0) {
      updateUI(ctx);
    }
    persistState();
  });

  // ── Event: Plan Completion & Next Actions ───────────────────────────

  pi.on("agent_end", async (event, ctx) => {
    // Check if execution is complete
    if (executionMode && todoItems.length > 0) {
      const allDone = todoItems.every((t) => t.completed);
      if (allDone) {
        const completedList = todoItems
          .map((t) => `~~${t.text}~~`)
          .join("\n");
        pi.sendMessage(
          {
            customType: "plan-complete",
            content: `**Plan Complete!** ✓\n\n${completedList}`,
            display: true,
          },
          { triggerTurn: false },
        );
        executionMode = false;
        todoItems = [];
        pi.setActiveTools(NORMAL_MODE_TOOLS);
        updateUI(ctx);
        persistState();
        return;
      }

      // Partial completion — check if we're at a pause point
      const lastAssistant = [...event.messages]
        .reverse()
        .find(isAssistantMessage);
      if (lastAssistant) {
        const text = getTextContent(lastAssistant);
        if (text.includes("⏸") || text.includes("PAUSE")) {
          pi.sendMessage(
            {
              customType: "plan-pause",
              content:
                "⏸️ **Pause point reached.** Review the completed phase before continuing.",
              display: true,
            },
            { triggerTurn: false },
          );
        }
      }
      return;
    }

    if (!planModeEnabled || !ctx.hasUI) return;

    // Extract plan steps from the last assistant message
    const lastAssistant = [...event.messages]
      .reverse()
      .find(isAssistantMessage);
    if (lastAssistant) {
      const text = getTextContent(lastAssistant);
      const extracted = extractTodosFromPlan(text);
      if (extracted.length > 0) {
        todoItems = extracted;
        updateUI(ctx);
        persistState();
      }
    }

    // Show plan steps if extracted
    if (todoItems.length > 0) {
      const todoListText = todoItems
        .map((t, i) => `${i + 1}. ○ ${t.text}`)
        .join("\n");
      pi.sendMessage(
        {
          customType: "plan-todo-list",
          content: `**Plan Steps (${todoItems.length}):**\n\n${todoListText}`,
          display: true,
        },
        { triggerTurn: false },
      );
    }

    // Prompt for next action
    const options = [
      todoItems.length > 0
        ? "Execute the plan (phase by phase)"
        : "Execute the plan",
      "Stay in plan mode (refine)",
      "Ask a clarifying question",
      "Exit plan mode",
    ];

    const choice = await ctx.ui.select("Plan mode — what next?", options);

    if (choice?.startsWith("Execute")) {
      planModeEnabled = false;
      executionMode = todoItems.length > 0;
      pi.setActiveTools(NORMAL_MODE_TOOLS);
      updateUI(ctx);
      persistState();

      const execMessage =
        todoItems.length > 0
          ? `Execute the plan phase by phase. Start with Phase 1: ${todoItems[0].text}\n\nAfter completing each phase, include a [DONE:n] tag and pause at ⏸️ markers to verify before continuing.`
          : "Execute the plan you just created. Follow the phases in order, marking each complete with [DONE:n] tags.";

      pi.sendMessage(
        {
          customType: "plan-mode-execute",
          content: execMessage,
          display: true,
        },
        { triggerTurn: true },
      );
    } else if (choice === "Stay in plan mode (refine)") {
      const refinement = await ctx.ui.editor(
        "What would you like to refine or explore further?",
        "",
      );
      if (refinement?.trim()) {
        pi.sendUserMessage(refinement.trim());
      }
    } else if (choice === "Ask a clarifying question") {
      const question = await ctx.ui.editor(
        "What question do you have for me?",
        "",
      );
      if (question?.trim()) {
        // Send the question as a user response, keeping plan mode active
        pi.sendUserMessage(
          `[User response to plan mode question]: ${question.trim()}`,
        );
      }
    } else if (choice === "Exit plan mode") {
      exitPlanMode(ctx);
    }
  });

  // ── Event: Restore State on Session Start ───────────────────────────

  pi.on("session_start", async (_event, ctx) => {
    // Check --plan flag
    if (pi.getFlag("plan") === true && !planModeEnabled) {
      planModeEnabled = true;
    }

    // Restore persisted state
    const entries = ctx.sessionManager.getEntries();
    const planModeEntry = entries
      .filter(
        (e: { type: string; customType?: string }) =>
          e.type === "custom" && e.customType === "plan-mode-v2",
      )
      .pop() as
      | { data?: { enabled: boolean; todos?: TodoItem[]; executing?: boolean } }
      | undefined;

    if (planModeEntry?.data) {
      planModeEnabled = planModeEntry.data.enabled ?? planModeEnabled;
      todoItems = planModeEntry.data.todos ?? todoItems;
      executionMode = planModeEntry.data.executing ?? executionMode;
    }

    // On resume, re-scan messages for [DONE:n] markers
    const isResume = planModeEntry !== undefined;
    if (isResume && executionMode && todoItems.length > 0) {
      let executeIndex = -1;
      for (let i = entries.length - 1; i >= 0; i--) {
        const entry = entries[i] as { type: string; customType?: string };
        if (entry.customType === "plan-mode-execute") {
          executeIndex = i;
          break;
        }
      }

      const messages: AssistantMessage[] = [];
      for (let i = executeIndex + 1; i < entries.length; i++) {
        const entry = entries[i];
        if (
          entry.type === "message" &&
          "message" in entry &&
          isAssistantMessage(entry.message as AgentMessage)
        ) {
          messages.push(entry.message as AssistantMessage);
        }
      }
      const allText = messages.map(getTextContent).join("\n");
      markCompletedSteps(allText, todoItems);
    }

    // Apply tool restrictions
    if (planModeEnabled) {
      pi.setActiveTools(PLAN_MODE_TOOLS);
    }
    updateUI(ctx);
  });

  // ── Event: Filter Stale Plan Context ────────────────────────────────

  pi.on("context", async (event) => {
    if (planModeEnabled || executionMode) return;

    // When not in plan mode, clean up plan-mode context messages
    return {
      messages: event.messages.filter((m) => {
        const msg = m as AgentMessage & { customType?: string };
        if (
          msg.customType === "plan-mode-context" ||
          msg.customType === "plan-execution-context"
        ) {
          return false;
        }
        if (msg.role !== "user") return true;

        const content = msg.content;
        if (typeof content === "string") {
          return !content.includes("[Plan Mode ACTIVE]");
        }
        if (Array.isArray(content)) {
          return !content.some(
            (c) =>
              c.type === "text" &&
              (c as TextContent).text?.includes("[Plan Mode ACTIVE]"),
          );
        }
        return true;
      }),
    };
  });
}
