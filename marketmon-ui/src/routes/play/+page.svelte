<script lang="ts">
	import type { PageServerData } from './$types';
	import Card from '../Card.svelte';
	import { slide, fade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import type { Action } from '$lib/game-types';
	import { updateGameState, isSuperEffective } from './update-game-state';

	export let data: PageServerData;

	let gameState = data.gameState;
	let selectedCard: string | null = null;
	let showHand = false;
	let notification = '';
	let notificationType: 'error' | 'success' = 'error';
	let notificationTimeout: ReturnType<typeof setTimeout>;

	const MAX_HEALTH = 50;

	function showNotification(msg: string, type: 'error' | 'success' = 'error') {
		notification = msg;
		notificationType = type;
		clearTimeout(notificationTimeout);
		notificationTimeout = setTimeout(() => (notification = ''), 3000);
	}

	function getHealthColor(health: number): string {
		if (health > 25) return 'var(--green)';
		if (health > 10) return 'var(--gold)';
		return 'var(--red)';
	}

	function playCard(cardTicker: string) {
		const health = data.cards.find(({ ticker }) => ticker === cardTicker)?.health || 0;
		if (health > gameState.you.health) {
			showNotification('Not enough HP to deploy this creature.');
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
		const attacker = data.cards.find(c => c.ticker === attackerTicker);
		const defender = data.cards.find(c => c.ticker === opponentTicker);
		if (attacker && defender && isSuperEffective(attacker.sector, defender.sector)) {
			showNotification(`Super effective! ${attacker.sector} → ${defender.sector} (1.5× damage)`, 'success');
		}
		const action: Action = {
			actionType: 'attack',
			data: { attacker: attackerTicker, opponent: opponentTicker }
		};
		gameState = updateGameState(gameState, action, data.cards);
		selectedCard = null;
	}
</script>

<div class="arena-page">
	<!-- Header -->
	<div class="arena-header">
		<a href="/" class="exit-link">&larr; Exit</a>
		<span class="arena-title font-display text-gold">Arena</span>
		<div style="width: 48px"></div>
	</div>

	<!-- Battlefield -->
	<div class="battlefield">
		<!-- Opponent Zone -->
		<div class="zone">
			<div class="zone-hud">
				<span class="hud-label font-mono">OPPONENT</span>
				<div class="hud-bar">
					<div class="bar-track">
						<div class="bar-fill" style="width: {Math.min(100, (gameState.opponent.health / MAX_HEALTH) * 100)}%; background: {getHealthColor(gameState.opponent.health)}"></div>
					</div>
					<span class="hud-hp font-mono">{gameState.opponent.health}</span>
				</div>
			</div>
			<div class="zone-field">
				{#if gameState.opponent.inPlay.length === 0}
					<div class="field-empty">No creatures deployed</div>
				{:else}
					<div class="field-row">
						{#each gameState.opponent.inPlay as card, i (card.ticker)}
							{@const cardData = data.cards.find(({ ticker }) => ticker === card.ticker)}
							<div class="fcard" transition:slide|local={{ delay: i * 100, duration: 500, easing: quintOut }}>
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
		<div class="divider">
			<div class="div-line"></div>
			<span class="div-vs font-display">VS</span>
			<div class="div-line"></div>
		</div>

		<!-- Your Zone -->
		<div class="zone">
			<div class="zone-field">
				{#if gameState.you.inPlay.length === 0}
					<div class="field-empty">Open your hand to deploy creatures</div>
				{:else}
					<div class="field-row">
						{#each gameState.you.inPlay as card, i (card.ticker)}
							{@const cardData = data.cards.find((c) => c.ticker === card.ticker)}
							<div
								class="fcard selectable"
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
										if (selectedCard === card.ticker) selectedCard = null;
										else if (!selectedCard) selectedCard = card.ticker;
									}}
									sizeMultiplier={0.8}
								/>
							</div>
						{/each}
					</div>
				{/if}
			</div>
			<div class="zone-hud">
				<span class="hud-label font-mono">YOU</span>
				<div class="hud-bar">
					<div class="bar-track">
						<div class="bar-fill" style="width: {Math.min(100, (gameState.you.health / MAX_HEALTH) * 100)}%; background: {getHealthColor(gameState.you.health)}"></div>
					</div>
					<span class="hud-hp font-mono">{gameState.you.health}</span>
				</div>
			</div>
		</div>
	</div>

	<!-- Action Bar -->
	{#if selectedCard}
		{@const sel = data.cards.find((c) => c.ticker === selectedCard)}
		<div class="action-bar" transition:slide|local={{ duration: 250, easing: quintOut }}>
			<span class="act-label font-mono">{sel?.creatureName || selectedCard}</span>
			<div class="act-btns">
				<button class="act grow" on:click={() => growCard(selectedCard || '')}>Grow</button>
				{#each gameState.opponent.inPlay as oc (oc.ticker)}
					{@const ocd = data.cards.find((c) => c.ticker === oc.ticker)}
					<button class="act attack" on:click={() => attackCard(selectedCard || '', oc.ticker)}>
						Attack {ocd?.creatureName || oc.ticker}
					</button>
				{/each}
				<button class="act cancel" on:click={() => (selectedCard = null)}>Cancel</button>
			</div>
		</div>
	{/if}

	<!-- Hand Toggle -->
	<button class="hand-btn font-mono" on:click={() => (showHand = !showHand)}>
		{showHand ? 'HIDE' : 'HAND'} [{gameState.you.hand.length}]
	</button>

	<!-- Hand Drawer -->
	{#if showHand}
		<div class="hand-drawer" transition:slide|local={{ duration: 350, easing: quintOut }}>
			{#if gameState.you.hand.length === 0}
				<div class="hand-empty font-mono">HAND EMPTY</div>
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
								on:click={() => { if (gameState.whosTurn === 'you') playCard(cardTicker); }}
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
		<div class="toast font-mono" class:toast-success={notificationType === 'success'} transition:fade|local={{ duration: 200 }}>
			{notification}
		</div>
	{/if}

	<!-- Game Over -->
	{#if gameState.winner}
		<div class="game-over" transition:fade|local={{ duration: 400 }}>
			<div class="go-card" class:win={gameState.winner === 'you'} class:lose={gameState.winner === 'opponent'}>
				{#if gameState.winner === 'you'}
					<p class="go-tag font-mono green">VICTORY</p>
					<h2 class="go-title font-display">You Win</h2>
					<p class="go-sub">Your portfolio dominated the arena.</p>
				{:else}
					<p class="go-tag font-mono red">DEFEAT</p>
					<h2 class="go-title font-display">You Lose</h2>
					<p class="go-sub">The market had other plans.</p>
				{/if}
				<div class="go-btns">
					<a href="/play" class="go-btn go-primary font-display">Play Again</a>
					<a href="/" class="go-btn go-secondary">Home</a>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.arena-page {
		position: relative;
		z-index: 1;
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	/* ---- Header ---- */
	.arena-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0.65rem 1.5rem;
		background: rgba(6, 6, 10, 0.85);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border-bottom: 1px solid var(--border);
		z-index: 10;
	}

	.exit-link {
		color: var(--text-muted);
		text-decoration: none;
		font-size: 0.85rem;
		font-weight: 600;
		transition: color 0.2s;
	}

	.exit-link:hover { color: var(--text-primary); }

	.arena-title {
		font-size: 1rem;
		font-weight: 700;
		letter-spacing: 0.1em;
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

	.zone {
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}

	/* ---- HUD (Health) ---- */
	.zone-hud {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.5rem 1rem;
		border-radius: 0.5rem;
		background: rgba(10, 10, 18, 0.5);
		border: 1px solid var(--border);
	}

	.hud-label {
		font-size: 0.65rem;
		font-weight: 700;
		letter-spacing: 0.15em;
		color: var(--text-muted);
		min-width: 72px;
	}

	.hud-bar {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 0.75rem;
	}

	.bar-track {
		flex: 1;
		height: 6px;
		border-radius: 3px;
		background: rgba(255, 255, 255, 0.06);
		overflow: hidden;
		max-width: 280px;
		border: 1px solid rgba(255, 255, 255, 0.04);
	}

	.bar-fill {
		height: 100%;
		border-radius: 3px;
		transition: width 0.4s ease, background 0.4s ease;
	}

	.hud-hp {
		font-size: 0.75rem;
		font-weight: 700;
		color: var(--text-secondary);
		min-width: 30px;
	}

	/* ---- Card Field ---- */
	.zone-field {
		min-height: 100px;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.field-row {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
		justify-content: center;
	}

	.fcard {
		border-radius: 1.25rem;
		padding: 3px;
		border: 2px solid transparent;
		transition: all 0.25s ease;
	}

	.fcard:hover { transform: translateY(-4px); }

	.fcard.selectable { cursor: pointer; }

	.fcard.selected {
		border-color: var(--purple-glow);
		box-shadow: 0 0 24px rgba(124, 58, 237, 0.3), 0 0 48px rgba(124, 58, 237, 0.1);
	}

	.field-empty {
		padding: 2rem 2.5rem;
		text-align: center;
		color: var(--text-muted);
		font-size: 0.85rem;
		border: 1px dashed rgba(201, 168, 76, 0.12);
		border-radius: 0.75rem;
	}

	/* ---- VS Divider ---- */
	.divider {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.15rem 0;
	}

	.div-line {
		flex: 1;
		height: 1px;
		background: linear-gradient(to right, transparent, var(--border), transparent);
	}

	.div-vs {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.2em;
		color: var(--gold-dim);
	}

	/* ---- Action Bar ---- */
	.action-bar {
		position: fixed;
		bottom: 56px;
		left: 50%;
		transform: translateX(-50%);
		display: flex;
		align-items: center;
		gap: 0.75rem;
		padding: 0.5rem 1rem;
		background: rgba(6, 6, 10, 0.92);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border: 1px solid var(--border);
		border-radius: 0.5rem;
		z-index: 30;
		max-width: 90vw;
		flex-wrap: wrap;
		justify-content: center;
	}

	.act-label {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		color: var(--purple-glow);
		white-space: nowrap;
	}

	.act-btns {
		display: flex;
		gap: 0.4rem;
		flex-wrap: wrap;
	}

	.act {
		padding: 0.4rem 0.9rem;
		border-radius: 0.375rem;
		border: 1px solid transparent;
		font-family: 'DM Sans', sans-serif;
		font-size: 0.75rem;
		font-weight: 700;
		cursor: pointer;
		transition: all 0.2s ease;
		white-space: nowrap;
	}

	.act.grow {
		background: rgba(0, 212, 123, 0.12);
		color: var(--green);
		border-color: rgba(0, 212, 123, 0.25);
	}

	.act.grow:hover {
		background: rgba(0, 212, 123, 0.2);
		transform: translateY(-1px);
	}

	.act.attack {
		background: rgba(255, 71, 87, 0.1);
		color: var(--red);
		border-color: rgba(255, 71, 87, 0.2);
	}

	.act.attack:hover {
		background: rgba(255, 71, 87, 0.18);
		transform: translateY(-1px);
	}

	.act.cancel {
		background: transparent;
		color: var(--text-muted);
		border-color: var(--border);
	}

	.act.cancel:hover { color: var(--text-secondary); background: rgba(255, 255, 255, 0.03); }

	/* ---- Hand Toggle ---- */
	.hand-btn {
		position: fixed;
		bottom: 14px;
		right: 1.5rem;
		padding: 0.45rem 1rem;
		border-radius: 0.375rem;
		background: rgba(201, 168, 76, 0.1);
		border: 1px solid rgba(201, 168, 76, 0.25);
		color: var(--gold);
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		cursor: pointer;
		z-index: 25;
		transition: all 0.2s ease;
	}

	.hand-btn:hover {
		background: rgba(201, 168, 76, 0.18);
		border-color: rgba(201, 168, 76, 0.4);
	}

	/* ---- Hand Drawer ---- */
	.hand-drawer {
		position: fixed;
		bottom: 0;
		left: 0;
		right: 0;
		z-index: 20;
		background: rgba(6, 6, 10, 0.96);
		backdrop-filter: blur(20px);
		-webkit-backdrop-filter: blur(20px);
		border-top: 1px solid rgba(201, 168, 76, 0.15);
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
		padding: 2px;
		border: 2px solid transparent;
	}

	.hand-card:hover {
		transform: translateY(-10px);
		border-color: rgba(201, 168, 76, 0.3);
	}

	.hand-empty {
		text-align: center;
		padding: 1.5rem;
		color: var(--text-muted);
		font-size: 0.7rem;
		letter-spacing: 0.15em;
	}

	/* ---- Toast ---- */
	.toast {
		position: fixed;
		top: 1rem;
		left: 50%;
		transform: translateX(-50%);
		padding: 0.6rem 1.25rem;
		border-radius: 0.375rem;
		background: rgba(255, 71, 87, 0.12);
		border: 1px solid rgba(255, 71, 87, 0.3);
		color: var(--red);
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.05em;
		z-index: 40;
		pointer-events: none;
	}

	.toast.toast-success {
		background: rgba(0, 212, 123, 0.12);
		border-color: rgba(0, 212, 123, 0.3);
		color: var(--green);
	}

	/* ---- Game Over ---- */
	.game-over {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.75);
		backdrop-filter: blur(8px);
		-webkit-backdrop-filter: blur(8px);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 50;
	}

	.go-card {
		text-align: center;
		padding: 3rem 3.5rem;
		border-radius: 1rem;
		border: 1px solid;
		animation: scaleIn 0.45s ease-out both;
	}

	.go-card.win {
		background: var(--bg-surface);
		border-color: rgba(0, 212, 123, 0.3);
		box-shadow: 0 0 40px rgba(0, 212, 123, 0.1);
	}

	.go-card.lose {
		background: var(--bg-surface);
		border-color: rgba(255, 71, 87, 0.3);
		box-shadow: 0 0 40px rgba(255, 71, 87, 0.1);
	}

	.go-tag {
		font-size: 0.7rem;
		font-weight: 700;
		letter-spacing: 0.2em;
		margin-bottom: 0.5rem;
	}

	.go-tag.green { color: var(--green); }
	.go-tag.red { color: var(--red); }

	.go-title {
		font-size: 2.5rem;
		font-weight: 900;
		letter-spacing: 0.04em;
		margin-bottom: 0.4rem;
	}

	.go-card.win .go-title { color: var(--green); }
	.go-card.lose .go-title { color: var(--red); }

	.go-sub {
		color: var(--text-secondary);
		font-size: 0.95rem;
		margin-bottom: 2rem;
	}

	.go-btns {
		display: flex;
		gap: 0.75rem;
		justify-content: center;
	}

	.go-btn {
		padding: 0.75rem 1.75rem;
		border-radius: 0.5rem;
		text-decoration: none;
		font-weight: 700;
		font-size: 0.9rem;
		transition: all 0.2s ease;
	}

	.go-primary {
		background: linear-gradient(135deg, #c9a84c, #a8873a);
		color: #0a0a12;
		box-shadow: 0 0 16px rgba(201, 168, 76, 0.2);
		letter-spacing: 0.04em;
	}

	.go-primary:hover {
		transform: translateY(-2px);
		box-shadow: 0 0 24px rgba(201, 168, 76, 0.3);
	}

	.go-secondary {
		background: transparent;
		border: 1px solid var(--border);
		color: var(--text-secondary);
	}

	.go-secondary:hover {
		border-color: var(--border-hover);
		color: var(--text-primary);
	}

	/* ---- Mobile ---- */
	@media (max-width: 768px) {
		.battlefield { padding: 0.75rem 1rem; }
		.field-empty { padding: 1.25rem 1.5rem; font-size: 0.8rem; }
		.bar-track { max-width: none; }
		.hud-label { min-width: auto; }
		.go-card { padding: 2rem 1.5rem; }
		.go-title { font-size: 2rem; }
		.go-btns { flex-direction: column; align-items: center; }
		.go-btn { width: 100%; max-width: 220px; text-align: center; }
		.toast { max-width: 90vw; text-align: center; font-size: 0.7rem; }
	}

	@media (max-width: 480px) {
		.arena-header { padding: 0.5rem 1rem; }
		.battlefield { padding: 0.5rem 0.5rem; gap: 0.35rem; }
		.zone-hud { padding: 0.4rem 0.6rem; gap: 0.5rem; }
		.hud-label { font-size: 0.6rem; letter-spacing: 0.1em; }
		.field-row { gap: 0.5rem; }
		.action-bar { bottom: 50px; padding: 0.4rem 0.75rem; gap: 0.5rem; }
		.act { padding: 0.35rem 0.7rem; font-size: 0.7rem; }
		.hand-btn { bottom: 10px; right: 1rem; padding: 0.4rem 0.75rem; font-size: 0.65rem; }
		.hand-scroll { padding: 0.5rem 0.75rem; gap: 0.5rem; }
		.go-card { padding: 1.75rem 1.25rem; margin: 0 1rem; }
		.go-title { font-size: 1.75rem; }
		.go-sub { font-size: 0.85rem; margin-bottom: 1.5rem; }
	}
</style>
