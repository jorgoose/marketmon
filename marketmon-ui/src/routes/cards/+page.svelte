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

	<div class="collection-page">
		<div class="page-header">
			<h1 class="page-title font-display">All Cards</h1>
			<p class="page-subtitle">
				{data.cards.length} creatures to discover
			</p>
		</div>

		<!-- Search & Filters -->
		<div class="filters">
			<div class="search-wrapper">
				<svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
					<circle cx="11" cy="11" r="8" />
					<path d="m21 21-4.35-4.35" />
				</svg>
				<input
					type="text"
					placeholder="Search name, ticker, or creature..."
					bind:value={searchQuery}
					class="search-input"
				/>
			</div>

			<div class="sector-filters">
				<button
					class="sector-chip"
					class:active={selectedSector === ''}
					on:click={() => (selectedSector = '')}
				>
					All
				</button>
				{#each sectors as sector}
					<button
						class="sector-chip"
						class:active={selectedSector === sector}
						on:click={() => (selectedSector = selectedSector === sector ? '' : sector)}
					>
						{sector}
					</button>
				{/each}
			</div>

			{#if searchQuery || selectedSector}
				<div class="results-count">
					Showing {filteredCards.length} of {data.cards.length}
				</div>
			{/if}
		</div>

		<!-- Card Grid -->
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
			<div class="empty-state">
				<p class="empty-title font-display">No creatures found!</p>
				<p class="empty-desc">Try a different search or filter.</p>
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

	.collection-page {
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
		font-size: 2.5rem;
		font-weight: 700;
		color: var(--yellow);
		text-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
	}

	.page-subtitle {
		color: rgba(255, 255, 255, 0.7);
		font-weight: 700;
		font-size: 1rem;
	}

	/* ---- Filters ---- */
	.filters {
		margin-bottom: 2rem;
		animation: fadeUp 0.5s ease-out 0.1s both;
	}

	.search-wrapper {
		position: relative;
		max-width: 460px;
		margin: 0 auto 1rem;
	}

	.search-icon {
		position: absolute;
		left: 1rem;
		top: 50%;
		transform: translateY(-50%);
		width: 18px;
		height: 18px;
		color: rgba(255, 255, 255, 0.4);
		pointer-events: none;
	}

	.search-input {
		width: 100%;
		padding: 0.8rem 1rem 0.8rem 2.75rem;
		border-radius: 9999px;
		border: 2px solid rgba(255, 255, 255, 0.15);
		background: rgba(255, 255, 255, 0.08);
		color: #fff;
		font-family: 'Nunito', sans-serif;
		font-size: 0.9rem;
		font-weight: 600;
		outline: none;
		transition: all 0.2s ease;
	}

	.search-input::placeholder {
		color: rgba(255, 255, 255, 0.4);
	}

	.search-input:focus {
		border-color: var(--yellow);
		background: rgba(255, 255, 255, 0.12);
		box-shadow: 0 0 0 4px rgba(251, 191, 36, 0.15);
	}

	.sector-filters {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		justify-content: center;
	}

	.sector-chip {
		padding: 0.4rem 0.9rem;
		border-radius: 9999px;
		border: 2px solid rgba(255, 255, 255, 0.12);
		background: rgba(255, 255, 255, 0.06);
		color: rgba(255, 255, 255, 0.75);
		font-size: 0.8rem;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.2s ease;
		font-family: 'Nunito', sans-serif;
	}

	.sector-chip:hover {
		background: rgba(255, 255, 255, 0.12);
		color: #fff;
	}

	.sector-chip.active {
		background: var(--yellow);
		border-color: var(--yellow);
		color: var(--blue-deep);
	}

	.results-count {
		text-align: center;
		margin-top: 0.75rem;
		font-size: 0.85rem;
		font-weight: 700;
		color: rgba(255, 255, 255, 0.5);
	}

	/* ---- Card Grid ---- */
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

	/* ---- Empty state ---- */
	.empty-state {
		text-align: center;
		padding: 4rem 1rem;
	}

	.empty-title {
		font-size: 1.5rem;
		margin-bottom: 0.5rem;
		color: var(--yellow);
	}

	.empty-desc {
		font-size: 0.95rem;
		color: rgba(255, 255, 255, 0.6);
		font-weight: 600;
	}
</style>
