<script lang="ts">
	import type { PageServerData } from './$types';
	import Card from '../Card.svelte';
	import { slide, fade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import type { Action } from '$lib/game-types';
	import { updateGameState } from './update-game-state';

	export let data: PageServerData;

	let gameState = data.gameState;
	let selectedCard: string | null = null;
	let showHand = false;
	let notification = '';
	let notificationTimeout: ReturnType<typeof setTimeout>;

	const MAX_HEALTH = 50;

	function showNotification(msg: string) {
		notification = msg;
		clearTimeout(notificationTimeout);
		notificationTimeout = setTimeout(() => (notification = ''), 3000);
	}

	function getHealthColor(health: number): string {
		if (health > 25) return '#22c55e';
		if (health > 10) return '#fbbf24';
		return '#ef4444';
	}

	function playCard(cardTicker: string) {
		const health = data.cards.find(({ ticker }) => ticker === cardTicker)?.health || 0;
		if (health > gameState.you.health) {
			showNotification('Not enough health to play this card!');
			return;
		}
		const action: Action = { actionType: 'play', data: cardTicker };
		gameState = updateGameState(gameState, action, data.cards);
		selectedCard = null;
	}

	function growCard(cardTicker: string) {
		const action: Action = { actionType: 'grow', data: cardTicker };
		gameState = updateGameState(gameState, action, data.cards);
		selectedCard = null;
	}

	function attackCard(attackerTicker: string, opponentTicker: string) {
		const action: Action = {
			actionType: 'attack',
			data: { attacker: attackerTicker, opponent: opponentTicker }
		};
		gameState = updateGameState(gameState, action, data.cards);
		selectedCard = null;
	}
</script>

<div class="battle-page">
	<!-- Header -->
	<div class="battle-header">
		<a href="/" class="exit-btn">&larr; Exit</a>
		<span class="battle-label font-display">Battle Arena</span>
		<div style="width: 60px"></div>
	</div>

	<!-- Battlefield -->
	<div class="battlefield">
		<!-- Opponent -->
		<div class="player-zone">
			<div class="zone-bar">
				<span class="zone-name font-display">Opponent</span>
				<div class="hp-bar">
					<div class="hp-track">
						<div
							class="hp-fill"
							style="width: {Math.min(100, (gameState.opponent.health / MAX_HEALTH) * 100)}%; background: {getHealthColor(gameState.opponent.health)}"
						></div>
					</div>
					<span class="hp-text">{gameState.opponent.health} HP</span>
				</div>
			</div>
			<div class="card-area">
				{#if gameState.opponent.inPlay.length === 0}
					<div class="field-empty">No creatures yet</div>
				{:else}
					<div class="field-cards">
						{#each gameState.opponent.inPlay as card, i (card.ticker)}
							{@const cardData = data.cards.find(({ ticker }) => ticker === card.ticker)}
							<div class="card-slot" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
								<Card
									name={cardData?.creatureName || ''}
									health={card.health}
									defense={cardData?.defense || 0}
									attack={cardData?.attack || 0}
									growth={cardData?.growth || 0}
									company={cardData?.name || ''}
									ticker={card.ticker}
									sector={cardData?.sector || ''}
									sizeMultiplier={0.8}
								/>
							</div>
						{/each}
					</div>
				{/if}
			</div>
		</div>

		<!-- Divider -->
		<div class="vs-divider">
			<div class="vs-line"></div>
			<span class="vs-badge font-display">VS</span>
			<div class="vs-line"></div>
		</div>

		<!-- You -->
		<div class="player-zone your-zone">
			<div class="card-area">
				{#if gameState.you.inPlay.length === 0}
					<div class="field-empty">Open your Hand to deploy creatures!</div>
				{:else}
					<div class="field-cards">
						{#each gameState.you.inPlay as card, i (card.ticker)}
							{@const cardData = data.cards.find((c) => c.ticker === card.ticker)}
							<div
								class="card-slot clickable"
								class:selected={selectedCard === card.ticker}
								transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}
							>
								<Card
									name={cardData?.creatureName || ''}
									health={card.health}
									defense={cardData?.defense || 0}
									attack={cardData?.attack || 0}
									growth={cardData?.growth || 0}
									company={cardData?.name || ''}
									ticker={card.ticker}
									sector={cardData?.sector || ''}
									on:click={() => {
										if (selectedCard === card.ticker) {
											selectedCard = null;
										} else if (!selectedCard) {
											selectedCard = card.ticker;
										}
									}}
									sizeMultiplier={0.8}
								/>
							</div>
						{/each}
					</div>
				{/if}
			</div>
			<div class="zone-bar">
				<span class="zone-name font-display">You</span>
				<div class="hp-bar">
					<div class="hp-track">
						<div
							class="hp-fill"
							style="width: {Math.min(100, (gameState.you.health / MAX_HEALTH) * 100)}%; background: {getHealthColor(gameState.you.health)}"
						></div>
					</div>
					<span class="hp-text">{gameState.you.health} HP</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Action Bar -->
	{#if selectedCard}
		{@const selectedCardData = data.cards.find((c) => c.ticker === selectedCard)}
		<div class="action-bar" transition:slide|local={{ duration: 250, easing: quintOut }}>
			<span class="action-label font-display">{selectedCardData?.creatureName || selectedCard}</span>
			<div class="action-btns">
				<button class="abtn grow-btn" on:click={() => growCard(selectedCard || '')}>
					Grow
				</button>
				{#each gameState.opponent.inPlay as opponentCard (opponentCard.ticker)}
					{@const opData = data.cards.find((c) => c.ticker === opponentCard.ticker)}
					<button class="abtn attack-btn" on:click={() => attackCard(selectedCard || '', opponentCard.ticker)}>
						Attack {opData?.creatureName || opponentCard.ticker}
					</button>
				{/each}
				<button class="abtn cancel-btn" on:click={() => (selectedCard = null)}>
					Cancel
				</button>
			</div>
		</div>
	{/if}

	<!-- Hand Toggle -->
	<button class="hand-toggle font-display" on:click={() => (showHand = !showHand)}>
		{showHand ? 'Hide' : 'Hand'} ({gameState.you.hand.length})
	</button>

	<!-- Hand Drawer -->
	{#if showHand}
		<div class="hand-drawer" transition:slide|local={{ duration: 350, easing: quintOut }}>
			{#if gameState.you.hand.length === 0}
				<div class="hand-empty">No cards in hand!</div>
			{:else}
				<div class="hand-scroll">
					{#each gameState.you.hand as cardTicker, i (cardTicker)}
						{@const cardData = data.cards.find((card) => card.ticker === cardTicker)}
						<div class="hand-card" transition:slide|local={{ delay: i * 80, duration: 400, easing: quintOut }}>
							<Card
								name={cardData?.creatureName || ''}
								health={cardData?.health || 0}
								defense={cardData?.defense || 0}
								attack={cardData?.attack || 0}
								growth={cardData?.growth || 0}
								on:click={() => {
									if (gameState.whosTurn === 'you') playCard(cardTicker);
								}}
								company={cardData?.name || ''}
								ticker={cardTicker}
								sector={cardData?.sector || ''}
								sizeMultiplier={0.75}
							/>
						</div>
					{/each}
				</div>
			{/if}
		</div>
	{/if}

	<!-- Toast -->
	{#if notification}
		<div class="toast" transition:fade|local={{ duration: 200 }}>
			{notification}
		</div>
	{/if}

	<!-- Game Over -->
	{#if gameState.winner}
		<div class="game-over" transition:fade|local={{ duration: 400 }}>
			<div class="go-card" class:win={gameState.winner === 'you'} class:lose={gameState.winner === 'opponent'}>
				{#if gameState.winner === 'you'}
					<h2 class="go-title font-display">You Win!</h2>
					<p class="go-desc">Your creatures dominated the arena!</p>
				{:else}
					<h2 class="go-title font-display">You Lose!</h2>
					<p class="go-desc">Better luck next battle...</p>
				{/if}
				<div class="go-actions">
					<a href="/play" class="go-btn go-primary font-display">Play Again</a>
					<a href="/" class="go-btn go-secondary">Home</a>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.battle-page {
		position: relative;
		z-index: 1;
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	/* ---- Header ---- */
	.battle-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.75rem 1.5rem;
		background: rgba(30, 64, 175, 0.7);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border-bottom: 2px solid rgba(255, 255, 255, 0.1);
		z-index: 10;
	}

	.exit-btn {
		color: rgba(255, 255, 255, 0.7);
		text-decoration: none;
		font-weight: 700;
		font-size: 0.9rem;
		transition: color 0.2s;
	}

	.exit-btn:hover { color: #fff; }

	.battle-label {
		font-size: 1.1rem;
		font-weight: 700;
		color: var(--yellow);
	}

	/* ---- Battlefield ---- */
	.battlefield {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: 1rem 1.5rem;
		gap: 0.5rem;
		overflow-y: auto;
	}

	.player-zone {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	/* ---- Zone Bar (Health) ---- */
	.zone-bar {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.6rem 1.25rem;
		border-radius: 1rem;
		background: rgba(255, 255, 255, 0.08);
		border: 2px solid rgba(255, 255, 255, 0.1);
	}

	.zone-name {
		font-weight: 700;
		font-size: 0.9rem;
		color: var(--yellow);
		min-width: 72px;
	}

	.hp-bar {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.hp-track {
		flex: 1;
		height: 10px;
		border-radius: 5px;
		background: rgba(255, 255, 255, 0.1);
		overflow: hidden;
		max-width: 300px;
		border: 1px solid rgba(255, 255, 255, 0.08);
	}

	.hp-fill {
		height: 100%;
		border-radius: 5px;
		transition: width 0.4s ease, background 0.4s ease;
	}

	.hp-text {
		font-size: 0.85rem;
		font-weight: 700;
		color: rgba(255, 255, 255, 0.8);
		min-width: 50px;
	}

	/* ---- Card Area ---- */
	.card-area {
		min-height: 100px;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.field-cards {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		justify-content: center;
	}

	.card-slot {
		border-radius: 1.25rem;
		padding: 4px;
		border: 3px solid transparent;
		transition: all 0.25s ease;
	}

	.card-slot:hover {
		transform: translateY(-4px);
	}

	.card-slot.clickable {
		cursor: pointer;
	}

	.card-slot.selected {
		border-color: var(--yellow);
		box-shadow: 0 0 20px rgba(251, 191, 36, 0.35), 0 0 40px rgba(251, 191, 36, 0.15);
	}

	.field-empty {
		padding: 2rem 2.5rem;
		text-align: center;
		color: rgba(255, 255, 255, 0.45);
		font-weight: 700;
		font-size: 0.95rem;
		border: 2px dashed rgba(255, 255, 255, 0.12);
		border-radius: 1.25rem;
	}

	/* ---- VS Divider ---- */
	.vs-divider {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.25rem 0;
	}

	.vs-line {
		flex: 1;
		height: 2px;
		background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.15), transparent);
	}

	.vs-badge {
		font-size: 0.85rem;
		font-weight: 700;
		color: var(--yellow);
		text-shadow: 0 1px 4px rgba(251, 191, 36, 0.3);
		letter-spacing: 0.1em;
	}

	/* ---- Action Bar ---- */
	.action-bar {
		position: fixed;
		bottom: 60px;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.6rem 1.25rem;
		background: rgba(30, 64, 175, 0.9);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border: 2px solid rgba(255, 255, 255, 0.15);
		border-radius: 9999px;
		z-index: 30;
		max-width: 90vw;
		flex-wrap: wrap;
		justify-content: center;
	}

	.action-label {
		font-size: 0.85rem;
		font-weight: 700;
		color: var(--yellow);
		white-space: nowrap;
	}

	.action-btns {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.abtn {
		padding: 0.45rem 1rem;
		border-radius: 9999px;
		border: 2px solid transparent;
		font-family: 'Nunito', sans-serif;
		font-size: 0.8rem;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.2s ease;
		white-space: nowrap;
	}

	.grow-btn {
		background: var(--green);
		color: #052e16;
	}

	.grow-btn:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
	}

	.attack-btn {
		background: var(--red);
		color: #fff;
	}

	.attack-btn:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
	}

	.cancel-btn {
		background: rgba(255, 255, 255, 0.1);
		color: rgba(255, 255, 255, 0.8);
		border-color: rgba(255, 255, 255, 0.15);
	}

	.cancel-btn:hover {
		background: rgba(255, 255, 255, 0.18);
	}

	/* ---- Hand Toggle ---- */
	.hand-toggle {
		position: fixed;
		bottom: 14px;
		right: 1.5rem;
		padding: 0.5rem 1.25rem;
		border-radius: 9999px;
		background: var(--yellow);
		border: none;
		color: var(--blue-deep);
		font-size: 0.9rem;
		font-weight: 700;
		cursor: pointer;
		z-index: 25;
		transition: all 0.2s ease;
		box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
	}

	.hand-toggle:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 18px rgba(251, 191, 36, 0.4);
	}

	/* ---- Hand Drawer ---- */
	.hand-drawer {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		z-index: 20;
		background: rgba(15, 40, 100, 0.95);
		backdrop-filter: blur(16px);
		-webkit-backdrop-filter: blur(16px);
		border-top: 3px solid rgba(251, 191, 36, 0.3);
		padding: 1rem 0;
	}

	.hand-scroll {
		display: flex;
		gap: 0.75rem;
		overflow-x: auto;
		padding: 0.5rem 1.5rem;
	}

	.hand-card {
		flex-shrink: 0;
		cursor: pointer;
		transition: transform 0.2s ease;
		border-radius: 1.25rem;
		padding: 3px;
		border: 2px solid transparent;
	}

	.hand-card:hover {
		transform: translateY(-10px);
		border-color: var(--yellow);
	}

	.hand-empty {
		text-align: center;
		padding: 1.5rem;
		color: rgba(255, 255, 255, 0.5);
		font-weight: 700;
	}

	/* ---- Toast ---- */
	.toast {
		position: fixed;
		top: 1rem;
		left: 50%;
		transform: translateX(-50%);
		padding: 0.75rem 1.5rem;
		border-radius: 9999px;
		background: var(--red);
		color: #fff;
		font-size: 0.9rem;
		font-weight: 700;
		z-index: 40;
		pointer-events: none;
		box-shadow: 0 4px 16px rgba(239, 68, 68, 0.35);
	}

	/* ---- Game Over ---- */
	.game-over {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.6);
		backdrop-filter: blur(6px);
		-webkit-backdrop-filter: blur(6px);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 50;
	}

	.go-card {
		text-align: center;
		padding: 3rem 3.5rem;
		border-radius: 2rem;
		border: 3px solid;
		animation: pop 0.5s ease-out both;
	}

	.go-card.win {
		background: linear-gradient(135deg, #166534, #15803d);
		border-color: var(--green);
		box-shadow: 0 0 40px rgba(34, 197, 94, 0.3);
	}

	.go-card.lose {
		background: linear-gradient(135deg, #7f1d1d, #991b1b);
		border-color: var(--red);
		box-shadow: 0 0 40px rgba(239, 68, 68, 0.3);
	}

	.go-title {
		font-size: 2.5rem;
		font-weight: 700;
		margin-bottom: 0.5rem;
		color: #fff;
	}

	.go-desc {
		color: rgba(255, 255, 255, 0.8);
		font-weight: 600;
		margin-bottom: 2rem;
	}

	.go-actions {
		display: flex;
		gap: 0.75rem;
		justify-content: center;
	}

	.go-btn {
		padding: 0.8rem 1.75rem;
		border-radius: 9999px;
		text-decoration: none;
		font-weight: 700;
		font-size: 1rem;
		transition: all 0.2s ease;
	}

	.go-primary {
		background: var(--yellow);
		color: var(--blue-deep);
		box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
	}

	.go-primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 6px 18px rgba(251, 191, 36, 0.4);
	}

	.go-secondary {
		background: rgba(255, 255, 255, 0.15);
		border: 2px solid rgba(255, 255, 255, 0.25);
		color: #fff;
	}

	.go-secondary:hover {
		background: rgba(255, 255, 255, 0.25);
	}
</style>
