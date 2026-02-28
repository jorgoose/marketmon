<script lang="ts">
	import { slide } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { afterUpdate } from 'svelte';

	export let messages: { text: string; type: string }[] = [];

	let logEl: HTMLDivElement;
	let expanded = true;

	const typeColors: Record<string, string> = {
		deploy: 'var(--gold)',
		damage: 'var(--red)',
		super: 'var(--green)',
		system: 'var(--purple-glow)'
	};

	afterUpdate(() => {
		if (logEl) logEl.scrollTop = logEl.scrollHeight;
	});
</script>

<!-- Desktop: floating panel -->
<div class="log-panel" class:collapsed={!expanded}>
	<button class="log-toggle font-mono" on:click={() => (expanded = !expanded)}>
		LOG [{messages.length}]
		<span class="toggle-arrow">{expanded ? '\u25BC' : '\u25B2'}</span>
	</button>
	{#if expanded}
		<div class="log-body" bind:this={logEl} transition:slide|local={{ duration: 250, easing: quintOut }}>
			{#if messages.length === 0}
				<div class="log-empty font-mono">Waiting for action...</div>
			{:else}
				{#each messages as msg, i (i)}
					<div
						class="log-entry font-mono"
						style="color: {typeColors[msg.type] || 'var(--text-secondary)'}"
						transition:slide|local={{ duration: 200, easing: quintOut }}
					>
						{msg.text}
					</div>
				{/each}
			{/if}
		</div>
	{/if}
</div>

<!-- Mobile: single-line ticker -->
<div class="log-ticker font-mono">
	{#if messages.length > 0}
		<span style="color: {typeColors[messages[messages.length - 1].type] || 'var(--text-secondary)'}">
			{messages[messages.length - 1].text}
		</span>
	{:else}
		<span style="color: var(--text-muted)">Waiting...</span>
	{/if}
</div>

<style>
	/* Desktop floating panel */
	.log-panel {
		position: fixed;
		bottom: 1rem;
		right: 1rem;
		width: 280px;
		z-index: 15;
		border-radius: 0.5rem;
		background: rgba(6, 6, 10, 0.92);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border: 1px solid var(--border);
		overflow: hidden;
	}

	.log-toggle {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		padding: 0.4rem 0.6rem;
		background: rgba(201, 168, 76, 0.06);
		border: none;
		border-bottom: 1px solid var(--border);
		color: var(--gold-dim);
		font-size: 0.6rem;
		font-weight: 700;
		letter-spacing: 0.12em;
		cursor: pointer;
		transition: background 0.2s;
	}

	.log-toggle:hover { background: rgba(201, 168, 76, 0.1); }

	.toggle-arrow { font-size: 0.5rem; }

	.log-body {
		max-height: 180px;
		overflow-y: auto;
		padding: 0.4rem;
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.log-body::-webkit-scrollbar { width: 3px; }
	.log-body::-webkit-scrollbar-track { background: transparent; }
	.log-body::-webkit-scrollbar-thumb { background: rgba(201, 168, 76, 0.15); border-radius: 3px; }

	.log-empty {
		font-size: 0.6rem;
		color: var(--text-muted);
		text-align: center;
		padding: 0.75rem;
	}

	.log-entry {
		font-size: 0.6rem;
		font-weight: 600;
		line-height: 1.5;
		padding: 0.15rem 0.35rem;
		border-radius: 0.2rem;
	}

	/* Mobile ticker */
	.log-ticker {
		display: none;
		padding: 0.3rem 0.75rem;
		background: rgba(6, 6, 10, 0.85);
		border-top: 1px solid var(--border);
		font-size: 0.6rem;
		font-weight: 600;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	@media (max-width: 768px) {
		.log-panel { display: none; }
		.log-ticker { display: block; }
	}

	@media (min-width: 769px) {
		.log-ticker { display: none; }
	}
</style>
