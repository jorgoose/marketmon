<script lang="ts">
	import type { PageServerData } from './$types';
	import Card from '../Card.svelte';
	import Navbar from '../Navbar.svelte';

	export let data: PageServerData;

	let searchQuery = '';
	let selectedSector = '';

	const sectors = [...new Set(data.cards.map((c) => c.sector))].sort();

	$: filteredCards = data.cards.filter((card) => {
		const q = searchQuery.toLowerCase();
		const matchesSearch =
			!q ||
			card.name.toLowerCase().includes(q) ||
			card.creatureName.toLowerCase().includes(q) ||
			card.ticker.toLowerCase().includes(q);
		const matchesSector = !selectedSector || card.sector === selectedSector;
		return matchesSearch && matchesSector;
	});
</script>

<div class="page">
	<Navbar />

	<div class="index-page">
		<div class="page-header">
			<h1 class="page-title font-display text-gold">The Index</h1>
			<p class="page-sub font-mono">{data.cards.length} CREATURES INDEXED</p>
		</div>

		<!-- Filters -->
		<div class="filters">
			<div class="search-box">
				<svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
					<circle cx="11" cy="11" r="8" />
					<path d="m21 21-4.35-4.35" />
				</svg>
				<input
					type="text"
					placeholder="Search ticker, name, or creature..."
					bind:value={searchQuery}
					class="search-input font-mono"
				/>
			</div>

			<div class="sector-row">
				<button
					class="chip"
					class:active={selectedSector === ''}
					on:click={() => (selectedSector = '')}
				>
					All
				</button>
				{#each sectors as sector}
					<button
						class="chip"
						class:active={selectedSector === sector}
						on:click={() => (selectedSector = selectedSector === sector ? '' : sector)}
					>
						{sector}
					</button>
				{/each}
			</div>

			{#if searchQuery || selectedSector}
				<p class="filter-count font-mono">
					{filteredCards.length} / {data.cards.length} results
				</p>
			{/if}
		</div>

		<!-- Grid -->
		{#if filteredCards.length > 0}
			<div class="card-grid">
				{#each filteredCards as card (card.ticker)}
					<div class="card-cell">
						<Card
							sizeMultiplier={0.85}
							name={card.creatureName}
							health={card.health || 0}
							defense={card.defense || 0}
							attack={card.attack || 0}
							growth={card.growth || 0}
							company={card.name}
							ticker={card.ticker}
							sector={card.sector}
						/>
					</div>
				{/each}
			</div>
		{:else}
			<div class="empty">
				<p class="empty-title font-display">No Results</p>
				<p class="empty-sub">Try adjusting your query or filters.</p>
			</div>
		{/if}
	</div>
</div>

<style>
	.page {
		position: relative;
		z-index: 1;
		min-height: 100vh;
	}

	.index-page {
		max-width: 1400px;
		margin: 0 auto;
		padding: 2rem 1.5rem 4rem;
	}

	.page-header {
		text-align: center;
		margin-bottom: 2rem;
		animation: fadeUp 0.5s ease-out both;
	}

	.page-title {
		font-size: 2.25rem;
		font-weight: 900;
		letter-spacing: 0.05em;
	}

	.page-sub {
		font-size: 0.7rem;
		letter-spacing: 0.15em;
		color: var(--text-muted);
		margin-top: 0.35rem;
	}

	/* ---- Filters ---- */
	.filters {
		margin-bottom: 2rem;
		animation: fadeUp 0.5s ease-out 0.1s both;
	}

	.search-box {
		position: relative;
		max-width: 440px;
		margin: 0 auto 1rem;
	}

	.search-icon {
		position: absolute;
		left: 0.9rem;
		top: 50%;
		transform: translateY(-50%);
		width: 16px;
		height: 16px;
		color: var(--text-muted);
		pointer-events: none;
	}

	.search-input {
		width: 100%;
		padding: 0.7rem 1rem 0.7rem 2.5rem;
		border-radius: 0.5rem;
		border: 1px solid var(--border);
		background: rgba(10, 10, 18, 0.6);
		color: var(--text-primary);
		font-size: 0.8rem;
		outline: none;
		transition: all 0.2s ease;
	}

	.search-input::placeholder {
		color: var(--text-muted);
	}

	.search-input:focus {
		border-color: var(--border-hover);
		box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.08);
	}

	.sector-row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.4rem;
		justify-content: center;
	}

	.chip {
		padding: 0.35rem 0.8rem;
		border-radius: 0.375rem;
		border: 1px solid var(--border);
		background: transparent;
		color: var(--text-secondary);
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		font-family: 'DM Sans', sans-serif;
	}

	.chip:hover {
		color: var(--text-primary);
		border-color: rgba(201, 168, 76, 0.2);
		background: rgba(201, 168, 76, 0.04);
	}

	.chip.active {
		color: var(--gold);
		border-color: rgba(201, 168, 76, 0.35);
		background: rgba(201, 168, 76, 0.08);
	}

	.filter-count {
		text-align: center;
		margin-top: 0.75rem;
		font-size: 0.7rem;
		letter-spacing: 0.1em;
		color: var(--text-muted);
	}

	/* ---- Grid ---- */
	.card-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
		gap: 1.25rem;
		justify-items: center;
		animation: fadeIn 0.4s ease-out 0.2s both;
	}

	.card-cell {
		transition: transform 0.25s ease;
	}

	.card-cell:hover {
		transform: translateY(-6px);
	}

	/* ---- Empty ---- */
	.empty {
		text-align: center;
		padding: 4rem 1rem;
	}

	.empty-title {
		font-size: 1.25rem;
		color: var(--gold);
		letter-spacing: 0.04em;
		margin-bottom: 0.4rem;
	}

	.empty-sub {
		font-size: 0.9rem;
		color: var(--text-muted);
	}
</style>
