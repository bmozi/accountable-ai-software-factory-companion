/* © 2026 John Briggs. MIT licensed; see ../../LICENSE-CODE. */
(() => {
  "use strict";
  const boundaryButtons = Array.from(document.querySelectorAll("[data-boundary]"));
  const panels = Array.from(document.querySelectorAll(".boundary-panel"));
  function selectBoundary(id) {
    for (const button of boundaryButtons) button.setAttribute("aria-pressed", String(button.dataset.boundary === id));
    for (const panel of panels) panel.hidden = panel.id !== `boundary-${id}`;
  }
  for (const button of boundaryButtons) button.addEventListener("click", () => selectBoundary(button.dataset.boundary));
  selectBoundary("intent");

  const scenarios = {
    corrected: {
      title: "Stale advice must be refreshed",
      change: "The source moved from version 1 to version 2. The advice still names version 1.",
      action: "Stop dependent use, inspect the correction and evaluate a newly derived view.",
      evidence: "Old and current source versions, recorded derivation, the blocked-use decision and the refreshed-view decision.",
      limit: "This protects recorded dependencies. It does not discover omitted ancestry or prove the source is true."
    },
    revoked: {
      title: "Withdrawn permission stops the effect",
      change: "Work was approved earlier, but its current permission has been withdrawn while it waits.",
      action: "Do not perform the effect. Ask the accountable authority to review a new, explicitly scoped request if work should continue.",
      evidence: "The current permission decision, the earlier approval reference, the stopped attempt and any separately authorized later request.",
      limit: "An earlier approval, a relevant policy document or a capable agent cannot restore withdrawn authority."
    },
    missing: {
      title: "A required check still needs evidence",
      change: "One check passed, but another required candidate-bound check has no verdict.",
      action: "Keep verification incomplete. The canonical teaching factory refuses disposition and does not create a delivery receipt.",
      evidence: "The exact candidate, applicable criteria, available check result, missing requirement and refusal. Retain this checkpoint trace without labeling it an issued receipt.",
      limit: "A green check cannot stand in for a missing required check. This teaching behavior is not a claim about every production receipt format."
    },
    learning: {
      title: "A useful observation is still a candidate",
      change: "A previous attempt suggests a useful practice, but no authorized learning decision has admitted it.",
      action: "Keep its influence at zero. Evaluate supporting evidence and applicability before a separate learning owner admits a scoped lesson.",
      evidence: "Observation, candidate lesson, validation evidence, authorized admission and recorded source dependencies. A later correction can retire the admitted lesson.",
      limit: "Repetition, retrieval rank and apparent success cannot grant a candidate authority over future work."
    }
  };
  const scenarioButtons = Array.from(document.querySelectorAll("[data-scenario]"));
  for (const button of scenarioButtons) {
    button.addEventListener("click", () => {
      const scenario = scenarios[button.dataset.scenario];
      if (!scenario) return;
      for (const item of scenarioButtons) item.setAttribute("aria-pressed", String(item === button));
      for (const key of ["title", "change", "action", "evidence", "limit"]) {
        document.getElementById(`decision-${key}`).textContent = scenario[key];
      }
    });
  }
  document.getElementById("print-guide").addEventListener("click", () => window.print());
})();
