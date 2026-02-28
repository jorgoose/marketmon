<script lang="ts">
	import Card from '../Card.svelte';
	import { scale } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import type { Card as CardType } from '$lib/game-types';

	export let card: { ticker: string; health: number } | null = null;
	export let cardData: CardType | undefined = undefined;
	export let isSelected: boolean = false;
	export let isAttackTarget: boolean = false;
	export let isPlayerSide: boolean = false;
	export let slotIndex: number = 0;
	export let sizeMultiplier: number = 0.65;

	$: maxHealth = cardData?.health || 1;
	$: currentHealth = card?.health || 0;
	$: hpPct = Math.min(100, (currentHealth / maxHealth) * 100);
	$: hpColor = currentHealth / maxHealth > 0.5 ? 'var(--green)' : currentHealth / maxHealth > 0.25 ? 'var(--gold)' : 'var(--red)';
</script>

<div
	class="slot"
	class:occupied={card !== null}
	class:selected={isSelected}
	class:attack-target={isAttackTarget}
	class:player-side={isPlayerSide}
	on:click
>
	{#if card && cardData}
		<div class="card-wrap" transition:scale|local={{ duration: 350, easing: quintOut, start: 0.5 }}>
			<Card
				name={cardData.creatureName}
				health={card.health}
				defense={cardData.defense}
				attack={cardData.attack}
				growth={cardData.growth}
				company={cardData.name}
				ticker={card.ticker}
				sector={cardData.sector}
				sizeMultiplier={sizeMultiplier}
				on:click
			/>
			<div class="slot-hp-bar">
				<div class="slot-hp-fill" style="width: {hpPct}%; background: {hpColor}"></div>
			</div>
		</div>
	{:else}
		<div class="empty-slot" style="width: {300 * sizeMultiplier}px; aspect-ratio: 63/88;">
			<span class="slot-num font-mono">{slotIndex + 1}</span>
		</div>
	{/if}
</div>

<style>
	.slot {
		position: relative;
		border-radius: 1rem;
		padding: 3px;
		border: 2px solid transparent;
		transition: all 0.25s ease;
		flex-shrink: 0;
	}

	.slot.player-side.occupied {
		cursor: pointer;
	}

	.slot.player-side.occupied:hover {
		transform: translateY(-4px);
	}

	.slot.selected {
		border-color: var(--purple-glow);
		box-shadow: 0 0 20px rgba(124, 58, 237, 0.3), 0 0 40px rgba(124, 58, 237, 0.1);
	}

	.slot.attack-target {
		border-color: var(--red);
		animation: pulseRed 1.2s ease-in-out infinite;
		cursor: pointer;
	}

	@keyframes pulseRed {
		0%, 100% { box-shadow: 0 0 8px rgba(255, 71, 87, 0.2); }
		50% { box-shadow: 0 0 24px rgba(255, 71, 87, 0.5), 0 0 48px rgba(255, 71, 87, 0.15); }
	}

	.card-wrap {
		position: relative;
	}

	.slot-hp-bar {
		height: 3px;
		border-radius: 2px;
		background: rgba(255, 255, 255, 0.08);
		margin-top: 4px;
		overflow: hidden;
	}

	.slot-hp-fill {
		height: 100%;
		border-radius: 2px;
		transition: width 0.4s ease;
	}

	.empty-slot {
		display: flex;
		align-items: center;
		justify-content: center;
		border: 2px dashed rgba(201, 168, 76, 0.15);
		border-radius: 16px;
		background: rgba(201, 168, 76, 0.02);
		transition: border-color 0.2s;
	}

	.slot.attack-target .empty-slot {
		border-color: rgba(255, 71, 87, 0.3);
	}

	.slot-num {
		font-size: 0.75rem;
		font-weight: 700;
		color: rgba(201, 168, 76, 0.15);
		letter-spacing: 0.1em;
	}

	@media (max-width: 480px) {
		.slot { padding: 2px; }
	}
</style>
