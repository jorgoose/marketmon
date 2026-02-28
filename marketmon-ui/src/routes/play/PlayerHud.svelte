<script lang="ts">
	export let label: string;
	export let health: number;
	export let maxHealth: number;
	export let isActive: boolean = false;
	export let side: 'player' | 'opponent' = 'player';

	$: hpPct = Math.min(100, (health / maxHealth) * 100);
	$: hpColor = health > 25 ? 'var(--green)' : health > 10 ? 'var(--gold)' : 'var(--red)';
</script>

<div class="hud" class:active={isActive}>
	<div class="hud-icon" class:player={side === 'player'} class:opponent={side === 'opponent'}>
		{#if side === 'player'}
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 12 0v1"/></svg>
		{:else}
			<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="6" width="18" height="12" rx="2"/><circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/></svg>
		{/if}
	</div>
	<span class="hud-label font-mono">{label}</span>
	<div class="hud-bar">
		<div class="bar-track">
			<div class="bar-fill" style="width: {hpPct}%; background: {hpColor}"></div>
		</div>
	</div>
	<span class="hud-hp font-mono">{health}/{maxHealth}</span>
	{#if isActive}
		<span class="turn-dot"></span>
	{/if}
</div>

<style>
	.hud {
		display: flex;
		align-items: center;
		gap: 0.6rem;
		padding: 0.45rem 0.75rem;
		border-radius: 0.5rem;
		background: rgba(10, 10, 18, 0.5);
		border: 1.5px solid var(--border);
		transition: border-color 0.3s, box-shadow 0.3s;
	}

	.hud.active {
		border-color: rgba(201, 168, 76, 0.4);
		box-shadow: 0 0 12px rgba(201, 168, 76, 0.08);
		animation: turnPulse 2s ease-in-out infinite;
	}

	@keyframes turnPulse {
		0%, 100% { box-shadow: 0 0 8px rgba(201, 168, 76, 0.06); }
		50% { box-shadow: 0 0 16px rgba(201, 168, 76, 0.15); }
	}

	.hud-icon {
		width: 20px;
		height: 20px;
		flex-shrink: 0;
	}

	.hud-icon.player { color: var(--cyan); }
	.hud-icon.opponent { color: var(--red); }

	.hud-label {
		font-size: 0.65rem;
		font-weight: 700;
		letter-spacing: 0.15em;
		color: var(--text-muted);
		white-space: nowrap;
	}

	.hud-bar {
		flex: 1;
		min-width: 0;
	}

	.bar-track {
		height: 6px;
		border-radius: 3px;
		background: rgba(255, 255, 255, 0.06);
		overflow: hidden;
		border: 1px solid rgba(255, 255, 255, 0.04);
	}

	.bar-fill {
		height: 100%;
		border-radius: 3px;
		transition: width 0.4s ease, background 0.4s ease;
	}

	.hud-hp {
		font-size: 0.7rem;
		font-weight: 700;
		color: var(--text-secondary);
		white-space: nowrap;
		min-width: 48px;
		text-align: right;
	}

	.turn-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--gold);
		flex-shrink: 0;
		animation: dotPulse 1.5s ease-in-out infinite;
	}

	@keyframes dotPulse {
		0%, 100% { opacity: 0.5; transform: scale(0.85); }
		50% { opacity: 1; transform: scale(1.1); }
	}

	@media (max-width: 480px) {
		.hud { padding: 0.35rem 0.5rem; gap: 0.4rem; }
		.hud-icon { width: 16px; height: 16px; }
		.hud-label { font-size: 0.6rem; }
		.hud-hp { font-size: 0.6rem; min-width: 40px; }
	}
</style>
